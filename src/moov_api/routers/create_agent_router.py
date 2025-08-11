from fastapi import APIRouter, Depends, Request
from langchain_core.messages import AIMessageChunk
from starlette.responses import StreamingResponse

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

    @router.post("/stream")
    async def stream(
        request: Request,
        body: AgentRequestBody,
        agent_service: AgentService = Depends(Container.depend_on("agent")),
    ):
        agent = await agent_service.get_agent(agent_name)

        async def gen():
            async for event, message in agent.astream(
                {
                    "messages": body.get_input(),
                },
                stream_mode=["messages", "tasks"],
                # stream_mode="messages",
            ):
                if await request.is_disconnected():
                    break

                if event == "messages":
                    message_chunk, _ = message
                    if isinstance(message_chunk, AIMessageChunk):
                        yield message_chunk.model_dump_json()
                elif event == "tasks":
                    print(message)

        return StreamingResponse(gen(), media_type="text/event-stream")

    return router
