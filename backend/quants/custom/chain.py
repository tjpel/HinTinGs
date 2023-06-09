from langchain.chains import VectorDBQAWithSourcesChain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.qa_with_sources.map_reduce_prompt import (
    COMBINE_PROMPT,
    EXAMPLE_PROMPT,
    QUESTION_PROMPT,
)
from langchain.docstore.document import Document
from langchain.llms.base import BaseLLM
from langchain.prompts.base import BasePromptTemplate
from typing import Any, Dict, List, Tuple

class CustomMapReduceChain(MapReduceDocumentsChain):
        """
        Combining documents by mapping a chain over them, then combining results.
        
        Edited from LangChain's MapReduceDocumentsChain:
        https://github.com/hwchase17/langchain/blob/master/langchain/chains/combine_documents/map_reduce.py 
        """

        def _process_results(
            self,
            results: List[Dict],
            docs,
            token_max: int = 3000,
            **kwargs: Any,
        ) -> Tuple[str, dict]:
            question_result_key = self.llm_chain.output_key
            result_docs = [
                Document(page_content=r[question_result_key], metadata=docs[i].metadata)
                # This uses metadata from the docs, and the textual results from `results`
                for i, r in enumerate(results)
            ]
            length_func = self.combine_document_chain.prompt_length
            num_tokens = length_func(result_docs, **kwargs)
            while num_tokens is not None and num_tokens > token_max:
                new_result_doc_list = _split_list_of_docs(
                    result_docs, length_func, token_max, **kwargs
                )
                result_docs = []
                for docs in new_result_doc_list:
                    new_doc = _collapse_docs(
                        docs, self._collapse_chain.combine_docs, **kwargs
                    )
                    result_docs.append(new_doc)
                num_tokens = self.combine_document_chain.prompt_length(
                    result_docs, **kwargs
                )
            if self.return_intermediate_steps:
                _results = [r[self.llm_chain.output_key] for r in results]
                extra_return_dict = {'intermediate_steps': _results}
            else:
                extra_return_dict = {}
            output, _ = self.combine_document_chain.combine_docs(result_docs, **kwargs)
            # overriding _process_results() to return result_docs
            # so that we can extract the relevant snippets to highlight for each source
            return output, extra_return_dict, result_docs
        
class CustomChain(VectorDBQAWithSourcesChain):
    """
    Custom chain built from LangChain's VectorDBQAWithSourcesChain.
    """
    document_key = 'docs'
    snippets_key = 'snippets'

    @classmethod
    def from_llm(
        cls,
        llm: BaseLLM,
        document_prompt: BasePromptTemplate = EXAMPLE_PROMPT,
        question_prompt: BasePromptTemplate = QUESTION_PROMPT,
        combine_prompt: BasePromptTemplate = COMBINE_PROMPT,
        **kwargs: Any,
    ):
        """Construct the chain from an LLM."""
        llm_question_chain = LLMChain(llm=llm, prompt=question_prompt)
        llm_combine_chain = LLMChain(llm=llm, prompt=combine_prompt)
        combine_results_chain = StuffDocumentsChain(
            llm_chain=llm_combine_chain,
            document_prompt=document_prompt,
            document_variable_name='summaries',
        )
        # override this method to use our own CustomMapReduceChain
        combine_document_chain = CustomMapReduceChain(
            llm_chain=llm_question_chain,
            combine_document_chain=combine_results_chain,
            document_variable_name='context',
        )
        return cls(
            combine_documents_chain=combine_document_chain,
            **kwargs,
        )

    @property
    def output_keys(self) -> List[str]:
        """
        Returns a list of valid output keys.
        """
        # override this method to include document_key and snippets_key
        return [self.answer_key, self.sources_answer_key, self.document_key, self.snippets_key]
    
    def _call(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """
        Run the query through the custom chain.

        Args:
            inputs: a dict containing a string key and value, used for asking the question
        Returns:
            a dict containing the following key-value pairs:
                'answer': the result generated from the LLM
                'sources': a string of the UUIDs of the source documents separated by commas
                'docs': a list of LangChain Documents containing the full content of each source
                    document used for answering the question in the page_contents field
                'snippets': a list of LangChain Documents containing the extracts from source
                    documents used for answering the question in the page_contents field
        """
        docs = self._get_docs(inputs)
        answer, _, snippets = self.combine_documents_chain.combine_docs(docs, **inputs)
        if 'SOURCES:' in answer:
            answer, sources = answer.split('SOURCES:')
        else:
            sources = ''

        return {
            self.answer_key: answer, 
            self.sources_answer_key: sources, 
            self.document_key: docs, 
            self.snippets_key: snippets
        }
    

