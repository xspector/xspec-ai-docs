---
name: xion
type: mul  # multiplicative
func: xsxirf
n_params: 13
family: [xion]
energy_range: [0.1, 200.]
source: manager/model.dat + XSmodelXion.tex
---

# xion

**multiplicative model** (`mul`), function `xsxirf`.

## Description

This model describes the reflected spectra of a photo-ionized accretion disk 
or a ring if one so chooses. The approach is similar to the one used for 
tables with stellar spectra. Namely, a large number of models are computed 
for a range of values of the spectral index, the incident X-ray flux, disk 
gravity, the thermal disk flux and iron abundance. Each model's output is 
an un-smeared reflected spectrum for 5 different inclination angles ranging 
from nearly pole-on to nearly face on, stored in a look-up table. The 
default geometry is that of a lamppost, with free parameters of the model 
being the height of the X-ray source above the disk, $h_X$, the dimensionless 
accretion rate through the disk, $\dot{m}$, the luminosity of the X-ray source, 
$L_X$, the inner and outer disk radii, and the spectral index. This defines 
the gravity parameter, the ratio of X-ray to thermal fluxes, etc., for each 
radius, which allows the use of a look-up table to approximate the reflected 
spectrum. This procedure is repeated for about 30 different radii. The total 
disk spectrum is then obtained by integrating over the disk surface, 
including relativistic smearing of the spectrum for a non-rotating black 
hole (e.g., Fabian 1989). 

In addition, the geometry of a central sphere (with power-law optically thin 
emissivity inside it) plus an outer cold disk, and the geometry of magnetic 
flares are available (par13 = 2 and 3, respectively). One can also turn off 
relativistic smearing to see what the local disk spectrum looks like 
(par12 = 2 in this case; otherwise leave it at 4). In addition, par11 = 1 
produces reflected plus direct spectrum/direct; par11 =2 produces 
(incident + reflected)/incident [note that normalization of incident and 
direct are different because of solid angles covered by the disk; 2 should 
be used for magnetic flare model]; and par11 =3 produces reflected/incident. 
Abundance is controlled by par9 and varies between 1 and 4 at the present. 
A complete description of the model is presented in
[Nayakshin & Kallman (2001)](https://ui.adsabs.harvard.edu/abs/2001ApJ...546..406N/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | height | r_s | 5 | 0 | 100 | 0 | 100 | 2 |  |
| 2 | lxovrld | — | 0.3 | 0.02 | 100 | 0.02 | 100 | 0.02 |  |
| 3 | rate | — | 0.05 | 0.001 | 1 | 0.001 | 1 | 0.001 |  |
| 4 | cosAng | — | 0.9 | 0 | 1 | 0 | 1 | 0.01 |  |
| 5 | inner | r_s | 3 | 2 | 1000 | 2 | 1000 | 0.01 |  |
| 6 | outer | r_s | 100 | 2.1 | 100000 | 2.1 | 100000 | 0.1 |  |
| 7 | index | — | 2 | 1.6 | 2.2 | 1.6 | 2.2 | 0.01 |  |
| 8 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 9 | Feabun | — | 1 | 0 | 5 | 0 | 5 | 0.1 | frozen by default |
| 10 | E_cut | keV | 150 | 20 | 300 | 20 | 300 | 0.1 |  |
| 11 | Ref_type | — | 1 | 1 | 3 | 1 | 3 | 0.01 | frozen by default |
| 12 | Rel_smear | — | 4 | 1 | 4 | 1 | 4 | 0.01 | frozen by default |
| 13 | Geometry | — | 1 | 1 | 4 | 1 | 4 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("xion*powerlaw")
# component: m.xion  (params as attributes)
```
