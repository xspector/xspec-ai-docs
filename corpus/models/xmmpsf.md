---
name: xmmpsf
type: mix  # mixing
func: U_Psf<XMM>(Psf,PsfTraits)
n_params: 4
family: [xmmpsf]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelXmmpsf.tex
---

# xmmpsf

**mixing model** (`mix`), function `U_Psf<XMM>(Psf,PsfTraits)`.

## Description

Mixing model for XMM data. Mixes the spectra between datagroups based on the 
PSF overlap between selected regions. A surface brightness model is required 
to calculate the mixing and this can be supplied in several ways. If 
XMMPSF-IMAGE has been set to some image file (using `xset`) then this 
image will be used for the surface brightness distribution. If XMMPSF-IMAGE 
has not been set then either a beta or two power-law model is used. In this 
case the model parameters determine the shape of the surface brightness 
distribution. If XMMPSF-RA and XMMPSF-DEC are set they are used as the center 
of the distribution. They should be specified either in decimal degrees or 
as hh:mm:ss.s and dd:mm:ss.s. If XMMPSF-RA and XMMPSF-DEC are not set then 
the centroid of the wmap will be used as the center of the surface 
brightness distribution. 

The model works by calculating the mixing factors. It will recalculate these 
factors if any of the XMMPSF-* or any of the model parameters are changed. 
Calculating the mixing factors is very slow so should be avoided as much as 
possible.  To speed things up, it is possible to save the mixing factor array 
to a FITS file and re-use it during a later calculation.  To save a mixing 
factor calculation, prior to loading the mixing model (using the `model` 
command), use `xset` to set the variable XMMPSF-MIXFACT-OFILEn to the 
name of the output FITS file, and where n is an integer corresponding to the 
observation number:

```
XSPEC> xset XMMPSF-MIXFACT-OFILE1 fact_obs1.fits
```

Conversely, a saved factor array can be read in by setting XMMPSF-MIXFACT-IFILEn:

```
XSPEC> xset XMMPSF-MIXFACT-IFILE1 fact_obs1.fits
```

Multiple observations can be fit simultaneously. In this case the observations 
should be read in each datagroup in the same order, e.g. 

XSPEC> data 1:1 obs1reg1 1:2 obs2reg1 1:3 obs3reg1 2:4 obs1reg2 2:5 obs2reg2

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Alpha | — | 2 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 2 | Beta | — | 0.66 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 3 | Core | arcmin | 1 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 4 | Switch | — | 0 |  |  |  |  |  | switch (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("xmmpsf")
# component: m.xmmpsf  (params as attributes)
```
