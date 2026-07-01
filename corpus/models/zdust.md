---
name: zdust
type: mul  # multiplicative
func: mszdst
n_params: 4
family: [zdust]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelZdust.tex
---

# zdust

**multiplicative model** (`mul`), function `mszdst`.

## Description

Extinction by dust grains from [Pei (1992)](https://ui.adsabs.harvard.edu/abs/1992ApJ...395..130P/abstract), suitable for IR, 
optical and UV energy bands, including the full energy ranges of the Swift 
UVOT and XMM-Newton OM detectors. Three models are included which 
characterize the extinction curves of (1) the Milky Way, (2) the LMC and 
(3) the SMC. The models can be modified by redshift and can therefore be 
applied to extragalactic sources. The transmission is set to unity shortward 
of 912 Angstroms in the rest frame of the dust. This is incorrect physically 
but does allow the model to be used in combination with an X-ray photoelectric 
absorption model such as `phabs`. Parameter 1 (method) describes 
which extinction curve (MW, LMC or SMC) will be constructed and should 
never be allowed to float during a fit. The extinction at V, A(V) = 
E(B-V) x Rv. Rv should typically remain frozen for a fit. Standard values 
for Rv are MW = 3.08, LMC = 3.16 and SMC = 2.93 (from table 2 of [Pei 1992](https://ui.adsabs.harvard.edu/abs/1992ApJ...395..130P/abstract)), 
although these may not be applicable to more distant dusty sources.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | method | — | 1 |  |  |  |  |  | switch (not fitted) |
| 2 | E_BmV | — | 0.1 | 0 | 100 | 0 | 100 | 0.01 |  |
| 3 | Rv | — | 3.1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 4 | Redshift | — | 0 | 0 | 20 | 0 | 20 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("zdust*powerlaw")
# component: m.zdust  (params as attributes)
```
