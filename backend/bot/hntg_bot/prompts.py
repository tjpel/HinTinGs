from langchain.output_parsers import RegexParser
from langchain.prompts import PromptTemplate

output_parser = RegexParser(
    regex=r"(.*?)\nScore: (.*)",
    output_keys=["answer", "score"],
)

prompt_base = """
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

In addition to giving an answer, also return a score of how fully it answered the user's question. This should be in the following format:

Question: [question here]
Helpful Answer: [answer here]
Score: [score between 0 and 100]

Begin!

Question: {question}
Helpful Answer:
"""

PROMPT = PromptTemplate(
    template=prompt_base,
    input_variables=["question"],
    output_parser=output_parser
)
