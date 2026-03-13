import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


logger = logging.getLogger("api_logger")


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        logger.info(
            f"Incoming Request: {request.method} {request.url}"
        )

        try:

            response = await call_next(request)

        except Exception as e:

            logger.error(
                f"Error occurred: {str(e)}"
            )

            raise e

        process_time = time.time() - start_time

        logger.info(
            f"Completed Response: {response.status_code} "
            f"in {process_time:.4f}s"
        )

        return response