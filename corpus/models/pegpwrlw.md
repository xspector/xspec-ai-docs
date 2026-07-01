---
name: pegpwrlw
type: add  # additive
func: xspegp
n_params: 4
family: [pegpwrlw]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPegpwrlw.tex
---

# pegpwrlw

**additive model** (`add`), function `xspegp`.

## Description

A power law with pegged normalization.

Using pegpwrlw or `cflux` * `powerlaw` should be equivalent. The former is preferred for simplicity.

$$A(E) = K E^{-\alpha}$$

where :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 1 | -2 | 9 | -3 | 10 | 0.01 |  |
| 2 | eMin | keV | 2 | -100 | 10000000000 | -100 | 10000000000 | 0.01 | frozen by default |
| 3 | eMax | keV | 10 | -100 | 10000000000 | -100 | 10000000000 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("pegpwrlw")
# component: m.pegpwrlw  (params as attributes)
```
