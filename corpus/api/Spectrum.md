---
class: Spectrum
module: spectrum.py
---

# Spectrum

**Spectral data class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| areaScale | — | get | The Spectrum area scaling factor. |
| background | — | get/set | Get/Set the spectrum's background. |
| backScale | — | get | The Spectrum background scaling factor. |
| cornorm | float | get/set | Get/Set the normalization of a spectrum's correction file. [float] |
| correction | — | get/set | Get/Set the correction file. |
| dataGroup | int | get | The data group to which the spectrum belongs [int]. |
| energies | tuple | get | Tuple of pairs of floats (also implemented as tuples) |
| eqwidth | tuple | get | Tuple of 3 floats containing the results of the most recent |
| exposure | float | get | The exposure time keyword value [float]. |
| fileName | str | get | The spectrum's file name [string]. |
| flux | tuple | get | A tuple containing the results of the most recent flux |
| ignored | list | get | A list of the currently ignored (1-based) channel numbers. |
| index | — | get | The spectrum's current index number within the AllData |
| isPoisson | bool | get | Boolean flag, true if spectrum has Poisson errors. |
| lumin | — | get | Similar to flux, the results of the most recent luminosity |
| multiresponse | — | get/set | Get/Set detector response ARRAY elements when using multiple |
| noticed | list | get | A list of the currently noticed (1-based) channel numbers. |
| rate | tuple | get | A tuple containing the total Spectrum rates in counts/sec. |
| response | — | get/set | Get/Set the detector response. |
| responsesUsed | list | get | Return a list of detector slot numbers with currently assigned |
| statistic | float | get | Spectrum's contribution to the total fit statistic [float]. |
| values | tuple | get | Tuple of floats containing the spectrum rates for noticed |
| variance | tuple | get | Tuple of floats containing the variance of each noticed |
| xflt | tuple | get | XFLT key-value pairs returned as a tuple of tuples |
| groupingFlags | tuple | get | Tuple of per-channel grouping flags {1, -1, 0} (GET only). |
| groupIntent | — | get | Cached source-side group intent as a string, e.g. ``"optbin 5"``, |
| backGroupMap | tuple | get | Tuple of per-source-bin super-bin indices for the |
| backGroupIntent | — | get | Cached background-side group intent as a string, e.g. |

## Methods

- `__init__(dataFile, backFile='USE_DEFAULT', respFile='USE_DEFAULT', arfFile='USE_DEFAULT')` — Construct a Spectrum object.
- `dummyrsp(lowE=None, highE=None, nBins=None, scaleType=None, chanOffset=None, chanWidth=None, sourceNum=1)` — Create a dummy response for this spectrum only.
- `fileinfo(keyword)` — Return the value of a particular keyword in the SPECTRUM extension.
- `group(groupArgs)` — Apply a `group` command to this spectrum.
- `ignore(ignoreRange)` — Ignore a range of the spectrum by channels or energy/wavelengths.
- `ignoredString()` — Return a string of ignored channel ranges.
- `notice(noticeRange)` — Notice a range of the spectrum by channels or energy/wavelengths.
- `noticedString()` — Return a string of noticed channel ranges.
- `show()` — Display information for this Spectrum object
