# Ground-truth benchmark

Validates that `xspec-run` produces statistically **trustworthy** results — not
just that the tools run. It generates synthetic spectra with known parameters
via `fakeit`, recovers them through the server (the same tools an agent uses),
and scores calibration.

```
python bench/benchmark.py [N_realizations]     # default 40; needs HEADAS
```

## What it measures

- **coverage** — fraction of realizations whose 1σ confidence interval contains
  the true value. Nominal 68.3%. Under-coverage ⇒ error bars too small;
  over-coverage ⇒ too large.
- **pull** — `(recovered − truth) / σ` across realizations; should be ~N(0,1):
  mean ≈ 0 (unbiased), std ≈ 1 (errors correctly sized). Pull catches problems
  coverage alone hides — a biased fit with oversized error bars can *look*
  well-covered.

## Cases

Absorbed/unabsorbed power law and plasma across bright/faint regimes, fit with
`cstat`. Plus a **trap**: the faint power law fit with `chi` on the *same
simulated data* (same seed) — `chi` is biased at low counts, which the pull
exposes even when its coverage looks fine.

## Interpreting

`cstat` cases should pass (coverage in band, pull mean ≈ 0, std ≈ 1). Coverage
is a noisy binomial estimate at small N — raise N (100+) for a tight number; the
pull statistics are the more robust signal. This is a tool-level, deterministic
calibration guard; an agent-in-the-loop layer could reuse the same scoring.
