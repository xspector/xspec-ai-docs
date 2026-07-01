---
name: bvcoolflow
type: add  # additive
func: C_bvcoolflow
n_params: 20
family: [coolflow, vcoolflow, bcoolflow, bvcoolflow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCoolflow.tex
---

# bvcoolflow

**additive model** (`add`), function `C_bvcoolflow`.

Variants documented together: `coolflow`, `vcoolflow`, `bcoolflow`, `bvcoolflow`.

## Description

A cooling flow model after [Mushotzky & Szymkowiak (1988)](https://ui.adsabs.harvard.edu/abs/1988ASIC..229...53M/abstract). This one differs from
`cflow` in setting the emissivity function to be the inverse
of the bolometric luminosity. Abundance ratios are set by the
`abund` command. Redshift is converted to distance using the
cosmology set by the `cosmo` command. The switch
parameter determines whether spectrum is calculated by running the
mekal code, by interpolating on a pre-calculated mekal table, using
the AtomDB data, or using the SPEX data. If the last two of these options are selected then see
the documentation on the `cie` model for a list of the
`xset` options which can be used to change the behaviour of the code.

Velocity broadening can only be used with switch=2 or switch=3.

For the `coolflow` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | lowT | keV | 0.1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.001 |  |
| 2 | highT | keV | 4 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.001 |  |
| 3 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | Redshift | — | 0.1 | 0 | 10 | 0 | 10 | 0.01 | frozen by default |
| 18 | Velocity | km/s | 0 | 0 | 10000 | 0 | 10000 | 10 | frozen by default |
| 19 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 20 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bvcoolflow")
# component: m.bvcoolflow  (params as attributes)
```
