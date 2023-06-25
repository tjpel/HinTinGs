from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import DirectoryLoader


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
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        # create a memory object, which tracks the conversation history
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

        # load the file directory, will use the unstructured
        loader = DirectoryLoader(path)
        documents = loader.load()

        # split by 3000 characters, which is about 500 words
        text_splitter = CharacterTextSplitter(chunk_size=3000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # turn text into embedding ➡️ Chroma vector db
        embeddings = OpenAIEmbeddings()
        self.docsearch = Chroma.from_documents(texts, embeddings)
        # chain_type_kwargs = {"prompt": PROMPT}

        # creates the QA chain, should reference to the source
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.docsearch.as_retriever(search_kwargs={"k": 2}),
            memory=memory,
        )

    def query(self, q: str) -> str:
        print("\nquery: ", q)
        # query = PROMPT.format(question = q)
        # print(query)
        res = self.qa({"question": q})["answer"]
        print("answer: ", res)
        return res

    def clear_memory(self):
        # creates the a new chain, but still has access to the pre-computed embeddings
        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.docsearch.as_retriever(search_kwargs={"k": 2}),
            memory=ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            ),
        )
