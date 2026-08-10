"""Shared Supabase client helper."""

from __future__ import annotations

import logging
from types import SimpleNamespace
from typing import Any

import httpx

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


class SupabaseQueryBuilder:
    def __init__(self, base_url: str, api_key: str, table_name: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.table_name = table_name
        self.select_columns = "*"
        self.filters: list[tuple[str, str]] = []
        self.order_by: str | None = None
        self.limit_value: int | None = None
        self.single = False

    def select(self, columns: str) -> "SupabaseQueryBuilder":
        self.select_columns = columns
        return self

    def eq(self, column: str, value: Any) -> "SupabaseQueryBuilder":
        serialized = "null" if value is None else "true" if value is True else "false" if value is False else str(value)
        self.filters.append((column, serialized))
        return self

    def order(self, column: str) -> "SupabaseQueryBuilder":
        self.order_by = column
        return self

    def limit(self, count: int) -> "SupabaseQueryBuilder":
        self.limit_value = count
        return self

    def maybe_single(self) -> "SupabaseQueryBuilder":
        self.single = True
        return self

    def execute(self) -> Any:
        url = f"{self.base_url}/rest/v1/{self.table_name}"
        params: list[tuple[str, str]] = []
        if self.select_columns:
            params.append(("select", self.select_columns))

        for column, serialized in self.filters:
            params.append((column, f"eq.{serialized}"))

        if self.order_by:
            params.append(("order", f"{self.order_by}.asc"))

        if self.single and self.limit_value is None:
            params.append(("limit", "1"))
        if self.limit_value is not None:
            params.append(("limit", str(self.limit_value)))

        headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = httpx.get(url, headers=headers, params=params or None, timeout=15)
        response.raise_for_status()
        payload = response.json()

        if not self.single:
            return SimpleNamespace(data=payload)

        if isinstance(payload, list):
            return SimpleNamespace(data=payload[0] if payload else None)
        return SimpleNamespace(data=payload)


class SupabaseRestClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def table(self, table_name: str) -> SupabaseQueryBuilder:
        return SupabaseQueryBuilder(self.base_url, self.api_key, table_name)


def get_supabase_client(settings: Settings | None = None) -> Any | None:
    settings = settings or get_settings()
    if not settings.supabase_url:
        return None

    candidates = [
        ("SUPABASE_SERVICE_ROLE_KEY", settings.supabase_service_role_key),
        ("SUPABASE_SERVICE_KEY", settings.supabase_service_key),
        ("SUPABASE_ANON_KEY", settings.supabase_anon_key),
    ]

    for key_name, key_value in candidates:
        if not key_value or not key_value.strip():
            continue

        try:
            client = SupabaseRestClient(settings.supabase_url, key_value.strip())
            response = client.table("site_profile").select("id").limit(1).execute()
            if response.data is not None:
                logger.info("Supabase client initialized with %s", key_name)
                return client
        except Exception as exc:
            logger.warning("Supabase auth failed with %s: %s", key_name, exc)

    logger.warning("No usable Supabase key could be validated for %s", settings.supabase_url)
    return None
