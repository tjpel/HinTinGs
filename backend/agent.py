from dotenv import load_dotenv

from langchain import LLMMathChain, SerpAPIWrapper, OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.memory import ConversationBufferWindowMemory
from langchain.document_loaders import DirectoryLoader
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader

# from nemoguardrails import LLMRails, RailsConfig
# from nemoguardrails.actions import action

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
        
        self.llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        self.search = SerpAPIWrapper() 
        self.llm_math_chain = LLMMathChain.from_llm(llm=self.llm, verbose=True)
        
        self.qa_chain = None
        # self.tools = [
        #     Tool(
        #         name = "Search",
        #         func=search.run,
        #         description="useful for when you need to answer questions about current events. You should ask targeted questions"
        #     ),
        #     Tool(
        #         name="Calculator",
        #         func=llm_math_chain.run,
        #         description="useful for when you need to answer questions about math"
        #     ),
        #     Tool(
        #         name="QA-System",
        #         func=query,
        #         description="useful for when asking questions about documents that you have uploaded"
        #     ),
        #     Tool(
        #         name="Diffusion",
        #         func=StableDiffusionTool().langchain.run,
        #         description="useful for when the user asks to create an image based on a prompt"
        #     )
        # ]
        
        # self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)


    def query(self, q: str) -> str:
        res = self.qa_chain({"query": q})
        answer = res["result"]
        source = res["source_documents"][0].metadata['source']
        return answer, source
    
    def load_docs(self):
        self.loader = DirectoryLoader(self.files_path)
        self.documents = self.loader.load()

    def process_docs(self):
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        texts = text_splitter.split_documents(self.documents)
        
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)
        
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", 
                                       retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
                                       return_source_documents=True)
