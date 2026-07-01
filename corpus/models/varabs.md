---
name: varabs
type: mul  # multiplicative
func: xsabsv
n_params: 18
family: [varabs, zvarabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelVarabs.tex
---

# varabs

**multiplicative model** (`mul`), function `xsabsv`.

Variants documented together: `varabs`, `zvarabs`.

## Description

A photoelectric absorption with variable abundances using
cross-sections set by the `xsect` command. The column for each
element is in units of the column in a solar abundance column of an
equivalent hydrogen column density of $10^{22}$cm$^{-2}$. The Solar
abundance table used is set by the `abund` command. These models
differ from the models `vphabs` and `zvphabs` only by
the units in which the abundances are expressed (`vphabs` and
`zvphabs` define these relative to the solar abundance, not in
terms of column density).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | H | sH22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 2 | He | sHe22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 3 | C | sC22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | N | sN22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 5 | O | sO22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 6 | Ne | sNe22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 7 | Na | sNa22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 8 | Mg | sMg22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 9 | Al | sAl22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 10 | Si | sSi22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 11 | S | sS22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 12 | Cl | sCl22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 13 | Ar | sAr22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 14 | Ca | sCa22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 15 | Cr | sCr22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 16 | Fe | sFe22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 17 | Co | sCo22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 18 | Ni | sNi22 | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("varabs*powerlaw")
# component: m.varabs  (params as attributes)
```
