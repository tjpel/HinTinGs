from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from pathlib import Path
from bot.prompts import PROMPT

# load environmental variables
load_dotenv()


class Bot:
    def __init__(self, path: str):
        """
        The constructor method for the Bot class takes a file path as input and initializes the class by loading and splitting the text using the TextLoader and CharacterTextSplitter
        classes. It also turns the text into embeddings and creates a Chroma vector database using OpenAIEmbeddings and Chroma. Finally, it sets up the RetrievalQA class using a GPT-3
        language model and the Chroma vector database.

        ### Parameters:
        - `path` (str): The file path to the set of documents to be queried.
        """
        self.path = path

        # load the file directory, will use the unstructured
        #self.load_docs()

        # turn text into embedding ➡️ Chroma vector db
        #self.process_docs()

        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        #chain_type_kwargs = {"prompt": PROMPT}

        self.qa = None

    def query(self, q: str) -> str:
        #print("\nquery: ", q)
        query = PROMPT.format(question = q)
        #print(query)
        res = self.qa.run(query)
        #print("answer: ", res)
        return res
    
    def load_docs(self):
        self.loader = DirectoryLoader(self.path)
        self.documents = self.loader.load()
        
    def process_docs(self):
        text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
        texts = text_splitter.split_documents(self.documents)
        
        embeddings = OpenAIEmbeddings()
        docsearch = Chroma.from_documents(texts, embeddings)
        
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="map_rerank",
            retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
        )