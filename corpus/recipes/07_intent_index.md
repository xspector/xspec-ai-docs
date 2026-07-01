---
title: Intent -> API reverse index (I want to X -> call Y)
audience: agent
priority: 4
---

# Intent -> API index

Find the exact call from what you want to do. PyXspec-first; Tcl shown for cross-reference. Every call is validated against `corpus/api/api.json` (see tests).

## Session / setup

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Run without blocking on prompts | `Fit.query = "yes"` | `query yes` | the single most important line for headless runs |
| Silence console output | `Xset.chatter = 0` | `chatter 0` |  |
| Set log-file verbosity | `Xset.logChatter = 10` | `chatter 10 10` |  |
| Open / close a log file | `Xset.openLog("run.log") ... Xset.closeLog()` | `log run.log ... log none` |  |
| Set RNG seed (reproducible) | `Xset.seed = 12345` | `xset seed 12345` |  |
| Reset all data and models | `AllData.clear(); AllModels.clear()` | `data none; model none` | do this at the top of a re-runnable script |
| Set abundance table | `Xset.abund = "wilm"` | `abund wilm` | tbabs assumes wilm |
| Set photoionization cross-sections | `Xset.xsect = "vern"` | `xsect vern` |  |
| Set cosmology | `Xset.cosmo = "70,0,0.73"` | `cosmo 70 0 0.73` |  |
| Set an arbitrary model xset key | `Xset.addModelString("APECROOT", "3.0.9")` | `xset APECROOT 3.0.9` | valid keys are in manifest.json xset_keys (documented subset) |
| Set parallel processes | `Xset.parallel.leven = 4  # also .error, .steppar` | `parallel leven 4` |  |

## Data

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Load a spectrum | `AllData("1:1 src.pha")` | `data 1:1 src.pha` | returns None; response/arf/background auto-load from the PHA header |
| Load multiple spectra (own groups) | `AllData("1:1 a.pha 2:2 b.pha")` | `data 1:1 a.pha 2:2 b.pha` | 2:1 would share one data group |
| Get the Spectrum object | `s = AllData(1)` | — | AllData(int) returns the Spectrum |
| Attach a response | `AllData(1).response = "r.rmf"` | `response r.rmf` | reading .response raises if none attached |
| Attach an ARF | `AllData(1).response.arf = "a.arf"` | `arf a.arf` |  |
| Attach a background | `AllData(1).background = "b.pha"` | `backgrnd b.pha` | reading .background raises if none attached |
| Restrict energy range | `AllData.ignore("**-0.5 10.0-**")` | `ignore **-0.5 10.0-**` |  |
| Ignore bad channels | `AllData.ignore("bad")` | `ignore bad` |  |
| Re-notice a range | `AllData.notice("0.5-10.0")` | `notice 0.5-10.0` |  |
| Remove a spectrum | `AllData -= 1` | `data 1 none` | AllData -= <n|Spectrum|"*">; "*" removes all |
| Count spectra / data groups | `AllData.nSpectra; AllData.nGroups` | — |  |
| Get exposure | `AllData(1).exposure` | — |  |
| Get count rate | `AllData(1).rate` | `tclout rate` |  |

## Model

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Define a model | `Model("tbabs*powerlaw")` | `model tbabs*powerlaw` |  |
| Define a named model for a source | `Model("phabs*po", "src2", sourceNum=2)` | `model src2:...` |  |
| Set a parameter value (by number) | `AllModels(1)(2).values = 1.8` | `newpar 2 1.8` |  |
| Set a parameter value (by name) | `m.powerlaw.PhoIndex = 1.8` | — | component attrs are the model.dat canonical names (m.TBabs, m.powerlaw) |
| Set value with limits | `AllModels(1)(2).values = "1.8,,0.5,0.5,3,3"` | `newpar 2 1.8,,0.5,0.5,3,3` | order: val,delta,min,bottom,top,max |
| Freeze / thaw a parameter | `AllModels(1)(2).frozen = True   # or False` | `freeze 2 / thaw 2` |  |
| Link parameters | `AllModels(2)(3).link = AllModels(1)(3)` | `newpar 2:3 = 1:3` | assign a Parameter object or an '=' string |
| Unlink a parameter | `AllModels(2)(3).untie()` | `untie 2:3` |  |
| Get a parameter value | `AllModels(1)(2).values[0]` | `tclout param 2` | values is a 6-list; [0] is the fitted value |
| List component names | `AllModels(1).componentNames` | `show model` |  |
| Number of parameters | `AllModels(1).nParameters` | — |  |
| Set many parameters at once | `AllModels(1).setPars(1.0, 1.8, 1e-3)` | — |  |
| Use a table model | `Model("atable{mod.fits}*powerlaw")` | `model atable{mod.fits}*powerlaw` | atable=additive table, mtable=multiplicative, etable=exponential |

