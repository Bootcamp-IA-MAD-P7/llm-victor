from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API configuration, read from environment variables."""

    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
