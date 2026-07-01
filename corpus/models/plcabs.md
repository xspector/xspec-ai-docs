---
name: plcabs
type: add  # additive
func: xsp1tr
n_params: 11
family: [plcabs]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelPlcabs.tex
---

# plcabs

**additive model** (`add`), function `xsp1tr`.

## Description

This model describes X-ray transmission of an isotropic source of
photons located at the center of a uniform, spherical distribution of
matter, correctly taking into account Compton scattering. The model
can be used for radial column densities up to $5\times 10^{-24}$
cm$^{-2}$. The valid energy range for which data can be modeled is
between 10 and 18.5 keV, depending on the column density. Details of
the physics of the model, the approximations used and further details
on the regimes of validity can be found in [Yaqoob (1997)](https://ui.adsabs.harvard.edu/abs/1997ApJ...479..184Y/abstract). In this particular incarnation, the initial spectrum is a power
law modified by a high-energy exponential cut-off above a certain
threshold energy.

Also, to improve the speed, a FAST option is available in which a full
integration over the input spectrum is replaced by a simple mean
energy shift for each bin. This option is obtained by setting
par9 to a value of 1 or greater and cannot be made
variable. Further, for single-scattering albedos less than the
critical albedo (i.e. par8) energy shifts are neglected
altogether. The recommended value for par8 is 0.1 which
corresponds to about 4 keV for cosmic abundances and is more than
adequate for ASCA data. 

Note that for column densities in the range $10^{23}$ -- $10^{24}$
cm$^{-2}$, the maximum number of scatterings which need be considered
for convergence of the spectrum of better than 1% is between 1 and
5. For column densities as high as $5\times 10^{24}$ cm$^{-2}$, the
maximum number of scatterings which need be considered for the same
level of convergence is 12. This parameter cannot be made variable.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | nmax | — | 1 |  |  |  |  |  | scale (not fitted) |
| 3 | FeAbun | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 4 | FeKedge | KeV | 7.11 | 7 | 10 | 7 | 10 | 0.01 | frozen by default |
| 5 | PhoIndex | — | 2 | -2 | 9 | -3 | 10 | 0.01 |  |
| 6 | HighECut | keV | 95 | 1 | 100 | 0.01 | 200 | 0.01 | frozen by default |
| 7 | foldE | — | 100 | 1 | 1000000 | 1 | 1000000 | 10 | frozen by default |
| 8 | acrit | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 9 | FAST | — | 0 |  |  |  |  |  | scale (not fitted) |
| 10 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 11 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("plcabs")
# component: m.plcabs  (params as attributes)
```
