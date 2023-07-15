from langchain import LLMMathChain, SerpAPIWrapper
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# initialize the llm, this particular model supports OpenAI functions 
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
search = SerpAPIWrapper() 
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

loader = DirectoryLoader("../data")
documents = loader.load()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# split by 1500 characters, which is about 250 words
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# turn text into embedding ➡️ Chroma vector db
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", 
                                       retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
                                       return_source_documents=True)
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    ),
    Tool(
        name="QA-System",
        func=qa_chain,
        description="useful for when asking questions about documents that you have uploaded"
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
agent.run("Based on the document, What is happening in New York?")
agent.run("What is the weather today in Amherst Massachusetts?")
agent.run("Based on the document, what is the langchain?")
agent.run("What is 10 raised to 1.8 power?")