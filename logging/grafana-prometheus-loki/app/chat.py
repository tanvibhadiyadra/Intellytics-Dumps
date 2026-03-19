from fastapi import APIRouter
from core.logging_setup import setup_logger


router = APIRouter(prefix="/chat", tags=["Chat"])
logger = setup_logger("chat-service")

@router.get("/")
async def chat():
    logger.info("Chat endpoint called")
    return {"msg": "chat online"}