
import aiofiles
from langchain_mcp_adapters.client import MultiServerMCPClient, StreamableHttpConnection
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from moov_core.settings import Settings


async def create_agent(
    settings: Settings,
) -> CompiledStateGraph:
    client = MultiServerMCPClient(
        {
            "tools": StreamableHttpConnection(
                url=f"http://{settings.host}:{settings.port}/v1/mcp/",
                transport="streamable_http",
            ),
        }
    )
    tools = await client.get_tools()

    async with aiofiles.open(settings.prompts.steering_agent_system_prompt) as f:
        system_prompt = await f.read()

    return create_react_agent(
        tools=tools,
        model=settings.llm.init_model(),
        prompt=system_prompt,
        name="default",
    )
