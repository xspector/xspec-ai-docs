---
name: xray-fit
description: >-
  Perform X-ray spectral analysis with XSPEC/PyXspec end-to-end: inspect a
  spectrum, consult a casebook of worked analyses, choose the statistic and
  energy range, fit a model, check fit quality, compute errors/flux, and export
  a reproducible script. Use whenever the user wants to fit or analyze an X-ray
  spectrum (a PHA/PI/PHA2 file), model a source (power law, apec, blackbody,
  absorbed continuum, etc.), or mentions XSPEC or PyXspec spectral fitting.
  Drives the xspec-ai-docs (reference) and xspec-run (execution) MCP servers.
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
- **Consult the casebook.** After inspecting the data, `find_cases` by its
  fingerprint and read the closest with `get_case`. Retrieved lessons are
  *hypotheses* to check against the data (each carries `applies_when` /
  `not_when`), never overrides — `assess_fit` is still the judge.
- **Choosing the statistic and energy range is a decision, not a default** — get
  them right (step 4) or the fit is silently wrong.
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
   grouped, and the total counts. This drives the fingerprint and the next
   decisions.

3. **Consult the casebook (reference server).** From `pha_info`, form the
   fingerprint — mission, counts regime (`vlow` <100 / `low` <1k / `mid` <10k /
   `high` <100k / `vhigh` >100k total counts), and the likely `source_type` —
   and call `find_cases(mission=..., counts_regime=..., source_type=...,
   model=...)`. Read the closest match with `get_case`: it carries the decisions
   (with the alternatives that were rejected and why), the outcome, and the
   cited lessons. Let it inform the steps below; verify each lesson's
   `applies_when` / `not_when` against the data at hand before relying on it. No
   match for a regime is a gap, not an error — proceed on first principles.

4. **Decide — the two that matter:**
   - **Statistic:** default `cstat` (correct across the low-count regime). Use
     `chi` *only* for data with high counts per bin that are already well
     grouped. Never `chi` on background-subtracted low-count data.
   - **Energy range:** always `ignore bad` plus the instrument's calibrated band
     (from `pha_info`'s mission; e.g. NuSTAR 3–79, XMM/Swift/NICER ~0.3–10,
     Chandra ~0.5–8). Fitting outside it injects garbage.
   - If the data are ungrouped and you need `chi`, `group_spectrum` first.

5. **Load (xspec-run).** `reset_session`; `load_data(pha, rmf=?, arf=?, back=?,
   energy_range="**-LO HI-**")` — attach responses only if `pha_info` showed
   them missing; set the statistic via `fit`'s argument or `set_parameter`
   workflow.

6. **Model.** `validate` each component name, then `define_model(expr)`. Set
   physically sensible starting values with `set_parameter` (use `get_model`
   limits/defaults). Prepend absorption (`tbabs`) for Galactic column; set
   `Xset.abund`/`xsect` if using absorption/plasma models.

7. **Fit and assess (iterate).** `fit("cstat")`, then **`assess_fit`**. If
   `issues` lists pegged parameters, systematic residuals (runs test), or poor
   goodness: adjust (free/fix/add a component, re-check the band) and refit.
   Repeat until `acceptable` or you can explain the residuals. A pegged
   parameter *and* a runs-test failure together usually means the model is
   structurally wrong, not badly initialised (see the casebook).

8. **Errors and derived quantities.** `error("2.706 <pars>")` for 90% CIs (check
   the status code; re-fit if a new minimum was found). `calc_flux` /
   `calc_lumin` for fluxes; for a flux *with* a real CI, wrap in `cflux`.

9. **Report.** Summarize parameters with CIs, statistic/dof, and flux. Call
   `export_script` and give the user the reproducible PyXspec script; use
   `plot_image` if a figure would help.

## Notes

- Everything runs headless (no GUI): "see" a fit via `plot` arrays or
  `plot_image` (renders a `.pdf`/`.ps`), never a plot window.
- **Version sanity:** `reset_session` reports the running XSPEC version and
  `corpus_info` (xspec-ai-docs) the version the corpus was generated from. If
  they differ at major.minor, note it — a model or parameter may have changed, so
  the reference could lag the engine; prefer `get_model` over assumptions.
- The casebook is the judgment layer and it grows: `find_cases` also takes free
  `text` (e.g. "background dominated", "F-test") and a `statistic` filter.
- For 100% API coverage beyond the structured tools, use `xspec_get` /
  `xspec_set` / `xspec_call`.
- Multiple spectra: call `load_data` repeatedly with increasing `spectrum`
  (and `group`) for a joint fit.
