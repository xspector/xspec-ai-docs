---
name: cflux
type: con  # convolution
func: C_cflux
n_params: 3
family: [cflux]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCflux.tex
---

# cflux

**convolution model** (`con`), function `C_cflux`.

## Description

A convolution model to calculate the 
flux of other model components. For example:

```
   cflux*phabs*(pow + gauss)
```

with the normalization of the power-law model fixed to a non-zero value 
gives the flux and error on the entire model.

```
   phabs*cflux*(pow + gauss)
```

again with the normalization of the power-law fixed to a non-zero value 
gives the unabsorbed flux and error. Finally,

```
   phabs*(pow + cflux*gauss)
```

with the normalizaton of the gaussian fixed to a non-zero value gives the 
flux and error on the gaussian component. Note that when the `cflux` model is 
used the normalization of one of the additive models **must** be fixed 
to a non-zero value. It is also important to ensure that the energy range 
over which the model is calculated (which is determined by the response 
matrix in use) covers the energy range for which the flux is calculated. 
If the model to which the `cflux` is applied integrates to zero then 
a divide-by-zero error will occur resulting in NaN values for the fit statistic.

Parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Emin | keV | 0.5 | 0 | 1000000 | 0 | 1000000 | 0.1 | frozen by default |
| 2 | Emax | keV | 10 | 0 | 1000000 | 0 | 1000000 | 0.1 | frozen by default |
| 3 | lg10Flux | cgs | -12 | -100 | 100 | -100 | 100 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("cflux*powerlaw")
# component: m.cflux  (params as attributes)
```
