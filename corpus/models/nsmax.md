---
name: nsmax
type: add  # additive
func: C_nsmax
n_params: 4
family: [nsmax]
energy_range: [0.05, 10.0]
source: manager/model.dat + XSmodelNsmax.tex
---

# nsmax

**additive model** (`add`), function `C_nsmax`.

## Description

This model has been superseded by `nsmaxg`.

This model interpolates from a grid of neutron star (NS) atmosphere
spectra to produce a final spectrum that depends on the parameters
listed below. The atmosphere spectra are obtained using the latest
equation of state and opacity results for a partially ionized,
strongly magnetized hydrogen or mid-Z element plasma. The models are
constructed by solving the coupled radiative transfer equations for
the two photon polarization modes in a magnetized medium, and the
atmosphere is in radiative and hydrostatic equilibrium. The atmosphere
models mainly depend on the surface effective temperature $T_{eff}$ and
magnetic field strength $B$ and inclination $\Theta_B$; there is also a
dependence on the surface gravity $g = (1+z_g)GM/R^2$, where
$1+z_g = \sqrt{1-2GM/R}$ is the gravitational redshift and $M$ and $R$ are the
NS mass and radius, respectively.

Two sets of models are given: one set with a single surface $B$ and
$T_{eff}$ and a set which is constructed with $B$ and $T_{eff}$
varying across the surface according to the magnetic dipole model (for
the latter, $\theta_m$ is the angle between the direction to the
observer and the magnetic axis). The effective temperatures span the
range $\log T_{eff} = 5.5 - 6.8$ for hydrogen and $\log T_{eff} = 5.8
- 6.9$ for mid-Z elements. The models with single ($B$,$T_{eff}$)
cover the energy range 0.05--10 keV, while the models with
($B$,$T_{eff}$)-distributions cover the range 0.09--5 keV.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | logTeff | K | 6 | 5.5 | 6.8 | 5.5 | 6.8 | 0.01 |  |
| 2 | redshift | — | 0.1 | 1e-05 | 1.5 | 1e-05 | 2 | 0.1 |  |
| 3 | specfile | — | 1200 |  |  |  |  |  | switch (not fitted) |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nsmax")
# component: m.nsmax  (params as attributes)
```
