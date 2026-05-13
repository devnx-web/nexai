---
sidebar_position: 11
title: "ACP Editor Integration"
description: "Use NexAi Agent inside ACP-compatible editors such as VS Code, Zed, and JetBrains"
---

# ACP Editor Integration

NexAi Agent can run as an ACP server, letting ACP-compatible editors talk to nexai over stdio and render:

- chat messages
- tool activity
- file diffs
- terminal commands
- approval prompts
- streamed thinking / response chunks

ACP is a good fit when you want nexai to behave like an editor-native coding agent instead of a standalone CLI or messaging bot.

## What nexai exposes in ACP mode

nexai runs with a curated `nexai-acp` toolset designed for editor workflows. It includes:

- file tools: `read_file`, `write_file`, `patch`, `search_files`
- terminal tools: `terminal`, `process`
- web/browser tools
- memory, todo, session search
- skills
- execute_code and delegate_task
- vision

It intentionally excludes things that do not fit typical editor UX, such as messaging delivery and cronjob management.

## Installation

Install nexai normally, then add the ACP extra:

```bash
pip install -e '.[acp]'
```

This installs the `agent-client-protocol` dependency and enables:

- `nexai acp`
- `nexai-acp`
- `python -m acp_adapter`

## Launching the ACP server

Any of the following starts nexai in ACP mode:

```bash
nexai acp
```

```bash
nexai-acp
```

```bash
python -m acp_adapter
```

nexai logs to stderr so stdout remains reserved for ACP JSON-RPC traffic.

## Editor setup

### VS Code

Install the [ACP Client](https://marketplace.visualstudio.com/items?itemName=formulahendry.acp-client) extension.

To connect:

1. Open the ACP Client panel from the Activity Bar.
2. Select **NexAi Agent** from the built-in agent list.
3. Connect and start chatting.

If you want to define nexai manually, add it through VS Code settings under `acp.agents`:

```json
{
  "acp.agents": {
    "NexAi Agent": {
      "command": "NexAi",
      "args": ["acp"]
    }
  }
}
```

### Zed

Example settings snippet:

```json
{
  "agent_servers": {
    "NexAi-agent": {
      "type": "custom",
      "command": "NexAi",
      "args": ["acp"],
    },
  },
}
```

### JetBrains

Use an ACP-compatible plugin and point it at:

```text
/path/to/nexai-agent/acp_registry
```

## Registry manifest

The ACP registry manifest lives at:

```text
acp_registry/agent.json
```

It advertises a command-based agent whose launch command is:

```text
nexai acp
```

## Configuration and credentials

ACP mode uses the same nexai configuration as the CLI:

- `~/.nexai/.env`
- `~/.nexai/config.yaml`
- `~/.nexai/skills/`
- `~/.nexai/state.db`

Provider resolution uses nexai' normal runtime resolver, so ACP inherits the currently configured provider and credentials.

## Session behavior

ACP sessions are tracked by the ACP adapter's in-memory session manager while the server is running.

Each session stores:

- session ID
- working directory
- selected model
- current conversation history
- cancel event

The underlying `AIAgent` still uses nexai' normal persistence/logging paths, but ACP `list/load/resume/fork` are scoped to the currently running ACP server process.

## Working directory behavior

ACP sessions bind the editor's cwd to the NexAi task ID so file and terminal tools run relative to the editor workspace, not the server process cwd.

## Approvals

Dangerous terminal commands can be routed back to the editor as approval prompts. ACP approval options are simpler than the CLI flow:

- allow once
- allow always
- deny

On timeout or error, the approval bridge denies the request.

## Troubleshooting

### ACP agent does not appear in the editor

Check:

- the editor is pointed at the correct `acp_registry/` path
- nexai is installed and on your PATH
- the ACP extra is installed (`pip install -e '.[acp]'`)

### ACP starts but immediately errors

Try these checks:

```bash
nexai doctor
nexai status
nexai acp
```

### Missing credentials

ACP mode does not have its own login flow. It uses nexai' existing provider setup. Configure credentials with:

```bash
nexai model
```

or by editing `~/.nexai/.env`.

## See also

- [ACP Internals](../../developer-guide/acp-internals.md)
- [Provider Runtime Resolution](../../developer-guide/provider-runtime.md)
- [Tools Runtime](../../developer-guide/tools-runtime.md)