## Fit

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Choose the fit statistic | `Fit.statMethod = "cstat"` | `statistic cstat` | cstat for low counts; chi only for well-grouped high counts |
| Choose the test statistic | `Fit.statTest = "chi"` | `statistic test chi` |  |
| Fit | `Fit.perform()` | `fit` |  |
| Global (multi-start) fit | `Fit.globalFit()` | `fit global` | derivative-free search then polish |
| Competitive basins after a global fit | `Fit.globalBasins` | — | flags degeneracies a single fit hides |
| Renormalize | `Fit.renorm()` | `renorm` |  |
| Get statistic and dof | `Fit.statistic; Fit.dof` | `tclout stat; tclout dof` |  |
| Set max fit iterations | `Fit.nIterations = 100` | `fit 100` |  |

## Errors / confidence

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Confidence interval for a parameter | `Fit.error("2.706 1-3"); AllModels(1)(1).error` | `error 1-3` | error is (lo, hi, code); code 'FFFFFFFFF' = clean |
| Steppar (1-D/2-D confidence scan) | `Fit.steppar("2 1.5 2.5 20")` | `steppar 2 1.5 2.5 20` |  |
| Get steppar results | `Fit.stepparResults("delstat")` | — |  |
| Goodness of fit (Monte Carlo) | `Fit.goodness(1000, sim=True)` | `goodness 1000 sim` | use this for cstat, not reduced-statistic |
| F-test | `Fit.ftest(chi2, dof2, chi1, dof1)` | `ftest chi2 dof2 chi1 dof1` |  |
| Covariance matrix | `Fit.covariance` | `tclout covariance` |  |

## Derived quantities

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Model flux | `AllModels.calcFlux("0.5 10.0"); AllData(1).flux` | `flux 0.5 10.0` | flux is a 6-tuple; calcFlux stores into Spectrum.flux, returns nothing |
| Flux with Monte-Carlo errors | `AllModels.calcFlux("0.5 10.0 err")` | `flux 0.5 10.0 err` |  |
| Fitted flux with a real confidence interval | `Model("cflux*tbabs*po"); Fit.error on the lg10Flux parameter` | — | wrap in cflux/cpflux; its flux parameter gets a proper CI |
| Luminosity | `AllModels.calcLumin("0.5 10.0 0.01"); AllData(1).lumin` | `lumin 0.5 10.0 0.01` | last arg is redshift |
| Equivalent width | `AllModels.eqwidth(2); AllData(1).eqwidth` | `eqwidth 2` | argument is the (additive line) component number |

## Plot / output

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Set plot device (no GUI) | `Plot.device = "/null"` | `cpd /null` | /null computes arrays without drawing |
| Set x-axis units | `Plot.xAxis = "keV"` | `setplot energy` |  |
| Plot data and residuals | `Plot("ldata", "delchi")` | `plot ldata delchi` |  |
| Extract plot arrays | `Plot.x(); Plot.y(); Plot.model()` | — | how to 'see' a fit with no display |
| Extract error bars | `Plot.yErr()` | — |  |
| Write a plot to a file | `Plot.device = "/png"; Plot("ldata")` | `cpd fig.png/png; plot ldata` |  |
| Plot individual model components | `Plot.addComp(1)` | — |  |

## Simulation / Bayesian

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Simulate a spectrum (fakeit) | `fs = FakeitSettings(response="r.rmf", exposure=1e4); AllData.fakeit(1, fs)` | `fakeit ...` | seed with Xset.seed for reproducibility |
| Run an MCMC chain | `Chain("c.fits", burn=1000, runLength=10000, walkers=20, algorithm="gw")` | `chain length 10000; chain burn 1000; chain run c.fits` | constructing the Chain runs it |
| Marginal statistics from chains | `AllChains.stat(2)` | `tclout chain stat` |  |
| Enable Bayesian priors | `Fit.bayes = "on"` | `bayes on` |  |
| Set a parameter prior | `AllModels(1)(1).prior = "cons"  # e.g. constant/jeffreys/gauss` | — |  |

## Save / restore

| I want to... | PyXspec | Tcl | Notes |
|--------------|---------|-----|-------|
| Save the whole session | `Xset.save("session.xcm", info="a")` | `save all session.xcm` |  |
| Restore a session | `Xset.restore("session.xcm")` | `@session.xcm` |  |
