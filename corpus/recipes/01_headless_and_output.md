---
title: Running XSPEC headless and getting structured results out
audience: agent
priority: 1
verified_against: PyXspec (XSUser/Python/xspec)
---

# Running headless + structured output

This is the first thing to get right. An agent driving XSPEC fails on turn one
if the process blocks on an interactive prompt, or if results can only be read
from scrolled text. Both are avoidable. **Prefer PyXspec**: results are typed
Python values and failures raise exceptions instead of stopping at a prompt.

## 1. Stop it from blocking

XSPEC pauses for user input in three places. Disable all three before doing
anything else.

| Blocking point | PyXspec | Interactive Tcl |
|---|---|---|
| Fit "number of trials exceeded — continue?" | `Fit.query = "yes"` | `query yes` |
| Chatter/paging of long output | `Xset.chatter = 10; Xset.logChatter = 10` | `chatter 10` |
| Reading a spectrum / proceed prompts | covered by `Fit.query` + non-interactive session | `query yes` |

`Fit.query` accepts `"yes"` (continue through the query — **use this for agents**),
`"no"` (stop the fit at the query and return control), or `"on"` (prompt).

```python
from xspec import Xset, Fit
Fit.query = "yes"       # never block mid-fit
Xset.chatter = 10       # console verbosity (0 = silent)
Xset.logChatter = 10    # log-file verbosity
```

## 2. No GUI — you cannot see a plot window

There is no display. Never rely on a PGPLOT window. Either:
- extract plot arrays as numbers (see §5), or
- render to a file device: `Plot.device = "/png"` (or `/svg`, `/ps`),
  cross-ref Tcl `cpd file.png/png`.

## 3. Capture the session log

```python
Xset.openLog("session.log")   # Tcl: log session.log
# ... work ...
Xset.closeLog()               # Tcl: log none
```

## 4. Minimal headless skeleton

```python
from xspec import AllData, AllModels, Model, Fit, Xset

Xset.chatter = 10
Fit.query = "yes"
AllData.clear(); AllModels.clear()          # start clean (idempotent runs)

AllData("1:1 src.pha")                       # response/arf/back auto-loaded
AllData.ignore("bad")
AllData.ignore("**-0.5 8.0-**")
Fit.statMethod = "cstat"
Model("tbabs*powerlaw")
Fit.perform()
```

## 5. Get results out as typed values (do NOT scrape text)

Interactive XSPEC forces `tclout` string-scraping. PyXspec exposes the same
numbers as attributes. This table is the core of agentic use.

| Result | PyXspec | Interactive Tcl (`tclout ...`) |
|---|---|---|
| Fit statistic | `Fit.statistic` → float | `tclout stat` |
| Degrees of freedom | `Fit.dof` → int | `tclout dof` |
| Statistic name / test | `Fit.statMethod`, `Fit.statTest` | — |
| Parameter value | `AllModels(1)(n).values[0]` | `tclout param n` |
| Parameter frozen? | `AllModels(1)(n).frozen` → bool | — |
| Confidence interval | `Fit.error("n")` then `AllModels(1)(n).error` → (lo, hi, code) | `error n` / `tclout error n` |
| Flux (after calc) | `AllData(1).flux` → tuple | `flux` / `tclout flux` |
| Count rate | `AllData(1).rate` | `tclout rate` |
| Exposure | `AllData(1).exposure` | — |

`Parameter.values` is a list `[value, delta, min, bottom, top, max]`; the fitted
value is `values[0]`. Setting is symmetric: `AllModels(1)(1).values = 1.8` or
`... .values = "1.8,,0.5,0.5,3,3"`.

### Errors (confidence intervals ≠ fit deltas)

```python
Fit.error("2.706 1-3")          # 90% (Δstat 2.706) for params 1–3
lo, hi, code = AllModels(1)(1).error
# `code` flags problems: e.g. new minimum found, hit hard limit.
```
Always check `code` — a non-empty status means the interval is unreliable
(commonly a new minimum: re-`Fit.perform()` and repeat).

### Flux / luminosity

```python
AllModels.calcFlux("0.5 10.0")               # Tcl: flux 0.5 10.0
val, elo, ehi, pval, pelo, pehi = AllData(1).flux
# (value, errLow, errHigh in ergs/cm^2/s), then the same triple in photons.
```
For a **fitted** flux with proper errors, wrap the model in `cflux`/`cpflux`
instead of a post-hoc `calcFlux` (see model docs).

## 6. "See" the fit without a display

```python
from xspec import Plot
Plot.device = "/null"          # compute arrays, draw nothing
Plot.xAxis = "keV"
Plot("data", "resid")          # or "ldata delchi", etc.
x   = Plot.x()                 # energy (or channel) centers
y   = Plot.y()                 # data
mod = Plot.model()             # folded model
# inspect residuals numerically instead of looking at a window
```
`Plot.x/y/model/yErr/addComp` take `(plotGroup, plotWindow)` for multi-spectrum
/ multi-panel cases.

## 7. Reproducibility

- Seed stochastic steps (fakeit, MCMC, `fit global`): `Xset.seed = 12345`.
- `AllData.clear()` / `AllModels.clear()` at the top so a re-run is deterministic.
- Record `Xset.abund` and `Xset.xsect` — they change absorption/plasma results
  (see the ingestion guide).

## 8. Exit cleanly

Let exceptions propagate (don't swallow them — the message is the diagnostic).
Close the log. Do not call the interactive `exit`.
