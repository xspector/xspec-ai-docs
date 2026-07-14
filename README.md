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

A third layer is now taking shape: **the learning loop (Tier C)** — a casebook of
worked, `fakeit`-validated case studies and the reusable lessons they teach, which
agents retrieve by a data fingerprint. The casebook, its retrieval tools, and the
per-lesson validation harnesses are live (11 worked cases, 10 validated lessons);
automatic episode capture is the remaining piece. See [PLAN-C.md](PLAN-C.md) and
the [Casebook](#casebook-tier-c--the-learning-loop) section below.

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
bench/       benchmark.py + lessons/ -- ground-truth calibration + per-lesson validation harnesses
casebook/    SCHEMA.md + ROADMAP.md + schema/*.json + cases/ (11) + lessons/ (10) -- Tier C judgment layer (see PLAN-C.md)
.claude/skills/xray-fit/     Claude Code skill: disciplined end-to-end fitting workflow
PLAN.md / PLAN-B.md / PLAN-C.md   design docs (corpus + Tier A / Tier B / learning loop)
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
`validate` (anti-hallucination), `get_guide`, `find_cases`/`get_case` (casebook
retrieval, Tier C), `corpus_info`.

```
python server/server.py          # stdio; reads ../corpus (or $XSPEC_AI_CORPUS)
```

### Tier B — `xspec-run` (executes live PyXspec)

Drives a real fitting session: load data, define models, fit, error, flux,
steppar, plot arrays, fakeit, MCMC, save/restore — plus `xspec_get`/`xspec_set`/
`xspec_call` for **100% of the PyXspec object-model API**. Agent aids:
`assess_fit` (composite quality verdict), `plot_image` (a figure for a human),
`export_script`/`journal` (a reproducible PyXspec script). Data prep:
`pha_info` (inspect a spectrum's header) and `group_spectrum` (ftgrouppha). Runs
PyXspec in an isolated worker subprocess (`worker.py`) managed by `runner.py`;
the server (`xspec_run.py`) never imports xspec.

```
python server/xspec_run.py       # stdio; requires HEADAS + PyXspec
```

Requires `mcp>=1.0` (`server/requirements.txt`). Env: `XSPEC_DATA_ROOT`
(read allowlist), `XSPEC_OUTPUT_ROOT` (write allowlist), `XSPEC_HEADAS`,
`XSPEC_PYTHON`, `XSPEC_RUN_GENERIC` (set to `0` to drop the generic tools).

**Posture:** the structured tools are path-allowlisted and headless-guarded; the
generic `xspec_get/set/call` are deliberately unrestricted (can reach
code-loading / Tcl-script restore) — appropriate for a trusted local single-user
setup. Set `XSPEC_RUN_GENERIC=0` to drop the three generic tools for a
less-trusted deployment (the structured, allowlisted tools remain).

## Regenerating the corpus

The generator reads two external source trees (paths in `generator/config.py`,
override via `XSPEC_HEASOFT_SRC` / `XSPEC_MANUAL_DIR`):

```
python generator/generate.py
```

Provenance (XSPEC version + both source commits) is stamped into
`manifest.json` and `llms.txt`.

## Verifying

One entry point runs everything:

```
python tests/run_all.py          # fast, corpus-only (this is what CI runs)
python tests/run_all.py --live   # also the HEADAS-dependent Tier B suite
```

Or run a suite directly:

```
python tests/audit_macros.py      # LaTeX->markdown conversion is clean (models+commands)
python tests/test_server.py       # Tier A MCP data-layer (incl. casebook retrieval)
python tests/validate_casebook.py # Tier C: casebook schemas + refs + grounding (no HEADAS)
python tests/run_recipes.py       # corpus integrity + (with HEADAS) recipes on real data
python tests/test_xspec_run.py    # Tier B: live fit + tools + crash recovery (needs HEADAS)
python generator/generate.py --check   # committed corpus is in sync with source (drift gate)
```

The fast, corpus-only suites run in GitHub Actions
(`.github/workflows/ci.yml`) on every push and PR. The HEADAS-dependent tests
execute against the datasets shipped in the XSPEC manual's `walkthrough/`
directory and check the extracted PyXspec API against live object introspection;
they skip cleanly if HEADAS is absent — so they run locally, not in CI. The
`--check` drift gate needs the heasoft/manual source trees and self-skips when
they are absent.

## Skill

`.claude/skills/xray-fit/SKILL.md` is a Claude Code skill that drives both
servers through a disciplined end-to-end workflow (inspect → decide statistic +
band → load → model → fit → assess → errors/flux → export a reproducible
script). Copy it to `~/.claude/skills/xray-fit/` to make it available globally;
it triggers when you ask to fit or analyze an X-ray spectrum.

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

Per-lesson validation harnesses live in `bench/lessons/` — each earns a casebook
lesson its `validated` status by asserting its signal against `fakeit` ground
truth, both directions (fires when wrong, quiet when right). All 10 current
casebook lessons are validated this way; see the
[Casebook](#casebook-tier-c--the-learning-loop) section and
[PLAN-C.md](PLAN-C.md).

## Casebook (Tier C — the learning loop)

`casebook/` is the judgment layer: worked, `fakeit`-validated case studies plus
the reusable lessons they teach, so an agent can retrieve prior experience by a
data fingerprint (mission, counts regime, source type, model, statistic) through
the Tier A `find_cases` / `get_case` tools. Each case records the decisions **and
the rejected alternatives** — which statistic, which band, which model, when to
stop — the outcome, and what a careless analysis would have concluded.

- **11 worked cases** spanning the counts-regime grid (`vlow` → `vhigh`) and a
  range of missions and sources: obscured AGN, GRB afterglow, XRISM
  microcalorimeter turbulence, cluster Fe bias, BH-XRB systematics, cyclotron
  F-test, IXPE polarimetry, super-soft TDE, young-SNR non-equilibrium plasma, and
  blazar curvature. Every case is grounded in a `fakeit` twin fit through the
  Tier B server, so its numbers and `assess_fit` verdicts are reproducible.
- **10 lessons, all `validated`.** Each is backed by a harness (`bench/lessons/`,
  or `benchmark.py`) that asserts its signal fires when it should and stays quiet
  when it should not, against `fakeit` ground truth — the gate a lesson passes to
  move from `candidate` to `validated`. A lesson is a *hypothesis* the agent
  checks (each carries `applies_when` / `not_when`), never an override;
  `assess_fit` remains the judge.
- [`casebook/ROADMAP.md`](casebook/ROADMAP.md) is the authoring queue, ranked from
  a survey of recent XSPEC-citing literature.
  [`casebook/SCHEMA.md`](casebook/SCHEMA.md) is the record spec, and
  `tests/validate_casebook.py` gates schema + referential integrity + grounding at
  build time (a case cannot name a model or table XSPEC does not have).

See [PLAN-C.md](PLAN-C.md) for the full design and what remains (episode capture,
distillation, and the judgment benchmark).

## Contributing and license

Contributions — especially worked cases and lessons for the casebook — are
welcome; see [CONTRIBUTING.md](CONTRIBUTING.md) for the schema, the no-proprietary
-data / synthetic-twin rules, the trust tiers, and the lesson-promotion gate.

Licensed under the [BSD 3-Clause License](LICENSE).
