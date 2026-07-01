---
name: zkerrbb
type: add  # additive
func: C_zkerrbb
n_params: 10
family: [kerrbb, zkerrbb]
energy_range: [0., 1.e6]
source: manager/model.dat + XSmodelKerrbb.tex
---

# zkerrbb

**additive model** (`add`), function `C_zkerrbb`.

Variants documented together: `kerrbb`, `zkerrbb`.

## Description

A multi-temperature blackbody model for a thin, steady state, general
relativistic accretion disk around a Kerr black hole. The effect of
self-irradiation of the disk is considered, and the torque at the
inner boundary of the disk is allowed to be non-zero. This model is
intended as an extension to `grad`, which assumes that the black hole is
non-rotating. For details see [Li et al. (2005)](https://ui.adsabs.harvard.edu/abs/2005ApJS..157..335L/abstract).

The redshift version `zkerrbb` has the mass accretion rate
parameter in units of Solar masses per year and the distance parameter
replaced by redshift.

Parameters for `kerrbb`:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | eta | — | 0 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 2 | a | — | 0.5 | -0.99 | 0.9999 | -0.99 | 0.9999 | 0.01 |  |
| 3 | i | deg | 30 | 0 | 85 | 0 | 85 | 0.01 | frozen by default |
| 4 | Mbh | M_sun | 10000000 | 3 | 10000000000 | 3 | 10000000000 | 0.01 |  |
| 5 | Mdd | M0yr | 1 | 0.0001 | 10000 | 1e-05 | 100000 | 0.01 |  |
| 6 | z | — | 0.01 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 7 | fcol | — | 2 | -100 | 100 | -100 | 100 | 0.01 | frozen by default |
| 8 | rflag | — | 1 |  |  |  |  |  | switch (not fitted) |
| 9 | lflag | — | 1 |  |  |  |  |  | switch (not fitted) |
| 10 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("zkerrbb")
# component: m.zkerrbb  (params as attributes)
```
