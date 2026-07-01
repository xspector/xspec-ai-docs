---
name: diskpbb
type: add  # additive
func: diskpbb
n_params: 3
family: [diskpbb]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelDiskpbb.tex
---

# diskpbb

**additive model** (`add`), function `diskpbb`.

## Description

A multiple blackbody disk model where local disk temperature T(r) is
proportional to $r^{-p}$, where $p$ is a free parameter. The standard disk
model, diskbb, is recovered if $p = 0.75$. If radial advection is
important then $p < 0.75$. See the discussion and examples in, e.g.,
[Mineshige et
  al. (1994)](https://ui.adsabs.harvard.edu/abs/1994ApJ...426..308M/abstract);
[Hirano et
  al. (1995)](https://ui.adsabs.harvard.edu/abs/1995ApJ...446..350H/abstract);
[Watarai et
  al. (2000)](https://ui.adsabs.harvard.edu/abs/2000PASJ...52..133W/abstract);
[Kubota and Makishima (2004)](https://ui.adsabs.harvard.edu/abs/2004ApJ...601..428K/abstract); [Kubota et al. (2005)](https://ui.adsabs.harvard.edu/abs/2005ApJ...631.1062K/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Tin | keV | 1 | 0.1 | 10 | 0.1 | 10 | 0.02 |  |
| 2 | p | — | 0.75 | 0.5 | 1 | 0.5 | 1 | 0.05 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("diskpbb")
# component: m.diskpbb  (params as attributes)
```
