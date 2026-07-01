---
name: carbatm
type: add  # additive
func: C_carbatm
n_params: 4
family: [carbatm]
energy_range: [0., 20.]
source: manager/model.dat + XSmodelCarbatm.tex
---

# carbatm

**additive model** (`add`), function `C_carbatm`.

## Description

The model provides the spectra emitted from a nonmagnetic carbon
atmosphere of a neutron star. The model spectra in a 0 - 20 keV range
of (unredshifted) photon energy are computed on a grid of surface
gravity accelerations log(g) = 13.7 - 14.9 (in cgs units) and
effective temperatures T = 1 - 4 MK. For a given set of the fitting
parameters, the surface gravity g and the gravitational redshift z are
derived from the mass M and radius R of the star. The trial spectra
are computed using a linear interpolation between the nearest model
spectra on the T-log(g) grid, and the boundaries of the energy
bins. The number of photons in each bin are divided by (1+z). This is
an updated version of the models presented in
[Suleimanov et
    al. (2014)](https://ui.adsabs.harvard.edu/abs/2014ApJS..210...13S/abstract). The
details can be found in [Suleimanov et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016EPJA...52...20S/abstract).

The directory used for the files required by this model can be changed
by using the `xset` command to set CARBATM.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | T | MK | 2 | 1 | 4 | 1 | 4 | 0.001 |  |
| 2 | NSmass | Msun | 1.4 | 0.6 | 2.8 | 0.6 | 2.8 | 0.001 |  |
| 3 | NSrad | km | 10 | 6 | 23 | 6 | 23 | 0.001 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("carbatm")
# component: m.carbatm  (params as attributes)
```
