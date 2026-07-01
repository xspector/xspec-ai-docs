---
title: Ingesting a dataset and the two decisions you must get right
audience: agent
priority: 2
verified_against: PyXspec (XSUser/Python/xspec)
---

# Data ingestion + the decisions that silently bias results

Given "a dataset," an agent must (a) discover what files it actually has, (b)
choose the **fit statistic**, and (c) choose the **energy range**. (b) and (c)
have no safe default — getting them wrong produces a fit that runs cleanly and
is wrong.

## 1. What a "dataset" is

The spectrum is a **PHA** file. It usually *references* its calibration and
background in header keywords:

| Keyword | Points to | XSPEC role |
|---|---|---|
| `RESPFILE` | RMF | redistribution matrix (channel ↔ energy) |
| `ANCRFILE` | ARF | effective area |
| `BACKFILE` | background PHA | subtracted / modeled background |
| `TELESCOP`, `INSTRUME` | mission + instrument | picks sensible energy band |

When these keywords are present, `AllData("1:1 src.pha")` **auto-loads** the
RMF, ARF, and background. Only attach them manually when they are missing.

## 2. Inspect before loading

Read the PHA header to learn what you have (mission, exposure, whether response
and background are linked, and whether the data are grouped):

```python
# Fastest: FITS header, no XSPEC state needed
from astropy.io import fits
h = fits.getheader("src.pha", "SPECTRUM")
mission = h.get("TELESCOP"), h.get("INSTRUME")
resp, arf, bkg = h.get("RESPFILE"), h.get("ANCRFILE"), h.get("BACKFILE")
grouped = h.get("GROUPING", 0)   # 1 => grouped; affects statistic choice
```
After loading, confirm via typed attributes. Note `.response` and
`.background` **raise if none is attached** — guard them:

```python
s = AllData(1)
s.exposure                                   # float, always present
rmf = s.response.rmf                          # RMF filename (raises if no response)
try:
    bkg = s.background.fileName               # raises if no background
except Exception:
    bkg = None
```

Manual attach only if needed:
```python
s = AllData(1)
s.response = "resp.rmf"            # Tcl: response resp.rmf
s.response.arf = "arf.arf"         # Tcl: arf arf.arf
s.background = "bkg.pha"           # Tcl: backgrnd bkg.pha
```

## 3. DECISION 1 — the fit statistic

The likelihood must match the data's noise. This is the most common silent error.

| Situation | Statistic | PyXspec | Why |
|---|---|---|---|
| Counts, ≳20–25 per bin (well grouped) | chi-squared | `Fit.statMethod = "chi"` | Gaussian approximation valid |
| Low counts / ungrouped, background-subtracted | **C-stat** | `Fit.statMethod = "cstat"` | Poisson; unbiased at low counts |
| Source + **Poisson background** modeled jointly | W-stat | `Fit.statMethod = "cstat"` with an unsubtracted background loaded | Cash variant for background |

Rules of thumb for an agent:
- **Default to `cstat`** unless the data are demonstrably well-grouped with high
  counts per bin. `cstat` is correct across the low-count regime where `chi`
  is biased; `chi` requires binning that discards resolution.
- Never use `chi` on background-**subtracted** low-count data — subtraction
  breaks the Poisson assumption `cstat` needs, and Gaussian errors are wrong too.
  Keep the background as a loaded background (not subtracted) and use `cstat`.
- With `cstat`, assess fit quality with `Fit.goodness()` (simulations), not the
  reduced statistic — reduced-cstat is not ~1 at a good fit.

## 4. DECISION 2 — the energy range

Always drop bad channels first, then restrict to the instrument's calibrated
band. Fitting outside the calibrated range injects garbage.

```python
AllData.ignore("bad")                 # flagged bad channels
AllData.ignore("**-0.5 8.0-**")       # keep 0.5–8 keV (example: Chandra ACIS)
# Tcl: ignore bad ; ignore **-0.5 8.0-**
```

Per-mission **starting** bands (defer to the instrument's current calibration;
these are sane defaults, not authority):

| Mission / instrument | Typical fit band (keV) |
|---|---|
| Chandra ACIS | 0.5 – 8 |
| XMM-Newton EPIC pn / MOS | 0.3 – 10 |
| NuSTAR (FPMA/FPMB) | 3 – 79 |
| Swift XRT | 0.3 – 10 |
| NICER XTI | 0.3 – 10 (soft sources 0.2–12) |
| Suzaku XIS / HXD-PIN | 0.5–10 / 12–70 |
| RXTE PCA | 3 – 20+ |
| eROSITA | 0.2 – 8 |
| XRISM Resolve / Athena X-IFU | 0.3 – 12 |

Notes:
- `ignore`/`notice` ranges are in the units of `AllData.ignore`'s argument
  (`**` = the array end). Set `Plot.xAxis` separately for display.
- For grouped-then-`chi` workflows, group to your minimum counts *before* loading
  (e.g. with `ftgrouppha`/`grppha`), not inside XSPEC.

## 5. Abundances and cross-sections affect absorption

Absorption (`tbabs`, `phabs`) and plasma (`apec`, …) models depend on the
abundance table and photoionization cross-sections. Set and record them:

```python
Xset.abund = "wilm"     # Tcl: abund wilm   (tbabs' reference table)
Xset.xsect = "vern"     # Tcl: xsect vern
```
`tbabs` in particular assumes `abund wilm` to reproduce its published model.

## 6. Multiple spectra and data groups

```python
AllData("1:1 obs1.pha 2:2 obs2.pha")   # two spectra, two data groups
# "1:1 ... 2:1 ..." would put both in ONE data group (shared model).
```
Data-group index controls which spectra share model parameters; get it right
before defining the model. `AllData.nSpectra`, `AllData.nGroups` confirm.

## 7. Ingestion checklist (agent)

1. Read PHA header → mission, exposure, RESPFILE/ANCRFILE/BACKFILE, GROUPING.
2. `AllData("1:1 src.pha")`; verify response + background attached.
3. `AllData.ignore("bad")` then the mission band.
4. Choose statistic (default `cstat`; `chi` only if well-grouped high counts).
5. Set `Xset.abund` / `Xset.xsect` if using absorption/plasma models.
6. Only now define the model and fit (see guide 01).
