---
name: logconst
type: mul  # multiplicative
func: C_logconst
n_params: 1
family: [logconst]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLogconst.tex
---

# logconst

**multiplicative model** (`mul`), function `C_logconst`.

## Description

This multiplicative model can be used to replace a linear
normalization of a model by a logarithmic normalization. To use
multiply the additive component by this model and freeze the
normalization of the additive component at one.

The parameters is:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | logfact | — | 0 | -20 | 20 | -20 | 20 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("logconst*powerlaw")
# component: m.logconst  (params as attributes)
```
