from contextlib import asynccontextmanager

from fastapi import FastAPI

from moov_agent import agent_service, create_agent
from moov_api.routers import agent_router, default_router
from moov_mcp import create_mcp


@asynccontextmanager
async def lifespan(app: FastAPI):
    mcp = await create_mcp()
    mcp_http = mcp.http_app()

    app.mount("/v1", mcp_http)

    async with mcp_http.lifespan(app):
        yield


def create_app() -> FastAPI:
    agent_service.register_agent_creator("default", create_agent)

    app = FastAPI(lifespan=lifespan)

    app.include_router(default_router)
    app.include_router(agent_router, prefix="/v1")

    return app
