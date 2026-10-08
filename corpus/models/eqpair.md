---
name: eqpair
type: add  # additive
func: C_xseqpair
n_params: 21
family: [eqpair, eqtherm, compth]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelEqpair.tex
---

# eqpair

**additive model** (`add`), function `C_xseqpair`.

Variants documented together: `eqpair`, `eqtherm`, `compth`.

## Description

These models are based on Paolo Coppi's hybrid thermal/non-thermal hot
plasma emission model for X-ray binaries. The underlying physics and a
detailed description of the code are included in the draft paper
http://www.astro.yale.edu/coppi/eqpair/eqpap4.ps.

Do not use these models without reading and understanding this
paper. Simplified models `eqtherm` and `compth` are provided for cases
where non-thermal processes are not important and photon-photon pair
production can be ignored. These should only be used if $l_{bb} <~ 10$.

The temperature of the thermal component of the electron distribution
and the total electron optical depth (for both ionization electrons
and electron-positron pairs) are written out if the chatter level is
set to 20. This information is important for checking
self-consistency.

In versions 1.10 and above the Compton reflection is done by a call to
the `ireflect` model code and the relativistic blurring by a call to
`rdblur`. This does introduce some changes in the spectrum from earlier
versions. For the case of a neutral reflector (i.e. the ionization
parameter is zero) more accurate opacities are calculated. For the
case of an ionized reflector the old version assumed that for the
purposes of calculating opacities the input spectrum was a power-law
(with index based on the 2--10 keV spectrum). The new version uses the
actual input spectrum, which is usually not a power law, giving
different opacities for a given ionization parameter and disk
temperature. The Greens' function integration required for the Compton
reflection calculation is performed to an accuracy of 0.01
(i.e. 1%). This can be changed using e.g. `xset` **EQPAIR_PRECISION 0.05**.

The parameters for all three models are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | l_hovl_s | — | 1 | 1e-06 | 1000000 | 1e-06 | 1000000 | 0.01 |  |
| 2 | l_bb | — | 100 | 0 | 10000 | 0 | 10000 | 1 |  |
| 3 | kT_bb | eV | 200 | 1 | 400000 | 1 | 400000 | 1 | frozen by default |
| 4 | l_ntol_h | — | 0.5 | 0 | 0.9999 | 0 | 0.9999 | 0.01 |  |
| 5 | tau_p | — | 0.1 | 0.0001 | 10 | 0.0001 | 10 | 0.0001 | frozen by default |
| 6 | radius | cm | 10000000 | 100000 | 1e+16 | 100000 | 1e+16 | 100000 | frozen by default |
| 7 | g_min | — | 1.3 | 1.2 | 1000 | 1.2 | 1000 | 0.01 | frozen by default |
| 8 | g_max | — | 1000 | 5 | 10000 | 5 | 10000 | 1 | frozen by default |
| 9 | G_inj | — | 2 | 0 | 5 | 0 | 5 | 0.1 | frozen by default |
| 10 | pairinj | — | 0 | 0 | 1 | 0 | 1 | 0.1 | frozen by default |
| 11 | cosIncl | — | 0.5 | 0.05 | 0.95 | 0.05 | 0.95 | 0.1 | frozen by default |
| 12 | Refl | — | 1 | 0 | 2 | 0 | 2 | 0.1 | frozen by default |
| 13 | Fe_abund | — | 1 | 0.1 | 10 | 0.1 | 10 | 0.01 | frozen by default |
| 14 | Ab_met | — | 1 | 0.1 | 10 | 0.1 | 10 | 0.01 | frozen by default |
| 15 | T_disk | K | 1000000 | 10000 | 1000000 | 10000 | 1000000 | 10 | frozen by default |
| 16 | xi | — | 0 | 0 | 1000 | 0 | 5000 | 10 |  |
| 17 | Beta | — | -10 | -10 | 10 | -10 | 10 | 0.01 | frozen by default |
| 18 | Rin | M | 10 | 6.001 | 1000 | 6.001 | 10000 | 0.1 | frozen by default |
| 19 | Rout | M | 1000 | 0 | 1000000 | 0 | 1000000 | 1 | frozen by default |
| 20 | redshift | — | 0 | 0 | 4 | 0 | 4 | 0.01 | frozen by default |
| 21 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("eqpair")
# component: m.eqpair  (params as attributes)
```
