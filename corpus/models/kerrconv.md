---
name: kerrconv
type: con  # convolution
func: C_spinconv
n_params: 7
family: [kerrconv]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelKerrconv.tex
---

# kerrconv

**convolution model** (`con`), function `C_spinconv`.

## Description

Convolves the current spectrum with the line shape from the `kerrdisk` 
model. A detailed description can be found in [Brenneman & Reynolds 
(2006)](https://ui.adsabs.harvard.edu/abs/2006ApJ...652.1028B/abstract). This model is quite slow so is best used after 
models such as `laor` or `diskline` have been employed to get 
an estimate of the best-fit parameters.

Note that due to the energy binning the convolution process can
produce spurious structures around sharp features in the spectrum
being convolved. We strongly recommend testing for this by using the
`energies` command to change the binning.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Index1 | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 2 | Index2 | — | 3 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 3 | r_br_g | — | 6 | 1 | 400 | 1 | 400 | 0.1 | frozen by default |
| 4 | a | — | 0.998 | 0 | 0.998 | 0 | 0.998 | 0.1 |  |
| 5 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 1 | frozen by default |
| 6 | Rin_ms | — | 1 | 1 | 400 | 1 | 400 | 0.1 | frozen by default |
| 7 | Rout_ms | — | 400 | 1 | 400 | 1 | 400 | 0.1 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("kerrconv*powerlaw")
# component: m.kerrconv  (params as attributes)
```
