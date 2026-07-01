---
name: reflect
type: con  # convolution
func: C_reflct
n_params: 5
family: [reflect]
energy_range: [0.001, 1.0e20]
source: manager/model.dat + XSmodelReflect.tex
---

# reflect

**convolution model** (`con`), function `C_reflct`.

## Description

Convolution model for reflection from neutral material according to the 
method of [Magdziarz & Zdziarski (1995)](https://ui.adsabs.harvard.edu/abs/1995MNRAS.273..837M/abstract). This is a 
generalization of the `pexrav` and `bexrav` models. The 
reflection component alone can be obtained for $rel_{refl}<0$. Then the 
actual reflection normalization is $|rel_{refl}|$ . Note that you need to 
change then the limits of $rel_{refl}$ excluding zero (as then the 
direct component appears). If $E_c=0$, there is no cutoff in the power law. 
The metal and iron abundance are variable with respect to those set by the 
command `abund`. The opacities are those set by the command `xsect`.
As expected in AGNs, H and He are assumed to be fully ionized.

When using this model it is essential to extend the energy range over 
which the model is calculated because photons at higher energies are 
Compton down-scattered into the target energy range. The energy range can 
be extended using the `energies` extend command. The upper 
limit on the energies should be set above that for which the input spectrum 
has significant flux. To speed up the model, calculation of the output 
spectrum can be limited to energies below a given value by using `xset` 
to define REFLECT_MAX_E (in units of keV). For instance, suppose that the 
original data extends up to 100 keV. To accurately determine the reflection 
it may be necessary to extend the energy range up to 500 keV. Now to avoid 
calculating the output spectrum between 100 and 500 keV use the command 
`xset` REFLECT_MAX_E 100.0.

The core of this model is a Greens' function integration with one numerical 
integral performed for each model energy. The numerical integration is 
done using an adaptive method which continues until a given estimated 
fractional precision is reached. The precision can be changed by setting 
REFLECT_PRECISION eg `xset` REFLECT_PRECISION 0.05. The default 
precision is 0.01 (ie 1%).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | rel_refl | — | 0 | -1 | 1000000 | -1 | 1000000 | 0.01 |  |
| 2 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 3 | abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 4 | Fe_abund | — | 1 | 0 | 1000000 | 0 | 1000000 | 0.01 | frozen by default |
| 5 | cosIncl | — | 0.45 | 0.05 | 0.95 | 0.05 | 0.95 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("reflect*powerlaw")
# component: m.reflect  (params as attributes)
```
