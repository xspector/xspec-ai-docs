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
- `info(name)` — A model component's definition, without loading it.
- `names(pattern='')` — The names of the model components matching a pattern.
- `addPyMod(func, parInfo, compType, calcsErrors=False, spectrumDependent=False, vectorized=False, units=None)` — Add a user-defined Python model function to XSPEC's models library.
- `calcFlux(eMin=None, eMax=None, err=False, number=None, level=None, cmdStr=None, zero=None)` — Calculate the model flux for a given energy range.
- `calcLumin(eMin=None, eMax=None, redshift=None, err=False, number=None, level=None, cmdStr=None, zero=None)` — Calculate the model luminosity for a given energy range and redshift.
- `clear()` — Remove all models.
- `projctDiagnostics()` — The conditioning of every projct component's deprojection, as of
- `mixingWeights(component, energy=None)` — The weights a mixing model component mixes with (`tclout
- `eqwidth(component, rangeFrac=None, err=False, number=None, level=None)` — Calculate the equivalent width of a model component.
- `setEnergies(arg1, arg2=None)` — Specify new energy binning for model fluxes.
- `identify(energy=None, delta=None, redshift=None, lineList=None, tplasma=None, emiss=None)` — Identify spectral lines.
- `identifyLines(energy, delta, top=20, group=1, model='')` — List the lines the current model emits (the 'identify fit' command).
- `initpackage(packageName, modDescrFile, dirPath=None, udmget=False)` — Initialize a package of local models.
- `lmod(packageName, dirPath=None)` — Load a local models library.
- `mdefine(commandStr=None)` — Define a simple model using an arithmetic expression.
- `setPars(*args)` — Change the value of multiple parameters from multiple
- `show(parIDs=None)` — Show all or a subset of Xspec model parameters.
- `simpars()` — Create a list of simulated parameter values.
- `systematicSingleModel(modelName)` — Get the systematic error setting for a specific model.
- `setSystematicSingleModel(modelName, value)` — Set a fractional systematic error for a specific model.
- `tclLoad(fullLibPath)` — Load a local model library by naming the library file directly.
- `setActive(modl_nm)` — Sets the model specified with modl_nm to active.
- `setInactive(modl_nm)` — Sets the model specified by modl_nm to inactive.
