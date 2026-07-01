---
name: hatm
type: add  # additive
func: C_hatm
n_params: 4
family: [hatm]
energy_range: [0., 20.]
source: manager/model.dat + XSmodelHatm.tex
---

# hatm

**additive model** (`add`), function `C_hatm`.

## Description

This model provides the spectra emitted from a nonmagnetic hydrogen
atmosphere of a neutron star. The model spectra in a 0 - 20 keV range
of (unredshifted) photon energy are computed on a grid of surface
gravity accelerations log(g)=13.7 - 14.9 (in cgs units) and effective
temperatures T = 0.5 - 10 MK. For a given set of the fitting
parameters, the surface gravity g and the gravitational redshift z are
derived from the mass M and radius R of the star. The trial spectra
are computed using a linear interpolation between the nearest model
spectra on the T-log(g) grid, and the boundaries of the energy bins
and the number of photons in each bin are divided by (1+z). The
details of the model can be found in [Suleimanov et al. (2017)](https://ui.adsabs.harvard.edu/abs/2017A%26A...600A..43S/abstract) and [Klochkov et
al. (2015)](https://ui.adsabs.harvard.edu/abs/2015A%26A...573A..53K/abstract).

The directory used for the files required by this model can be changed
by using the `xset` command to set HATM.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | T | MK | 3 | 0.5 | 10 | 0.5 | 10 | 0.001 |  |
| 2 | NSmass | Msun | 1.4 | 0.6 | 2.8 | 0.6 | 2.8 | 0.001 |  |
| 3 | NSrad | km | 10 | 5 | 23 | 5 | 23 | 0.001 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("hatm")
# component: m.hatm  (params as attributes)
```
