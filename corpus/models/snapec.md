---
name: snapec
type: add  # additive
func: C_snapec
n_params: 7
family: [snapec, bsnapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSnapec.tex
---

# snapec

**additive model** (`add`), function `C_snapec`.

Variants documented together: `snapec`, `bsnapec`.

## Description

This model calculates the spectrum for a galaxy cluster using the
`apec` model with relative abundances based on SN yields. The
relative amounts of SNIa and SNII can be set and there are a wide
variety of different SN yield calculations available. It is
straightforward to add the results of new yield calculations as they
become available in the literature. This model is described in
[Bulbul, Smith & Loewenstein (2012)](https://ui.adsabs.harvard.edu/abs/2012ApJ...753...54B/abstract).
All the standard `apec` `xset` options can be used.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | N_SNe | 10^9 | 1 | 0 | 1e+20 | 0 | 1e+20 | 0.1 |  |
| 3 | R | — | 1 | 0 | 1e+20 | 0 | 1e+20 | 0.1 |  |
| 4 | SNIModelIndex | — | 1 | 0 | 125 | 0 | 125 | 1 | frozen by default |
| 5 | SNIIModelIndex | — | 1 | 0 | 125 | 0 | 125 | 1 | frozen by default |
| 6 | redshift | — | 0 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("snapec")
# component: m.snapec  (params as attributes)
```
