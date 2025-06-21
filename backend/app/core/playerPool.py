from fastapi import WebSocket
from app.core.playerSession import PlayerSession
from app.models.player import Player
from app.utils.logger import logger_init
import logging

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

class PlayerPool:
    def __init__(self):
        self.sessions: dict[str, PlayerSession] = {} # key = username

    def username_exists(self, username: str) -> bool:
        return username in self.sessions

    async def create_player(self, username: str) -> PlayerSession:
        if self.username_exists(username):
            raise ValueError(f"Username '{username}' is already taken")
        player = await Player.create(username)
        session = PlayerSession(player)
        self.sessions[username] = session
        logger.info(f"Created session for {username}")
        return session

    def get(self, username: str) -> PlayerSession | None:
        return self.sessions.get(username)

    async def connect_websocket(self, username: str, websocket: WebSocket):
        session = self.get(username)
        if session:
            await websocket.accept()
            session.websocket = websocket
            logger.info(f"WebSocket connected for {username}")

    def disconnect_websocket(self, username: str):
        session = self.get(username)
        if session and session.websocket:
            session.disconnect()
            logger.info(f"WebSocket disconnected for {username}")

    async def send_to(self, username: str, message: dict):
        session = self.get(username)
        if session and session.websocket:
            await session.send(message)
            logger.info(f"Sent message to {username}")

    async def broadcast(self, message: dict):
        for session in self.sessions.values():
            if session.websocket:
                await session.send(message)
        logger.info("Broadcast message sent")

player_pool = PlayerPool()