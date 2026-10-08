---
name: dummyrsp
aliases: [xdummyrsp]
also_documents: []
source: XSdummyrsp.tex
---

# dummyrsp

**create and assign dummy response**

Create a ``dummy'' response, covering a given energy range.

**Syntax:** `dummyrsp` [<low energy> [<high energy>
[<# of ranges> [log| linear [<channel offset> [<channel width>
[<sourceNun>:<specNum>]]]]]]] [chanlog| chanlin]

**Syntax:** `dummyrsp` none [[<sourceNum>:]<spectrum range>]

This command creates a dummy response matrix based on the given command line 
arguments, which will either supersede the current response matrix until
it is removed, or create a response matrix if one is not currently present. There 
are two main uses for this command: to do a "quick and dirty" analysis of 
uncalibrated data (mode 1), and to examine the behaviour of the current 
model outside the range of the data's energy response (mode 2).  
**Note that mode 2 usage has now been rendered redundant by the more 
flexible `energies` command.**

All parameters are optional.  The initial default values for the arguments 
are 0.01 keV, 100 keV, 200 logarithmic energy steps, 0.0 channel offset, 
and 0.0 channel width.  The default values of the first 5 parameters will 
be modified each time the parameter is explicitly entered.  The channel width 
parameter however always defaults to 0.0 which indicates mode 2 operation, 
described below.  

In addition to the 6 optional parameters allowed for versions 11.x and 
earlier, a seventh optional parameter has been added allowing the user to 
apply the dummy response to just one particular source of a spectrum.  
It consists of two integers for (1-based) source number and spectrum number, 
separated by a colon.  Either both integers should be entered, or they 
should be left out entirely.  ie. A dummy response is either made for 
EVERY source in every spectrum, or just 1 source in 1 spectrum.  
This parameter always defaults to all sources and all spectra.

For mode 1 usage, simply enter a non-zero value for the channel width.  
In this instance, one has a spectrum for which typically no response matrix 
is currently available. This command will create a diagonal response matrix 
with perfect efficiency, allowing for the differences in binning between the 
photon energies and the detector channel energies (see example below).  
The response matrix will range in energy from `<low energy>` to 
`<high energy>`, using `<# of ranges>` as the number of steps 
into which the range is logarithmically or linearly divided. The detector 
channels are assigned to have widths of energy `<channel width>` 
(specified in keV), the lower bound of the first channel starting at an 
energy of `<channel offset>`. Then the data can be fit to models, 
etc., under conditions that assume a perfect detector response. 

The keyword `chanlog`, anywhere on the line, makes the detector
channels logarithmically spaced instead: `<channel offset>` is then the
lower edge of the first channel (in keV, and must be greater than 0) and
`<channel width>` the fractional width $\Delta E/E$, so channel $i$
(counting from 0) runs from $\mathrm{offset}\,(1+w)^i$ to
$\mathrm{offset}\,(1+w)^{i+1}$. `chanlin` returns to linear channels.
Like the channel offset, the choice is remembered for later `dummyrsp`
commands; it starts as `chanlin`. It has no effect in mode 2 (channel
width 0). `save` does not record a dummy response, linear or
logarithmic.

For mode 2 usage (channel width = 0.0), one can use this command to examine 
the current model outside the range of the energy response of the detector. 
When examining several aspects of the current model, such as plotting it or 
determining flux, XSPEC uses the current evaluation array. This, in turn, 
is defined by the current response files being used, which depend on the 
various detectors. For example, low energy datasets (such as those from 
the EXOSAT LEs) may have responses covering 0.05 to 2 keV, while non-imaging 
proportional counters can span the range from 1 to 30 keV. If the user 
wishes to examine the behavior of the model outside of the current range, 
then he or she temporarily must create a dummy response file that will 
cause the model to be evaluated from `<low energy>` to `<high energy>`, 
using `<# of ranges>` as the number of steps into which the range is 
logarithmically or linearly divided. If one wishes only to set the energy 
response range, than the `<channel width>` argument may be omitted. 
In this case, or in the case where no data file has been read in, all entries 
of the dummy response matrix are set to zero. Under these circumstances the 
dummyrsp has no physically correct way of mapping the model into the data 
PHA channels, so the user should not try to fit-or plot-the data while 
the dummyrsp is active in this mode.   Also, data need not even be loaded 
when calling this command in mode 2.

A dummy response stays until it is removed: `ignore` and
`notice` (in every form, including `notice all` and
`ignore bad`) leave it in place, and a `data` command removes
it only from the spectra it replaces or deletes --- loading or removing
another spectrum leaves it alone.  (Before XSPEC 13.0.2 any `ignore`,
`notice` or `data` command restored the original responses.)

`dummyrsp none` removes the dummy responses and restores the
responses they replaced, or no response if there was none.  With a spectrum
range (`2`, `1-3`, `1,4-5`) it does so only for those
spectra, and with <sourceNum>`:` in front only for that source of
those spectra.  The `response` command with no arguments removes every
dummy response, as `dummyrsp none` with no range does.

The exception is a spectrum faked on a dummy response by `fakeit`:
that dummy is the spectrum's own response, so neither `dummyrsp none`
nor the bare `response` removes it (a further `dummyrsp` over it
is removed as usual).

**Examples:**

```
XSPEC> dummyrsp
//Create the dummy response for all spectra and sources with the 
//default limits, initially .01, 100, and 200 bins.
XSPEC> dummyrsp .001 1
//Create a dummy response with 200 bins that cover the range from 
//0.001 to 1 keV.
XSPEC> dummyrsp ,,,500
//The same range, but now with 500 bins.
XSPEC> dummyrsp ,,,,lin
//The same range, but now with linearly spaced bins.
XSPEC> dummyrsp ,,,,,0.1
//The same range, but now create a diagonal response matrix, with 
//channel widths of 0.1 keV.
XSPEC> dummyrsp 0.05 50 3000 log 0.5 0.01 chanlog
//Channels each 1% wide in energy, the first starting at 0.5 keV.
XSPEC> dummyrsp none 2
//Restore spectrum 2's original response; other dummies stay.
XSPEC> response
//Restore any previous correct responses.
```

Example dummy response matrix:

Assume a spectrum with 4 channels, then

```
XSPEC> dummyrsp .0 30.0 3 lin 5.0 8.0
```

will produce the following response:

& 4{c|}{Detector channel energies}

Energies & 5.0-13.0 & 13.0-21.0 & 21.0-29.0 & 29.0-37.0

0.0-10.0 & 0.5 & 0 & 0 & 0

10.0-20.0 & 0.3 & 0.7 & 0 & 0

20.0-30.0 & 0 & 0.1 & 0.8 & 0.1
