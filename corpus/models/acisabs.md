---
name: acisabs
type: mul  # multiplicative
func: C_acisabs
n_params: 8
family: [acisabs]
energy_range: [0.03, 15]
source: manager/model.dat + XSmodelAcisabs.tex
---

# acisabs

**multiplicative model** (`mul`), function `C_acisabs`.

## Description

This model accounts for the decay in the ACIS quantum efficiency most likely 
caused by molecular contamination of the ACIS filters. The user needs to 
supply the number of days between Chandra launch and observation. The `acisabs` 
parameters related to the composition of the hydrocarbon  and the rate of decay 
should be frozen and not modified. The present version of `acisabs` 
is to be used for the analysis of bare ACIS I and ACIS S data. For the 
present version of `acisabs` one must use the standard qe file 
vN0003 instead of the optional vN0004 file.

Because of the present large uncertainty in the ACIS gain at energies 
below 350eV we recommend that events in the 0-350eV range be ignored in the 
spectral analysis until the gain issue is resolved. 

`acisabs` calculates the mass absorption coefficients of the 
contaminant from atomic scattering factor files provided at

[http://henke.lbl.gov/optical_constants/asf.html](http://henke.lbl.gov/optical_constants/asf.html)

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Tdays | days | 850 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 2 | norm | — | 0.00722 | 0 | 1 | 0 | 1 | 1e-05 | frozen by default |
| 3 | tauinf | — | 0.582 | 0 | 1 | 0 | 1 | 0.1 | frozen by default |
| 4 | tefold | days | 620 | 1 | 10000 | 1 | 10000 | 1 | frozen by default |
| 5 | nC | — | 10 | 0 | 50 | 0 | 50 | 1 | frozen by default |
| 6 | nH | — | 20 | 1 | 50 | 1 | 50 | 1 | frozen by default |
| 7 | nO | — | 2 | 0 | 50 | 0 | 50 | 1 | frozen by default |
| 8 | nN | — | 1 | 0 | 50 | 0 | 50 | 1 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("acisabs*powerlaw")
# component: m.acisabs  (params as attributes)
```
