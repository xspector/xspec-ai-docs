---
name: cempow
type: add  # additive
func: C_cempow
n_params: 7
family: [cempow, vcempow, bcempow, bvcempow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCempow.tex
---

# cempow

**additive model** (`add`), function `C_cempow`.

Variants documented together: `cempow`, `vcempow`, `bcempow`, `bvcempow`.

## Description

A multi-temperature plasma emission model. Emission measures follow a
power-law in temperature, $dEM = (T/T_{max})^{\alpha}\,d\log_{10}(T)$,
summed over a grid uniform in $\log_{10}(T)$ with a step of 0.1. Written
in terms of $dT$ this is $dEM =
(T/T_{max})^{\alpha-1}dT/(T_{max}\ln 10)$; note the factor of $\ln 10$,
which arises because the model integrates over $\log_{10}(T)$ rather than
over $T$. The switch parameter
determines whether the spectrum is calculated by running the mekal code,
by interpolating on a pre-calculated mekal table, using the AtomDB
data, or the SPEX data. The final two options are now
preferred. See the `cie` model for further information and options.

For the `cempow` and `bcempow` versions, the abundance ratios are set by the
`abund` command. The `vcempow` and `bvcempow` variants allow the user to
define the abundances. The reference for this model is
[Singh et al. (1996, ApJ, 456,
  766)](https://ui.adsabs.harvard.edu/abs/1996ApJ...456..766S/abstract).

Velocity broadening can only be used with switch=2 or switch=3.

For `cempow` the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | alpha | — | 1 | 0.01 | 10 | 0.01 | 20 | 0.01 | frozen by default |
| 2 | Tmax | keV | 1 | 0.02725 | 100 | 0.02725 | 100 | 0.01 |  |
| 3 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 4 | abundanc | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("cempow")
# component: m.cempow  (params as attributes)
```
