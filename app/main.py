from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.include_router(api_router, prefix="/api")

    @application.get("/", tags=["system"])
    async def index() -> dict[str, str]:
        return {"message": f"Welcome to {settings.app_name}"}

    return application


app = create_app()
