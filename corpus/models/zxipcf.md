---
name: zxipcf
type: mul  # multiplicative
func: C_zxipcf
n_params: 4
family: [zxipcf]
energy_range: [0.01, 1.e20]
source: manager/model.dat + XSmodelZxipcf.tex
---

# zxipcf

**multiplicative model** (`mul`), function `C_zxipcf`.

## Description

This model uses a grid of XSTAR photionized absorption models (calculated 
assuming a microturbulent velocity of 200km/s) for the absorption, then 
assumes that this only covers some fraction f of the source, while the 
remaining (1-f) of the spectrum is seen directly. This is the model used 
by [Reeves et al. (2008)](https://ui.adsabs.harvard.edu/abs/2008MNRAS.385L.108R/abstract) 'On why the iron K-shell absorption in AGN is not 
the signature of the local warm-hot intergalactic medium', and may also be 
more generally applicable to the spectral complexity seen in Narrow Line 
Seyfert 1 AGN ([Miller et al. 2007](https://ui.adsabs.harvard.edu/abs/2006A%26A...453L..13M/abstract)).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Nh | 10^22 | 10 | 0.05 | 500 | 0.05 | 500 | 0.1 |  |
| 2 | log_xi | — | 3 | -3 | 6 | -3 | 6 | 0.01 |  |
| 3 | CvrFract | — | 0.5 | 0 | 1 | 0 | 1 | 0.01 |  |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zxipcf*powerlaw")
# component: m.zxipcf  (params as attributes)
```
