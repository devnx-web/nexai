"""Shared helpers for direct xAI HTTP integrations."""

from __future__ import annotations


def nexai_xai_user_agent() -> str:
    """Return a stable nexai-specific User-Agent for xAI HTTP calls."""
    try:
        from nexai_cli import __version__
    except Exception:
        __version__ = "unknown"
    return f"nexai-Agent/{__version__}"
