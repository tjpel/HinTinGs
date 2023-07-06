from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import DirectoryLoader
from nemoguardrails import LLMRails, RailsConfig
from nemoguardrails.actions import action


# load environmental variables
load_dotenv()


class Bot:
    def __init__(self, files_path: str, config_path: str = "config/base"):
        """
        The constructor method for the Bot class takes a file path as input and initializes the class by loading and splitting the text using the TextLoader and CharacterTextSplitter
        classes. It also turns the text into embeddings and creates a Chroma vector database using OpenAIEmbeddings and Chroma. Finally, it sets up the RetrievalQA class using a GPT-3
        language model and the Chroma vector database.

        ### Parameters:
        - `files_path` (str): The file path to the set of documents to be queried.
        - `config_path` (str): The file path to the guardrails config folder. Defaults to "config/base"
        """
        self.files_path = files_path
        self.config_path = config_path

        # set up NeMo rails
        config = RailsConfig.from_path(config_path)

        # initialize
        self.app = LLMRails(config)

        # create a memory object, which tracks the conversation history
        self.chat_history = []

        # load the file directory, will use the unstructured
        loader = DirectoryLoader(files_path)
        documents = loader.load()

        # split by 1500 characters, which is about 250 words
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # turn text into embedding ➡️ Chroma vector db
        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_documents(texts, embeddings)
        # chain_type_kwargs = {"prompt": PROMPT}

        # use prompt engineering, and the map reduce chain
        question_generator = LLMChain(llm=self.app.llm, prompt=CONDENSE_QUESTION_PROMPT)
        doc_chain = load_qa_chain(self.app.llm, chain_type="map_reduce")

        # creates the QA chain, should reference to the source
        self.qa = ConversationalRetrievalChain(
            retriever=self.docsearch.as_retriever(search_kwargs={"k": 2}),
            question_generator=question_generator,
            combine_docs_chain=doc_chain,
        )

        self.app.register_action(self.query_base_chain, name="main_chain")

    @action()
    async def query_base_chain(self, q: str):
        return self.qa({"question": q, "chat_history": self.chat_history})["answer"]

    def query(self, q: str) -> str:
        print("\nquery: ", q)
        # query = PROMPT.format(question = q)
        # print(query)
        res = self.app.generate(q)
        print("answer: ", res)
        return res

    def clear_memory(self):
        self.history = []
