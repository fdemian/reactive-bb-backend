from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import iterate_in_threadpool


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("=================")
        print("==================")
        body = await request.json()
        print(body)
        print("=================------")

        response = await call_next(request)
        response_body = [section async for section in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        print(response_body[0].decode())
        print("?????????")
        return response
