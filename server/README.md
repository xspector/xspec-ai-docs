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
| `find_cases(mission, counts_regime, source_type, model, statistic, text)` | retrieve worked casebook cases by data fingerprint (Tier C); ranked, lessons summarized |
| `get_case(case_id)` | full worked case + the full text of every lesson it cites |
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

---

# Tier B — execution server (`xspec_run.py`, proof-of-concept)

A **separate** server that drives a live PyXspec so an agent can actually run an
analysis (load → model → fit → inspect). Design: [../PLAN-B.md](../PLAN-B.md).
Keep it separate from the read-only Tier A server; it is opt-in and higher-risk.

**Tools (B1–B3):** `reset_session`, `load_data`, `define_model`, `fit`,
`get_state`, `set_parameter`, `error`, `calc_flux`, `calc_lumin`, `steppar`,
`plot`, `fakeit`, `run_mcmc`, `save_session`, `restore_session`.

**Agent aids:** `assess_fit` (composite quality check — pegged limits, residual
runs test, reduced-chi sanity, optional Monte-Carlo goodness → `{acceptable,
issues, issue_kinds}`), `plot_image` (render a figure for a human; device
inferred from extension — `.pdf` (recommended) or `.ps`; this giza build's other
hardcopy drivers, incl. png/gif, don't work reliably in the worker),
`export_script` / `journal` (emit a standalone PyXspec script reproducing the
session — a reproducible artifact).

**Data prep (pre-analysis; no session needed):** `pha_info` (inspect a PHA
header — mission, exposure, linked RMF/ARF/background, grouping, counts),
`group_spectrum` (ftgrouppha via heasoftpy; grouptype min/snmin/opt/…; embeds
absolute response/arf/background paths so the grouped output is self-contained).

**Full API coverage:** `xspec_get`, `xspec_set`, `xspec_call` navigate the live
object graph (`ROOT.attr(int)...` against AllData/AllModels/Fit/Xset/Plot/
AllChains) to reach **any** attribute or method — 100% of the object-model API,
not just the structured tools. Unrestricted (per design decision): these do
not enforce the filesystem allowlist and can reach code-loading/`restore` (RCE);
appropriate for trusted local use. Set `XSPEC_RUN_GENERIC=0` to drop all three
for a less-trusted deployment (the structured, allowlisted tools remain).

Resource caps: steppar grid, MCMC length, fakeit spectra count, and a worker
CPU-time `ulimit`. For the structured tools, read paths must be under
`XSPEC_DATA_ROOT`; written files (chains, `.xcm`) under `XSPEC_OUTPUT_ROOT`.

**How it works:** the server (`xspec_run.py`) never imports `xspec`; it manages a
worker subprocess (`worker.py`) that runs PyXspec in a HEADAS-initialized shell.
The worker sends JSON responses on a dedicated fd (XSPEC's stdout noise is
discarded). Calls are serialized (XSPEC is not thread-safe) with per-call
timeouts; data paths are restricted to `XSPEC_DATA_ROOT`.

**Env:** `XSPEC_DATA_ROOT` (allowlisted read dir), `XSPEC_OUTPUT_ROOT`
(allowlisted write dir for chains/.xcm), `XSPEC_HEADAS` (HEADAS path),
`XSPEC_PYTHON` (interpreter that can import `xspec`), `XSPEC_RUN_GENERIC`
(`0`/`false`/`no`/`off` drops `xspec_get`/`xspec_set`/`xspec_call`; default on).

**Config entry:**

```json
{
  "mcpServers": {
    "xspec-run": {
      "command": "/opt/miniconda3/bin/python",
      "args": ["/Users/kaa/software/xspec-ai-docs/server/xspec_run.py"],
      "env": {
        "XSPEC_DATA_ROOT": "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough",
        "XSPEC_HEADAS": "/Users/kaa/software/heasoft/aarch64-apple-darwin25.5.0"
      }
    }
  }
}
```

Test: `python tests/test_xspec_run.py` (skips if HEADAS is absent; otherwise
runs a real fit against the walkthrough data through the worker protocol).
