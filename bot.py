from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
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
        self.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history",return_messages=True)


        # load the file directory, will use the unstructured
        loader = DirectoryLoader(files_path)
        documents = loader.load()

        # split by 1500 characters, which is about 250 words
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # turn text into embedding ➡️ Chroma vector db
        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_documents(texts, embeddings)

        # creates the QA chain, should reference to the source
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.app.llm,
            retriever=self.docsearch.as_retriever(search_kwargs={"k": 2}),
            chain_type="map_rerank",
            verbose=True,
            memory=self.memory,
        )

        self.app.register_action(self.query_base_chain, name="main_chain")

    @action()
    async def query_base_chain(self, q: str):
        return self.qa({"question": q})["answer"] 

    def query(self, q: str) -> str:
        print("\nquery: ", q)
        # query = PROMPT.format(question = q)
        # print(query)
        res = self.app.generate(q)
        print("answer: ", res)
        return res

    def clear_memory(self):
        # creates the a new chain, but still has access to the pre-computed embeddings
        self.memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history", return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.app.llm,
            retriever=self.docsearch.as_retriever(search_kwargs={"k": 2}),
            chain_type="map_rerank",
            verbose=True,
            memory=self.memory,
        )
