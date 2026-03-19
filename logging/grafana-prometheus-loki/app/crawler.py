from fastapi import APIRouter
from core.logging_setup import setup_logger

router = APIRouter(prefix="/crawler", tags=["Crawler"])
logger = setup_logger("crawler-service")

@router.get("/")
async def run_crawl():
    logger.info("Crawler started")
    logger.info("Fetching URLs")
    logger.warning("Fetching URLs took longer than expected")
    logger.info("Crawler finished")
    return {"status": "success", "data": "Crawler is active"}
