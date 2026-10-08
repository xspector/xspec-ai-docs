---
name: ascac
type: mix  # mixing
func: U_Cluster
n_params: 4
family: [ascac]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelAscac.tex
---

# ascac

**mixing model** (`mix`), function `U_Cluster`.

## Description

Mixing model for ASCA data. Written for cluster data so uses beta or two 
power-law surface brightness models. Includes a calculation of the telescope 
effective area so no arf should be applied to input files. Note that this 
model is very slow if any of the parameters are free. 

The model is used by reading spectra in as separate datagroups. Each input 
file requires an XFLTnnnn keyword set to ``region: N'' where N is a different 
number for each file (eg if concentric annuli are in use then number outwards). 
The normalizations for each datagroup should be linked since the `ascac` 
model takes care of the relative normalizations based on the surface 
brightness model used. A maximum of five different spatial regions is allowed. 
The absolute normalization is not reliable so this model should not be used 
to derive fluxes.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Alpha | — | 2 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 2 | Beta | — | 0.66 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 3 | Core | arcmin | 1 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 4 | Switch | — | 0 |  |  |  |  |  | switch (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("ascac")
# component: m.ascac  (params as attributes)
```
