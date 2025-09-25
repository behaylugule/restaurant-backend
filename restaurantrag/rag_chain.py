import os
from dotenv import load_dotenv
from  langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

# 1. Load PDF
loader = PyPDFLoader("resume_files/resume.pdf")
docs = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

# 3. Create embeddings + Chroma vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = Chroma.from_documents(chunks, embeddings, collection_name="resume")

# 4. LLM with streaming
llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0)

# 5. Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 6. RAG Chain
resume_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
    memory=memory,
    return_source_documents=True,
)
