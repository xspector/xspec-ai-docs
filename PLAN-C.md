# Tier C — the learning loop (design)

Status: **design recorded 2026-07-02 — nothing implemented.** This documents the
judgment/worked-case-studies discussion and the decision record on trained
models. Owner: Keith Arnaud.

Goal (verbatim): *"a system which learns so that the agents get cleverer the
more data analysis they do."*

Tier A gives an agent knowledge (what exists, exact parameters). Tier B gives it
hands (a live, verified PyXspec). Tier C is judgment: the tacit knowledge of an
experienced X-ray astronomer — when to add a component, when errors are
meaningless, which statistic in which regime, when to stop — captured so that it
**accumulates** from real analyses instead of being written once.

---

## 1. What "learning" means here

No weight updates (see §8). Three mechanisms, in increasing order of commitment:

1. **Episodic memory** — every analysis run through `xspec-run` is captured
   automatically as a structured *episode* (data fingerprint, decisions,
   actions, outcome). Future sessions retrieve similar past analyses. Fast,
   automatic, private to the local machine.
2. **Distilled cases** — episodes are condensed into reviewed, generalized
   *case* entries in this repo: situation → decision points → outcome → lesson.
   This is the shareable knowledge.
3. **Promotion** — a lesson that recurs across independent cases **and**
   survives synthetic validation is promoted into the task-layer guides or the
   `xray-fit` skill, changing default behavior for all future analyses.
   Human-approved, always.

