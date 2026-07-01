---
name: nlapec
type: add  # additive
func: C_nlapec
n_params: 4
family: [nlapec]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelNlapec.tex
---

# nlapec

**additive model** (`add`), function `C_nlapec`.

## Description

A continuum-only emission spectrum from collisionally-ionized diffuse gas 
calculated using the ATOMDB code. More information can be found at 
http://atomdb.org/ which should be consulted by anyone running this 
model. This default version number can be changed by modifiying the 
ATOMDB_VERSION string in your Xspec.init file.

See the documentation on the `apec` model for a list of the
`xset` options which can be used to change the behaviour of the
apec code.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.001 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nlapec")
# component: m.nlapec  (params as attributes)
```
