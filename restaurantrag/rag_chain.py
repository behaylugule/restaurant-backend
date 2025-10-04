import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document

from asgiref.sync import sync_to_async
from menu.models import Menu, MenuCategory
from api.models import Shop

# Load environment variables
load_dotenv()

# ---------- ORM helper functions ----------

@sync_to_async
def get_shop(restaurant_id: int):
    try:
        return Shop.objects.get(id=restaurant_id)
    except Shop.DoesNotExist:
        return None

@sync_to_async
def get_categories(shop):
    return list(MenuCategory.objects.filter(shop=shop))

@sync_to_async
def get_items(category):
    return list(Menu.objects.filter(menu_category=category))

# ---------- RAG helpers ----------

async def get_restaurant_documents(restaurant_id: int):
    """Fetch restaurant info, categories, and menu items from DB asynchronously"""
    shop = await get_shop(restaurant_id)
    if not shop:
        return []

    documents = [
        Document(page_content=f"Restaurant Name: {shop.name}\nAddress: {shop.address}\n")
    ]

    categories = await get_categories(shop)
    for category in categories:
        items = await get_items(category)
        for item in items:
            documents.append(Document(
                page_content=(
                    f"Category: {category.name}\n"
                    f"Item: {item.name}\n"
                    f"Price: {item.price}\n"
                    f"Description: {item.description}\n"
                )
            ))
    return documents


async def get_restaurant_chain(restaurant_id: int) -> ConversationalRetrievalChain:
    """Create a dynamic RAG chain for a specific restaurant asynchronously"""
    documents = await get_restaurant_documents(restaurant_id)
    if not documents:
        raise ValueError("No restaurant data found.")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectordb = Chroma.from_documents(
        documents,
        embeddings,
        collection_name=f"restaurant_{restaurant_id}",
        persist_directory=f"./chroma_store/restaurant_{restaurant_id}"
    )
    vectordb.persist()

    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",   # optional, defaults to "input"
        output_key="answer",    # ✅ store only the 'answer' in memory
        return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
        output_key="answer"
    )
    return chain
