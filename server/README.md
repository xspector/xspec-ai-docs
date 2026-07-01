# MCP server (Tier A — read-only)

Exposes the generated corpus as MCP tools so an agent can query models,
commands, the PyXspec class API, task guides, and validate names against the
authoritative grounding set — without reading files directly. Read-only; no
XSPEC execution.

## Tools

| Tool | Purpose |
|------|---------|
| `get_model(name)` | model component type + full parameter schema (limits/defaults/frozen) + prose |
| `list_models(type)` | list models, optionally by type (`add`/`mul`/`con`/`acn`) |
| `get_command(name)` | interactive-command syntax + examples (aliases resolved) |
| `get_api(class_name)` | PyXspec class attributes (type/access) + method signatures; accepts class or singleton |
| `lookup_intent(query)` | "how do I X?" → exact PyXspec call (+ Tcl) |
| `validate(name, kind)` | check a name against the grounding set (anti-hallucination); returns canonical form or suggestions |
| `get_guide(name)` | task-layer guides; no arg lists them |
| `corpus_info()` | provenance (XSPEC version + source commits) + counts |

## Requirements

```
pip install "mcp>=1.0"
```

The corpus is read from `../corpus` by default; override with the
`XSPEC_AI_CORPUS` environment variable.

## Run (stdio)

```
python server/server.py
```

## Client configuration

Add to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`,
or a `.mcp.json`). See `mcp-config.example.json`:

```json
{
  "mcpServers": {
    "xspec-ai-docs": {
      "command": "/opt/miniconda3/bin/python",
      "args": ["/Users/kaa/software/xspec-ai-docs/server/server.py"],
      "env": { "XSPEC_AI_CORPUS": "/Users/kaa/software/xspec-ai-docs/corpus" }
    }
  }
}
```

## Design

`corpus.py` is a pure, MCP-free data-access layer (unit-tested in
`tests/test_server.py`); `server.py` is a thin FastMCP wrapper over it. The
server bundles no data — it reads the same corpus the generator produces, so it
never drifts from the docs.
