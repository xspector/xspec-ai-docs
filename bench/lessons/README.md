# Lesson validation harnesses

One harness per casebook lesson that claims a testable signal. Each generates
data from a **known truth** via `fakeit` and asserts the lesson's signal fires
when it should and stays quiet when it should not — the gate a lesson passes to
move from `candidate` to `validated` (see [../../PLAN-C.md](../../PLAN-C.md) and
[../../CONTRIBUTING.md](../../CONTRIBUTING.md)).

This is what makes the casebook *learn* rather than *drift*: a lesson is promoted
on evidence (a passing harness + recurrence across cases), not on how often it
was asserted.

## Contract

- Named `<lesson-id>.py`, matching the lesson's `validation:` field.
- Needs HEADAS/PyXspec (the runner bootstraps it); prints `SKIPPED` and exits 0
  if HEADAS is absent, so it is safe in any environment.
- Exits non-zero if the lesson does **not** hold — a good harness tests **both**
  directions (signal present when the model/setup is wrong; absent when right),
  so it cannot be passed by a detector that always (or never) fires.

## Present

| Harness | Validates |
|---|---|
| `peg-at-limit-means-wrong-model.py` | a parameter pegged at a limit **and** correlated residuals ⇒ structurally wrong model. Fits `tbabs*powerlaw` to power-law+line data (nH pegs at 0 + residuals) vs. the correct `powerlaw+gaussian` at truth (quiet). |
| `flat-photon-index-means-absorption.py` | an implausibly flat/inverted photon index **and** a soft residual (but **not** a pegged parameter) ⇒ missing intrinsic absorption. Fits Galactic-only `tbabs*powerlaw` to an absorbed Seyfert twin (Γ→−1.0 + residual) vs. the correct `tbabs*ztbabs*powerlaw` at truth (Γ→1.73, quiet). |
| `counts-per-bin-not-total-drives-statistic.py` | counts **per bin**, not total, set the statistic. On a real XRISM/Resolve twin (27k counts, median 1/bin), chi biases the Fe abundance to 1.00 (truth 0.70) behind a reduced chi of 0.67 while cstat recovers it. **HEADAS-only + needs the 372 MB Resolve RMF locally** (self-skips otherwise); ~2–3 min. |
| `single-temperature-fe-bias.py` | a single-temperature fit to multi-phase ICM biases the iron abundance. Fits `tbabs*apec` to a two-phase (1.0+2.5 keV, Fe=0.5) twin → Fe=0.17 at cstat/dof=5.5, vs. `tbabs*(apec+apec)` → Fe=0.51 at cstat/dof=1.1. (Thaws apec's frozen-by-default Abundanc.) |
| `systematics-dominate-above-1e5-counts.py` | above ~10⁵ counts statistics fall below the calibration floor. On a bright `tbabs*(diskbb+powerlaw+gaussian)` twin faked at 10⁶ and 10⁴ counts: the disk-temperature stat error is ±0.34% at 10⁶, and the Fe line is Δχ²=40.6 (6.4σ) at 10⁶ but 0 at 10⁴. |
| `ftest-invalid-for-line-significance.py` | Monte-Carlo: 150 line-free `cutoffpl` sims, each fit with a searched `gabs`. The naive χ²₁ 1% threshold (Δχ²>6.63) is cleared by ~8% of null sims, not 1% — the F-test is anti-conservative for searched lines. |
| `below-100-counts-cannot-discriminate-models.py` | model discrimination needs counts. A `bbodyrad` (kT=0.1) twin faked at ~80 counts is fit equally by `diskbb` (Δcstat=−1.6, wrong model wins); at ~40000 counts diskbb is decisively worse (Δcstat=+170). |
| `young-plasma-needs-nei-not-equilibrium.py` | a young/under-ionized plasma needs NEI. Equilibrium `apec` fit to a `nei` twin (kT=3, Tau=1e10) returns kT=0.55 keV (6× low) at Δcstat=+1070 worse; `nei` recovers kT=3.2 and Tau=1e10. |

## Run

```
python bench/lessons/<lesson-id>.py
```

(The ground-truth *calibration* benchmark for the tooling itself is one level up,
`bench/benchmark.py`.)
