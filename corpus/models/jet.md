---
name: jet
type: add  # additive
func: jet
n_params: 16
family: [jet]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelJet.tex
---

# jet

**additive model** (`add`), function `jet`.

## Description

This is the single zone, leptonic relativistic jet code of
[Ghisellini & Tavecchio
(2009)](https://ui.adsabs.harvard.edu/abs/2009MNRAS.397..985G/abstract),
hereafter GT09, as used in [Ghisellini et
al. (2010)](https://ui.adsabs.harvard.edu/abs/2010MNRAS.402..497G/abstract), coded
up by [Gardner & Done
(2017)](https://ui.adsabs.harvard.edu/abs/2018MNRAS.473.2639G/abstract). Please reference all of these papers if you use this model in xspec.

The default parameters reproduce the mean FSRQ spectrum in G10 (except
that the synchrotron self absorption cutoff is at a lower frequency)
The spectrum longward of this cutoff is assumed to have a flat
spectrum in L$_{\nu}$, as appropriate for the sum of self-absorbed components
further down the jet.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | mass | solar | 1000000000 | 1 | 10000000000 | 1 | 10000000000 | 1 | frozen by default |
| 2 | Dco | Mpc | 3350.6 | 1 | 100000000 | 1 | 100000000 | 1 | frozen by default |
| 3 | log_mdot | logL/LEdd | -1 | -5 | 2 | -5 | 2 | 0.01 |  |
| 4 | thetaobs | deg | 3 | 0 | 90 | 0 | 90 | 1 | frozen by default |
| 5 | BulkG | — | 13 | 1 | 100 | 1 | 100 | 1 | frozen by default |
| 6 | phi | rad | 0.1 | 0.01 | 100 | 0.01 | 100 | 1 | frozen by default |
| 7 | zdiss | Rg | 1275 | 10 | 10000 | 10 | 10000 | 1 | frozen by default |
| 8 | B | Gau | 2.6 | 0.01 | 15 | 0.01 | 15 | 1 | frozen by default |
| 9 | logPrel | — | 43.3 | 40 | 48 | 40 | 48 | 1 | frozen by default |
| 10 | gmin_inj | — | 1 | 1 | 1000 | 1 | 1000 | 1 | frozen by default |
| 11 | gbreak | — | 300 | 10 | 10000 | 10 | 10000 | 1 | frozen by default |
| 12 | gmax | — | 3000 | 1000 | 1000000 | 1000 | 1000000 | 1 | frozen by default |
| 13 | s1 | — | 1 | -1 | 1 | -1 | 1 | 1 | frozen by default |
| 14 | s2 | — | 2.7 | 1 | 5 | 1 | 5 | 1 | frozen by default |
| 15 | z | — | 0 | 0 | 10 | 0 | 10 | 1 | frozen by default |
| 16 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("jet")
# component: m.jet  (params as attributes)
```
