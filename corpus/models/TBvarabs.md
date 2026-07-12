---
name: TBvarabs
type: mul  # multiplicative
func: C_tbvabs
n_params: 42
family: [tbabs, ztbabs, tbfeo, tbgas, tbgrain, tbpcf, tbvarabs, tbrel]
energy_range: [0.03, 1.e20]
source: manager/model.dat + XSmodelTbabs.tex
---

# TBvarabs

**multiplicative model** (`mul`), function `C_tbvabs`.

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

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | He | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 3 | C | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 4 | N | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 5 | O | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 6 | Ne | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 7 | Na | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 8 | Mg | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 9 | Al | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 10 | Si | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 11 | S | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 12 | Cl | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 13 | Ar | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 14 | Ca | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 15 | Cr | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 16 | Fe | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 17 | Co | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 18 | Ni | — | 1 | 0 | 5 | 0 | 1e+38 | 0.01 | frozen by default |
| 19 | H2 | — | 0.2 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 20 | rho | g/cm^3 | 1 | 0 | 5 | 0 | 5 | 0.01 | frozen by default |
| 21 | amin | mum | 0.025 | 0 | 0.25 | 0 | 0.25 | 0.01 | frozen by default |
| 22 | amax | mum | 0.25 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 23 | PL | — | 3.5 | 0 | 5 | 0 | 5 | 0.01 | frozen by default |
| 24 | H_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 25 | He_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 26 | C_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 27 | N_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 28 | O_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 29 | Ne_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 30 | Na_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 31 | Mg_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 32 | Al_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 33 | Si_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 34 | S_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 35 | Cl_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 36 | Ar_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 37 | Ca_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 38 | Cr_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 39 | Fe_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 40 | Co_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 41 | Ni_dep | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 42 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("TBvarabs*powerlaw")
# component: m.tbvarabs  (params as attributes)
```
