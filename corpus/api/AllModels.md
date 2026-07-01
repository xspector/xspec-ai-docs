---
class: ModelManager
singleton: AllModels
module: model.py
---

# AllModels

Singleton instance `AllModels` (class `ModelManager`).

**Models container.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| sources | — | get | A dictionary containing the currently active <source number>:<model name> assignments. |
| systematic | — | get/set | The fractional model systematic error. |

## Methods

- `__init__()`
- `__call__(groupNum, modName='')` — Get Model objects from the AllModels container.
- `addPyMod(func, parInfo, compType, calcsErrors=False, spectrumDependent=False)` — Add a user-defined Python model function to XSPEC's models library.
- `calcFlux(cmdStr)` — Calculate the model flux for a given energy range.
- `calcLumin(cmdStr)` — Calculate the model luminosity for a given energy range and redshift.
- `clear()` — Remove all models.
- `eqwidth(component, rangeFrac=None, err=False, number=None, level=None)` — Calculate the equivalent width of a model component.
- `setEnergies(arg1, arg2=None)` — Specify new energy binning for model fluxes.
- `identify(energy=None, delta=None, redshift=None, lineList=None, tplasma=None, emiss=None)` — Identify spectral lines.
- `initpackage(packageName, modDescrFile, dirPath=None, udmget=False)` — Initialize a package of local models.
- `lmod(packageName, dirPath=None)` — Load a local models library.
- `mdefine(commandStr=None)` — Define a simple model using an arithmetic expression.
- `setPars(*args)` — Change the value of multiple parameters from multiple
- `show(parIDs=None)` — Show all or a subset of Xspec model parameters.
- `simpars()` — Create a list of simulated parameter values.
- `systematicSingleModel(modelName)` — Get the systematic error setting for a specific model.
- `setSystematicSingleModel(modelName, value)` — Set a fractional systematic error for a specific model.
- `tclLoad(fullLibPath)` — Load a local model library by calling Tcl's 'load' command.
- `setActive(modl_nm)` — Sets the model specified with modl_nm to active.
- `setInactive(modl_nm)` — Sets the model specified by modl_nm to inactive.
