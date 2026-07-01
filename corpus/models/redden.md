---
name: redden
type: mul  # multiplicative
func: xscred
n_params: 1
family: [redden]
energy_range: [3.72e-4, 9.92e-3]
source: manager/model.dat + XSmodelRedden.tex
---

# redden

**multiplicative model** (`mul`), function `xscred`.

## Description

IR/optical/UV extinction from [Cardelli et al. (1989)](https://ui.adsabs.harvard.edu/abs/1989ApJ...345..245C/abstract). The 
transmission is set to unity shortward of the Lyman limit. This is 
incorrect physically but does allow the model to be used in combination 
with an X-ray photoelectric absorption model such as `phabs`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | E_BmV | — | 0.05 | 0 | 10 | 0 | 10 | 0.001 |  |

## PyXspec

```python
from xspec import Model
m = Model("redden*powerlaw")
# component: m.redden  (params as attributes)
```
