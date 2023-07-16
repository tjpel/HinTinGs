from dotenv import load_dotenv

from langchain import LLMMathChain, SerpAPIWrapper, OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.document_loaders import DirectoryLoader
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader

from nemoguardrails import LLMRails, RailsConfig
from nemoguardrails.actions import action

from gradio_tools.tools import StableDiffusionTool


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
        # initialize NeMo App
        self.app = LLMRails(config)

        #initilize search
        self.search = SerpAPIWrapper()

        #initilize math chain
        self.llm_math_chain = LLMMathChain.from_llm(ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613"), verbose=True)

        # create a memory object, which tracks the conversation history
        self.memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history",return_messages=True)

    @action()
    async def query_base_chain(self, q: str):
        return self.qa({"question": q})["answer"] 

    def query(self, q: str) -> str:
        print("\nquery: ", q)
        res = self.agent.run(q)
        print("answer: ", res)
        return res
    
    def load_docs(self):
        self.loader = DirectoryLoader(self.files_path)
        self.documents = self.loader.load()

    def process_docs(self):
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
        texts = text_splitter.split_documents(self.documents)
        
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)

        # creates the QA chain, should reference to the source
        self.qa = ConversationalRetrievalChain.from_llm(
             llm=self.app.llm,
             retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
             chain_type="stuff",
            # verbose=True,
            memory=self.memory,
         )

        #allows NeMo app to query our self.qa (ConversationalRetrievalChain)
        self.app.register_action(self.query_base_chain, name="main_chain")

        tools = [
            Tool(
                name = "Search",
                func=self.search.run,
                description="useful for when you need to answer questions about current events. You should ask targeted questions"
            ),
            Tool(
                name="Calculator",
                func=self.llm_math_chain.run,
                description="useful for when you need to answer questions about math"
            ),
            Tool(
                name="QA-System",
                func=self.app.generate,
                description="useful for when asking questions about documents that you have uploaded"
            ),
            Tool(
                name="Diffusion",
                func=StableDiffusionTool().langchain.run,
                description="useful for when the user asks to create an image based on a prompt"
            )
        ]

        self.agent = initialize_agent(tools, ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613"), agent=AgentType.OPENAI_FUNCTIONS, verbose=True) #TODO: This is throwing an error 

"""
    def clear_memory(self):
        # creates the a new chain, but still has access to the pre-computed embeddings
        self.memory = ConversationBufferWindowMemory(k=3, memory_key="chat_history", return_messages=True)
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.app.llm,
            retriever=self.docsearch.as_retriever(search_kwargs={"k": 2}),
            chain_type="stuff",
            # verbose=True,
            memory=self.memory,
        )
"""
