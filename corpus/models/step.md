---
name: step
type: add  # additive
func: xsstep
n_params: 3
family: [step]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelStep.tex
---

# step

**additive model** (`add`), function `xsstep`.

## Description

A step function convolved with a gaussian.

$$A(E) = {K\over{2}}[1-\mbox{erf}({(E-E_s)\over{\sqrt{2}\sigma}})]$$

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Energy | keV | 6.5 | 0 | 100 | 0 | 100 | 0.05 |  |
| 2 | Sigma | keV | 0.1 | 0 | 10 | 0 | 20 | 0.05 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("step")
# component: m.step  (params as attributes)
```
