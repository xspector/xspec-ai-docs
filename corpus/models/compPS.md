---
name: compPS
type: add  # additive
func: C_xscompps
n_params: 20
family: [compPS]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelCompps.tex
---

# compPS

**additive model** (`add`), function `C_xscompps`.

## Description

Comptonization spectra computed for different geometries using exact
numerical solution of the radiative transfer equation. The
computational ``iterative scattering method'' is similar to the standard
Lambda-iteration and is described in [Poutanen & Svensson
  (1996, ApJ 470, 249; PS96)](https://ui.adsabs.harvard.edu/abs/1996ApJ...470..249P/abstract).  The Compton scattering kernel is the exact one
as derived by [Jones (1968, Phys. Rev. 167,
  1159)](https://ui.adsabs.harvard.edu/abs/1968PhRv..167.1159J/abstract).
See PS96 for additional references.

Comptonization spectra depend on the geometry (slab, sphere,
hemisphere, cylinder), Thomson optical depth tau, parameters of the
electron distribution, spectral distribution of soft seed photons, the
way seed soft photons are injected to the electron cloud, and the
inclination angle of the observer.

The resulting spectrum is reflected from the cool medium according to
the computational method of [Magdziarz & Zdziarski (1995)](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract) (see
`reflect`, `pexrav`, `pexriv`
models). $rel_{refl}$ is the solid angle of the cold material visible
from the Comptonizing source (in units of $2\pi$), other parameters
determine the abundances and ionization state of reflecting material
(Fe_ab_re, Me_ab, xi, Tdisk). The reflected spectrum is smeared out by
rotation of the disk due to special and general relativistic effects
using ``diskline''-type kernel (with parameters Betor10, Rin, Rout).

Electron distribution function can be Maxwellian, power-law, cutoff
Maxwellian, or hybrid (with low temperature Maxwellian plus a
power-law tail).

Possible geometries include plane-parallel slab, cylinder (described
by the height-to-radius ratio H/R), sphere, or hemisphere. By default
the lower boundary of the ``cloud'' (not for spherical geometry) is
fully absorbive (e.g. cold disk). However, by varying covering factor
parameter cov_fac, it may be made transparent for radiation. In that
case, photons from the ``upper'' cloud can also be upscattered in the
``lower'' cloud below the disk. This geometry is that for an accretion
disk with cold cloudlets in the central plane ([Zdziarski et
al. 1998, MNRAS 301, 435](https://ui.adsabs.harvard.edu/abs/1998MNRAS.301..435Z/abstract)).  For cylinder and hemisphere geometries,
an approximate solution is obtained by averaging specific intensities
over horizontal layers (see PS96). For slab and sphere geometries, no
approximation is made.

The seed photons can be injected to the electron cloud either
isotropically and homogeneously through out the cloud, or at the
bottom of the slab, cylinder, hemisphere or center of the sphere (or
from the central plane of the slab if cov_frac is not 1). For the sphere,
there exist a possibility (IGEOM=-5) for photon injection according to
the eigenfunction of the diffusion equation
$\sin(\pi*\tau'/\tau)/(\pi*\tau'/\tau)$, where $\tau'$ is the optical
depth measured from the center (see [Sunyaev & Titarchuk 1980](https://ui.adsabs.harvard.edu/abs/1980A&A....86..121S/abstract)).

Seed photons can be black body (`bbodyrad`) for Tbb positive
or multicolor disk (`diskbb`) for Tbb negative. The
normalization of the model also follows those models: (1) Tbb positive, K =
(RKM)**2 /(D10)**2, where D10 is the distance in units of 10 kpc and
RKM is the source radius in km; (2) Tbb negative, K = (RKM)**2 /(D10)**2
cos(theta), where theta is the inclination angle.

Thomson optical depth of the cloud is not always good parameter to
fit.  Instead the Compton parameter y=4 * tau * Theta (where Theta= Te
(keV) / 511 ) can be used. Parameter y is directly related to the
spectral index and therefore is much more stable in fitting
procedure. The fitting can be done taking 6th parameter negative, and
optical depth then can be obtained via tau= y/(4* Te / 511).

The region of parameter space where the numerical method produces
reasonable results is constrained as follows : 1) Electron temperature
Te > 10 keV; 2) Thomson optical depth tau < 1.5 for
slab geometry and tau < 3, for other geometries.

In versions 4.0 and above the Compton reflection is done by a call to
the `ireflect` model code and the relativistic blurring by a
call to `rdblur`. This does introduce some changes in the
spectrum from earlier versions. For the case of a neutral reflector
(i.e. the ionization parameter is zero) more accurate opacities are
calculated. For the case of an ionized reflector the old version
assumed that for the purposes of calculating opacities the input
spectrum was a power-law (with index based on the 2--10 keV
spectrum). The new version uses the actual input spectrum, which is
usually not a power law, giving different opacities for a given
ionization parameter and disk temperature. The Greens' function
integration required for the Compton reflection calculation is
performed to an accuracy of 0.01 (i.e. 1%). This can be changed using
e.g. `xset` **COMPPS_PRECISION 0.05**.

The model parameters are as follows :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kTe | keV | 100 | 20 | 100000 | 20 | 100000 | 10 |  |
| 2 | EleIndex | — | 2 | 0 | 5 | 0 | 5 | 0.01 | frozen by default |
| 3 | Gmin | — | -1 | -1 | 10 | -1 | 10 | 0.1 | frozen by default |
| 4 | Gmax | — | 1000 | 10 | 10000 | 10 | 10000 | 1 | frozen by default |
| 5 | kTbb | keV | 0.1 | 0.001 | 10 | 0.001 | 10 | 0.01 | frozen by default |
| 6 | tau_y | — | 1 | 0.05 | 3 | 0.05 | 3 | 0.1 |  |
| 7 | geom | — | 0 | -5 | 4 | -5 | 4 | 1 | frozen by default |
| 8 | HovR_cyl | — | 1 | 0.5 | 2 | 0.5 | 2 | 1 | frozen by default |
| 9 | cosIncl | — | 0.5 | 0.05 | 0.95 | 0.05 | 0.95 | 0.1 | frozen by default |
| 10 | cov_frac | — | 1 | 0 | 1 | 0 | 1 | 0.1 | frozen by default |
| 11 | rel_refl | — | 0 | 0 | 10000 | 0 | 10000 | 0.1 | frozen by default |
| 12 | Fe_ab_re | — | 1 | 0.1 | 10 | 0.1 | 10 | 0.01 | frozen by default |
| 13 | Me_ab | — | 1 | 0.1 | 10 | 0.1 | 10 | 0.01 | frozen by default |
| 14 | xi | — | 0 | 0 | 100000 | 0 | 100000 | 0.1 | frozen by default |
| 15 | Tdisk | K | 1000000 | 10000 | 1000000 | 10000 | 1000000 | 10 | frozen by default |
| 16 | Betor10 | — | -10 | -10 | 10 | -10 | 10 | 0.1 | frozen by default |
| 17 | Rin | Rs | 10 | 6.001 | 1000 | 6.001 | 10000 | 0.1 | frozen by default |
| 18 | Rout | Rs | 1000 | 0 | 1000000 | 0 | 1000000 | 1 | frozen by default |
| 19 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 20 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("compPS")
# component: m.compps  (params as attributes)
```
