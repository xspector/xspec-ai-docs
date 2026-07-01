# xspec-ai-docs

AI-optimized documentation for XSPEC and PyXspec — a machine-consumable corpus
designed for agents that actually run spectral analysis, not for human reading.

See [PLAN.md](PLAN.md) for the full design and rationale.

## Entry point

`llms.txt` is the root index (models, PyXspec API, commands, guides, grounding).
An agent should start there.

## Layout

```
llms.txt                     root index (generated)
corpus/
  api/       <Class>.md + api.json   PyXspec class API (attrs w/ type+access, method sigs)
  models/    <name>.md + .json       328 models (params/limits from model.dat + prose)
  commands/  <cmd>.md                79 interactive commands
  recipes/   00_object_model.md, 01..06 guides, tcl_pyxspec_map.md
  manifest.json                      full grounding set (anti-hallucination)
generator/   generate.py + extractors (config, modeldat, texmacros, grounding, api)
server/      MCP server (Tier A, read-only) over the corpus — see server/README.md
tests/       run_recipes.py (integrity + live-data recipes), audit_macros.py,
             test_server.py (MCP data-layer)
```

## MCP server

`server/` exposes the corpus as MCP tools (get_model, list_models, get_command,
get_api, lookup_intent, validate, get_guide, corpus_info) — read-only, no XSPEC
execution. See [server/README.md](server/README.md).

Two content layers: an **auto-generated reference layer** (models, commands,
PyXspec API — regenerated from source, never drifts) and a **hand-authored task
layer** (the guides in `corpus/recipes/`, PyXspec-first).

## Regenerating

The generator reads two external source trees (paths in `generator/config.py`,
override via `XSPEC_HEASOFT_SRC` / `XSPEC_MANUAL_DIR`):

```
python generator/generate.py
```

Provenance (XSPEC version + both source commits) is stamped into
`manifest.json` and `llms.txt`.

## Verifying

```
python tests/audit_macros.py     # LaTeX->markdown conversion is clean (models+commands)
python tests/run_recipes.py      # corpus integrity + (with HEADAS) recipes run on real data
```

`run_recipes.py` tier 2 requires an initialized HEADAS/PyXspec; it executes the
documented recipes against the datasets shipped in the XSPEC manual's
`walkthrough/` directory and checks the extracted PyXspec API against live
object introspection.
