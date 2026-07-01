---
name: smaug
type: add  # additive
func: c_xsmaug
n_params: 23
family: [smaug]
energy_range: [0.0E+00, 1.0E+20]
source: manager/model.dat + XSmodelSmaug.tex
---

# smaug

**additive model** (`add`), function `c_xsmaug`.

## Description

This model performs an analytical deprojection of an extended,
optically-thin and spherically-symmetric source. A thorough
description of the model is given in [Pizzolato et al. (2003)](https://ui.adsabs.harvard.edu/abs/2003ApJ...592...62P/abstract). In this model the 3D distributions of hydrogen, metals and
temperature throughout the source are given specific functional forms
dependent on a number of parameters, whose values are determined by
the fitting procedure. The user has to extract the spectra in annular
sectors, concentric about the emission peak. The inner boundary (in
arcmin), the outer by the fitting procedure. The user has to extract
the spectra in annular sectors, concentric about the emission
peak. Three additional XFLTnnnn keywords must be added (e.g. with the
ftools fkeypar). These should take the values ``inner: x'', ``outer: y'',
``width: z'' where x, y, z are the inner boundary (in arcmin), the outer
boundary (also in arcmin), and the width (in degrees), respectively,
of each annular sector. Some parameters of `smaug` define the redshift
and other options (see below). The other, ``relevant'' ones define the
3D distributions of hydrogen density, temperature and metal abundance,
determined by a simultaneous fit of the spectra. The cosmological
parameters can be set using the `cosmo` command.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT.cc | keV | 1 | 0.1 | 10 | 0.08 | 100 | 0.01 |  |
| 2 | kT.dt | keV | 1 | 0 | 10 | 0 | 100 | 0.01 |  |
| 3 | kT.ix | — | 0 | 0 | 10 | 0 | 10 | 0.001 | frozen by default |
| 4 | kT.ir | Mpc | 0.1 | 0.0001 | 1 | 0.0001 | 1 | 0.001 | frozen by default |
| 5 | kT.cx | — | 0.5 | 0 | 10 | 0 | 10 | 0.001 |  |
| 6 | kT.cr | Mpc | 0.1 | 0.0001 | 10 | 0.0001 | 20 | 0.01 |  |
| 7 | kT.tx | — | 0 | 0 | 10 | 0 | 10 | 0.001 | frozen by default |
| 8 | kT.tr | Mpc | 0.5 | 0.0001 | 1 | 0.0001 | 3 | 0.01 | frozen by default |
| 9 | nH.cc | cm**-3 | 1 | 1e-06 | 3 | 1e-06 | 3 | 0.01 | frozen by default |
| 10 | nH.ff | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 11 | nH.cx | — | 0.5 | 0 | 10 | 0 | 10 | 0.001 |  |
| 12 | nH.cr | Mpc | 0.1 | 0.0001 | 1 | 0.0001 | 2 | 0.01 |  |
| 13 | nH.gx | — | 0 | 0 | 10 | 0 | 10 | 0.001 | frozen by default |
| 14 | nH.gr | Mpc | 0.002 | 0.0001 | 10 | 0.0001 | 20 | 0.001 | frozen by default |
| 15 | Ab.cc | solar | 1 | 0 | 3 | 0 | 5 | 0.01 | frozen by default |
| 16 | Ab.xx | — | 0 | 0 | 10 | 0 | 10 | 0.001 | frozen by default |
| 17 | Ab.rr | Mpc | 0.1 | 0.0001 | 1 | 0.0001 | 1 | 0.01 | frozen by default |
| 18 | redshift | — | 0.01 | 0.0001 | 10 | 0.0001 | 10 | 1 | frozen by default |
| 19 | meshpts | — | 10 | 1 | 10000 | 1 | 10000 | 1 | frozen by default |
| 20 | rcutoff | Mpc | 2 | 1 | 3 | 1 | 3 | 0.01 | frozen by default |
| 21 | mode | — | 1 | 0 | 2 | 0 | 2 | 1 | frozen by default |
| 22 | itype | — | 2 | 1 | 4 | 1 | 4 | 1 | frozen by default |
| 23 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("smaug")
# component: m.smaug  (params as attributes)
```
