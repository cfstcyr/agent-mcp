from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient, StreamableHttpConnection
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent

from moov_agent.llm_models import llm_model
from moov_core.settings import Settings, get_settings


async def create_agent(
    settings: Settings = get_settings(),
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

    with Path.open(settings.prompts.steering_agent_system_prompt) as f:
        system_prompt = f.read()

    return create_react_agent(
        tools=tools,
        model=llm_model,
        prompt=system_prompt,
        name="default",
    )
