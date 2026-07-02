---
name: xray-fit
description: >-
  Perform X-ray spectral analysis with XSPEC/PyXspec end-to-end: inspect a
  spectrum, choose the statistic and energy range, fit a model, check fit
  quality, compute errors/flux, and export a reproducible script. Use whenever
  the user wants to fit or analyze an X-ray spectrum (a PHA/PI/PHA2 file), model
  a source (power law, apec, blackbody, absorbed continuum, etc.), or mentions
  XSPEC or PyXspec spectral fitting. Drives the xspec-ai-docs (reference) and
  xspec-run (execution) MCP servers.
---

# X-ray spectral fitting

Run a disciplined analysis using the two MCP servers. **Do not answer from
memory or hand-write PyXspec** — use the tools: the reference server is
authoritative, and the execution server runs a real, verified PyXspec session.

If either server's tools are unavailable, say so and stop — do not fall back to
free-hand scripts.

## Golden rules

- **Never invent a name.** Before using any model, command, statistic, xset key,
  or abundance table, confirm it with `validate` (xspec-ai-docs). If unsure which
  model fits, use `get_model` / `list_models` / `lookup_intent`.
- **Choosing the statistic and energy range is a decision, not a default** — get
  them right (step 3) or the fit is silently wrong.
- **Never trust a fit you haven't assessed.** Always run `assess_fit` and act on
  its `issues` before reporting parameters.
- **Deliver a reproducible artifact** — end with `export_script`.

## Procedure

1. **Orient (reference server).** If you need the workflow or a model's
   parameters, pull `get_guide("00_object_model")`, `get_guide("02")`
   (ingestion + decisions), and `get_model(<name>)`. Use `lookup_intent("...")`
   to find the exact call for any step.

2. **Inspect the data (xspec-run `pha_info`).** Learn the mission/instrument,
   exposure, whether RESPFILE/ANCRFILE/BACKFILE are linked, whether it's already
   grouped, and the total counts. This drives the next two decisions.

3. **Decide — the two that matter:**
   - **Statistic:** default `cstat` (correct across the low-count regime). Use
     `chi` *only* for data with high counts per bin that are already well
     grouped. Never `chi` on background-subtracted low-count data.
   - **Energy range:** always `ignore bad` plus the instrument's calibrated band
     (from `pha_info`'s mission; e.g. NuSTAR 3–79, XMM/Swift/NICER ~0.3–10,
     Chandra ~0.5–8). Fitting outside it injects garbage.
   - If the data are ungrouped and you need `chi`, `group_spectrum` first.

4. **Load (xspec-run).** `reset_session`; `load_data(pha, rmf=?, arf=?, back=?,
   energy_range="**-LO HI-**")` — attach responses only if `pha_info` showed
   them missing; set the statistic via `fit`'s argument or `set_parameter`
   workflow.

5. **Model.** `validate` each component name, then `define_model(expr)`. Set
   physically sensible starting values with `set_parameter` (use `get_model`
   limits/defaults). Prepend absorption (`tbabs`) for Galactic column; set
   `Xset.abund`/`xsect` if using absorption/plasma models.

6. **Fit and assess (iterate).** `fit("cstat")`, then **`assess_fit`**. If
   `issues` lists pegged parameters, systematic residuals (runs test), or poor
   goodness: adjust (free/fix/add a component, re-check the band) and refit.
   Repeat until `acceptable` or you can explain the residuals.

7. **Errors and derived quantities.** `error("2.706 <pars>")` for 90% CIs (check
   the status code; re-fit if a new minimum was found). `calc_flux` /
   `calc_lumin` for fluxes; for a flux *with* a real CI, wrap in `cflux`.

8. **Report.** Summarize parameters with CIs, statistic/dof, and flux. Call
   `export_script` and give the user the reproducible PyXspec script; use
   `plot_image` if a figure would help.

## Notes

- Everything runs headless (no GUI): "see" a fit via `plot` arrays or
  `plot_image`, never a plot window.
- For 100% API coverage beyond the structured tools, use `xspec_get` /
  `xspec_set` / `xspec_call`.
- Multiple spectra: call `load_data` repeatedly with increasing `spectrum`
  (and `group`) for a joint fit.
