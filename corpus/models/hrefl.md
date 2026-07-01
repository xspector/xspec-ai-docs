---
name: hrefl
type: mul  # multiplicative
func: xshrfl
n_params: 8
family: [hrefl]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelHrefl.tex
---

# hrefl

**multiplicative model** (`mul`), function `xshrfl`.

## Description

A simple multiplicative reflection model due to Tahir Yaqoob. This model gives 
the reflected X-ray spectrum from a cold, optically thick, circular slab with 
inner and outer radii (Ri & Ro, respectively) illuminated by a point source 
a height H above the center of the slab. The main difference between this 
model and other reflection models is that analytic approximations are used 
for the Chandrasekar H functions (and their integrals) and ELASTIC SCATTERING 
is assumed (see [Basko 1978](https://ui.adsabs.harvard.edu/abs/1978ApJ...223..268B/abstract)). The elastic-scattering 
approximation means that the model is ONLY VALID UP TO $\approx$ 15 keV in 
the source frame. Future enhancements will include fudge factors that will 
allow extension up to 100 keV. The fact that no integration is involved at 
any point makes the routine very fast and particularly suitable for 
generating error contours, especially when fitting a large number of data 
channels. The model is multiplicative, and so can be used with ANY 
incident continuum.

Parameters are as follows:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | thetamin | — | 0 | 0 | 90 | 0 | 90 | 0.1 | frozen by default |
| 2 | thetamax | — | 90 | 0 | 90 | 0 | 90 | 0.1 | frozen by default |
| 3 | thetaobs | — | 60 | 0 | 90 | 0 | 90 | 0.01 |  |
| 4 | Feabun | — | 1 | 0 | 100 | 0 | 200 | 0.01 | frozen by default |
| 5 | FeKedge | keV | 7.11 | 7 | 10 | 7 | 10 | 0.01 | frozen by default |
| 6 | Escfrac | — | 1 | 0 | 500 | 0 | 1000 | 0.01 |  |
| 7 | covfac | — | 1 | 0 | 500 | 0 | 1000 | 0.01 |  |
| 8 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("hrefl*powerlaw")
# component: m.hrefl  (params as attributes)
```
