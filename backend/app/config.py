from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """API configuration, read from environment variables."""

    cors_origins: str = "http://localhost:5173"

    # Catálogo de modelos de texto: pares "id|etiqueta" separados por comas
    text_models: str = (
        "openai/gpt-oss-120b|GPT-OSS 120B (Groq),"
        "openai/gpt-oss-20b|GPT-OSS 20B (Groq),"
        "qwen/qwen3.8-27b|Qwen 3.8 27B (Groq)"
    )
    # También son el fallback de Groq, en este orden
    openrouter_models: str = (
        "nvidia/nemotron-3-super-120b-a12b:free|Nemotron 3 Super 120B (OpenRouter),"
        "nvidia/nemotron-3.5-lightning:free|Nemotron 3.5 Lightning (OpenRouter),"
        "poolside/laguna-s-2.1:free|Laguna S 2.1 (OpenRouter)"
    )

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
    default_model_groq: str = "openai/gpt-oss-120b"
