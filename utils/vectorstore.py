# restaurantrag/utils/vectorstore.py
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

BASE_VECTOR_PATH = os.path.join("chroma_dbs")

def get_vectorstore(restaurant_id: int):
    """Return a persistent Chroma instance per restaurant."""
    os.makedirs(BASE_VECTOR_PATH, exist_ok=True)
    persist_dir = os.path.join(BASE_VECTOR_PATH, f"restaurant_{restaurant_id}")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectordb = Chroma(
        collection_name=f"restaurant_{restaurant_id}",
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
    return vectordb
