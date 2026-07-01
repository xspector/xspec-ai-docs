---
name: zxipab
type: mul  # multiplicative
func: zxipab
n_params: 5
family: [zxipab]
energy_range: [0.01, 1.e20]
source: manager/model.dat + XSmodelZxipab.tex
---

# zxipab

**multiplicative model** (`mul`), function `zxipab`.

## Description

This is an extension of the `pwab` model in which the complex absorption
is modelled as a power-law distribution of covering fraction and
column of ionised absorbers. Unlike `pwab`, which is based on neutral
absorbers, `zxipab` utilizes pre-calculated grid of XSTAR
photo-ionisation model also used by zxipcf model, with ionising
parameter log (xi). See [Islam & Mukai (2021)](https://ui.adsabs.harvard.edu/abs/2021arXiv210705636I/abstract) for details.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nHmin | 10^22 | 0.01 | 1e-07 | 1000 | 1e-07 | 1000000 | 0.01 |  |
| 2 | nHmax | 10^22 | 10 | 1e-07 | 1000 | 1e-07 | 1000000 | 0.01 |  |
| 3 | beta | — | 0 | -10 | 10 | -10 | 10 | 0.01 |  |
| 4 | log_xi | — | 3 | -3 | 6 | -3 | 6 | 0.01 |  |
| 5 | redshift | — | 0 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zxipab*powerlaw")
# component: m.zxipab  (params as attributes)
```