**The asset that makes this safe:** `fakeit` provides ground truth on demand.
Any candidate heuristic ("prefer cstat below N counts", "don't quote errors
when a parameter sits within X of a limit") can be encoded as a synthetic
scenario with known parameters and scored — did following the lesson improve
recovery and coverage? That is the difference between a system that *learns*
and one that *drifts*. `bench/benchmark.py` already does exactly this scoring
(the chi-on-low-counts trap is the prototype); Tier C points it at lessons.

## 2. The loop

```
analysis (xspec-run session, driven by the xray-fit skill)
   │  export_script fires → episode.json written alongside
   │  (journal + pha_info fingerprint + decision notes + assess_fit history
   │   + final state + outcome label)
   ▼
episodes/            local, raw, private (XSPEC_OUTPUT_ROOT — never committed)
   │  distill: agent drafts a case in the schema; human reviews; git commit
   ▼
casebook/            in-repo, scrubbed, general — the shared judgment layer
   │  validate: lesson → fakeit scenario in bench/lessons/, scored with/without
   ▼
promotion            validated + recurrent → guide/skill edit via reviewed PR
   ▲
retrieval            find_cases() from pha_info's fingerprint, at analysis start
```

Two loops at different speeds and trust levels:

- **Private fast loop** — episodes accumulate automatically; the agent recalls
  "you fit this source class in March; here is what worked." No review burden.
- **Shared slow loop** — reviewed cases in the repo. Because it is git,
  community contributions arrive as PRs with provenance; at XSPEC-user-base
  scale this becomes the accumulating, validated judgment layer for everyone.
  That is the endgame that actually delivers "cleverer the more analysis it
  does" — one user's episode volume is slow; a community's is not.

## 3. The unit of knowledge — case schema

Designed first, because it unifies everything: the hand-authored worked studies
(the original deferred item), machine-captured episodes, and retrieval all use
the same shape. A case file is markdown with YAML frontmatter — the frontmatter
is the retrieval index, the prose body is the worked study.

```yaml
id: nicer-lowcount-thermal-001
title: Low-count NICER thermal point source
context:                        # retrieval key — computable from pha_info
  mission: NICER
  instrument: XTI
  counts_regime: low            # vlow <100 | low 100-1k | mid 1k-10k | high >10k
  grouped: false
  background: model             # none | subtracted | model | dominated
  source_class: thermal point source
  model_family: [bbodyrad, nsatmos]
decisions:
  - point: statistic            # statistic | band | grouping | model | errors | stop
    choice: cstat
    rejected: "chi — biases kT low ~15% at these counts"
  - point: model
    path: "bbodyrad -> nsatmos"
    trigger: "kT pegged at hard limit + runs-test failure in 1-2 keV"
outcome:
  verdict: bench-validated      # recorded | human-reviewed | bench-validated
  result: { kT_keV: ..., ci90: [...] }
lessons:
  - id: cstat-lowcount-thermal
    rule: "..."
    applies_when: "..."
    not_when: "..."             # explicit non-applicability — required
    validation: bench/lessons/cstat-lowcount.py   # absent until validated
provenance:
  source: hand-authored         # or: episode <id>
  date: 2026-07-02
  reviewed_by: kaa
```

```markdown
<prose body: the narrative worked study — what was tried, what the residuals
looked like, why each decision was made, what a less careful analysis would
have concluded and why it would be wrong.>
```

Vocabulary fixed by a `casebook/SCHEMA.md`: counts-regime buckets, decision
points, verdict levels, background modes — discrete keys so retrieval is
structured matching, not fuzzy search.

## 4. Component design

**Retrieval (Tier A grows two tools).** `find_cases(mission?, counts_regime?,
source_class?, model_family?, text?)` → ranked matches with their lessons;
`get_case(id)` → full case. Scoring: weighted exact-field matches, text as
tiebreak. No embeddings — the casebook will be tens-to-hundreds of entries;
structured filtering is sufficient, debuggable, and dependency-free. Because
`pha_info` already returns mission/instrument/exposure/counts/grouping, the
fingerprint is computed mechanically — the skill consults the casebook right
after inspecting the data without having to formulate a query.

**Capture (Tier B).** Episode emission hooks `export_script` — the skill
already mandates it as the final step, so capture comes free with existing
discipline. Episode record: fingerprint, journal, `assess_fit` history, final
state (params + CIs + stat/dof), and an auto-computed outcome label
(`converged_clean` = last assess acceptable + clean error codes;
`converged_with_caveats`; `abandoned`; `failed`). Plus one new lightweight
worker tool, `note(text, tag?)`, appended to the journal; the skill requires it
at the statistic / band / model-change decision points so *rationale* is
interleaved with actions. Episodes live under `XSPEC_OUTPUT_ROOT/episodes/` —
they may contain user paths and private data, so they are never committed;
cases are the scrubbed derivative.

**Distillation.** A `/distill-case` pass: given an episode and `SCHEMA.md`,
draft a case file for human review. Git is the review gate — nothing enters
`casebook/` without a human commit.

**Validation.** `bench/lessons/<id>.py`: a fakeit scenario generator with known
truth, a scripted policy *without* the lesson vs *with* it, and a metric
(recovery bias, CI coverage, or decision accuracy). Cheap and deterministic —
the "policy" for decision-type lessons is scripted, not a full agent run.

**Promotion policy.** A lesson is eligible to change `corpus/recipes/` or the
skill only when (a) it has a passing `bench/lessons/` validation, (b) it recurs
in ≥3 independent cases, and (c) a human approves the PR. Recurrence alone is
never sufficient (§6).

**Measurement — the judgment benchmark.** "Cleverer" must be a number. Extend
`bench/` with scenarios scored on *decisions*, not just parameter recovery:
does the agent choose cstat on low counts, refuse to quote errors on a pegged
parameter, detect the need for a second component, stop adding components when
justified? Run end-to-end through the skill periodically and track the score
against casebook size. Without this curve, "learning" is an anecdote.

## 5. What already exists vs. what is new

| Existing piece | Role in the loop |
|---|---|
| `journal` / `export_script` (worker) | capture hook — episodes ride on it |
| `assess_fit` | outcome labeling + runtime judge of retrieved lessons |
| `pha_info` | retrieval fingerprint, computed mechanically |
| `bench/benchmark.py` | validation harness template (chi trap = first "lesson") |
| Tier A server + `intent_index` | retrieval pattern + home for `find_cases` |
| `corpus/recipes/` guides + `xray-fit` skill | promotion target |
| git repo | review gate + community distribution channel |

New: the schema, the seed casebook, two Tier A tools, the episode writer +
`note()`, `/distill-case`, `bench/lessons/`, the judgment benchmark. Mostly
wiring and content — no new machinery class.

## 6. Failure modes and defenses

| Risk | Mechanism | Defense |
|---|---|---|
| Selection bias | episodes record what the agent *did*, not what was *right* | distill only from validated outcomes (bench- or human-confirmed) |
| Frequency ≠ correctness | the same mistake N times looks like a pattern | promotion gated on fakeit validation, never on recurrence alone |
| Retrieval misfire | similar-but-wrong case applied confidently | mandatory `applies_when`/`not_when`; lessons are hypotheses; `assess_fit` remains the judge, always |
| Silent drift | guides/skill change without oversight | promotion only via human-approved PR |
| Unmeasured improvement | "cleverer" as anecdote | judgment benchmark tracked vs. casebook size |
| Privacy / size | raw episodes hold user paths and data | episodes local-only; cases are scrubbed derivatives |

## 7. Phasing

- **L1 — schema + seed casebook + retrieval.** This *absorbs the deferred
  worked-case-studies item*: 6–10 canonical studies written in the schema, each
  encoding at least one trap — high-count CCD continuum; low-count cstat point
  source; thermal plasma with abundance choices; background-dominated source;
  joint multi-instrument fit; an F-test-misuse case; a
  when-to-stop-adding-components case. Deliverables: `casebook/SCHEMA.md`,
  `casebook/cases/*.md`, Tier A `find_cases`/`get_case`, skill step "consult
  casebook after `pha_info`", generator indexes the casebook into the manifest.
- **L2 — episode capture.** Episode writer on `export_script`; `note()` tool;
  skill mandates decision notes; episodes under the output root.
- **L3 — distillation + validation.** `/distill-case`; `bench/lessons/`
  harness; the judgment benchmark; promotion policy in force.
- **L4 — community loop.** Contribution guide (provenance + review
  requirements), PR-based case review; revisit retrieval scaling (embeddings)
  only if the casebook exceeds a few hundred entries. Sociological design: §10.

## 8. Decision record — trained models (2026-07-02)

Question: should we build a small targeted LLM instead of (or alongside) this?

| Option | Decision | Reasoning |
|---|---|---|
| Small LLM from scratch on the domain | **Rejected** | Corpus is orders of magnitude too small for general competence; the result would reason worse than any frontier model while still hallucinating. |
| Fine-tune a small open model on the *knowledge* (models/params/syntax) | **Rejected** | Fine-tuning teaches style/behavior, not reliable facts — it would invent parameter names at the edges, the exact failure `validate` exists to stop. Retrieval wins on every axis: verifiably exact (generated from `model.dat`), regenerates in minutes per XSPEC release (a fine-tune goes stale), and model-agnostic (the MCP layer makes any frontier model XSPEC-literate; frontier models improve for free — weights are a depreciating asset). |
| Fine-tune on the *judgment* (LoRA on decision episodes) | **Deferred, not rejected** | Right idea, wrong order: it needs on the order of thousands of *validated* decision episodes, and today there are zero. The Tier C loop **is the training-data pipeline** — every validated episode is a training pair. Revisit when ALL of: (1) ~1000+ validated episodes exist; (2) the judgment benchmark exists to score it; (3) a candidate beats frontier + retrieval on that benchmark; (4) there is a cost/privacy/scale driver. |
| Narrow supervised models (not LLMs) | **Viable early — best near-term trained artifact** | fakeit changes the economics: unlimited labeled data by construction. Standout: a **residual-pattern classifier** — generate spectra with a known missing component (line, edge, second continuum, wrong abundance), fit the deliberately wrong model, and the labeled delchi arrays are free; train a small 1D CNN to classify "what kind of thing is missing" and plug it into `assess_fit` as a suggestion channel. Table-model emulators are the same category. |
| Survey-scale cascade (local distilled model triages, frontier handles hard cases) | **Future scenario** | Relevant when fitting ~10⁵ sources (eROSITA-class) where a frontier API call per source is untenable. Note: with validated data in hand, most routine decisions (statistic given counts, band given mission) collapse to scripted policy + a classifier — the LLM is reserved for cases that genuinely need reasoning. |

Summary: build the casebook loop first because it is the *prerequisite* for any
targeted model, not a substitute for it. If a trained artifact is wanted
sooner, the fakeit-synthesized residual classifier is the highest-value,
lowest-risk start.

## 9. Relationship to Tiers A and B

Tier C is data + two retrieval tools + one capture hook — not a third server.
`find_cases`/`get_case` live in the Tier A server (read-only, like the rest of
the corpus); episode capture and `note()` live in the Tier B worker. The
casebook is corpus content, regenerated/indexed by the same generator, stamped
with the same provenance.

## 10. Community accumulation — the sociological design (2026-07-02)

The failure mode of scientific case libraries is the empty wiki, not bad
schema. The design starts from a reframe: **"accumulate from many users"
conflates two different resources.** The knowledge space is finite and
concentrated — missions × count regimes × source classes × traps saturates at
a few hundred cases, and most of the judgment lives in a few dozen experts and
in archives that already exist. The target is *coverage*, not mass
participation. Two channels with different mechanisms:

| Channel | Who | Effort | Yields |
|---|---|---|---|
| **Depth** | few experts + existing archives | review-only (agent drafts) | the lessons — casebook content |
| **Breadth** | many users, opt-in | zero (automatic, scrubbed) | priors + epidemiology — which traps fire in the wild, which cases to commission, real-world frequencies for the judgment benchmark |

**Depth channel — mine what exists before soliciting anything new.** The
largest untapped case corpus is the XSPEC mailing-list/forum archive: decades
of real user problems with expert answers attached — (situation, decision,
lesson) in raw form. Likewise helpdesk ticket archives (HEASARC/CXC/XMM SOC)
and instrument-team analysis guides. An agent pass drafts cases from
high-value threads; an expert reviews. This bootstraps hundreds of candidates
with no one asked to do new work. Going forward it becomes a flywheel: every
forum question answered anyway is agent-drafted into a case as a side effect —
*answer once, encode forever*. This is the one scheme whose incentive lands on
the maintainer: support burden **decreases** as the corpus grows, because the
agent starts answering the recurring questions.

**Breadth channel — telemetry, not contribution.** An opt-in flag shares
scrubbed episode fingerprints: mission, counts regime, model families tried,
decision sequence, outcome flags. Deliberately excluded: source names,
coordinates, parameter values (an unusual kT for a known source is
unpublished science; one leak destroys trust). The payload must be
inspectable before send.

**Levers for voluntary case contribution** (the ones with astronomy
precedent):

- **Byproduct, not task.** The episode already exists; the agent drafts the
  case; submission is one command. Hours become one decision.
- **Synthetic twin.** A contributor's real analysis is reproduced as a fakeit
  scenario with similar parameters: the shared case contains *no proprietary
  data* (dissolves the embargo problem) and arrives *pre-validated* (the twin
  has known truth). Privacy and quality control in one move.
- **Credit that counts.** Attribution on every case; a Zenodo DOI for the
  casebook; a periodic casebook paper with contributors as co-authors
  (Astropy/AtomDB precedent). The deeper model is the **medical case report**:
  medicine solved exactly this problem — accumulating practitioner judgment —
  by making the short, structured, peer-reviewed, *citable* case a recognized
  publication genre.
- **Authority seeding.** The seed cases set the bar and format; contributors
  imitate what they see. A reviewed-by badge from known experts is what
  distinguishes the casebook from a forum thread — *vetting is the product*.
- **Teaching double-duty.** The casebook is also the by-example textbook the
  field lacks. Summer schools can assign case-writing with mentor review — a
  steady, supervised contribution stream, and every student reader is a
  future contributor.

**Structural issues at scale:**

- **Review bottleneck / bus factor.** "Email the maintainer" 2.0 recreates the
  succession problem. Tiered trust instead: `contrib/` (unreviewed; retrieval
  flags the tier) → bench-validated (the fakeit harness passed it) →
  expert-reviewed core. The validation harness matters *sociologically* here:
  it is an automated reviewer — the only kind that scales — converting "do I
  trust this stranger's lesson" into "does it pass the synthetic test."
- **Governance and home.** A personal repo invites fragmentation (each data
  center doing its own). The stable equilibrium mirrors CALDB: instrument
  teams own their mission's cases along existing funded institutional lines;
  HEASARC or a community org hosts; curation is a *funded job* — sustained
  curation in astronomy is essentially never volunteer work (CALDB, AtomDB,
  CHIANTI are all staffed).

**Sequencing constraint under all of it:** nobody contributes to the casebook
of a tool they don't use. Adoption first — the tooling must make individual
analyses visibly better with the seed casebook alone. Telemetry and submission
hooks ship quietly with the tool; the contribution drive starts only after the
value is proven. Archive mining runs regardless, since it needs no one's
participation.
