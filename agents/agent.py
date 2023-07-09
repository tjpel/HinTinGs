from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo,
)
from dotenv import load_dotenv

load_dotenv()

loader = DirectoryLoader("../data")
documents = loader.load()

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# split by 1500 characters, which is about 250 words
text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# turn text into embedding ➡️ Chroma vector db
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

vectorstore_info = VectorStoreInfo(
    name="user_documents",
    description="documents that the user uploaded",
    vectorstore=docsearch,
)

toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
agent_executor = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)

# run vector search agent
agent_executor("What did Xingyu do in the arduino project?")

# while True:
#     user_input = input("question: ")
#     if user_input == "exit":
#         break
#     agent_executor.run(user_input)
