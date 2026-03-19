from fastapi import FastAPI
from prometheus_client import start_http_server
from core.logging_setup import setup_logger

from core.shared_utils import monitor_middleware
from app.chat import router as chat_router
from app.crawler import router as crawler_router
from app.lineage import router as lineage_router

app = FastAPI(title="Zane Unified POC")
# Start Prometheus metrics server
start_http_server(9000, addr="0.0.0.0")

# Middleware
app.middleware("http")(monitor_middleware)

# Routers
app.include_router(chat_router)
app.include_router(crawler_router)
app.include_router(lineage_router)

logger = setup_logger("app-service")
logger.info("App service starting up")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def on_startup():
    logger.info("App service ready — all dependencies loaded")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("App service shutting down")

