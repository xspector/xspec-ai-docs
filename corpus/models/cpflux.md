---
name: cpflux
type: con  # convolution
func: C_cpflux
n_params: 3
family: [cpflux]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCpflux.tex
---

# cpflux

**convolution model** (`con`), function `C_cpflux`.

## Description

A convolution model to calculate the photon flux of other model components. 
For example :

```
   cpflux*phabs*(pow + gauss)
```

with the normalization of the power-law model fixed to a non-zero value gives 
the photon flux and error on the entire model.

```
   phabs*cpflux*(pow + gauss)
```

again with the normalization of the power-law fixed to a non-zero value gives 
the unabsorbed photon flux and error. Finally,

```
   phabs*(pow + cpflux*gauss)
```

with the normalizaton of the gaussian fixed to a non-zero value gives the 
photon flux and error on the gaussian component. Note that when the `cpflux`
model is used the normalization of one of the additive models **must** be 
fixed to a non-zero value. It is also important to ensure that the energy range 
over which the model is calculated (which is determined by the response matrix 
in use) covers the energy range for which the photon flux is calculated. If 
the model to which the `cpflux` is applied integrates to zero then a 
divide-by-zero error will occur resulting in NaN values for the fit statistic.

Parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Emin | keV | 0.5 | 0 | 1000000 | 0 | 1000000 | 0.1 | frozen by default |
| 2 | Emax | keV | 10 | 0 | 1000000 | 0 | 1000000 | 0.1 | frozen by default |
| 3 | Flux | — | 1 | 0 | 10000000000 | 0 | 10000000000 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("cpflux*powerlaw")
# component: m.cpflux  (params as attributes)
```
