from fastapi import FastAPI
from logging_setup import setup_logger

app = FastAPI()

logger = setup_logger("crawler-service")
logger.info("=====Crawler service started=====")

@app.get("/crawl")
def crawl():

    logger.info("Crawler started")

    logger.info("Fetching URLs")

    logger.warning("Fetching URLs took longer than expected")

    logger.info("Crawler finished")

    return {"status": "crawl complete"}