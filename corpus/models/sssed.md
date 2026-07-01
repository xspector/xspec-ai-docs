---
name: sssed
type: add  # additive
func: sssed
n_params: 15
family: [SSsed]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelSssed.tex
---

# sssed

**additive model** (`add`), function `sssed`.

## Description

The SSsed model was developed by Kubota et al. (2024 MNRAS 528, 1668)
to describe spectral energy distribution (SED) of black hole binaries
(BHBs). This model is a revised version of the agnsed model (Kubota &
Done 2018, MNRAS, 489, 524), but it was tuned to BHBs, and especially
to their intermediate spectra where there are clearly two Compton
components as well as (truncated) disc. The key concept is that the
flow is radially stratified such that the accretion power is emitted
as (colour-corrected) black body radiation at $r > r_{cor}$, while it is emitted as
inverse-Comptonization by both the thermal and non-thermal corona at
$r < r_{cor}$.
The seed photons are assumed to be emitted from the underlying passive
disc at $r < r_{cor}$. All the emission is constrained by the standard disc
emissivity by Shakura & Sunyaev (1973), with $Mdot$
constant with radius. If the components of the outer disc are visible,
both parameters $r_{cor}$ and $r_{in}$ are determined independently. In cases where the
outer disc is not visible, such as in the bright hard state, caution
is needed in interpreting the obtained value of $r_{cor}$.

The parameters of the SSsed model are summarised below. Note that the
model has some switching parameters controlling the following behaviors:

- If parameter 6 is negative, the model gives the hot Comptonisation component at $r < r_{cor}$.

- If parameter 7 is negative, the model gives the non-thermal Comptonisation component at $r < r_{cor}$.

- If parameter 9 is negative, the model gives the outer disc.

- If parameter 12 is -1, the code will use the self-gravity radius
  as calculate from Laor & Netzer (1989, MNRAS, 238, 897).

- Colour correction is included when parameter 14 is
  set to 1, while it is not included when this
  parameter is set to 0. For BHB spectra, this
  parameter should be fixed at 1.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | mass | solar | 10 | 1 | 10000000000 | 1 | 10000000000 | 0.1 | frozen by default |
| 2 | dist | kpc | 10 | 0.1 | 1000000000 | 0.1 | 1000000000 | 0.1 | frozen by default |
| 3 | logmdot | real | 0.1 | -3 | 3 | -3 | 3 | 0.001 |  |
| 4 | Rin | Rg | 6 | 1 | 500 | 1 | 500 | 0.01 |  |
| 5 | cosi | — | 0.5 | 0 | 0.95 | 0 | 0.95 | 0.1 | frozen by default |
| 6 | kTe_th | keV(-th) | 10 | 4 | 300 | 4 | 300 | 0.001 |  |
| 7 | kTe_nt | keV(-nt) | 300 | 10 | 300 | 10 | 300 | 0.001 | frozen by default |
| 8 | Gamma_th | — | 1.7 | 1.4 | 4 | 1.4 | 4 | 0.001 |  |
| 9 | Gamma_nt | (-disk) | 2.2 | 1.9 | 4 | 1.9 | 4 | 0.001 |  |
| 10 | frac_th | — | 0.2 | 0 | 1 | 0 | 1 | 0.001 |  |
| 11 | Rcor | Rg | 10 | 1 | 5000 | 1 | 5000 | 0.01 |  |
| 12 | logrout | (-selfg) | -1 | -1 | 7 | -1 | 7 | 0.1 | frozen by default |
| 13 | redshift | — | 0 | 0 | 1 | 0 | 1 | 1 | frozen by default |
| 14 | color_cor | 0off/1on | 1 | 0 | 1 | 0 | 1 | 1 | frozen by default |
| 15 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("sssed")
# component: m.sssed  (params as attributes)
```
