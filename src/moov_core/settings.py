from functools import cache
from pathlib import Path

from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field, FilePath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PromptSettings(BaseSettings):
    steering_agent_system_prompt: FilePath = Path(
        "./conf/prompts/steering-agent-system.txt"
    )


class LLMSettings(BaseModel):
    model: str
    provider: str
    api_key: SecretStr
    temperature: float = 0.1
    reasoning: dict = Field(default_factory=lambda: {"effort": "low"})

    def init_model(self):
        return init_chat_model(
            model=self.model,
            model_provider=self.provider,
            api_key=self.api_key.get_secret_value(),
            temperature=self.temperature,
            reasoning=self.reasoning,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        cli_parse_args=True,
        extra="ignore",
    )

    # API
    host: str = Field("127.0.0.1")
    port: int = Field(8000)
    reload: bool = Field(default=False)

    # LLM
    llm: LLMSettings
    prompts: PromptSettings = PromptSettings()


@cache
def get_settings() -> Settings:
    """
    Get the application settings.

    Returns:
        Settings: The application settings.
    """
    return Settings()  # type: ignore


def async_settings_wrapper(func):
    def wrapper(settings: Settings):
        async def async_func(*args, **kwargs):
            return await func(settings, *args, **kwargs)

        return async_func

    return wrapper
