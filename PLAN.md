# XSPEC / PyXspec AI Documentation — Design & Plan

Status: **corpus complete** — reference layer (328 models + 79 command docs),
full task layer (6 guides), and full grounding manifest all generate from source;
executable claims verified against live data; auditor clean over 407 docs.
Owner: Keith Arnaud
Generated-from XSPEC version: *(stamped by generator at build time)*

---

## 1. Purpose

Provide documentation optimized for **AI consumption**, not humans, so that an
agent can perform real X-ray spectral analysis with XSPEC/PyXspec end-to-end:
load a dataset, choose a statistic and energy range, define and fit a model,
compute errors and fluxes, and return results as structured data.

- **Audience:** AI, **agentic-first** (a tool-executing agent such as Claude
  Code), while also serving Q&A assistants.
- **Existing docs are for humans:** the LaTeX manual (`Xspec-aux/doc/manual`)
  and the PyXspec Sphinx docs (in the heasoft tree) are prose-first, have no
  machine-readable parameter layer, and provide **no mapping** between the
  interactive Tcl command and the equivalent PyXspec call. This project fills
  those gaps.

## 2. Delivery model

- **Structured text corpus now, MCP server later.** The corpus is authored so
  it doubles as the MCP's backing data — no rework when the server is added.
- **Drive surface: PyXspec-first**, interactive Tcl cross-referenced. PyXspec
  returns typed values, raises exceptions instead of blocking on interactive
  prompts, and avoids `tclout` string-scraping — all better for an execution
  loop. Every recipe leads in PyXspec and shows the Tcl equivalent.

## 3. Content = two layers

### 3.1 Reference layer — auto-generated, full coverage

| Entry type          | Source of truth (authoritative)                                   | Output                       |
|---------------------|-------------------------------------------------------------------|------------------------------|
| Models (~300)       | `manager/model.dat` (component type, params, unit, default, hard/soft limits, fit-delta/frozen) **joined with** prose from `XSmodel*.tex` | markdown+frontmatter + JSON  |
| Commands            | `XS<cmd>.tex` (custom macros → markdown)                           | markdown+frontmatter         |
| PyXspec API         | `XSUser/Python/xspec/*.py` (`ast` extraction of `property`/`def` + docstrings; authoritative — matches installed API) → 18 class docs (`corpus/api/`) + `api.json`, verified against live `dir()` introspection | markdown+frontmatter + JSON  |
| **Tcl ↔ PyXspec map** | generated join                                                   | inline in each command doc **and** a standalone bidirectional table |

Key structural facts the generator must honor:
- **One `.tex` documents many model variants** (e.g. `XSmodelTbabs.tex` → 8
  variants, `XSmodelApec.tex` → 6), all listed in `\xslabel{}`. `model.dat` has
  a separate authoritative entry per variant. **Join key: `\xslabel` → tex
  file; params always from `model.dat`.**
- **Additive models get an implicit `norm` parameter** appended (not in
  `model.dat`).
- **Switch/scale params** appear as `$name value` in `model.dat` (not fitted).
- The prose `xspartable` is a *lossy* human rendering of `model.dat` and is
  **not** used for parameter facts — only for descriptive text.

### 3.2 Task layer — hand-authored (exists in neither doc set), PyXspec-first

Ranked by what an agent hits first when handed a dataset:

1. **Headless-run + structured-output guide** — ✅ authored
   (`corpus/recipes/01_headless_and_output.md`), API verified against live data.
2. **Data-ingestion + decisions guide** — ✅ authored
   (`corpus/recipes/02_data_ingestion_and_decisions.md`), API verified.
3. **End-to-end runnable recipes** — ✅ authored (`03_recipes.md`), 10 recipes
   (fit, error, flux/lumin, steppar, plot, fakeit, MCMC, joint fit, goodness,
   save/restore); every executable claim verified against live data.
4. **Anti-patterns / known failure modes** — ✅ authored (`04_antipatterns.md`).
5. **Error-message catalog** — ✅ authored (`05_error_catalog.md`); strings
   grepped verbatim from XSPEC source (XSFit/XSModel/XSUser).
6. **Model-selection guidance** — ✅ authored (`06_model_selection.md`);
   component-type counts derived from the model.dat corpus (228 add / 75 mul /
   24 con / 1 acn).
