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
| dataModels | — | get | Every data model on every spectrum, spectrum order then the order |

## Methods

- `__init__()`
- `__call__(expr)` — DataManager get or set spectra.
- `load(records, preserve=False)` — Load a batch of spectra: the typed form of *AllData("...")*.
- `loadArrays(eLow, eHigh, flux, fluxErr, xunit='keV', yunit='ph/cm^2/s', fileName=None, group=None, slot=None, rows=None, preserve=False)` — Load tabulated flux data: *load([DataRecord.fromArrays(...)])*.
- `clear()` — Remove all spectra from the data container.
- `removeDataModels()` — Remove every data model from every spectrum (*dmodel clear*).
- `registeredDataModels()` — The data models that can be attached (model.dat type dat).
- `backModel(expr, name='bkg', spectra=None, response=None, arf=None)` — Fit the background with a model, together with the source.
- `backModelNone(spectra=None)` — Undo :meth:`backModel` for the given source spectra (default all).
- `backModels()` — The backmodel set-up: a dict with "components" (each a dict of
- `diagrsp()` — Diagonalize the current response matrix for ideal response.
- `dummyrsp(lowE=None, highE=None, nBins=None, scaleType=None, chanOffset=None, chanWidth=None, chanLog=None)` — Create a dummy response and apply it to all spectra.
- `fakeit(nSpectra=1, settings=None, applyStats=True, filePrefix='', noWrite=False)` — Produce spectra with simulated data using XSPEC's fakeit command.
- `group(groupArgs)` — Apply a `group` command to all loaded spectra.
- `ignore(ignoreRange)` — Apply an ingore channels range to multiple loaded spectra.
- `notice(noticeRange)` — Apply a notice channels range to multiple loaded spectra.
- `removeDummyrsp(spectra=None)` — Remove dummy responses, restore original responses (if any).
- `show()` — Display information for all loaded spectra.
