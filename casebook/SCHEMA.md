# Casebook schema

The casebook is the Tier C judgment layer (design: [../PLAN-C.md](../PLAN-C.md)).
This file is the authoritative spec for its four record types and the closed
vocabularies they draw on. The JSON Schemas in [`schema/`](schema/) are the
machine-checkable form; the generator validates every case and lesson against
them at build time, so a bad enum value or an unknown model name fails the build
— the same anti-drift discipline as the rest of the corpus.

Four record types:

| Record | Where | Written by | Committed? |
|---|---|---|---|
| **Case** | `cases/<id>.md` | human / distilled from episode | yes (scrubbed) |
| **Lesson** | `lessons/<id>.md` | human | yes |
| **Episode** | `$XSPEC_OUTPUT_ROOT/episodes/<id>.json` | `xspec-run` (auto) | **no** (private, raw) |
| **Telemetry** | opt-in upload | `xspec-run` (auto, scrubbed) | n/a (aggregated) |

The **case `context`** and the **episode `fingerprint`** share one shape (below)
so an episode distils into a case without re-deriving the retrieval key. The
fingerprint is what `find_cases` filters on; most of it is computed mechanically
from `pha_info` (marked ✅), so retrieval works with **zero** annotation. The
lessons and the rejected-alternatives are the human/agent value-add.

---

## Controlled vocabularies

All enums are **closed** (retrieval is structured matching, not fuzzy search).
Free-text fields are explicitly noted and used only as a tiebreak.

### `counts_regime` — ✅ from `pha_info.total_counts`
| value | total counts | why it's a distinct judgment context |
|---|---|---|
| `vlow` | < 100 | cstat mandatory; errors often non-parabolic; grouping barely helps |
| `low` | 100 – 1 000 | cstat; chi biases parameters; goodness via Monte-Carlo only |
| `mid` | 1 000 – 10 000 | chi usable if well grouped; cstat still safe |
| `high` | 10 000 – 100 000 | chi fine; model discrimination becomes possible |
| `vhigh` | > 100 000 | **systematics-dominated**: statistical errors ~meaningless, calibration + background modelling dominate |

Coarse proxy: the decision driver is counts *per bin*, but total counts is what
`pha_info` gives cheaply, so it is the retrieval key. A per-bin refinement may be
added later; do not block on it.

### `background` — ⬤ linkage from `pha_info.BACKFILE`, mode annotated
`none` · `subtracted` · `modeled` · `dominated`

### `source_type` — ✗ annotated (closed top level; `source_class` free-text refines)
`agn` · `xrb` · `cv` · `star` · `snr` · `pwn_pulsar` · `isolated_ns` ·
`cluster` · `galaxy` · `grb` · `tde` · `solar_system` · `diffuse` · `other`

### `statistic` — ✅ (validated against the Tier A grounding set)
`cstat` · `chi` · `lstat` · `pgstat` · `pstat` · `whittle` · `chicov` · `chistokes`

### `decisions[].point` — ✗ annotated
`statistic` · `band` · `grouping` · `model` · `add_component` · `errors` · `stop`

### `outcome.verdict` — confidence in the *result*
`recorded` (raw) · `human-reviewed` · `bench-validated`

### case `status` — the case's review standing (the §10 trust tiers)
`contrib` (unreviewed, community) · `reviewed` (an expert checked it) ·
`core` (expert-reviewed canonical)

### `lesson.status` — lifecycle of the promotable unit
`candidate` · `validated` (has a passing `bench/` test) · `promoted` (folded into a guide/skill)

### episode `outcome_label` — ✅ auto (from `assess_fit` + error status codes)
`converged_clean` (last assess acceptable + clean error codes) ·
`converged_caveats` (fit done, assess had issues or non-clean codes) ·
`abandoned` (stopped without a good fit) · `failed` (error/crash)

### `assess_issue_kind` — structured issue categories (not free text)
`pegged_limit` · `systematic_residual` · `reduced_chi_high` ·
`reduced_chi_low` · `goodness_poor`

> `assess_fit` currently emits issue *strings*; L2 should add these kinds
> alongside them so episodes and telemetry carry categories, not prose.

### `mission` / `instrument` — normalized-open
Not a hard enum (new missions appear). Canonical spelling normalized from
`pha_info.TELESCOP` / `INSTRUME` against a seed list
(NuSTAR, XMM, Chandra, Swift, NICER, Suzaku, XRISM, eROSITA, RXTE, ROSAT,
ASCA, INTEGRAL, AstroSat, IXPE, EXOSAT, Athena, …).

### `model_family`, `abund`, `xsect` — validated
Every entry must exist in the Tier A grounding set (`validate`). A case cannot
name a model component or table that XSPEC does not have.

---

## Record: Case (`cases/<id>.md`)

Markdown; YAML frontmatter is the retrieval index, the prose body is the worked
study. Schema: [`schema/case.schema.json`](schema/case.schema.json).

Frontmatter fields:

