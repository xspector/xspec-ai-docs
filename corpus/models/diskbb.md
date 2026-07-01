---
name: diskbb
type: add  # additive
func: xsdskb
n_params: 2
family: [diskbb]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelDiskbb.tex
---

# diskbb

**additive model** (`add`), function `xsdskb`.

## Description

The spectrum from an accretion disk consisting of multiple blackbody
components. For example, see [Mitsuda et
  al. (1984)](https://ui.adsabs.harvard.edu/abs/1984PASJ...36..741M/abstract)
or [Makishima et al. (1986)](https://ui.adsabs.harvard.edu/abs/1986ApJ...308..635M/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Tin | keV | 1 | 0 | 1000 | 0 | 1000 | 0.01 |  |
| 2 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("diskbb")
# component: m.diskbb  (params as attributes)
```
