# Contributing

Two very different things live in this repo, with different contribution rules:

- The **reference corpus** (`corpus/`, `generator/`) is **generated from source**
  (`model.dat`, PyXspec, the LaTeX manual). Do not hand-edit `corpus/` — fix the
  source or the generator and regenerate (`python generator/generate.py`).
- The **casebook** (`casebook/`) is the **hand-authored judgment layer** — worked
  analysis cases and the reusable lessons drawn from them. This is where
  community contributions accumulate, and what the rest of this file is about.

See [PLAN-C.md](PLAN-C.md) for the full design of the learning loop; the schema
and controlled vocabularies are in [casebook/SCHEMA.md](casebook/SCHEMA.md).

## What makes a good case

A worked analysis that teaches a *decision*, not just a result: which statistic
and band, when to add or drop a component, when errors are trustworthy, when to
stop — and, crucially, **what a careless analysis would have concluded and why
it is wrong**. One case should carry at least one reusable lesson.

## The rules that protect the casebook

1. **No proprietary or unpublished data.** A shared case must not depend on
   private data. Reproduce your analysis as a **synthetic twin**: a `fakeit`
   scenario with similar parameters (a `bench/lessons/` harness, or a documented
   recipe). This both removes the embargo problem and makes the case
   *pre-validated* against known truth.
2. **Scrub identifying detail.** No source names, coordinates, ObsIDs, exposures,
   or fitted parameter *values* tied to a real target — an unusual parameter for
   a named source can be unpublished science. Cases carry categorical context
   (mission, counts regime, source type, model family), not identification.
3. **Never invent a name.** Every `model_family`, `abund`, `xsect`, and
   `statistic` must exist in the grounding set — the build gate checks this.
4. **State applicability.** Every lesson needs both `applies_when` **and**
   `not_when`. A lesson with no stated non-applicability will be rejected: an
   over-broad lesson applied to the wrong case is worse than no lesson.

## How to add a case

1. Read [casebook/SCHEMA.md](casebook/SCHEMA.md) and an existing case
   (`casebook/cases/nicer-lowcount-thermal-001.md`).
2. Add `casebook/cases/<id>.md` (frontmatter + prose) and any new
   `casebook/lessons/<id>.md` it cites. `id` is kebab-case and equals the
   filename stem. **Quote dates** (`date: "2026-07-02"`).
3. Validate: `python tests/validate_casebook.py` — checks the schemas,
   referential integrity, and the grounding set. It must pass.
4. Open a PR with provenance in the frontmatter (`source`, `contributor`,
   `date`).

## Trust tiers (the `status` field)

Retrieval surfaces a case's tier, so contributions are useful immediately without
waiting on full review:

- `contrib` — submitted, not yet reviewed.
- `reviewed` — an expert has checked it.
- `core` — expert-reviewed canonical; sets the bar for the format.

## Promoting a lesson (candidate → validated → promoted)

A lesson is `candidate` until it has a **validation harness** under
`bench/lessons/<id>.py` that generates data from a known truth and asserts the
lesson's signal (e.g. that `assess_fit` fires when the model is wrong and stays
quiet when it is right — see `bench/lessons/peg-at-limit-means-wrong-model.py`).
A passing harness makes it `validated`.

A lesson may only be `promoted` into the task-layer guides or the `xray-fit`
skill (changing default agent behavior) when **all** of: it is `validated`, it
recurs across **≥3 independent cases** (`evidence_cases`), and a maintainer
approves the PR. Recurrence alone never promotes — the harness is the gate.

## Attribution

Contributors are credited on their cases (`provenance`). The intent is for the
casebook to be citable as a body of work; keep provenance accurate.

## Developing the tooling

Run the full check suite before a PR:

```
python tests/run_all.py          # fast, corpus-only (what CI runs)
python tests/run_all.py --live   # also the HEADAS-dependent Tier B suite
```

CI runs the fast suite on every push/PR. The HEADAS-dependent tests and the
`generator/generate.py --check` drift gate run locally.

Licensed under the terms in [LICENSE](LICENSE).
