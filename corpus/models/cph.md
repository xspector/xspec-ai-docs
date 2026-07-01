---
name: cph
type: add  # additive
func: C_cph
n_params: 5
family: [cph, vcph, bcph, bvcph]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCph.tex
---

# cph

**additive model** (`add`), function `C_cph`.

Variants documented together: `cph`, `vcph`, `bcph`, `bvcph`.

## Description

This cph (Cooling+Heating) model is a modification of `coolflow` to
include heating as described in [Zhoolideh
    Haghighi, Afshordi & Khoshroshahi
    (2018)](https://arxiv.org/abs/1806.08822). The peak temperature
parameter is the peak of the emission measure distribution and occurs
where the cooling and heating timescales are equal.

The `coolflow` model had parameters for low and high temperature but
these are not necessary for the cph model since the emission measure
does not diverge at low temperatures. The model integrates the
emission measure distribution from 0.01 to 50 keV.

Velocity broadening can only be used with switch=2 or switch=3. See the
`cie` model for further information and options.

For cph the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | peakT | keV | 2.2 | 0.1 | 100 | 0.1 | 100 | 0.001 |  |
| 2 | Abund | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 3 | Redshift | — | 0.1 | 0 | 50 | 0 | 50 | 0.01 | frozen by default |
| 4 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 5 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cph")
# component: m.cph  (params as attributes)
```
