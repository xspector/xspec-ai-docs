---
name: zbabs
type: mul  # multiplicative
func: c_xszbabs
n_params: 4
family: [zbabs]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelZbabs.tex
---

# zbabs

**multiplicative model** (`mul`), function `c_xszbabs`.

## Description

The ISM attenuation due to neutral H, neutral He and once ionized He. This 
is a modified version of the [Rumph et al. (1994)](https://ui.adsabs.harvard.edu/abs/1994AJ....107.2108R/abstract)
model, using the ismatten program by Pat Jelinsky, and allows the user to set the model redshift.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 0.0001 | 0 | 100000 | 0 | 1000000 | 1e-05 |  |
| 2 | nHeI | 10^22 | 1e-05 | 0 | 100000 | 0 | 1000000 | 1e-06 |  |
| 3 | nHeII | 10^22 | 1e-06 | 0 | 100000 | 0 | 1000000 | 1e-07 |  |
| 4 | z | — | 0 | 0 | 100000 | 0 | 1000000 | 1e-06 |  |

## PyXspec

```python
from xspec import Model
m = Model("zbabs*powerlaw")
# component: m.zbabs  (params as attributes)
```
