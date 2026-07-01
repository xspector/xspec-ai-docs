---
name: rgsxsrc
type: con  # convolution
func: C_rgsxsrc
n_params: 1
family: [rgsxsrc]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelRgsxsrc.tex
---

# rgsxsrc

**convolution model** (`con`), function `C_rgsxsrc`.

## Description

This model convolves the input spectrum by an angular structure
function so that it can be used with the standard RGS response matrix,
which assumes a point source. This will only be of value for
moderately extended (one arcmin) sources.

The angular structure function is calculated from an input image,
boresight position and extraction region size. There are two ways of
passing this information to the model. Either the information can be
given by three XFLTnnnn keywords in the spectrum or the information
can be read from an external file.

An example of the first option is to include the keywords:

```
XFLT0001 = 'Image:/local/data/mymachine/myusername/mos1.fit'
XFLT0002 = 'Boresight:05:25:02.9 -69:38:30 339.760974'
XFLT0003 = 'Extraction:1.8'
```

For the second option, the xset variable RGS_XSOURCE_FILE
should be set to the name of the file containing the information. An
example of this file is:

```
RGS_XSOURCE_IMAGE /local/data/mymachine/myusername/mos1.fit 
RGS_XSOURCE_BORESIGHT 05:25:02.9 -69:38:30 339.760974 
RGS_XSOURCE_EXTRACTION 1.8 
```

The RA and Dec of the source can be determined from the image or from
the headers of the source spectrum. The position angle can be found in
the image headers.

The model parameter is:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | order | — | -1 | -3 | -1 | -3 | -1 | 1 | frozen by default |

## PyXspec

```python
from xspec import Model
m = Model("rgsxsrc*powerlaw")
# component: m.rgsxsrc  (params as attributes)
```
