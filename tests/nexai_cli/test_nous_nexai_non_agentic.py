"""Tests for the Nous-nexai-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"nexai"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``nexai-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "nexai" tag namespace.

``is_nous_nexai_non_agentic`` should only match the actual Nous Research
nexai-3 / nexai-4 chat family.
"""

from __future__ import annotations

import pytest

from nexai_cli.model_switch import (
    _NEXAI_MODEL_WARNING,
    _check_nexai_model_warning,
    is_nous_nexai_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "NousResearch/nexai-3-Llama-3.1-70B",
        "NousResearch/nexai-3-Llama-3.1-405B",
        "nexai-3",
        "nexai-3",
        "nexai-4",
        "nexai-4-405b",
        "nexai_4_70b",
        "openrouter/nexai3:70b",
        "openrouter/nousresearch/nexai-4-405b",
        "NousResearch/nexai3",
        "nexai-3.1",
    ],
)
def test_matches_real_nous_nexai_chat_models(model_name: str) -> None:
    assert is_nous_nexai_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Nous nexai 3/4"
    )
    assert _check_nexai_model_warning(model_name) == _NEXAI_MODEL_WARNING


@pytest.mark.parametrize(
    "model_name",
    [
        # Kyle's local Modelfile — qwen3:14b under a custom tag
        "nexai-brain:qwen3-14b-ctx16k",
        "nexai-brain:qwen3-14b-ctx32k",
        "nexai-honcho:qwen3-8b-ctx8k",
        # Plain unrelated models
        "qwen3:14b",
        "qwen3-coder:30b",
        "qwen2.5:14b",
        "claude-opus-4-6",
        "anthropic/claude-sonnet-4.5",
        "gpt-5",
        "openai/gpt-4o",
        "google/gemini-2.5-flash",
        "deepseek-chat",
        # Non-chat nexai models we don't warn about
        "nexai-llm-2",
        "nexai2-pro",
        "nous-nexai-2-mistral",
        # Edge cases
        "",
        "nexai",  # bare "nexai" isn't the 3/4 family
        "nexai-brain",
        "brain-nexai-3-impostor",  # "3" not preceded by /: boundary
    ],
)
def test_does_not_match_unrelated_models(model_name: str) -> None:
    assert not is_nous_nexai_non_agentic(model_name), (
        f"expected {model_name!r} NOT to be flagged as Nous nexai 3/4"
    )
    assert _check_nexai_model_warning(model_name) == ""


def test_none_like_inputs_are_safe() -> None:
    assert is_nous_nexai_non_agentic("") is False
    # Defensive: the helper shouldn't crash on None-ish falsy input either.
    assert _check_nexai_model_warning("") == ""
