---
name: nsmaxg
type: add  # additive
func: C_nsmaxg
n_params: 6
family: [nsmaxg]
energy_range: [0.05, 10.0]
source: manager/model.dat + XSmodelNsmaxg.tex
---

# nsmaxg

**additive model** (`add`), function `C_nsmaxg`.

## Description

The `nsmaxg` model interpolates from a grid of neutron star (NS)
atmosphere spectra to produce a final spectrum that depends on the
parameters listed below. Atmosphere spectra are obtained using the
latest equation of state and opacity results for a partially ionized,
strongly magnetized hydrogen or mid-Z element plasma. Models are
constructed by solving the coupled radiative transfer equations for
the two photon polarization modes in a magnetized medium, and the
atmosphere is in radiative and hydrostatic equilibrium. Atmosphere
models mainly depend on the surface effective temperature $T_{eff}$ and
magnetic field strength $B$ and inclination $\Theta_B$; there is also a
dependence on the surface gravity $g = (1+z_g)GM/R^2$, where
$1+z_g = 1/\sqrt{1-2GM/R}$ is the gravitational redshift and $M$ and $R$ are the
NS mass and radius, respectively.

Two sets of models are available: one set with a single surface $B$ and
$T_{eff}$ [some models allow for varying $g$, in the range $\log g$ (cm/s$^2$) =
 13.6--15.4] and a set which is constructed with $B$ and $T_{eff}$ varying
across the surface according to the magnetic dipole model ($\theta_m$ is the
angle between the direction to the observer and the magnetic
axis). Effective temperatures span the range $\log T_{eff} (K)$ =
5.5--6.8. Models with single ($B$,$T_{eff}$) cover the energy range 0.05--10
keV, while models with ($B$,$T_{eff}$)-distributions cover the range 0.09--5
keV.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | logTeff | K | 6 | 5.5 | 6.9 | 5.5 | 6.9 | 0.01 |  |
| 2 | M_ns | Msun | 1.4 | 0.5 | 3 | 0.5 | 3 | 0.1 |  |
| 3 | R_ns | km | 10 | 5 | 30 | 5 | 30 | 0.1 |  |
| 4 | dist | kpc | 1 | 0.01 | 100 | 0.01 | 100 | 0.1 |  |
| 5 | specfile | — | 1200 |  |  |  |  |  | switch (not fitted) |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nsmaxg")
# component: m.nsmaxg  (params as attributes)
```
