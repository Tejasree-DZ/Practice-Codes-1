import logging
import time

from fastapi import Request

LOG = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    start = time.time()
    LOG.info("→ %s %s", request.method, request.url.path)
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    LOG.info("← %s %s %s (%.1fms)",
             request.method, request.url.path,
             response.status_code, duration)
    return response