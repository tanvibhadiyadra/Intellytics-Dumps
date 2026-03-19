import logging
import time
from fastapi import FastAPI

app = FastAPI()

# Logging configuration
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.get("/")
def home():
    logging.info("Home endpoint accessed")
    return {"message": "Hello from logging POC"}

@app.get("/error")
def error():
    logging.error("Simulated database connection failure")
    return {"error": "Simulated error"}

@app.get("/generate-logs")
def generate_logs():
    for i in range(20):
        logging.info(f"Processing request {i}")
        if i % 5 == 0:
            logging.warning(f"High response time detected {i}")
        if i % 7 == 0:
            logging.error(f"Database timeout at request {i}")
        time.sleep(0.2)

    return {"status": "20 logs generated"}