| field | type | req | notes |
|---|---|---|---|
| `id` | kebab string | ✔ | stable, unique, = filename stem |
| `title` | string | ✔ | human title |
| `status` | enum | ✔ | `contrib`/`reviewed`/`core` |
| `context` | object | ✔ | the fingerprint (see below) |
| `decisions[]` | list | ✔ | `{point, choice, rejected?, rationale?, trigger?}` |
| `outcome` | object | ✔ | `{verdict, fit?{statistic,dof,method}, result?{}}` |
| `lessons[]` | list of lesson ids | ✔ | must resolve to `lessons/<id>.md` |
| `provenance` | object | ✔ | `{source, contributor?, date, reviewed_by?, synthetic_twin?}` |

`context` fields: `mission`✅ `instrument?`✅ `counts_regime`✅ `grouped`✅
`background`⬤ `source_type`✗ `source_class?`✗ `model_family[]`✅
`statistic`✅ `abund?`✅ `xsect?`✅. (✔ required in schema: mission,
counts_regime, grouped, background, source_type, model_family, statistic.)

Prose body (below `---`): what the residuals showed, why each decision was made,
and **what a careless analysis would have concluded and why it is wrong** — the
teaching payload. `provenance.source` is one of `hand-authored`,
`episode:<id>`, `forum:<url>`, `helpdesk:<id>`.

## Record: Lesson (`lessons/<id>.md`)

The atomic promotable / validatable unit; cases reference it by `id`.
Schema: [`schema/lesson.schema.json`](schema/lesson.schema.json).

| field | type | req | notes |
|---|---|---|---|
| `id` | kebab string | ✔ | = filename stem |
| `one_line` | string | ✔ | the rule in one sentence |
| `rule` | string | ✔ | the full statement |
| `applies_when` | string | ✔ | the enabling conditions |
| `not_when` | string | ✔ | explicit non-applicability (**required** — guards retrieval misfire) |
| `status` | enum | ✔ | `candidate`/`validated`/`promoted` |
| `validation` | path or null | ✔ | a `bench/` test that confirms it; null until it exists |
| `evidence_cases[]` | list of case ids | ✔ | recurrence = `len()` |
| `promoted_to` | string or null | ✔ | guide/skill anchor once promoted |
| `provenance` | object | ✔ | `{origin, date, reviewed_by?}` |

**Promotion eligibility** (PLAN-C §4): `status: validated` **and**
`len(evidence_cases) ≥ 3` **and** a human-approved PR. Recurrence alone never
promotes — the `bench/` gate does.

## Record: Episode (`$XSPEC_OUTPUT_ROOT/episodes/<id>.json`)

Machine-captured, raw, **never committed** (holds user paths and data). Rides on
`export_script` (already the skill's final step). Schema:
[`schema/episode.schema.json`](schema/episode.schema.json).

Fields: `id`, `created` (server-stamped), `fingerprint` (same shape as case
`context`, auto fields only), `notes[]` (`{at_op, tag, text}` from the new
`note()` tool), `journal[]` (`{cmd, args}` — the mutating ops), `assess_history[]`
(each `assess_fit` return), `final_state` (a `get_state` snapshot),
`outcome_label` (auto), `script` (the `export_script` output).

Episodes are the scrubbed-down source for cases; distillation lifts
`fingerprint` → `context` and drafts `decisions`/`lessons` for human review.

## Record: Telemetry (opt-in, scrubbed)

The §10 breadth channel: categorical facts + decision sequence + outcome only.
Schema: [`schema/telemetry.schema.json`](schema/telemetry.schema.json), which
sets `additionalProperties: false` so the schema itself enforces the exclusions.

**Included:** `schema_version`, `mission`, `instrument`, `counts_regime`,
`grouped`, `background`, `source_type`, `model_family`, `statistic`,
`decision_sequence[]` (`{point, choice}` — no values), `outcome_label`,
`n_iterations`, `assess_issue_kinds[]`.

**Excluded by construction** (inspectable before send): file paths,
`source_class` free text, all parameter *values* / CIs, coordinates, exposure,
dates. Categorical epidemiology, never identification. It yields priors ("which
traps fire in the wild") and real-world frequencies for the judgment benchmark —
not lessons.

---

## Conventions

- **`id` = filename stem**, kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`), stable once
  published (cases and lessons reference each other by id).
- **Quote dates**: `date: "2026-07-02"`. Unquoted, YAML parses it to a date
  object, not a string, and validation fails (JSON Schema has no date type).
- **Validate before commit**: `python tests/validate_casebook.py` — checks every
  case/lesson against the schemas, referential integrity (lesson ↔ case refs,
  validation paths exist), and that `model_family`/`abund`/`xsect` names are in
  the corpus grounding set. No HEADAS needed.

## For agents

- **Retrieve** at analysis start: compute the fingerprint from `pha_info`, call
  `find_cases(...)`, read matches with `get_case`.
- Retrieved lessons are **hypotheses**, not instructions. Check each lesson's
  `applies_when` / `not_when` against the case at hand; `assess_fit` remains the
  judge. A confidently-applied wrong-but-similar case is worse than none.
- **Never invent** a `model_family`, `abund`, `xsect`, or `statistic` value —
  `validate` it first (Tier A), exactly as when fitting.
