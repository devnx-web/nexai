# Langfuse Observability Plugin

This plugin ships bundled with NexAi but is **opt-in** — it only loads when
you explicitly enable it.

## Enable

Pick one:

```bash
# Interactive: walks you through credentials + SDK install + enable
nexai tools  # → Langfuse Observability

# Manual
pip install langfuse
nexai plugins enable observability/langfuse
```

## Required credentials

Set these in `~/.nexai/.env` (or via `nexai tools`):

```bash
NEXAI_LANGFUSE_PUBLIC_KEY=pk-lf-...
NEXAI_LANGFUSE_SECRET_KEY=sk-lf-...
NEXAI_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```

Without the SDK or credentials the hooks no-op silently — the plugin fails
open.

## Verify

```bash
nexai plugins list                 # observability/langfuse should show "enabled"
nexai chat -q "hello"              # then check Langfuse for a "NexAi turn" trace
```

## Optional tuning

```bash
NEXAI_LANGFUSE_ENV=production       # environment tag
NEXAI_LANGFUSE_RELEASE=v1.0.0       # release tag
NEXAI_LANGFUSE_SAMPLE_RATE=0.5      # sample 50% of traces
NEXAI_LANGFUSE_MAX_CHARS=12000      # max chars per field (default: 12000)
NEXAI_LANGFUSE_DEBUG=true           # verbose plugin logging
```

## Disable

```bash
nexai plugins disable observability/langfuse
```
