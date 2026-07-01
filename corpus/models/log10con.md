---
name: log10con
type: mul  # multiplicative
func: C_log10con
n_params: 1
family: [log10con]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelLog10con.tex
---

# log10con

**multiplicative model** (`mul`), function `C_log10con`.

## Description

This multiplicative model can be used to replace a linear
normalization of a model by a base 10 logarithmic normalization. To use
multiply the additive component by this model and freeze the
normalization of the additive component at one.

The parameters is:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | log10fac | — | 0 | -20 | 20 | -20 | 20 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("log10con*powerlaw")
# component: m.log10con  (params as attributes)
```
