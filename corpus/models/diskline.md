---
name: diskline
type: add  # additive
func: C_diskline
n_params: 6
family: [diskline]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelDiskline.tex
---

# diskline

**additive model** (`add`), function `C_diskline`.

## Description

A line emission from a relativistic accretion disk. See
[Fabian et al. (1989)](https://ui.adsabs.harvard.edu/abs/1989MNRAS.238..729F/abstract). Setting par2 to 10 is the special case of the
accretion disk emissivity law $(1-\sqrt{6/R})/R^3$.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LineE | keV | 6.7 | 0 | 100 | 0 | 100 | 0.05 |  |
| 2 | Betor10 | — | -2 | -10 | 20 | -10 | 20 | 0.01 | frozen by default |
| 3 | Rin_M | — | 10 | 6 | 1000 | 6 | 10000 | 0.1 | frozen by default |
| 4 | Rout_M | — | 1000 | 0 | 1000000 | 0 | 10000000 | 1 | frozen by default |
| 5 | Incl | deg | 30 | 0 | 90 | 0 | 90 | 0.05 |  |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("diskline")
# component: m.diskline  (params as attributes)
```
