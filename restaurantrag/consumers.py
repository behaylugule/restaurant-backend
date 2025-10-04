import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .rag_chain import get_restaurant_chain  # async function
from .callbacks import WebSocketCallbackHandler


class RestaurantChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.restaurant_id = self.scope['url_route']['kwargs']['restaurant_id']
        self.room_group_name = f"restaurant_{self.restaurant_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        query = data.get("query", "")

        if not query:
            return

        # ✅ Await the async chain factory
        restaurant_chain = await get_restaurant_chain(self.restaurant_id)

        # Callback handler for token streaming
        handler = WebSocketCallbackHandler(self)

        # ✅ Run chain asynchronously
        result = await restaurant_chain.acall(
            {"question": query},
            callbacks=[handler]
        )

        # Final answer + sources
        print("==========================")
        print(result.get("answer", ""))
        print("========================")
        answer = result.get("answer", "")
        sources = [doc.page_content for doc in result.get("source_documents", [])]
        

        await self.send(text_data=json.dumps({
            "answer": answer,
            "sources": sources
        }))
