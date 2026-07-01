---
name: simpl
type: con  # convolution
func: C_simpl
n_params: 3
family: [simpl]
energy_range: [0.05, 1.e6]
source: manager/model.dat + XSmodelSimpl.tex
---

# simpl

**convolution model** (`con`), function `C_simpl`.

## Description

The SIMple Power Law model:  An empirical model of Comptonization in which a 
fraction of the photons in an input seed spectrum is scattered into a 
power-law component ([Steiner et al. 2009](https://ui.adsabs.harvard.edu/abs/2009PASP..121.1279S/abstract)).  
It is designed for use with soft thermal spectra that are not Compton thick 
and that have a photon index Gamma > 1. `simpl` offers the 
advantage of operating in a self consistent manner, linking the seed spectrum 
to the generated power law.  Compared to `powerlaw`, `simpl` 
gives equally good fits while also employing just two parameters, and 
`simpl` has the virtue of eliminating the divergence of `powerlaw` 
at low energies.  Because `simpl` redistributes input photons to 
higher (and lower energies), for detectors with limited response matrices 
(at high or low energies), or with poor resolution, the sampled energies 
should be extended to adequately cover the relevant energy range (for details 
and an example, see the appendix in [Steiner et al. (2009)](https://ui.adsabs.harvard.edu/abs/2009PASP..121.1279S/abstract)).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Gamma | — | 2.3 | 1.1 | 4 | 1 | 5 | 0.05 |  |
| 2 | FracSctr | — | 0.05 | 0 | 0.4 | 0 | 1 | 0.005 |  |
| 3 | UpScOnly | — | 1 | 0 | 100 | 0 | 100 | 1 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("simpl*powerlaw")
# component: m.simpl  (params as attributes)
```
