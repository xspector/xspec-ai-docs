---
title: Anti-patterns and known failure modes
audience: agent
priority: 4
verified_against: PyXspec + XSPEC source error strings
---

# Anti-patterns (don't do this)

Ordered by how often an agent hits them. Each gives the wrong move, the symptom,
and the fix.

## Ordering / state

- **Fitting before loading data.** `Fit.perform()` with nothing loaded →
  `No data loaded`. Load a spectrum first.
- **Fitting before defining a model.** →
  `*** A default (unnamed) model is not defined.` Call `Model(...)` first.
- **Defining a model before a response is available.** Without an RMF the model
  cannot be folded: `<spectrum> has no response for source 1`. Load the PHA
  (auto-attaches its RMF) or set `AllData(1).response` before `Model(...)`.
- **Reusing state across runs.** Stale spectra/models leak between runs. Start
  with `AllData.clear(); AllModels.clear()` for deterministic behavior.

## Statistic / data

- **Using `chi` on low-count or background-subtracted data.** Runs fine, biases
  parameters, and can warn about bins with zero variance. Use `cstat` (guide 02
  §3).
- **Judging a `cstat` fit by reduced statistic ≈ 1.** It isn't ~1 at a good fit.
  Use `Fit.goodness(...)`.
- **Fitting outside the calibrated band.** Not dropping `bad` channels or
  fitting beyond the instrument range injects garbage. `ignore bad` then the
  mission band (guide 02 §4).

## Parameters

- **`values` is a list, not a scalar.** `AllModels(1)(1).values` returns
  `[val, delta, min, bottom, top, max]`. The fitted value is `values[0]`.
  Assigning a scalar sets the value; use the string form to set limits.
- **Wrong parameter index.** Component parameters are numbered across the whole
  model (component 2's first param is not index 1). Prefer named access
  (`m.powerlaw.PhoIndex`) or confirm indices with `AllModels(1).show()`.
- **Freezing a linked parameter.** → `<par> is linked and cannot be frozen.`
  Untie first (`AllModels(1)(n).untie()`), or freeze the driving parameter.
- **Setting a value outside limits.** → `... out of range (have ...)`. Widen the
  soft limits via the string form (`.values = "1e6,,0,0,1e7,1e7"`) — but check
  the `model.dat` hard limits first (they're in each model's JSON).
- **Bad links.** `Attempt to link parameter to itself` /
  `... link from switch to real valued parameter`. Links must be real→real and
  acyclic.

## Confidence / errors

- **Treating fit-step deltas as confidence intervals.** They are not. Use
  `Fit.error(...)` (guide 01 §5).
- **Ignoring the error status code.** A new minimum found during `error` /
  `steppar` prints `A new minimum has been found` and invalidates the interval —
  re-`Fit.perform()` and redo. Also `Cannot do error calc: Reduced Chi^2 (= ...)`
  means the fit is too poor for meaningful errors — improve the fit first.

## Fluxes / models

- **`calcFlux` gives no parameter-error propagation.** For a flux *with* a real
  CI, wrap the model in `cflux`/`cpflux` and run `Fit.error` on its flux
  parameter (recipe R3).
- **Confusing model component types.** Multiplicative (`tbabs`) and convolution
  (`cflux`, `gsmooth`) models are meaningless alone — they modify an additive
  model. `tbabs` by itself has nothing to absorb (guide 06).
- **Hallucinated model/command names.** Do not invent. Every valid model name,
  component type, and parameter is in `manifest.json`; check there before using
  a name you're unsure of.

## Table models / files

- **Bad table-model path.** → `Table Model file not found or has errors` /
  `Cannot find table model file`. `atable`/`mtable` need a readable FITS path.

## Environment

- **Assuming a display exists.** No GUI; never rely on a plot window
  (guide 01 §6).
- **Forgetting abundance/cross-section state.** `tbabs` assumes `abund wilm`;
  changing `Xset.abund`/`Xset.xsect` changes results. Set and record them.
