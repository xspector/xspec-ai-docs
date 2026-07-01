---
name: vraymond
type: add  # additive
func: C_vraysmith
n_params: 15
family: [raymond, vraymond]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRaymond.tex
---

# vraymond

**additive model** (`add`), function `C_vraysmith`.

Variants documented together: `raymond`, `vraymond`.

## Description

An emission spectrum from hot, diffuse gas based on the model
calculations of [Raymond & Smith
  (1977)](https://ui.adsabs.harvard.edu/abs/1977ApJS...35..419R/abstract) including
line emissions from several elements. This model interpolates on a
grid of spectra for different temperatures. The grid is
logarithmically spaced with 80 temperatures ranging from 0.008 to 80
keV.

The `vraymond` variant allows independent parameters to set
the abundances. Abundances are the number of nuclei per Hydrogen
nucleus relative to the Solar abundances as set by the `abund` command.

For the `raymond` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 6.5 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | He | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 3 | C | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 4 | N | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 5 | O | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 6 | Ne | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 7 | Mg | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 8 | Si | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 9 | S | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 10 | Ar | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 11 | Ca | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 12 | Fe | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 13 | Ni | — | 1 | 0 | 1000 | 0 | 10000 | 0.01 | frozen by default |
| 14 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 15 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vraymond")
# component: m.vraymond  (params as attributes)
```
