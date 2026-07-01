---
name: expabs
type: mul  # multiplicative
func: xsabsc
n_params: 1
family: [expabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelExpabs.tex
---

# expabs

**multiplicative model** (`mul`), function `xsabsc`.

## Description

A low-energy exponential rolloff.

$$M(E) = exp(-E_c/E)$$

where:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LowECut | keV | 2 | 0 | 100 | 0 | 200 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("expabs*powerlaw")
# component: m.expabs  (params as attributes)
```
