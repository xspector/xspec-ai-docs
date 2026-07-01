---
name: cabs
type: mul  # multiplicative
func: xscabs
n_params: 1
family: [cabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCabs.tex
---

# cabs

**multiplicative model** (`mul`), function `xscabs`.

## Description

Optically-thin Compton scattering.

$$M(E)=exp(-\eta_H\sigma_T(E))$$

where $\sigma_T(E)$ is the Thomson cross-section with Klein-Nishina 
corrections at high energies. Note that this model does not do frequency 
downshifting so is only valid for scattering out of the beam.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |

## PyXspec

```python
from xspec import Model
m = Model("cabs*powerlaw")
# component: m.cabs  (params as attributes)
```
