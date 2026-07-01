---
title: Error and warning catalog (cause → fix)
audience: agent
priority: 5
verified_against: literal strings grepped from XSPEC source (XSFit/XSModel/XSUser)
---

# Error / warning catalog

For an execution loop: match on the substring, apply the fix. Strings are taken
verbatim from the XSPEC source; match on the distinctive fragment (surrounding
punctuation/values vary). In PyXspec most of these surface as a raised
`Exception` carrying the same text.

## Setup / ordering

| Message fragment | Cause | Fix |
|---|---|---|
| `No data loaded` | operation needs a spectrum; none loaded | `AllData("1:1 src.pha")` first |
| `A default (unnamed) model is not defined` | fit/eval before a model exists | `Model("...")` first |
| `has no response for source` | model folding needs an RMF; none attached | load PHA (auto-RMF) or set `AllData(1).response` |
| `not found associated with spectrum` / `cannot be found in the SPECTRUM extension of` | referenced keyword/file missing from PHA | check RESPFILE/ANCRFILE/BACKFILE; attach manually |
| `do not contain the same energy bins and/or channels` | response/spectrum grid mismatch | use the matching RMF for that spectrum |

## Parameters / links

| Message fragment | Cause | Fix |
|---|---|---|
| `out of range (have ...)` | value beyond soft/hard limit | set within limits, or widen soft limits (check hard limits in model JSON) |
| `is linked and cannot be frozen` | freezing a tied parameter | `untie()` first, or freeze the driving parameter |
| `Attempt to link parameter to itself` | self-referential link | link to a different parameter |
| `Attempt to create link from switch to real valued parameter` / `... real valued parameter to a switch` | link crosses a switch/scale parameter | links must be real→real |
| `Link expression gives divide by zero error` | link formula divides by zero at current values | fix the link expression |
| `cannot delete the last component in the model` | removing the only component | redefine the model instead |

## Fit / error / steppar

| Message fragment | Cause | Fix |
|---|---|---|
| `A new minimum has been found` | `error`/`steppar` found a better fit | re-`Fit.perform()`, then redo the error/steppar |
| `Cannot do error calc: Reduced Chi^2 (= ...)` | fit too poor for meaningful errors | improve the fit (or the tolerance) before `error` |
| `Apparent non-monotonicity in statistic space detected` | rough/degenerate statistic surface near the error bound | inspect with `steppar`; consider a global fit / different start |
| `will automatically exit from trials loop` | max fit trials hit (would normally query) | expected under `Fit.query="yes"`; check convergence, raise `Fit.nIterations` |
| `is not a recognised error type` | bad `error`/statistic keyword | use a valid option (message lists them) |
| `Error processing step parameter args, check syntax` | malformed `steppar` argument | fix the `steppar` string |

## Table / data files

| Message fragment | Cause | Fix |
|---|---|---|
| `Table Model file not found or has errors: file` / `Cannot find table model file` | `atable`/`mtable` path bad or file corrupt | give a readable FITS table path |
| `Table Model Type incorrect` | add/mul table mismatch | use `atable` for additive, `mtable` for multiplicative tables |
| `cannot open log file` / `cannot open line list file named` | output/aux file not writable or missing | check path/permissions |

## Install / environment

| Message fragment | Cause | Fix |
|---|---|---|
| `XSPEC not properly installed - cannot find manager, script, or help directory` | `HEADAS` not initialized / bad install | source `headas-init.sh` before launching |
| `XSPEC not properly installed - cannot find spectral directory` | model data dir missing | check `$HEADAS/../spectral/modelData` |
| `local model directory must either be ...` | bad `lmod`/`initpackage` path | give a valid local-model directory |
