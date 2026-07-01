---
name: disk
type: add  # additive
func: disk
n_params: 4
family: [disk]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelDisk.tex
---

# disk

**additive model** (`add`), function `disk`.

## Description

The spectrum from an accretion disk, where the opacities are dominated
by free-free absorption, i.e., the so-called blackbody disk model. Not
correct for a disk around a neutron star.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | accrate | — | 1 | 0.001 | 9 | 0.0001 | 10 | 0.01 |  |
| 2 | CenMass | Msun | 1.4 | 0.4 | 10 | 0.1 | 20 | 0.01 | frozen by default |
| 3 | Rinn | — | 1.03 | 1.01 | 1.03 | 1 | 1.04 | 0.001 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("disk")
# component: m.disk  (params as attributes)
```
