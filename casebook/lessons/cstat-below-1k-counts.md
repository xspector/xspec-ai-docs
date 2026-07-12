---
id: cstat-below-1k-counts
one_line: "Use cstat, not chi, below ~1000 total counts on Poisson data."
rule: >
  With chi (Gaussian per-bin errors) on low-count spectra the Gaussian
  approximation fails and under-populated bins bias the best-fit parameters
  (and classically pull fluxes low). cstat is the Poisson likelihood and is
  unbiased in this regime. Prefer cstat whenever counts are low; reserve chi
  for high counts-per-bin, well-grouped data.
applies_when: >
  counts_regime in [vlow, low]; Poisson data (POISSERR true); background either
  none or modelled simultaneously.
not_when: >
  high counts per bin already (chi is fine and faster to reason about); OR
  background-SUBTRACTED data, where cstat is not valid and the right move is to
  model the background and then use cstat, or group up and use chi.
status: validated
validation: bench/benchmark.py
evidence_cases: [nicer-lowcount-thermal-001]
promoted_to: null
provenance:
  origin: hand-authored
  date: "2026-07-02"
  reviewed_by: [kaa]
---

# Use cstat, not chi, on low counts

`bench/benchmark.py` demonstrates this directly: it fits the *same* faint
simulated power law (exposure 3000, norm 1e-4) with both statistics and scores
coverage and pull against the known truth. The `chi` case is labelled `TRAP` and
shows measurably worse coverage / larger pull bias than the `cstat` case on
identical data — the calibration harness fails the run if `chi` is *not*
degraded, so this lesson is continuously re-verified.

The dedicated per-lesson harness (`bench/lessons/cstat-lowcount.py`) is the
future home once `bench/lessons/` exists (PLAN-C L3); until then `benchmark.py`
is the standing validation.

**Promotion status:** validated, but only one evidence case so far — needs ≥3
independent cases before it is eligible to change the guides/skill (PLAN-C §4).
The statistic default in the `xray-fit` skill already reflects it.
