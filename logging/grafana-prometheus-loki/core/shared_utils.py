import time
from fastapi import Request
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "zane_requests_total", "Total requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "zane_latency_seconds", "Request latency", ["endpoint"]
)

async def monitor_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method, 
        endpoint=request.url.path, 
        http_status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
    
    return response