import os
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.schema import Document
# 👇 Import SystemMessagePromptTemplate
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from asgiref.sync import sync_to_async
from menu.models import Menu, MenuCategory
from api.models import Shop
from utils.vectorstore import get_vectorstore

# Load environment variables
load_dotenv()  


async def get_restaurant_chain(restaurant_id: int) -> ConversationalRetrievalChain:
    """Create a dynamic RAG chain for a specific restaurant asynchronously with a system prompt"""

    
    # 1. Define your System Prompt
    system_prompt_template = (
        "You are a helpful and friendly AI assistant for a restaurant. "
        F"Your name is restaurant{restaurant_id}. Your primary goal is to answer questions about the "
        "restaurant's **menu, location, and hours** based *only* on the provided context. "
        "If the answer is not found in the context, politely state that you don't have "
        "that information. Do not mention the existence of the context documents."
    )
    
    # 2. Create the System Message Prompt Template
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template)
    
    # 3. Create a custom template for the RAG chain
    # The default template for ConversationalRetrievalChain.from_llm
    # is a combination of system_message + history + question + context
    # By passing a template, you can customize this structure.
    
    # NOTE: The default prompt for this chain when using a custom template
    # expects 'chat_history', 'context', and 'question' as input variables.
    # The SystemMessagePromptTemplate is added *before* the other parts.
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            ("human", "{chat_history}"),
            ("human", "Context: {context}"),
            ("human", "Question: {question}"),
        ]
    )

    vectordb = await sync_to_async(get_vectorstore)(restaurant_id)

    llm = ChatOpenAI(model="gpt-4o-mini", streaming=True, temperature=0)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        output_key="answer",
        return_messages=True
    )
    
    # 4. Pass the custom prompt to the chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": int(restaurant_id)}),
        memory=memory,
        return_source_documents=True,
        output_key="answer",
        # Pass the custom prompt
        combine_docs_chain_kwargs={"prompt": qa_prompt} 
    )
    return chain