---
name: cheb6
type: add  # additive
func: C_cheb6
n_params: 11
family: [cheb6, vcheb6, bcheb6, bvcheb6]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCheb6.tex
---

# cheb6

**additive model** (`add`), function `C_cheb6`.

Variants documented together: `cheb6`, `vcheb6`, `bcheb6`, `bvcheb6`.

## Description

`cheb6` is a multi-temperature collisional-ionization model
using a sixth-order Chebyshev polynomial for the
differential emission measure. The DEM is not constrained to be
positive. The differential emission measure is defined per unit
$\log_{10}(T)$,

$$dEM = Q(x)\,(T/10^{6}\,{\rm K})\,d\log_{10}(T), \qquad
Q(x) = \sum_{j=1}^{6} a_j T_j(x), \qquad
x = 0.8\left(\log_{10}T[{\rm K}] - 5.5\right) - 1,$$

where $T_j$ is the Chebyshev polynomial of the first kind of order $j$
and the coefficients $a_1$--$a_6$ are par1--6. Note that the sum starts
at $j=1$: there is no constant ($T_0$) term, so the DEM cannot be given
a temperature-independent offset. The variable $x$ maps
$\log_{10}T[{\rm K}] = 5.5$--8.0 onto $[-1,1]$, and the sum is evaluated
on a grid uniform in $\log_{10}(T)$ over that range with a step of 0.1.
As for `cempow`, expressing the DEM in terms of $dT$ instead
introduces a factor of $\ln 10$. The switch parameter determines whether spectrum is
calculated by running the mekal code, by interpolating on a
pre-calculated mekal table, using the AtomDB data or the SPEX
data. The final two options
are now preferred. See the `cie` model for further information
and options. The reference for this model is [Singh et al. (1996,
ApJ, 456, 766)](https://ui.adsabs.harvard.edu/abs/1996ApJ...456..766S/abstract).

Velocity broadening can only be used with switch=2 or switch=3.

For `cheb6` the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | CPcoef1 | — | 1 | -1 | 1 | -1 | 1 | 0.1 |  |
| 2 | CPcoef2 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 3 | CPcoef3 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 4 | CPcoef4 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 5 | CPcoef5 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 6 | CPcoef6 | — | 0.5 | -1 | 1 | -1 | 1 | 0.01 |  |
| 7 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 8 | abundanc | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 9 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 10 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 11 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cheb6")
# component: m.cheb6  (params as attributes)
```
