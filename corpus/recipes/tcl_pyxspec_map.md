# Tcl ↔ PyXspec map (prototype slice)

Bidirectional lookup between interactive XSPEC (Tcl) commands and the PyXspec
API. Agentic code should prefer PyXspec (typed returns, exceptions instead of
blocking prompts). Signatures taken from `XSUser/Python/xspec/*.py`.

| Interactive Tcl | PyXspec | Notes |
|-----------------|---------|-------|
| `data 1:1 src.pha` | `AllData("1:1 src.pha")` or `Spectrum("src.pha")` | RMF/ARF/back auto-loaded from PHA header if present |
| `response resp.rmf` | `AllData(1).response = "resp.rmf"` | only needed if not in PHA header |
| `arf arf.arf` | `AllData(1).response.arf = "arf.arf"` | |
| `backgrnd bkg.pha` | `AllData(1).background = "bkg.pha"` | |
| `ignore bad` | `AllData.ignore("bad")` | |
| `ignore **-0.5 10.0-**` | `AllData.ignore("**-0.5 10.0-**")` | energy range trim |
| `model tbabs*powerlaw` | `Model("tbabs*powerlaw")` | returns a `Model` |
| `newpar 1 0.1` | `AllModels(1)(1).values = 0.1` | one parameter |
| `freeze 1` / `thaw 1` | `AllModels(1)(1).frozen = True/False` | |
| `statistic cstat` | `Fit.statMethod = "cstat"` | choose before fitting |
| `query yes` | `Fit.query = "yes"` | **required for headless runs** |
| `fit` | `Fit.perform()` | |
| `error 1` | `Fit.error("1")` | confidence intervals |
| `tclout stat` | `Fit.statistic` | typed float, no string-scraping |
| `tclout dof` | `Fit.dof` | |
| `tclout param 1` | `AllModels(1)(1).values` | |
| `flux 0.5 10.0` | `AllModels.calcFlux("0.5 10.0")` then `AllData(1).flux` | |
| `plot data resid` | `Plot("data","resid")` then `Plot.x()/y()/model()` | extract arrays; no GUI needed |
