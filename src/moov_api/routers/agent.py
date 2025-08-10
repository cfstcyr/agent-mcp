import logging

from fastapi import APIRouter
from langchain_core.messages import BaseMessage
from pydantic import BaseModel

from moov_agent.agent_service import agent_service

agent_router = APIRouter()
log = logging.getLogger(__name__)


class ResponseBody(BaseModel):
    input: str


@agent_router.post("/response")
async def response(body: ResponseBody):
    log.info("Agent responses endpoint called")
    agent = await agent_service.get_agent("default")

    res = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": body.input,
                }
            ]
        }
    )

    return {
        "output": [
            {
                "role": message.type,
                "content": message.content,
                "id": message.id,
            }
            for message in res["messages"]
            if isinstance(message, BaseMessage) and message.content
        ]
    }
