---
name: uvred
type: mul  # multiplicative
func: xsred
n_params: 1
family: [uvred]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelUvred.tex
---

# uvred

**multiplicative model** (`mul`), function `xsred`.

## Description

A UV reddening using Seaton's law ([1979](https://ui.adsabs.harvard.edu/abs/1979MNRAS.187P..73S/abstract)). Valid from 
1000-3704. The transmission is set to unity shortward of the Lyman limit. 
This is incorrect physically but does allow the model to be used in 
combination with an X-ray photoelectric absorption model such as `phabs`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | E_BmV | — | 0.05 | 0 | 10 | 0 | 10 | 0.001 |  |

## PyXspec

```python
from xspec import Model
m = Model("uvred*powerlaw")
# component: m.uvred  (params as attributes)
```
