from quants.custom.chain import CustomChain
from quants.custom.prompts import CUSTOM_COMBINE_PROMPT
from quants.custom.validation import validate_answers
from quants.custom.llm import CustomOpenAI
from quants.custom.postgres_faiss import PostgresFAISS
from quants.custom.helper_models.document import DocumentHelper

def process_query(query, question):
    """
    Given documents and a question, use an LLM to generate an answer using
    context only from the given documents.

    Args:
        query: a Django QuerySet of all SourceDocuments to be used for 
            answering the question
        question: a string of the question to be answered

    Returns:
        a string of the validated answer, a string of the answer before
        validation, and a list of Snippets of the source documents used in
        answering the question
    """
    # generate store on the fly
    store = PostgresFAISS.from_query(query)
    # instantiate the custom chain
    chain = CustomChain.from_llm(
        llm=CustomOpenAI(temperature=0, model_name='gpt-3.5-turbo'), 
        combine_prompt=CUSTOM_COMBINE_PROMPT,
        vectorstore=store
    )
    # run the chain
    results = chain({'question': question})
    validated_answer = validate_answers(results)
    # post processing of the results
    original_answer = results.get(chain.answer_key).split(':::')
    sources = results.get(chain.sources_answer_key)
    raw_snippets = results.get(chain.snippets_key)

    snippets = DocumentHelper.parse_snippets(sources, raw_snippets)

    return validated_answer, original_answer, snippets