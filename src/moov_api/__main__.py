import uvicorn
from dotenv import load_dotenv

from moov_core.settings import Settings, get_settings


def main(settings: Settings = get_settings()) -> None:
    load_dotenv()

    uvicorn.run(
        "moov_api:create_app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
