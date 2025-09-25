import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .rag_chain import resume_chain
from .callbacks import WebSocketCallbackHandler

class ResumeChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        query = data.get("query", "")

        # Callback handler for streaming tokens
        handler = WebSocketCallbackHandler(self)

        # Run LangChain RAG chain with streaming
        result = await resume_chain.acall({"question": query}, callbacks=[handler])

        # Send source documents after completion
        sources = [doc.page_content for doc in result.get("source_documents", [])]
        await self.send(text_data=json.dumps({"sources": sources}))
