"""Resolve NEXAI_HOME for standalone skill scripts.

Skill scripts may run outside the nexai process (e.g. system Python,
nix env, CI) where ``nexai_constants`` is not importable.  This module
provides the same ``get_nexai_home()`` and ``display_nexai_home()``
contracts as ``nexai_constants`` without requiring it on ``sys.path``.

When ``nexai_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``nexai_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``NEXAI_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from nexai_constants import display_nexai_home as display_nexai_home
    from nexai_constants import get_nexai_home as get_nexai_home
except (ModuleNotFoundError, ImportError):

    def get_nexai_home() -> Path:
        """Return the nexai home directory (default: ~/.nexai).

        Mirrors ``nexai_constants.get_nexai_home()``."""
        val = os.environ.get("NEXAI_HOME", "").strip()
        return Path(val) if val else Path.home() / ".nexai"

    def display_nexai_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``nexai_constants.display_nexai_home()``."""
        home = get_nexai_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
