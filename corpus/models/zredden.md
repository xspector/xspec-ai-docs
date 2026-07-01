---
name: zredden
type: mul  # multiplicative
func: xszcrd
n_params: 2
family: [zredden]
energy_range: [3.72e-4, 9.92e-3]
source: manager/model.dat + XSmodelZredden.tex
---

# zredden

**multiplicative model** (`mul`), function `xszcrd`.

## Description

IR/optical/UV extinction from [Cardelli et al. (1989)](https://ui.adsabs.harvard.edu/abs/1989ApJ...345..245C/abstract).  
The transmission is set to unity shortward of 900 Angstroms. This is incorrect 
physically but does allow the model to be used in combination with an X-ray 
photoelectric absorption model such as `phabs`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | E_BmV | — | 0.05 | 0 | 10 | 0 | 10 | 0.001 |  |
| 2 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zredden*powerlaw")
# component: m.zredden  (params as attributes)
```
