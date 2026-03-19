"""
app_service.py
==============
Run:  uvicorn app_service:app --port 8000 --reload

Endpoints
---------
  GET /chat      — happy path
  GET /lineage   — simulates a processing error
  GET /health    — standard liveness probe (every prod service needs this)
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logging_setup import setup_logger

app = FastAPI(title="App Service")

# Module-level logger — created once when the file is imported
logger = setup_logger("app-service")

# Log at startup so we know the service came up (useful in prod)
logger.info("App service starting up")


# ── Startup / shutdown lifecycle ──────────────────────────────────────────
# Edge case: what if a DB connection or config fails at boot?
# Lifecycle hooks let you catch that before requests start coming in.
@app.on_event("startup")
async def on_startup():
    logger.info("App service ready — all dependencies loaded")


@app.on_event("shutdown")
async def on_shutdown():
    # Good practice: log shutdown so you can distinguish crash vs clean stop
    logger.info("App service shutting down")


# ── Global exception handler ──────────────────────────────────────────────
# Edge case: any unhandled exception anywhere in the app lands here.
# Without this, errors are silent from a logging perspective.
@app.exception_handler(Exception)
async def unhandled_exception(request: Request, exc: Exception):
    logger.critical(
        f"Unhandled exception on {request.method} {request.url.path} | {type(exc).__name__}: {exc}"
    )
    return JSONResponse(status_code=500, content={"error": "Internal server error"})


# ── Endpoints ─────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    """
    Liveness probe — orchestrators (K8s, ECS) call this to know if the
    container is alive. Always log at DEBUG so it doesn't spam dashboards.
    """
    logger.debug("Health probe received")
    return {"status": "ok"}


@app.get("/chat")
def chat():
    logger.info("Chat endpoint called")

    # Edge case: what if the AI model backend is slow or unavailable?
    # Here we just simulate success, but in real code you'd wrap the
    # model call in try/except and log the failure properly.
    logger.debug("Preparing chat response — no model errors")

    return {"msg": "chat working"}


@app.get("/lineage")
def lineage():
    logger.info("Lineage processing started")

    # Edge case: lineage graph can be massive — log before the heavy work
    # so you know exactly where a timeout or OOM happened
    logger.debug("Building lineage graph from metadata store")

    try:
        # Simulate something going wrong mid-processing
        raise ValueError("Lineage node missing upstream dependency")

    except ValueError as e:
        # ERROR: something failed but the service itself is still running
        logger.error(f"Lineage processing failed | reason={e}")
        return {"msg": "lineage failed", "error": str(e)}

    # This line only runs if no exception — good to log success explicitly
    logger.info("Lineage processing completed successfully")
    return {"msg": "lineage done"}