---
name: raymond
type: add  # additive
func: C_raysmith
n_params: 4
family: [raymond, vraymond]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRaymond.tex
---

# raymond

**additive model** (`add`), function `C_raysmith`.

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
| 1 | kT | keV | 1 | 0.008 | 64 | 0.008 | 64 | 0.01 |  |
| 2 | Abundanc | — | 1 | 0 | 5 | 0 | 5 | 0.001 | frozen by default |
| 3 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("raymond")
# component: m.raymond  (params as attributes)
```
