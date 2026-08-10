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
    cors_origins: str = "*"

    # Groq (AI assistant + optional NLP)
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # Supabase (PostgreSQL + optional pgvector)
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_service_role_key: str = ""
    supabase_anon_key: str = ""
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
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def cors_allow_credentials(self) -> bool:
        return self.cors_origin_list != ["*"]

    @property
    def groq_enabled(self) -> bool:
        return bool(self.groq_api_key) and self.use_groq_ai

    @property
    def active_supabase_key(self) -> str:
        for candidate in (self.supabase_service_role_key, self.supabase_service_key, self.supabase_anon_key):
            if candidate and candidate.strip():
                return candidate.strip()
        return ""

    @property
    def supabase_enabled(self) -> bool:
        return bool(self.supabase_url and self.active_supabase_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
