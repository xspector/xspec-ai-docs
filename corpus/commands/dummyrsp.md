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
[<sourceNun>:<specNum>]]]]]]]

This command creates a dummy response matrix based on the given command line 
arguments, which will either temporarily supersede the current response 
matrix, or create a response matrix if one is not currently present. There 
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

The previous response matrices can be reimplemented with the `response` 
command, with no arguments. Any use of the `data` and `notice` 
commands will replace the dummy response with a correct set of matrices, 
or with no response matrix if none was originally present.

**Examples:**

```
XSPEC12> dummyrsp
//Create the dummy response for all spectra and sources with the 
//default limits, initially .01, 100, and 200 bins.
XSPEC12> dummyrsp .001 1
//Create a dummy response with 200 bins that cover the range from 
//0.001 to 1 keV.
XSPEC12> dummyrsp ,,,500
//The same range, but now with 500 bins.
XSPEC12> dummyrsp ,,,,lin
//The same range, but now with linearly spaced bins.
XSPEC12> dummyrsp ,,,,,0.1
//The same range, but now create a diagonal response matrix, with 
//channel widths of 0.1 keV.
XSPEC12> response
//Restore any previous correct responses.
```

Example dummy response matrix:

Assume a spectrum with 4 channels, then

```
XSPEC12> dummyrsp .0 30.0 3 lin 5.0 8.0
```

will produce the following response:

& 4{c|}{Detector channel energies}

Energies & 5.0-13.0 & 13.0-21.0 & 21.0-29.0 & 29.0-37.0

0.0-10.0 & 0.5 & 0 & 0 & 0

10.0-20.0 & 0.3 & 0.7 & 0 & 0

20.0-30.0 & 0 & 0.1 & 0.8 & 0.1
