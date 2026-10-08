---
name: crossarf
type: mix  # mixing
func: U_CrossArf
n_params: 0
family: [crossarf]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelCrossarf.tex
---

# crossarf

**mixing model** (`mix`), function `U_CrossArf`.

## Description

This is a general model for use when simultaneously fitting spectra
from multiple regions with a telescope whose psf is large enough to
scatter emission between the regions.

The model requires arf files to have been calculated for the
contribution from each region to each other region. Each spectrum then
needs an XFLTnnnn keyword set to ``CrossArfRegion:N'' where N is the
region number (no particular scheme is required to assign region
numbers as long as they are unique) as well as a series of XFLTnnnn
keywords setting the cross arfs from region to region using the values
``CrossArfFromNToM:arffile'' where arffile is the arf giving the
contributions to region M from region N.

As an example suppose that we have four regions then the keywords in
the spectrum for the first region could be:

```
XFLT0001 = 'CrossArfRegion:1'
XFLT0002 = 'CrossArfFrom1To2:test_1_2.arf'
XFLT0003 = 'CrossArfFrom1To3:test_1_3.arf'
XFLT0004 = 'CrossArfFrom1To4:test_1_4.arf'
```

Note that it does not matter which spectrum contains the definitions
for all the cross arfs as long as the spectra read in have the
complete list required.

Multiple emission components in a region

A region may contain more than one emission component whose spatial
distributions differ -- for instance an extended source together with a
point source. Because the two components scatter into the neighbouring
regions by different amounts, a single set of cross arfs is not enough; each
component is instead handled as a separate source (see the `model`
command), with its own arfs loaded by the `arf` command. Two cases
arise:

- A component that is itself spread across several regions and mixes
between them is given its own `crossarf` source. If there are two or
more such components with different spatial distributions, each is a separate
`crossarf` source and their cross arfs are distinguished by a source
tag in the XFLT keyword name, ``CrossArfSrcSFromNToM:arffile'', where S is
the source number and, as before, arffile gives the contribution to region M
from region N. The original ``CrossArfFromNToM'' form, with no source tag, is
treated as belonging to source 1. The ``CrossArfRegion'' keyword is not
source tagged, since the region a spectrum belongs to is the same for all
sources.

- A component confined to a single region does not need a
`crossarf` at all: it is added as an ordinary source with the arfs
giving its contribution to each detector region.

*Example 1: an extended source in both regions and a point
source in one of them.** The extended emission fills both regions and mixes
between them, so it is a `crossarf` source (source 1). The point
source lies in region 1 only; it is seen in both detector regions but does
not mix, so it is an ordinary source (source 2) with the two arfs giving its
contribution to each detector. Load the two spectra as two data groups and
attach both sources' responses:

```
XSPEC> data 1:1 region1.pha 2:2 region2.pha
XSPEC> response 1:1 region1.rmf
XSPEC> arf 1:1 ext_1to1.arf
XSPEC> response 1:2 region2.rmf
XSPEC> arf 1:2 ext_2to2.arf
XSPEC> response 2:1 region1.rmf
XSPEC> arf 2:1 pt_1to1.arf
XSPEC> response 2:2 region2.rmf
XSPEC> arf 2:2 pt_1to2.arf
```

The extended `crossarf` (source 1) is the only mixing source, so its
cross arfs use the plain (untagged) keyword form. In the spectrum for region
1:

```
XFLT0001 = 'CrossArfRegion:1'
XFLT0002 = 'CrossArfFrom2To1:ext_2to1.arf'
```

and in the spectrum for region 2:

```
XFLT0001 = 'CrossArfRegion:2'
XFLT0002 = 'CrossArfFrom1To2:ext_1to2.arf'
```

Define the two models:

```
XSPEC> model 1:ext crossarf*(tbabs*apec)
XSPEC> model 2:pt  tbabs*powerlaw
```

The extended emission generally differs between the two regions, so give its
data-group-2 parameters their own values (untying them from data group 1).
The point source is a single object, so leave its data-group-2 parameters
linked to data group 1 (the default for a new data group). The point source
appears in region 2's spectrum only through its arf pt_1to2 -- no mixing
keyword is needed for it.

*Example 2: two mixing components.** If instead two components
are each spread across both regions with different spatial distributions --
for example a cool and a hot plasma phase -- then each needs its own
`crossarf`, and the source tag distinguishes their cross arfs. Load
each source's diagonal arf as in Example 1 (+arf 1:1 cool_1to1.arf+,
+arf 2:1 hot_1to1.arf+, and so on), and in the spectrum for region 1:

```
XFLT0001 = 'CrossArfRegion:1'
XFLT0002 = 'CrossArfSrc1From2To1:cool_2to1.arf'
XFLT0003 = 'CrossArfSrc2From2To1:hot_2to1.arf'
```

Then define one `crossarf` per component:

```
XSPEC> model 1:cool crossarf*(tbabs*apec)
XSPEC> model 2:hot  crossarf*(tbabs*apec)
```

Here CrossArfSrc1 supplies the cool component's cross arfs and
CrossArfSrc2 the hot component's; each `crossarf` mixes only
its own component, and XSPEC sums the source contributions in every spectrum.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|

## PyXspec

```python
from xspec import Model
m = Model("crossarf")
# component: m.crossarf  (params as attributes)
```
