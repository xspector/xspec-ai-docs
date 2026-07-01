---
name: bexriv
type: add  # additive
func: C_xsbexriv
n_params: 12
family: [bexriv]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelBexriv.tex
---

# bexriv

**additive model** (`add`), function `C_xsbexriv`.

## Description

A broken power-law spectrum multiplied by exponential high-energy
cutoff, exp(-E/Ec), and reflected from ionized material. See [Magdziarz
& Zdziarski (1995)](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract) for details.

The output spectrum is the sum of an e-folded broken power law and the
reflection component. The reflection component alone can be obtained
for $|rel_{refl}| < 0$. Then the actual reflection normalization is
$|rel_{refl}|$. Note that you need to change then the limits of
$|rel_{refl}|$ excluding zero (as then the direct component
appears). If $E_c = 0$, there is no cutoff in the power law. The metal
and iron abundance are variable with respect to those set by the
command `abund`.

The core of this model is a Greens' function integration with one
numerical integral performed for each model energy. The numerical 
integration is done using an adaptive method which continues until 
a given estimated fractional precision is reached. The precision can 
be changed by setting BEXRIV_PRECISION eg `xset` **BEXRIV_PRECISION 0.05**. The default precision is 0.01 (ie 1%).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Gamma1 | — | 2 | -9 | 9 | -10 | 10 | 0.01 |  |
| 2 | breakE | keV | 10 | 0.1 | 1000 | 0.1 | 1000 | 0.1 |  |
| 3 | Gamma2 | — | 2 | -9 | 9 | -10 | 10 | 0.01 |  |
| 4 | foldE | keV | 100 | 1 | 1000000 | 1 | 1000000 | 10 |  |
| 5 | rel_refl | — | 0 | 0 | 1000000 | 0 | 1000000 | 0.01 |  |
| 6 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 7 | abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 8 | Fe_abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 9 | cosIncl | — | 0.45 | 0.05 | 0.95 | 0.05 | 0.95 | 0.01 | frozen by default |
| 10 | T_disk | K | 30000 | 10000 | 1000000 | 10000 | 1000000 | 1000 | frozen by default |
| 11 | xi | erg cm/s | 1 | 0 | 1000 | 0 | 5000 | 0.1 |  |
| 12 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bexriv")
# component: m.bexriv  (params as attributes)
```
