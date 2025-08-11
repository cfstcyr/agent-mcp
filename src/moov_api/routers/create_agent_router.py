from fastapi import APIRouter, Depends

from moov_api.container import Container
from moov_api.models.agent import AgentRequestBody, AgentRequestResponse
from moov_api.services import AgentService


def create_agent_router(agent_name: str) -> APIRouter:
    router = APIRouter()

    @router.post("/response")
    async def response(
        body: AgentRequestBody,
        agent_service: AgentService = Depends(Container.depend_on("agent")),
    ):
        agent = await agent_service.get_agent(agent_name)
        res = await agent.ainvoke(
            {
                "messages": body.get_input(),
            }
        )

        return AgentRequestResponse(
            output=res["messages"],
        )

    return router
