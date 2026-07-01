---
name: vvgadem
type: add  # additive
func: C_vvgaussDem
n_params: 36
family: [gadem, vgadem, vvgadem, bgadem, bvgadem, bvvgadem]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelGadem.tex
---

# vvgadem

**additive model** (`add`), function `C_vvgaussDem`.

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
| 4 | H | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | Li | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Be | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | B | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | F | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 18 | P | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 19 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 20 | Cl | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 21 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 22 | K | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 23 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 24 | Sc | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 25 | Ti | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 26 | V | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 27 | Cr | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 28 | Mn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 29 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 30 | Co | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 31 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 32 | Cu | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 33 | Zn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 34 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 35 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 36 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vvgadem")
# component: m.vvgadem  (params as attributes)
```
