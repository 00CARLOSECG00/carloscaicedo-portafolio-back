"""Application settings — all secrets and service URLs come from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    environment: str = "development"
    api_prefix: str = "/api"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Groq (AI assistant + optional NLP)
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Supabase (PostgreSQL + optional pgvector)
    supabase_url: str = ""
    supabase_service_key: str = ""
    database_url: str = ""

    # Feature flags
    use_groq_ai: bool = True
    use_supabase_knowledge: bool = True
    use_supabase_databases: bool = False
    use_supabase_content: bool = True

    # Limits
    max_nlp_input_length: int = 4000
    max_ai_message_length: int = 4000

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def groq_enabled(self) -> bool:
        return bool(self.groq_api_key) and self.use_groq_ai

    @property
    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
