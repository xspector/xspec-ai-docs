# xspec-ai-docs

AI-optimized documentation for XSPEC and PyXspec — a machine-consumable corpus
for agents that actually run spectral analysis, plus two MCP servers that expose
it and drive a live PyXspec.

Three things live here:

1. **A docs corpus** — models, commands, PyXspec class API, task guides, and a
   grounding manifest, generated from source. See [PLAN.md](PLAN.md).
2. **`xspec-ai-docs` MCP server (Tier A)** — read-only lookups over the corpus.
3. **`xspec-run` MCP server (Tier B)** — executes a live PyXspec session. See
   [PLAN-B.md](PLAN-B.md).

## Entry point

`llms.txt` is the root index (models, PyXspec API, commands, guides, grounding).
An agent should start there.

## Layout

```
llms.txt                     root index (generated)
corpus/
  api/       <Class>.md + api.json   PyXspec class API (18 classes; attrs w/ type+access, method sigs)
  models/    <name>.md + .json       328 models (params/limits from model.dat + prose)
  commands/  <cmd>.md                79 interactive commands
  recipes/   00_object_model.md, 01..07 guides, tcl_pyxspec_map.md
  manifest.json                      full grounding set (anti-hallucination)
  intent_index.json                  "I want to X -> call Y" (also recipes/07)
generator/   generate.py + extractors (config, modeldat, texmacros, grounding, api, intents)
server/      MCP servers: server.py (Tier A) + xspec_run.py/runner.py/worker.py (Tier B)
             -- see server/README.md
tests/       audit_macros.py, run_recipes.py, test_server.py (Tier A),
             test_xspec_run.py (Tier B)
bench/       benchmark.py -- ground-truth calibration of xspec-run (see bench/README.md)
PLAN.md / PLAN-B.md          design docs (corpus + Tier A / Tier B)
```

Two content layers: an **auto-generated reference layer** (models, commands,
PyXspec API — regenerated from source, never drifts) and a **hand-authored task
layer** (the guides in `corpus/recipes/`, PyXspec-first).

## MCP servers

Full details and client config in [server/README.md](server/README.md);
`server/mcp-config.example.json` has both entries ready to adapt.

### Tier A — `xspec-ai-docs` (read-only)

Lookups over the corpus; no XSPEC execution, safe to run anywhere.
Tools: `get_model`, `list_models`, `get_command`, `get_api`, `lookup_intent`,
`validate` (anti-hallucination), `get_guide`, `corpus_info`.

```
python server/server.py          # stdio; reads ../corpus (or $XSPEC_AI_CORPUS)
```

### Tier B — `xspec-run` (executes live PyXspec)

Drives a real fitting session: load data, define models, fit, error, flux,
steppar, plot arrays, fakeit, MCMC, save/restore — plus `xspec_get`/`xspec_set`/
`xspec_call` for **100% of the PyXspec object-model API**. Agent aids:
`assess_fit` (composite quality verdict), `plot_image` (a figure for a human),
`export_script`/`journal` (a reproducible PyXspec script of the session). Runs
PyXspec in an isolated worker subprocess (`worker.py`) managed by `runner.py`;
the server (`xspec_run.py`) never imports xspec.

```
python server/xspec_run.py       # stdio; requires HEADAS + PyXspec
```

Requires `mcp>=1.0` (`server/requirements.txt`). Env: `XSPEC_DATA_ROOT`
(read allowlist), `XSPEC_OUTPUT_ROOT` (write allowlist), `XSPEC_HEADAS`,
`XSPEC_PYTHON`.

**Posture:** the structured tools are path-allowlisted and headless-guarded; the
generic `xspec_get/set/call` are deliberately unrestricted (can reach
code-loading / Tcl-script restore) — appropriate for a trusted local single-user
setup. Drop the three generic tools for a less-trusted deployment.

## Regenerating the corpus

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
python tests/run_recipes.py      # corpus integrity + (with HEADAS) recipes on real data
python tests/test_server.py      # Tier A MCP data-layer
python tests/test_xspec_run.py   # Tier B: live fit + tools + crash recovery (needs HEADAS)
```

The HEADAS-dependent tests execute against the datasets shipped in the XSPEC
manual's `walkthrough/` directory and check the extracted PyXspec API against
live object introspection; they skip cleanly if HEADAS is absent.

## Benchmarking

```
python bench/benchmark.py [N]    # ground-truth calibration of xspec-run (needs HEADAS)
```

Generates synthetic spectra with known parameters via `fakeit`, recovers them
through the server, and scores **coverage** (does the truth land in the 90%/1σ
CI at the nominal rate?) and **pull** (unbiased, correctly-sized errors) — with
a trap showing `chi` is mis-calibrated on low counts where `cstat` is not. This
measures whether the results are trustworthy, not just that the tools run. See
[bench/README.md](bench/README.md).
