---
name: zigm
type: mul  # multiplicative
func: zigm
n_params: 3
family: [zigm]
energy_range: [0.0, 1.0e20]
source: manager/model.dat + XSmodelZigm.tex
---

# zigm

**multiplicative model** (`mul`), function `zigm`.

## Description

This multiplicative model computes the mean attenuation of the optical/UV 
spectrum of an object at redshift z at a random position on the sky due to 
intergalactic medium (IGM) clouds following either 
[Madau (1995)](https://ui.adsabs.harvard.edu/abs/1995ApJ...441...18M/abstract)
or [Meiksin (2006)](https://ui.adsabs.harvard.edu/abs/2006MNRAS.365..833M/abstract). 
The model calculates the mean expected attenuation due to resonant scattering 
by Lyman transitions and photoelectric absorption shortward of the Lyman limit. 
Attenuation by Helium and metals are not included in the Meiksin model, but 
are expected to be small. The total attenuation is set to zero for wavelengths 
less than 900 Angstroms. The user chooses whether to include attenuation due 
to photoelectric absorption.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | redshift | — | 0 |  |  |  |  |  | scale (not fitted) |
| 2 | model | — | 0 |  |  |  |  |  | switch (not fitted) |
| 3 | lyman_limit | — | 1 |  |  |  |  |  | switch (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("zigm*powerlaw")
# component: m.zigm  (params as attributes)
```
