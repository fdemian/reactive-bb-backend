import contextlib
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.config import environ
from starlette.middleware.cors import CORSMiddleware
from api.graphql_handler import get_graphql_handler
from starlette.middleware.authentication import AuthenticationMiddleware
from api.middlewares.auth_middleware import AuthBackend
from api.middlewares.background_middleware import BackgroundTaskMiddleware
from api.resolvers.refresh import refresh_tokens
from starlette.responses import JSONResponse
from starlette.requests import Request
from api.schema import graphl_schema
from api.resolvers.login import login, logout
from api.resolvers.oauth import oauth
from api.database.utils import get_engine
from broadcaster import Broadcast


def on_auth_error(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"error": str(exc)}, status_code=412)


@contextlib.asynccontextmanager
async def lifespan(app) -> None:
    broadcast = Broadcast("memory://")
    await broadcast.connect()
    engine = get_engine()
    app.state.engine = engine
    app.state.broadcast = broadcast
    yield
    app.state.engine = None
    engine.dispose()
    await broadcast.disconnect()


def get_main_app() -> Starlette:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_headers=["*"],
            allow_methods=["OPTIONS", "GET", "POST"],
            allow_credentials=True,
        ),
        Middleware(
            AuthenticationMiddleware, backend=AuthBackend(), on_error=on_auth_error
        ),
        Middleware(BackgroundTaskMiddleware),
    ]

    # Move environment.
    environment = environ["ENVIRON"]
    graphql_handler = get_graphql_handler(graphl_schema, environment)

    routes = [
        Route("/api/oauth", endpoint=oauth, methods=["POST"]),
        Route("/api/login", endpoint=login, methods=["POST"]),
        Route("/api/logout", endpoint=logout, methods=["POST"]),
        Route("/api/refresh", endpoint=refresh_tokens, methods=["POST"]),
        Route("/api/graphql", endpoint=graphql_handler, name="graphql"),
        WebSocketRoute(
            "/api/subscriptions", endpoint=graphql_handler, name="graphqlws"
        ),
        Mount(
            "/api/locales",
            StaticFiles(directory="locales", html=False),
            name="api.locales",
        ),
        Mount("/", StaticFiles(directory=".", html=True), name="index.route"),
    ]

    app = Starlette(lifespan=lifespan, routes=routes, middleware=middleware)
    return app
