---
name: ssa
type: add  # additive
func: ssa
n_params: 3
family: [ssa]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelSsa.tex
---

# ssa

**additive model** (`add`), function `ssa`.

## Description

The strangeon star atmosphere (ssa) model describes the radiation from interstellar medium accreted plasma atmosphere on a strangeon star surface and its spectrum. The ssa could simply be regarded as the upper layer of a normal neutron star because the radiation from strangeon matter can be neglected (Wang et al. 2017, 1705.03763). The atmosphere is in radiative, thermal equilibrium and two-temperature. The ssa spectrum is based on bremsstrahlung from an extremely thin hydrogen plasma. More details of the ssa model are described in Wang et al. (2017, ApJ, 837, 81).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | te | — | 0.1 | 0.01 | 0.5 | 0.01 | 0.5 | 1e-05 |  |
| 2 | y | — | 0.7 | 0.0001 | 1000 | 0.0001 | 1000 | 1e-05 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("ssa")
# component: m.ssa  (params as attributes)
```
