---
name: thcomp
type: con  # convolution
func: thcompf
n_params: 4
family: [thcomp]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelThcomp.tex
---

# thcomp

**convolution model** (`con`), function `thcompf`.

## Description

ThComp is a replacement for the `nthcomp` model
([Zdziarski et
  al. 1996](https://ui.adsabs.harvard.edu/abs/1996MNRAS.283..193Z/abstract)). It agrees much better
than `nthcomp` with actual Monte Carlo spectra from
Comptonization, see [Zdziarski et al. (2020)](https://ui.adsabs.harvard.edu/abs/2020MNRAS.492.5234Z/abstract) for
details. See [Nied{\'z}wiecki et al. (2019)](https://ui.adsabs.harvard.edu/abs/2019MNRAS.485.2942N/abstract) for
analogous comparison with `nthcomp`, showing substantial
discrepancies. ThComp describes spectra from Comptonization by
thermal electrons emitted by a spherical source with the
sinusoidal-like spatial distribution of the seed photons (as in
`compST`, [Sunyaev & Titarchuk 1980](https://ui.adsabs.harvard.edu/abs/1980A%26A....86..121S/abstract)). It is a convolution
model, and thus it can Comptonize any seed photon distribution, either
hard or soft, and it describes both upscattering and downscattering
(see [Zdziarski et al. 2020](https://ui.adsabs.harvard.edu/abs/2020MNRAS.492.5234Z/abstract) for examples). In the case of upscattering
of some seed photons (e.g. blackbody or disc blackbody), it is a much
better description of the continuum shape from thermal Comptonization
than an exponentially cutoff power law, but has similar corresponding
free parameters, the spectral index, $\Gamma$, and the high-energy
cutoff, parameterized by the electron temperature ($kT_e$). That
cutoff is much sharper than an exponential. The model also provides
correct description of Comptonized spectra at energies comparable to
those of the seed photons. Note that the model has no normalization
parameter since its normalization follows from that of the seed
photons.

Please reference [Zdziarski et
  al. (2020)](https://ui.adsabs.harvard.edu/abs/2020MNRAS.492.5234Z/abstract) if you use it. 

For this model to work correctly the energy range should be extended
beyond that required by the response, e.g. by using the command:
energies 0.01 1000.0 1000 log

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Gamma_tau | — | 1.7 | 1.001 | 5 | 1.001 | 10 | 0.01 |  |
| 2 | kT_e | keV | 50 | 0.5 | 150 | 0.5 | 150 | 0.1 |  |
| 3 | cov_frac | — | 1 | 0 | 1 | 0 | 1 | 0.001 |  |
| 4 | z | — | 0 | 0 | 5 | 0 | 5 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("thcomp*powerlaw")
# component: m.thcomp  (params as attributes)
```
