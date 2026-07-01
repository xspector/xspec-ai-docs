---
name: nthComp
type: add  # additive
func: donthcomp
n_params: 6
family: [nthcomp]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelNthcomp.tex
---

# nthComp

**additive model** (`add`), function `donthcomp`.

## Description

Please note that this model is now superseded by `thcomp`
which is more accurate and also works for any seed photon spectrum.

Nthcomp is a { much} better description of the continuum shape from
thermal comptonisation than an exponentially cutoff power law, but is
not that much more complicated in terms of parameters. The high energy
cutoff is sharper than an exponential, and is parameterized by the
electron temperature ($kT_e$). VERY roughly, an exponential rollover
energy $E_c = 2-3 kT_e$ but the shape is very different, so it impacts on
the reflected fraction as well. Another major effect (especially for
X-ray binaries) is that it incorporates the low energy rollover. The
hot electrons Compton UPscatter seed photons so there are few photons
in the scattered spectrum at energies below the typical seed photon
energies, making it significantly different to a power law below this
energy. Typically the physical picture is that these seed photons are
(quasi)blackbody (eg neutron star boundary layer) or disk blackbody in
shape. Either of these shapes can be selected (input type), both being
parameterized by a seed photon temperature ($kT_{bb}$). Between the low
and high energy rollovers the shape of the spectrum is set by the
combination of electron scattering optical depth and electron
temperature. It is not necessarily a power law, but can be
parameterized by an asymptotic power law index ($\Gamma$). Details of
this are given in [Zycki, Done & Smith (1999)](https://ui.adsabs.harvard.edu/abs/1999MNRAS.309..561Z/abstract), including a
self-consistent reflection component which is NOT released here as it
was written using non-FITS standard files so has significant issues
with portability.

This is the thermally comptonized continuum model of [Zdziarski,
Johnson & Magdziarz (1996)](https://ui.adsabs.harvard.edu/abs/1996MNRAS.283..193Z/abstract), as extended by [Zycki, Done
& Smith (1999)](https://ui.adsabs.harvard.edu/abs/1999MNRAS.309..561Z/abstract). Please reference these papers if you use
it.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Gamma | — | 1.7 | 1.001 | 5 | 1.001 | 10 | 0.01 |  |
| 2 | kT_e | keV | 100 | 5 | 1000 | 1 | 1000 | 0.1 |  |
| 3 | kT_bb | keV | 0.1 | 0.001 | 10 | 0.001 | 10 | 1 | frozen by default |
| 4 | inp_type | 0/1 | 0 | 0 | 1 | 0 | 1 | 1 | frozen by default |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nthComp")
# component: m.nthcomp  (params as attributes)
```
