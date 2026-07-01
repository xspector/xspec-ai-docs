---
class: XspecSettings
singleton: Xset
module: xset.py
---

# Xset

Singleton instance `Xset` (class `XspecSettings`).

**Storage class for Xspec settings.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| abund | — | get/set | Get/Set the abundance table used in the plasma emission and |
| allowNewAttributes | — | get/set | Get/Set the flag which allows the setting of new |
| allowPrompting | — | get/set | Get/Set flag determining whether user prompting occurs. |
| chatter | int | get/set | Get/Set the console chatter level [int]. |
| logChatter | int | get/set | Get/Set the log chatter level [int]. |
| cosmo | — | get/set | Get/Set the cosmology values. |
| log | — | get | Get only: Returns the currently opened log file object, |
| modelStrings | — | get/set | XSPEC's internal database of <string_name>, |
| parallel | — | get | An attribute for controlling the number of parallel |
| seed | — | get/set | Re-seed and re-initialize XSPEC's random-number generator |
| version | — | get | The version strings for PyXspec and standard XSPEC. |
| xsect | — | get/set | Get/set the photoelectric absorption cross-sections in use |

## Methods

- `__init__()`
- `addModelString(key, value)` — Add a key,value pair of strings to XSPEC's internal database.
- `delModelString(key)` — Remove a key,value pair from XSPEC's internal model string database.
- `getModelString(key)` — Get the value for a particular key string in XSPEC's internal
- `closeLog()` — Close XSPEC's current log file.
- `openLog(fileName)` — Open a file and set it to be XSPEC's log file.
- `show()`
- `restore(fileName)` — Restore the data/model configuration and settings.
- `save(fileName, info='a')` — Save the data and model configuration and XSPEC settings
