from fastmcp import FastMCP

from .tools import analysis_mcp


async def create_mcp() -> FastMCP:
    mcp = FastMCP(name="Tool Example")

    await mcp.import_server(analysis_mcp)

    tools = await mcp.get_tools()
    print(f"Registered tools: {', '.join(tool for tool in tools)}")

    return mcp
