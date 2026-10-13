from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API configuration, read from environment variables."""

    cors_origins: str = "http://localhost:5173"

    text_models: str = "llama-3.1-8b-instant|Llama 3.1 8B Instant"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    # LLM providers
    groq_api_key: str = ""
    openrouter_api_key: str = ""

    # Vector store: local by default, any Qdrant through the environment
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""

    # Defaults
    default_model_groq: str = "llama-3.1-8b-instant"
    openrouter_model: str = "meta-llama/llama-3.1-8b-instruct"
