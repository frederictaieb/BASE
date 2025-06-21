from fastapi import WebSocket
from app.models.player import Player

class PlayerSession:
    def __init__(self, player: Player, websocket: WebSocket = None):
        self.player = player
        self.websocket = websocket

    def is_connected(self) -> bool:
        return self.websocket is not None

    async def send(self, message: dict):
        if self.websocket:
            await self.websocket.send_json(message)

    def disconnect(self):
        self.websocket = None