---
name: rfxconv
type: con  # convolution
func: C_rfxconv
n_params: 5
family: [rfxconv]
energy_range: [0.001, 1.0e20]
source: manager/model.dat + XSmodelRfxconv.tex
---

# rfxconv

**convolution model** (`con`), function `C_rfxconv`.

## Description

This convolution model from Chris Done combines the ionized disk table
model from Ross and Fabian with the Magdziarz & Zdziarski Compton
reflection code. It is described in [Kolehmainen, Done & Diaz Trigo
(2011)](https://ui.adsabs.harvard.edu/abs/2011MNRAS.416..311K/abstract) and is a modification of the model first described in [Done &
Gierlinski (2006)](https://ui.adsabs.harvard.edu/abs/2006MNRAS.367..659D/abstract).

The algorithm used is as follows.

- Determine the average power-law index of the input spectrum
  between 2 and 10 keV. For this index and the other input parameters
  interpolate on the table models to generate the reflected spectrum
  from the ionized disk.

- Estimate the average power-law index of the reflected spectrum
  over the range 12 - 14 keV.

- Iterate over the Compton reflection models changing the
  cross-section at 10 keV until a match is found with the index
  calculated in the previous step.

- Renormalize the reflection spectrum calculated in step 1 to
  match the Compton reflection calculated in step 3 at 14 keV.

- Calculate the final reflection spectrum by using the
  renormalized ionized disk spectrum below 14 keV and the Compton
  reflection spectrum above 14 keV.

When using this model it is essential to extend the energy range over
which the model is calculated because photons at higher energies are
Compton down-scattered into the target energy range. The energy range
can be extended using the extend command. The upper limit on the
energies should be set above that for which the input spectrum has
significant flux. To speed up the model, calculation of the output
spectrum can be limited to energies below a given value by using xset
to define RFXCONV_MAX_E (in units of keV). For instance, suppose that
the original data extends up to 100 keV. To accurately determine the
reflection it may be necessary to extend the energy range up to 500
keV. Now to avoid calculating the output spectrum between 100 and 500
keV use the command xset RFXCONV_MAX_E 100.0.

The core of this model is a Greens' function integration with one
numerical integral performed for each model energy. The numerical
integration is done using an adaptive method which continues until 
a given estimated fractional precision is reached. The precision can 
be changed by setting RFXCONV_PRECISION eg xset RFXCONV_PRECISION 0.05. 
The default precision is 0.01 (ie 1%).

To use different ionized disk table model files than those installed
change the directory searched for these files using xset RFXCONV_DIR.

The model parameters are as follows.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | rel_refl | — | -1 | -1 | 1000000 | -1 | 1000000 | 0.01 |  |
| 2 | redshift | — | 0 | 0 | 4 | 0 | 4 | 0.01 | frozen by default |
| 3 | Fe_abund | — | 1 | 0.5 | 3 | 0.5 | 3 | 0.01 | frozen by default |
| 4 | cosIncl | — | 0.5 | 0.05 | 0.95 | 0.05 | 0.95 | 0.01 | frozen by default |
| 5 | log_xi | — | 1 | 1 | 6 | 1 | 6 | 0.02 |  |

## PyXspec

```python
from xspec import Model
m = Model("rfxconv*powerlaw")
# component: m.rfxconv  (params as attributes)
```
