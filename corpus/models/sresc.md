---
name: sresc
type: add  # additive
func: sresc
n_params: 3
family: [sresc]
energy_range: [1.e-20, 1.e+20]
source: manager/model.dat + XSmodelSresc.tex
---

# sresc

**additive model** (`add`), function `sresc`.

## Description

The synchrotron spectrum from an electron distribution limited by
particle escape above some energy. The electrons are shock-accelerated
in a Sedov blast wave encountering a constant-density medium
containing a uniform magnetic field. The model includes variations in
electron acceleration efficiency with shock obliquity, and post-shock
radiative and adiabatic losses, as described in [Reynolds (1998)](https://ui.adsabs.harvard.edu/abs/1998ApJ...493..375R/abstract). This is a highly specific, detailed model for a fairly
narrow set of conditions. See also [Reynolds
  (1996)](https://ui.adsabs.harvard.edu/abs/1996ApJ...459L..13R/abstract). Note
that the radio spectral index and flux can be obtained from [
Green's Catalogue for galactic SNRS](http://www.mrao.cam.ac.uk/surveys/snrs).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | alpha | — | 0.5 | 0.3 | 0.8 | 1e-05 | 1 | 0.05 |  |
| 2 | rolloff | Hz | 2.42e+17 | 1000000000000000.0 | 1e+19 | 10000000000 | 1e+25 | 10000000000 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("sresc")
# component: m.sresc  (params as attributes)
```
