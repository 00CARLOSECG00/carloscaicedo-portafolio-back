"""Shared Supabase client helper."""

from __future__ import annotations

import logging
from typing import Any

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


def get_supabase_client(settings: Settings | None = None) -> Any | None:
    settings = settings or get_settings()
    if not settings.supabase_enabled:
        return None
    try:
        from supabase import create_client

        return create_client(settings.supabase_url, settings.supabase_service_key)
    except Exception as exc:
        logger.warning("Supabase client unavailable: %s", exc)
        return None
