---
name: clumin
type: con  # convolution
func: C_clumin
n_params: 4
family: [clumin]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelClumin.tex
---

# clumin

**convolution model** (`con`), function `C_clumin`.

## Description

A convolution model to calculate the 
luminosity of other model components. For example:

```
   clumin*phabs*(pow + gauss)
```

with the normalization of the power-law model fixed to a non-zero value 
gives the luminosity and error on the entire model.

```
   phabs*clumin*(pow + gauss)
```

again with the normalization of the power-law fixed to a non-zero value 
gives the unabsorbed luminosity and error. Finally,

```
   phabs*(pow + clumin*gauss)
```

with the normalizaton of the gaussian fixed to a non-zero value gives the 
luminosity and error on the gaussian component. Note that when the `clumin` model is 
used the normalization of one of the additive models **must** be fixed 
to a non-zero value. It is also important to ensure that the energy range 
over which the model is calculated (which is determined by the response 
matrix in use) covers the energy range for which the luminosity is calculated. 
If the model to which the `clumin` is applied integrates to zero then 
a divide-by-zero error will occur resulting in NaN values for the fit statistic.

Parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Emin | keV | 0.5 | 0 | 1000000 | 0 | 1000000 | 0.1 | frozen by default |
| 2 | Emax | keV | 10 | 0 | 1000000 | 0 | 1000000 | 0.1 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | lg10Lum | cgs | 40 | -100 | 100 | -100 | 100 | 0.01 |  |

## PyXspec

```python
from xspec import Model
m = Model("clumin*powerlaw")
# component: m.clumin  (params as attributes)
```
