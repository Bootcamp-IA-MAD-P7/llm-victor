from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings

from .api.generate import router as generate_router
from .api.health import router as health_router
from .api.models import router as models_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="AI Content Studio API")
    app.state.settings = settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(generate_router)
    app.include_router(models_router)
    return app


app = create_app()
