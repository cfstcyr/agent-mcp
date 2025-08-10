import logging
from collections.abc import Callable, Coroutine
from typing import Any

from langgraph.graph.state import CompiledStateGraph

log = logging.getLogger(__name__)

CreateAgentFunction = Callable[[], Coroutine[Any, Any, CompiledStateGraph]]


class AgentService:
    _create_agent_functions: dict[str, CreateAgentFunction] = {}
    _agents: dict[str, CompiledStateGraph] = {}

    def __init__(self):
        self._create_agent_functions = {}

    def register_agent_creator(self, name: str, creator: CreateAgentFunction):
        """
        Register a function that creates an agent.

        Args:
            name (str): The name of the agent.
            creator (Callable[[], CompiledStateGraph]): A function that returns a CompiledStateGraph.

        Raises:
            ValueError: If an agent creator with the same name already exists.
        """
        if name in self._create_agent_functions:
            raise ValueError(f"Agent creator for {name} already exists.")
        log.debug("Registering agent creator: {name}", name)
        self._create_agent_functions[name] = creator

    async def get_agent(self, name: str) -> CompiledStateGraph:
        """
        Get an agent by name, creating it if it does not exist.

        Args:
            name (str): The name of the agent to retrieve.

        Returns:
            CompiledStateGraph: The agent with the specified name.

        Raises:
            ValueError: If the agent does not exist and no creator function is registered for it.
        """
        if name not in self._agents:
            if name not in self._create_agent_functions:
                raise ValueError(f"Agent with name {name} does not exist.")
            log.debug("Creating agent: {name}", name)
            self._agents[name] = await self._create_agent_functions[name]()
        return self._agents[name]


agent_service = AgentService()
