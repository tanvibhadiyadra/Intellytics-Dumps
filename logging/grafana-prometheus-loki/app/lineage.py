from fastapi import APIRouter
from core.logging_setup import setup_logger

router = APIRouter(prefix="/lineage", tags=["Lineage"])
logger = setup_logger("lineage-service")

@router.get("/")
async def lineage():
    logger.info("Lineage processing started")
    logger.debug("Building lineage graph from metadata store")
    try:
        raise ValueError("Lineage node missing upstream dependency")

    except ValueError as e:
        logger.error(f"Lineage processing failed | reason={e}")
        return {"msg": "lineage failed", "error": str(e)}

    logger.info("Lineage processing completed successfully")
    return {"msg": "lineage done"}
