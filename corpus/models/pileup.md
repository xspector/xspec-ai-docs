---
name: pileup
type: acn  # pile-up/acn
func: C_pileup
n_params: 7
family: [pileup]
energy_range: [0.001, 1.0e20]
source: manager/model.dat + XSmodelPileup.tex
---

# pileup

**pile-up/acn model** (`acn`), function `C_pileup`.

## Description

CCD pile-up model used for brightish point sources observed by Chandra. This 
is an implementation of the fast pile-up algorithm proposed by John Davis 
(see http://space.mit.edu/ davis/papers/pileup2001.pdf). The frame time 
and maximum number of photons to pile up should be fixed. The grade morphing 
is expressed through a single parameter, alpha, which should be left as a free 
parameter. This model should be considered in beta test. Note that to 
calculate fluxes etc. for the model you must remove the `pileup` 
component. The pile-up model is similar to the operation of the convolution 
models, differing only in the treatment of the detector efficiency during the 
convolution.  Note that `renorm` will not work with `pileup` 
since increasing the normalization does not linearly increase the predicted 
count rate.  Therefore you should set `renorm none` prior to doing a 
fit with `pileup`.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | fr_time | s | 3.2 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 2 | max_ph | — | 5 | 1 | 20 | 1 | 20 | 0.01 | frozen by default |
| 3 | g0 | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 4 | alpha | — | 1 | 0 | 1 | 0 | 1 | 0.01 |  |
| 5 | psffrac | — | 0.95 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 6 | nregions | — | 1 |  |  |  |  |  | scale (not fitted) |
| 7 | fracexpo | — | 1 |  |  |  |  |  | scale (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("pileup")
# component: m.pileup  (params as attributes)
```
