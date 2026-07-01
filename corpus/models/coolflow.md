---
name: coolflow
type: add  # additive
func: C_coolflow
n_params: 6
family: [coolflow, vcoolflow, bcoolflow, bvcoolflow]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCoolflow.tex
---

# coolflow

**additive model** (`add`), function `C_coolflow`.

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
| 3 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.01 |  |
| 4 | Redshift | — | 0.1 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | switch | — | 2 |  |  |  |  |  | switch (not fitted) |
| 6 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("coolflow")
# component: m.coolflow  (params as attributes)
```