7. **Intent → API reverse index** — ✅ (`07_intent_index.md` +
   `intent_index.json`): 70 "I want to X → call Y" entries, PyXspec-first with
   Tcl cross-reference. Every API reference is validated against `api.json`
   (tests fail if an entry names a call that doesn't exist).

> All six task-layer docs authored (2026-07-01). Reference layer + task layer
> complete; remaining: full grounding manifest (step 3), commands reference.

## 4. Grounding manifest (JSON) — full grounding set

Everything an AI could hallucinate becomes checkable against one manifest.
**Status: implemented** (`corpus/manifest.json`), each with provenance:
- models — 328 (from `model.dat`: name, component type, param schema)
- command tokens — 161 incl. aliases (`XSGlobal.cxx createCommandMap`, authoritative)
- command docs — 79 (`Commands.tex` \input list)
- statistics — fit (8) + test (4) (`XSstatistic.tex` / appendix)
- plot types — 38 (`PlotCommandCreator.cxx`)
- `tclout` keys — 73 (`XStclout.tex`)
- `xset` keys — documented subset (best-effort; xset takes arbitrary keys)
- abundance tables — 10 + file/read (`manager/abundances.dat`)
- cross-sections — vern/bcmc/obcm (`NeutralOpacity.cxx`)

## 5. Build, packaging, maintenance

- **Separate repo/package** (this repo), with an `llms.txt` root index (titles +
  one-line summaries + paths) as the AI entry point. The future MCP server reads
  the same tree.
- **Generator** (Python): reads from **two source trees** — heasoft
  (`model.dat`, PyXspec `.py`, Sphinx) and the manual repo (`XS*.tex`) — and
  emits the corpus + manifest. Because it reads external trees, it needs:
  - configured, pinned paths to both trees, and
  - an **XSPEC-version stamp** written into the manifest and `llms.txt`.
- **Build-integrated regeneration:** the reference layer + manifest are rebuilt
  from source so they never drift. The task layer is version-controlled and
  human-reviewed.
- **Verification: automated test harness.** Every recipe is executed against the
  datasets shipped in `Xspec-aux/doc/manual/walkthrough` (`s54405.pha` + ACIS
  rmf/arf, polarization toy data); a recipe that errors fails the build.

## 6. Risks / open items

1. ~~Confirm items 3–6 of the task layer are all in scope.~~ Done (all in scope).
2. **Macro dictionary:** `.tex` uses custom macros (`\syn`, `\xscmd`,
   `\xscmdii`, `\modname`, `\argdes`, `\argval`, `xspartable`, `\pubreflink`,
   `\plasmanorm`, `\cgsflux`, …). The extractor needs an explicit macro→markdown
   map (~15–20 macros), not a generic LaTeX converter. Prototype validates this.
3. **Version pinning:** manifest/`llms.txt` must stamp the XSPEC version and the
   commit of both source trees used.
4. **PyXspec docstring quality varies** — some `property` docstrings are thin and
   may need curated supplements for key classes.

## 7. Repository layout

```
xspec-ai-docs/
  PLAN.md                     # this file
  llms.txt                    # root index (generated)
  generator/
    config.py                 # pinned source paths + version stamp
    texmacros.py              # macro dictionary + LaTeX→markdown
    modeldat.py               # model.dat parser
    generate.py               # orchestrator
  corpus/
    models/     <name>.md + <name>.json
    commands/   <cmd>.md
    recipes/    task-layer docs, tcl_pyxspec_map.md
    manifest.json             # full grounding set (generated)
  tests/
    run_recipes.py            # executes recipes against walkthrough data
```

## 8. Prototype scope (this iteration)

Validate extraction + join on a representative slice before committing to all
~300 models:
- Models: `powerlaw` (additive, implicit norm), `TBabs` (multiplicative,
  scaled unit), `apec` (additive, multi-variant tex, frozen params).
- Commands + Tcl↔PyXspec map: `data`, `model`, `fit`.
- Emit `corpus/models/*.{md,json}`, a partial `manifest.json`, and the mapping
  doc. Confirms the macro dictionary and the `model.dat`↔`.tex` join on real
  data.
