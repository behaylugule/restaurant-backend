# restaurantrag/tasks.py
from celery import shared_task
from menu.models import Menu
from utils.vectorstore import get_vectorstore
from langchain.embeddings import OpenAIEmbeddings
import logging

logger = logging.getLogger(__name__)

@shared_task(name="update_restaurant_embeddings")
def update_restaurant_embeddings_task(restaurant_id: int):
    """
    Celery task: embed all documents for a given restaurant
    and store them in the Chroma vector database.
    """
    try:
        docs = Menu.objects.filter(shop_id=restaurant_id)
        if not docs.exists():
            logger.warning(f"No documents found for restaurant {restaurant_id}")
            return f"No documents found for restaurant {restaurant_id}."

        vectordb = get_vectorstore(restaurant_id)
        texts = [F"name:{doc.name} price:{doc.price} description:{doc.description}" for doc in docs]
        metadatas = [{"id": doc.id} for doc in docs]

        vectordb.add_texts(texts=texts, metadatas=metadatas)
        vectordb.persist()

        logger.info(f"✅ Embedded {len(docs)} documents for restaurant {restaurant_id}")
        return f"✅ Embedded {len(docs)} documents for restaurant {restaurant_id}"
    except Exception as e:
        logger.error(f"❌ Failed to embed restaurant {restaurant_id}: {e}", exc_info=True)
        return f"Error embedding restaurant {restaurant_id}: {e}"
