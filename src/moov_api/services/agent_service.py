from collections.abc import Callable, Coroutine
from typing import Any, Self

from langgraph.graph.state import CompiledStateGraph

from moov_core.settings import Settings

CreateAgentFunction = Callable[[Settings], CompiledStateGraph]
CreateAgentAsyncFunction = Callable[[Settings], Coroutine[Any, Any, CompiledStateGraph]]
CreateAgent = CompiledStateGraph | CreateAgentFunction | CreateAgentAsyncFunction


class AgentService:
    settings: Settings
    _agent_creators: dict[str, CreateAgent]
    _agents: dict[str, CompiledStateGraph]

    def __init__(self, settings: Settings):
        self.settings = settings
        self._agent_creators = {}
        self._agents = {}

    def register(self, name: str, creator: CreateAgent) -> Self:
        """
        Register a function or a CompiledStateGraph that creates an agent.

        Args:
            name (str): The name of the agent.
            creator (CreateAgent): A function or CompiledStateGraph that creates the agent.

        Raises:
            ValueError: If an agent creator with the same name already exists.

        Returns:
            Self: The current instance for method chaining.
        """
        if name in self._agent_creators:
            raise ValueError(f"Agent creator for {name} already exists.")

        self._agent_creators[name] = creator

        return self

    async def get_agent(self, name: str) -> CompiledStateGraph:
        """
        Get an agent by name, creating it if it does not exist.

        Args:
            name (str): The name of the agent to retrieve.

        Returns:
            CompiledStateGraph: The agent with the specified name.
        """
        if name not in self._agents:
            self._agents[name] = await self._resolve_agent(name)

        return self._agents[name]

    async def _resolve_agent(self, name: str) -> CompiledStateGraph:
        """
        Resolve an agent by name, ensuring it is created if not already available.

        Args:
            name (str): The name of the agent to resolve.

        Raises:
            ValueError: If the agent does not exist and no creator function is registered for it.

        Returns:
            CompiledStateGraph: The resolved agent.
        """
        if name not in self._agent_creators:
            raise ValueError(f"Agent with name {name} does not exist.")

        creator = self._agent_creators[name]

        if isinstance(creator, CompiledStateGraph):
            return creator
        if callable(creator):
            result = creator(self.settings)
            if isinstance(result, CompiledStateGraph):
                return result
            return await result

        raise ValueError(f"Invalid creator for agent {name}: {creator}")
