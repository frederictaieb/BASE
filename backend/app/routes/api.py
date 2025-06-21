from fastapi import APIRouter
from app.models.player import Player
from app.core.playerPool import player_pool

from app.utils.logger import logger_init
import logging

logger_init(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/api/helloworld")
async def helloworld():
    return {"message": "Hello from FastAPI!"}



@router.get("/api/register_player")
async def register_player(username: str):
    await player_pool.create_player(username)
    logger.info(f"Player {username} created")
    return {"message": "Player registered", "player": username}

@router.get("/api/get_player")
async def get_player(username: str):
    return player_pool.get(username)

@router.get("/api/get_players")
def get_players():
    return player_pool.sessions
    logger.info(f"Players: {player_pool.players}")
    return {"message": "Players", "players": player_pool.players}
