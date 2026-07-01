---
class: DataManager
singleton: AllData
module: data.py
---

# AllData

Singleton instance `AllData` (class `DataManager`).

**Spectral data container.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| nGroups | int | get | The number of data groups [int]. |
| nSpectra | int | get | The number of loaded spectra [int]. |

## Methods

- `__init__()`
- `__call__(expr)` — DataManager get or set spectra.
- `clear()` — Remove all spectra from the data container.
- `diagrsp()` — Diagonalize the current response matrix for ideal response.
- `dummyrsp(lowE=None, highE=None, nBins=None, scaleType=None, chanOffset=None, chanWidth=None)` — Create a dummy response and apply it to all spectra.
- `fakeit(nSpectra=1, settings=None, applyStats=True, filePrefix='', noWrite=False)` — Produce spectra with simulated data using XSPEC's fakeit command.
- `group(groupArgs)` — Apply a `group` command to all loaded spectra.
- `ignore(ignoreRange)` — Apply an ingore channels range to multiple loaded spectra.
- `notice(noticeRange)` — Apply a notice channels range to multiple loaded spectra.
- `removeDummyrsp()` — Remove all dummy responses, restore original responses (if any).
- `show()` — Display information for all loaded spectra.
