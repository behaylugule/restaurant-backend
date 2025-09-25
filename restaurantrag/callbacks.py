from langchain.callbacks.base import BaseCallbackHandler
import json

class WebSocketCallbackHandler(BaseCallbackHandler):
    def __init__(self, websocket):
        self.websocket = websocket

    async def on_llm_new_token(self, token: str, **kwargs):
        await self.websocket.send(text_data=json.dumps({"delta": token}))

    async def on_llm_end(self, response, **kwargs):
        await self.websocket.send(text_data=json.dumps({"done": True}))
