---
name: kerrd
type: add  # additive
func: C_kerrd
n_params: 8
family: [kerrd]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelKerrd.tex
---

# kerrd

**additive model** (`add`), function `C_kerrd`.

## Description

Optically thick extreme-Kerr disk model based on the same
tranfer-function used in the `laor` Kerr disk-line model. Local
emission is simply assumed to be the diluted blackbody. See
[Laor
  (1991)](https://ui.adsabs.harvard.edu/abs/1991ApJ...376...90L/abstract) for an explanation of the transfer function. See [Ebisawa et
al. (2003)](https://ui.adsabs.harvard.edu/abs/2003ApJ...597..780E/abstract) for examples of using this model.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | distance | kpc | 1 | 0.01 | 1000 | 0.01 | 1000 | 1 | frozen by default |
| 2 | TcoloTeff | — | 1.5 | 1 | 2 | 1 | 2 | 1 | frozen by default |
| 3 | M | solar | 1 | 0.1 | 100 | 0.1 | 100 | 0.1 |  |
| 4 | Mdot | 1e18 | 1 | 0.01 | 100 | 0.01 | 100 | 0.1 |  |
| 5 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 1 | frozen by default |
| 6 | Rin | Rg | 1.235 | 1.235 | 100 | 1.235 | 100 | 1 | frozen by default |
| 7 | Rout | Rg | 100000 | 10000 | 100000000 | 10000 | 100000000 | 1 | frozen by default |
| 8 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("kerrd")
# component: m.kerrd  (params as attributes)
```
