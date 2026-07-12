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

## Run

```
python bench/lessons/<lesson-id>.py
```

(The ground-truth *calibration* benchmark for the tooling itself is one level up,
`bench/benchmark.py`.)
