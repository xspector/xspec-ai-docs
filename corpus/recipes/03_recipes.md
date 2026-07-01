---
title: End-to-end runnable recipes (PyXspec-first)
audience: agent
priority: 3
verified_against: PyXspec; recipes exercised in tests/run_recipes.py
---

# End-to-end recipes

Copy-pasteable workflows. Each assumes the headless setup from guide 01
(`Fit.query="yes"`, chatter set) and the ingestion decisions from guide 02
(statistic, energy range). Import once:

```python
from xspec import (AllData, AllModels, Model, Fit, Xset, Plot,
                   FakeitSettings, Chain, AllChains)
```

## R1 — Absorbed power-law fit

```python
Fit.query = "yes"; Xset.abund = "wilm"
AllData.clear(); AllModels.clear()
AllData("1:1 src.pha")
AllData.ignore("bad"); AllData.ignore("**-0.5 8.0-**")
Fit.statMethod = "cstat"
m = Model("tbabs*powerlaw")
m.TBabs.nH = 0.1                       # component.parameter access
m.powerlaw.PhoIndex = 1.8
Fit.perform()
print(Fit.statistic, Fit.dof)
```
Tcl: `data 1:1 src.pha; ignore bad; ignore **-0.5 8.0-**; statistic cstat;`
`model tbabs*powerlaw; fit`.

## R2 — Confidence intervals

```python
Fit.error("2.706 1-3")                 # 90% for params 1–3
for i in (1, 2, 3):
    lo, hi, code = AllModels(1)(i).error
    if code.strip("F") and code != "FFFFFFFFF":   # non-clean status
        pass  # investigate; commonly a new minimum -> refit and repeat
```

## R3 — Flux and luminosity (with errors)

Post-hoc (no parameter error propagation):
```python
AllModels.calcFlux("0.5 10.0 err")     # err -> Monte-Carlo flux errors
val, elo, ehi, *_ = AllData(1).flux
AllModels.calcLumin("0.5 10.0 0.01")   # last arg = redshift
lum, llo, lhi, *_ = AllData(1).lumin
```
Preferred for a fitted flux with proper errors — wrap in `cflux` (a convolution
model whose `lg10Flux` parameter *is* the flux, so `Fit.error` gives its CI):
```python
Model("cflux*tbabs*powerlaw")          # set cflux Emin/Emax, freeze powerlaw norm
Fit.perform(); Fit.error("1.0 <lg10Flux parnum>")
```

## R4 — Steppar (1-D/2-D confidence scan)

```python
Fit.steppar("2 1.5 2.5 20")            # param 2 over [1.5,2.5] in 20 steps
res = Fit.stepparResults("delstat")    # array of Δstat; also "2" for the values
# 2-D contour: Fit.steppar("2 1.5 2.5 20 3 0.05 0.2 20")
```

## R5 — Plot to arrays and to a file

```python
Plot.device = "/null"; Plot.xAxis = "keV"
Plot("ldata", "delchi")
energy, data, model_ = Plot.x(), Plot.y(), Plot.model()
resid = Plot.y(1, 2)                    # panel 2 (delchi) y-values
Plot.device = "/png"; Plot("ldata","delchi")   # also write a figure
```

## R6 — Simulate a spectrum (fakeit)

```python
fs = FakeitSettings(response="resp.rmf", arf="arf.arf",
                    exposure=10000.0, fileName="fake.pha")
Xset.seed = 12345                      # reproducible
AllData.fakeit(1, fs)                  # applyStats=True adds Poisson noise
Fit.perform()
```

## R7 — MCMC posterior (creating a Chain runs it)

```python
Fit.perform()                          # start from the best fit
c = Chain("chain.fits", burn=1000, runLength=10000,
          algorithm="gw", walkers=20)  # __init__ runs the chain
# AllChains now holds it; margins & Fit.error draw on it:
m1, m2 = AllChains.stat(2), AllChains.stat(3)   # marginal stats for a param
```

## R8 — Joint fit of multiple spectra

```python
AllData("1:1 obsA.pha 2:2 obsB.pha")   # 2 spectra, 2 data groups
Model("tbabs*powerlaw")                # params replicate per data group
AllModels(2).powerlaw.PhoIndex.link = AllModels(1).powerlaw.PhoIndex  # tie index
AllModels(2)(3).untie()                # free a linked par if needed
Fit.perform()
```

## R9 — Goodness of fit for C-stat

```python
Fit.statMethod = "cstat"; Fit.perform()
pct = Fit.goodness(1000, sim=True)     # % of sims with stat below observed
```
Do not judge a cstat fit by reduced-statistic ≈ 1 — use `goodness`.

## R10 — Save / restore the whole session

```python
Xset.save("session.xcm", info="a")     # model + data + settings; Tcl: save all
# later:
Xset.restore("session.xcm")
```
