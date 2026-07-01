---
name: vvwdem
type: add  # additive
func: C_vvwDem
n_params: 37
family: [wdem, vwdem, vvwdem, bwdem, bvwdem, bvvwdem]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelWdem.tex
---

# vvwdem

**additive model** (`add`), function `C_vvwDem`.

Variants documented together: `wdem`, `vwdem`, `vvwdem`, `bwdem`, `bvwdem`, `bvvwdem`.

## Description

A multi-temperature collisional-ionization equilibrium plasma emission model.
The emission measure distribution is a
powerlaw:

$$\frac{dY}{dT} = \left\{
\begin{array}{ll}
0            & {\rm if\quad} T \leq \beta T_{max} \\
c T^{\alpha} & {\rm if\quad} \beta T_{max} < T < T_{max} \\
0            & {\rm if\quad} T_{max} \leq < T \\
\end{array}
\right\}$$

where $Y$ is the emission measure and $c$ is chosen so that the total
emission measure equals the normalization parameter
([Kaastra et al. 2004](https://ui.adsabs.harvard.edu/abs/2004A%26A...413..415K/abstract)).

The switch parameter determines whether the spectrum is
calculated by running the mekal code, by interpolating on a
pre-calculated mekal table, using the AtomDB data, or the SPEX
data. The final two options are now preferred. See the `cie`
model for further information and options.

For the `wdem` version, the abundance ratios are set by the
`abund` command. The `vwdem` variant allows the user to
define abundances for the more common elements while `vvwdem` has 
parameters for abundances of all elements up to Zn. See the documentation
on the `apec` model for further information.
 
Velocity broadening can only be used with switch=2 or switch=3.

The parameters for `wdem` are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Tmax | keV | 1 | 0.01 | 10 | 0.01 | 20 | 0.01 |  |
| 2 | beta | — | 0.1 | 0.01 | 1 | 0.01 | 1 | 0.01 |  |
| 3 | inv_slope | — | 0.25 | -1 | 10 | -1 | 10 | 0.01 |  |
| 4 | nH | cm^-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 5 | H | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Li | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Be | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | B | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | F | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 18 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 19 | P | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 20 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 21 | Cl | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 22 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 23 | K | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 24 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 25 | Sc | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 26 | Ti | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 27 | V | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 28 | Cr | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 29 | Mn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 30 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 31 | Co | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 32 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 33 | Cu | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 34 | Zn | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 35 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 36 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 37 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vvwdem")
# component: m.vvwdem  (params as attributes)
```
