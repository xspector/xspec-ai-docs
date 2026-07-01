---
name: slimbh
type: add  # additive
func: c_slimbbmodel
n_params: 10
family: [slimbh]
energy_range: [1.0e3, 1.0e5]
source: manager/model.dat + XSmodelSlimbh.tex
---

# slimbh

**additive model** (`add`), function `c_slimbbmodel`.

## Description

This is a relativistic model for X-ray continuum of stationary slim
accretion disks around stallar mass black holes. This model is based
on disk radial structure solutions presented in
[Sadowski et al. (2011)](https://ui.adsabs.harvard.edu/abs/2011arXiv1108.0396S/abstract) combined with
vertical structure computed using
[TLUSTY](http://nova.astro.umd.edu/index.html) code
to make the best model for X-ray continuum for a wide range of
luminosities up to Eddington limit. See also
[Straub et al. (2011)](https://ui.adsabs.harvard.edu/abs/2011A&A...533A..67S/abstract).

Using the `xset` command to set SLIMBB_DEBUG to 1 will cause
debug information to be written to a log file. The table file used by
this model can be replaced by setting SLIMBB_DIR and SLIMBB_TABLE to
the directory and name of the file, respectively.

The parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | M | Msun | 10 | 0 | 1000 | 0 | 1000 | 1 | frozen by default |
| 2 | a | GM/c | 0 | 0 | 0.999 | 0 | 0.999 | 0.01 |  |
| 3 | lumin | L_Edd | 0.5 | 0.05 | 1 | 0.05 | 1 | 0.05 |  |
| 4 | alpha | — | 0.1 | 0.005 | 0.1 | 0.005 | 0.1 | 1 | frozen by default |
| 5 | inc | deg | 60 | 0 | 85 | 0 | 85 | 1 | frozen by default |
| 6 | D | kpc | 10 | 0 | 10000 | 0 | 10000 | 1 | frozen by default |
| 7 | f_hard | — | -1 | -10 | 10 | -10 | 10 | 1 | frozen by default |
| 8 | lflag | — | 1 |  |  |  |  |  | switch (not fitted) |
| 9 | vflag | — | 1 |  |  |  |  |  | switch (not fitted) |
| 10 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("slimbh")
# component: m.slimbh  (params as attributes)
```
