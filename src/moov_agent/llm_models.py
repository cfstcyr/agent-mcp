from langchain_openai import ChatOpenAI

from moov_core.settings import get_settings

llm_model = ChatOpenAI(
    model="gpt-5-mini",
    api_key=get_settings().openai_api_key,
    temperature=0.1,
    reasoning={
        "effort": "low",
    },
)
