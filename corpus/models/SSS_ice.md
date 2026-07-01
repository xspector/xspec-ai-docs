---
name: SSS_ice
type: mul  # multiplicative
func: xssssi
n_params: 1
family: [SSSice]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSssice.tex
---

# SSS_ice

**multiplicative model** (`mul`), function `xssssi`.

## Description

The Einstein Observatory SSS ice absorption.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | clumps | — | 0 | 0 | 10 | 0 | 10 | 0.005 |  |

## PyXspec

```python
from xspec import Model
m = Model("SSS_ice*powerlaw")
# component: m.sssice  (params as attributes)
```
