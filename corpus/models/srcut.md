---
name: srcut
type: add  # additive
func: srcut
n_params: 3
family: [srcut]
energy_range: [1.e-20, 1.e+20]
source: manager/model.dat + XSmodelSrcut.tex
---

# srcut

**additive model** (`add`), function `srcut`.

## Description

`srcut` describes the synchrotron spectrum from an exponentially cut off
power-law distribution of electrons in a homogeneous magnetic
field. This spectrum is itself a power-law, rolling off more slowly
than exponential in photon energies. Though more realistic than a
power-law, it is highly oversimplified, but does give the maximally
curved physically plausible spectrum and can be used to set limits on
maximum accelerated-electron energies even in remnants whose X-rays
are thermal. See [Reynolds & Keohane
  (1999)](https://ui.adsabs.harvard.edu/abs/1999ApJ...525..368R/abstract) and [Reynolds (1998)](https://ui.adsabs.harvard.edu/abs/1998ApJ...493..375R/abstract). Note that the radio spectral
index and flux can be obtained from [Green's Catalogue for galactic SNRs](http://www.mrao.cam.ac.uk/surveys/snrs).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | alpha | — | 0.5 | 0.3 | 0.8 | 1e-05 | 1 | 0.05 |  |
| 2 | break | Hz | 2.42e+17 | 1000000000000000.0 | 1e+19 | 10000000000 | 1e+25 | 10000000000 |  |
| 3 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("srcut")
# component: m.srcut  (params as attributes)
```
