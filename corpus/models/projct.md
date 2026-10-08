---
name: projct
type: mix  # mixing
func: U_Projection
n_params: 3
family: [projct]
energy_range: [0.001, 1.0e20]
source: manager/model.dat + XSmodelProjct.tex
---

# projct

**mixing model** (`mix`), function `U_Projection`.

## Description

This model performs a 3-D to 2-D projection of prolate ellipsoidal
shells onto elliptical annuli. The annuli can have varying
ellipticities and position angles but must have the same center. The
user should extract spectra in a series of annuli. Each spectrum needs
three additional keywords (as XFLTnnnn) in the spectrum
extension. These should be ``major: x'', ``minor: y'', ``orient: z''
where x, y, z are the semi-major axis, semi-minor axis, and position
angle (in degrees), respectively, for the outer boundary of the
annulus. (If an oblate model is required then switch the values of
major and minor and add ninety degrees to orient.) It is assumed that
the inner boundary is specified by the outer boundary of the previous
annulus. The lengths can be in any consistent units although for
numerical accuracy they should have reasonable values. Optional pairs
of extra XFLTnnnn keywords can be used to specify start and end angles
for a partial annulus. These have keys angleNl and angleNu so typical
keyword values might be ``angle1l: 30.0'' and ``angle1u: 45.0''. These
angles should be given relative to the same zero as the position
angle.

The user reads in the spectra as separate datagroups and sets model parameters 
for each datagroup. The model for datagroup J will be the model in the shell 
whose outer boundary is a prolate ellipsoid of semi-major and semi-minor axes 
given by the semi-major and semi-minor axes in the XFLT keywords for 
dataset J. The `projct` model sums up the appropriate fractions of 
each ellipsoid model to make the projected spectrum.

For example, suppose we extract spectrum from three elliptical regions defined 
by (1,0.5,0), (2,1,0), (3,1.5,0). That is the first region is in an ellipse of 
semi-major axis 1 and semi-minor axis 0.5. The second region is an elliptical 
annulus whose inner boundary has semi-major axis 1 and semi-minor axes 0.5 and 
whose outer boundary has semi-major axis 2 and semi-minor axis 1. The third 
region is defined similarly. The model fit has a temperature of 2 keV for the 
first datagroup, 3 keV for the second, and 4 keV for the third. The actual 
model fit to the first dataset has contributions from all three temperatures, 
the second only from the 3 and 4 keV components, and the third only from the 
4 keV component. The weighting is the fraction of the ellipsoidal volume 
intersected by the elliptical annular cross-section. Thus the normalizations 
correspond to the emission measure in each ellipsoidal shell.

If multiple observations are to be analyzed, data sets from different 
observations corresponding to the same annulus should be part of the same 
data group.  For example, given the following 4 data files:

Data sets for obs 1:  obs1_an1, obs1_an2
Data sets for obs 2:  obs2_an1, obs2_an2

The proper data loading command is:

```
XSPEC>data 1:1 obs1_an1 1:2 obs2_an1 2:3 obs1_an2 2:4 obs2_an2
```

The `projct` model has 3 (fixed) parameters, which can be used to define 
the inner ellipse of the region being analyzed. For instance, in the example 
above we could have only read in spectra for the outer two regions but then 
set the `projct` parameters to (1.0,0.5,0.0). This would have allowed 
us to determine the temperatures and emission measures of the outer two 
annuli without having to worry about fitting a model to the central region.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | major | — | 0 |  |  |  |  |  | scale (not fitted) |
| 2 | minor | — | 0 |  |  |  |  |  | scale (not fitted) |
| 3 | orient | — | 0 |  |  |  |  |  | scale (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("projct")
# component: m.projct  (params as attributes)
```
