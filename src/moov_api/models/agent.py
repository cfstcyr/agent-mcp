from langchain_core.messages import (
    BaseMessage,
    MessageLikeRepresentation,
    convert_to_messages,
)
from pydantic import BaseModel


class AgentRequestBody(BaseModel):
    input: MessageLikeRepresentation | list[MessageLikeRepresentation]

    def get_input(self) -> list[BaseMessage]:
        """Convert the input to a list of BaseMessage.

        Returns:
            List of BaseMessage instances.
        """
        return convert_to_messages(
            self.input if isinstance(self.input, list) else [self.input]
        )


class AgentRequestResponse(BaseModel):
    output: list[BaseMessage]
