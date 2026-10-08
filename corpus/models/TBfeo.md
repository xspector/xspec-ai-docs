---
name: TBfeo
type: mul  # multiplicative
func: C_tbfeo
n_params: 4
family: [tbabs, ztbabs, tbfeo, tbgas, tbgrain, tbpcf, tbvarabs, tbrel]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelTbabs.tex
---

# TBfeo

**multiplicative model** (`mul`), function `C_tbfeo`.

Variants documented together: `tbabs`, `ztbabs`, `tbfeo`, `tbgas`, `tbgrain`, `tbpcf`, `tbvarabs`, `tbrel`.

## Description

The Tuebingen-Boulder ISM absorption model. This model calculates the cross 
section for X-ray absorption by the ISM as the sum of the cross sections 
for X-ray absorption due to the gas-phase ISM, the grain-phase ISM, and 
the molecules in the ISM. In the grain-phase ISM, the effect of shielding 
by the grains is accounted for, but is extremely small. In the molecular 
contribution to the ISM cross section, only molecular hydrogen is 
considered. In the gas-phase ISM, the cross section is the sum of the 
photoionization cross sections of the different elements, weighted by 
abundance and taking into account depletion onto grains.

In addition to the updates to the photoionization cross sections, the 
gas-phase cross section differs from previous values as a result of updates 
to the ISM abundances.  These updated abundances are available through the 
`abund` `wilm` command. Details of updates to the 
photoionization cross sections as well as to abundances can be found in 
[Wilms, Allen & McCray (2000)](https://ui.adsabs.harvard.edu/abs/2000ApJ...542..914W/abstract).

Two versions of this model are available depending on the setting of
TBABSVERSION. The newer version (the default) dates from 2016 and
includes high resolution edge structures for the K-edges of oxygen and
neon and the L-edges of iron. The newer version is 25 times faster than
the older version or the phabs model. To recover the older version use
xset TBABSVERSION 1.

The parameters which reference abundances relative to Solar are using the Solar 
abundances as set by the `abund` command.

`tbabs` allows the user to vary just the hydrogen column.
`tbred` and `ztbred` add the optical/UV
reddening of the same column.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | O | — | 1 | 0 | 5 | -1e+38 | 1e+38 | 0.01 | frozen by default |
| 3 | Fe | — | 1 | 0 | 5 | -1e+38 | 1e+38 | 0.01 | frozen by default |
| 4 | redshift | — | 0 | 0 | 10 | -1 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("TBfeo*powerlaw")
# component: m.tbfeo  (params as attributes)
```
