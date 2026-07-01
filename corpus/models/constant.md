---
name: constant
type: mul  # multiplicative
func: xscnst
n_params: 1
family: [constant]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelConstant.tex
---

# constant

**multiplicative model** (`mul`), function `xscnst`.

## Description

An energy-independent multiplicative factor.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | factor | — | 1 | 0 | 10000000000 | 0 | 10000000000 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("constant*powerlaw")
# component: m.constant  (params as attributes)
```
