---
title: PyXspec object model and indexing contract
audience: agent
priority: 0
verified_against: live introspection (tests/run_recipes.py)
---

# PyXspec object model (load this first)

The API is a small object graph reached through six singletons. Get the graph
and the indexing right and most errors disappear.

## Singletons

| Singleton | Class | Role |
|---|---|---|
| `AllData` | DataManager | loaded spectra; `AllData("1:1 f.pha")` loads (returns None) |
| `AllModels` | ModelManager | active models; `AllModels(1)` is the model for source 1 |
| `Fit` | FitManager | fitting, errors, statistic |
| `Xset` | XspecSettings | global settings (abund, xsect, chatter, seed, logs) |
| `Plot` | PlotManager | plotting + array extraction |
| `AllChains` | ChainManager | MCMC chains |

## The graph

```
AllData(i)            -> Spectrum         # i = spectrum number (1-indexed)
  Spectrum.response   -> Response         # RAISES if none attached
    Response.arf      -> Arf
  Spectrum.background -> Background        # RAISES if none attached
AllModels(i)          -> Model            # i = source number (1-indexed)
  Model.<compName>    -> Component         # e.g. m.TBabs, m.powerlaw
    Component.<parName> -> Parameter
  AllModels(i)(n)     -> Parameter        # n = parameter number across the model
Model(exprString)     -> Model            # constructing loads the model
Chain(fileName, ...)  -> Chain            # constructing RUNS the chain
```

## Indexing rules

- Everything user-facing is **1-indexed**: `AllData(1)`, `AllModels(1)(1)`.
- `AllModels(src)(parNum)` numbers parameters across the **whole** model, not
  per component. Prefer named access: `m.powerlaw.PhoIndex`.
- Component attribute names are the **model.dat canonical names** (`m.TBabs`,
  not `m.tbabs`); read them from `Model.componentNames`.

## Behavioral quirks that bite (memorize these)

- `AllData("1:1 f.pha")` **returns None** — the load is a side effect; get the
  object with `AllData(1)`.
- `Spectrum.response` and `Spectrum.background` **raise** when none is attached
  — guard with try/except.
- `Parameter.values` is a **6-list** `[val, delta, min, bottom, top, max]`; the
  fitted value is `values[0]`.
- `Parameter.error` is a **3-tuple** `(low, high, code)`; `code == "FFFFFFFFF"`
  means clean, any other flags a problem (e.g. new minimum).
- `Spectrum.flux`/`lumin` are **6-tuples** (value, errLo, errHi in cgs, then the
  same triple in photons); populated only after `AllModels.calcFlux/calcLumin`.
- `AllModels.calcFlux(...)` **stores into** `Spectrum.flux`; it does not return.
- Constructing a `Chain(...)` **runs** it immediately.
- Read-only attributes raise "Cannot rebind ..." on assignment — see each
  class's attribute table (access = get).

Full per-class attribute/method tables: `corpus/api/<Class>.md`; machine form:
`corpus/api/api.json`.
