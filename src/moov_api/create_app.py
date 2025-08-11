from contextlib import asynccontextmanager

from fastapi import FastAPI

from moov_agent import create_agent
from moov_api.container import Container
from moov_api.routers import create_agent_router, default_router
from moov_api.services.agent_service import AgentService
from moov_core.settings import Settings, get_settings
from moov_mcp import create_mcp


def create_container(settings: Settings) -> Container:
    return (
        Container()
        .register("settings", settings)
        .register("agent", AgentService(settings).register("default", create_agent))
    )


def create_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        create_container(settings).setup_app(app)

        mcp = await create_mcp()
        mcp_http = mcp.http_app()

        app.mount("/v1", mcp_http)

        async with mcp_http.lifespan(app):
            yield

    return lifespan


def create_app(settings: Settings = get_settings()) -> FastAPI:
    lifespan = create_lifespan(settings)
    app = FastAPI(lifespan=lifespan)

    app.include_router(default_router)
    app.include_router(create_agent_router("default"), prefix="/v1")

    return app
