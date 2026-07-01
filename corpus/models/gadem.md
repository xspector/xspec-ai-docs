---
name: gadem
type: add  # additive
func: C_gaussDem
n_params: 7
family: [gadem, vgadem, vvgadem, bgadem, bvgadem, bvvgadem]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelGadem.tex
---

# gadem

**additive model** (`add`), function `C_gaussDem`.

Variants documented together: `gadem`, `vgadem`, `vvgadem`, `bgadem`, `bvgadem`, `bvvgadem`.

## Description

A multi-temperature collisional-ionization equilibrium plasma emission model.
The emission measure distribution is a gaussian with mean
and sigma given by the first two model parameters. The switch
parameter determines the spectrum will be calculated by running the mekal code,
by interpolating on a pre-calculated mekal table, using the AtomDB
data, or the SPEX data. The final two options are now
preferred. See the `cie` model for further information and options.

For the `gadem` version, the abundance ratios are set by the
`abund` command. The `vgadem` variant allows the user to
define abundances for the more common elements. See the documentation
on the `cie` model for information on using additional
elements included in AtomDB and SPEX.

Velocity broadening can only be used with switch=2 or switch=3.

The parameters for `gadem` are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Tmean | keV | 4 | 0.01 | 10 | 0.01 | 20 | 0.01 | frozen by default |
| 2 | Tsigma | keV | 0.1 | 0.01 | 100 | 0.01 | 100 | 0.01 |  |
| 3 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 4 | abundanc | — | 1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 5 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 6 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 7 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("gadem")
# component: m.gadem  (params as attributes)
```
