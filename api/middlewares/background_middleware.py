from starlette.middleware.base import BaseHTTPMiddleware


class BackgroundTaskMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.background = None
        response = await call_next(request)
        if request.state.background:
            response.background = request.state.background
        return response
