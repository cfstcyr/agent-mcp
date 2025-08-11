import logging

from fastmcp import FastMCP

from .tools import analysis_mcp

log = logging.getLogger(__name__)


async def create_mcp() -> FastMCP:
    mcp = FastMCP(name="Tool Example")

    await mcp.import_server(analysis_mcp)

    tools = await mcp.get_tools()
    log.info("Registered tools: %s", tools)

    return mcp
