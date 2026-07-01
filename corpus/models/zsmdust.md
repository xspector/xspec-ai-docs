---
name: zsmdust
type: mul  # multiplicative
func: msldst
n_params: 4
family: [zsmdust]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelZsmdust.tex
---

# zsmdust

**multiplicative model** (`mul`), function `msldst`.

## Description

Extinction by dust grains suited to starburst galaxies and the hosts of 
gamma ray bursts. The model can be applied over the IR, optical and UV 
energy bands, including the full energy ranges of the Swift UVOT and 
XMM-Newton OM detectors. The transmission is set to unity shortward of 
912 Angstroms in the rest frame of the dust. This is incorrect physically 
but does allow the model to be used in combination with an X-ray photoelectric 
absorption model such as `phabs`. The extinction curve contains no 
spectral features and is characterized by a powerlaw slope over spectral 
wavelength. This model has been justified by e.g. [Savaglio & Fall (2004)](https://ui.adsabs.harvard.edu/abs/2004ApJ...614..293S/abstract) because the apparent low metallicities within GRB hosts result in 
no significant spectral features within the extinction curve, unlike those 
found in local galaxies. The extinction at V, A(V) = E(B-V) x Rv. Standard 
values for Rv are Milky Way = 3.08, LMC = 3.16 and SMC = 2.93 (from table 
2 of [Pei (1992)](https://ui.adsabs.harvard.edu/abs/1992ApJ...395..130P/abstract), although these may not be applicable to 
more distant dusty sources.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | E_BmV | — | 0.1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 2 | ExtIndex | — | 1 | -10 | 10 | -10 | 10 | 0.01 |  |
| 3 | Rv | — | 3.1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 4 | redshift | z | 0 | 0 | 20 | 0 | 20 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zsmdust*powerlaw")
# component: m.zsmdust  (params as attributes)
```
