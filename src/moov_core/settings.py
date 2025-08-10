from functools import cache
from pathlib import Path

from pydantic import Field, FilePath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PromptSettings(BaseSettings):
    steering_agent_system_prompt: FilePath = Path("./conf/prompts/steering-agent-system.txt")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        cli_parse_args=True,
        extra="ignore",
    )

    # API
    host: str = Field("127.0.0.1")
    port: int = Field(8000)
    reload: bool = Field(default=False)

    # LLM
    openai_api_key: SecretStr
    prompts: PromptSettings = PromptSettings()


@cache
def get_settings() -> Settings:
    """
    Get the application settings.

    Returns:
        Settings: The application settings.
    """
    return Settings()  # type: ignore
