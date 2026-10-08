---
class: DataRecord
module: data.py
---

# DataRecord

**One file's worth of an AllData.load() batch.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| file | — | instance |  |
| group | — | instance |  |
| slot | — | instance |  |
| rows | — | instance |  |
| response | — | instance |  |
| arf | — | instance |  |
| background | — | instance |  |
| fileName | — | instance |  |

## Methods

- `__init__(file, group=None, slot=None, rows=None, response=None, arf=None, background=None, fileName=None)`
- `fromArrays(cls, eLow, eHigh, flux, fluxErr, xunit='keV', yunit='ph/cm^2/s', fileName=None, group=None, slot=None, rows=None)` — A record for tabulated flux data (what *ftflx2xsp* makes).
- `fromCounts(cls, counts, exposure, response, arf=None, background=None, channels=None, poisson=True, statErr=None, fileName=None, group=None, slot=None)` — A record for counts per channel.
