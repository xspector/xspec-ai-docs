---
name: nsa
type: add  # additive
func: nsa
n_params: 5
family: [nsa]
energy_range: [.05, 12.]
source: manager/model.dat + XSmodelNsa.tex
---

# nsa

**additive model** (`add`), function `nsa`.

## Description

This model provides the spectra in the X-ray range (0.05--10 keV)
emitted from a hydrogen atmosphere of a neutron star. There are three
options : nonmagnetized (B $< 10^8 - 10^9$ G) with a uniform surface
(effective) temperature in the range of $\log T_{eff}(K) = 5.0 - 7.0$; a
field B = $10^{12}$ G with a uniform surface (effective) temperature in the
range of $\log T_{eff}(K) = 5.5 - 6.8$; a field B = $10^{13}$ G with a uniform
surface (effective) temperature in the range of $\log T_{eff}(K) = 5.5 -
6.8$. The atmosphere is in radiative and hydrostatic equilibrium;
sources of heat are well below the atmosphere. The Comptonization
effects (significant at $T_{eff} > 3\times 10^6$ K) are taken into account. The
model spectra are provided as seen by a distant observer, with
allowance for the GR effects. The user is advised to keep $M_{ns}$ and $R_{ns}$
fixed and fit the temperature and the normalization. MagField must be
fixed at one of 0, $10^{12}$, or $10^{13}$.

The values of the effective temperature and radius as measured by a
distant observer (``values at infinity'') are :

$$T^{\inf}_{eff} = T_{eff} \times g_r
R^{\inf}_{ns} = R_{ns}/g_r$$

where

$$g_r = \sqrt{1 - 2.952\times M_{ns}/R_{ns}}$$

is the gravitational redshift parameter.

Please send your comments/questions to Slava Zavlin
([vyacheslav.zavlin@msfc.nasa.gov](mailto:vyacheslav.zavlin@msfc.nasa.gov)) and/or George Pavlov
([pavlov@astro.psu.edu](mailto:pavlov@astro.psu.edu)). If you publish results obtained using these
models, please reference [Zavlin, Pavlov & Shibanov
  (1996)](https://ui.adsabs.harvard.edu/abs/1996A%26A...315..141Z/abstract) for
nonmagnetic models, and [Pavlov et al. (1995)](https://ui.adsabs.harvard.edu/abs/1995ASIC..450...71P/abstract) for magnetic models.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LogT_eff | K | 6 | 5 | 7 | 5 | 7 | 0.01 |  |
| 2 | M_ns | Msun | 1.4 | 0.5 | 2.5 | 0.5 | 2.5 | 0.1 |  |
| 3 | R_ns | km | 10 | 5 | 20 | 5 | 20 | 0.1 |  |
| 4 | MagField | G | 0 | 0 | 50000000000000 | 0 | 50000000000000 | 1000000000 | frozen by default |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nsa")
# component: m.nsa  (params as attributes)
```
