---
title: Choosing and combining models
audience: agent
priority: 6
verified_against: component types counted from model.dat corpus
---

# Model selection & composition

## The four component types (composition rules)

Model.dat classifies every model; counts in this corpus:

| Type | Code | Count | Role | Valid alone? |
|---|---|---|---|---|
| Additive | `add` | 228 | emission — a source spectrum; carries a `norm` | yes |
| Multiplicative | `mul` | 75 | multiplies the spectrum bin-by-bin (absorption, edges) | **no** |
| Convolution | `con` | 24 | transforms the spectrum (smooth, shift, flux-set, blur) | **no** |
| Pile-up (acn) | `acn` | 1 | detector pile-up (`pileup`) | special |

Rules:
- A model expression **must contain at least one additive** component — that is
  the thing being emitted. `mul` and `con` only modify it.
- Multiplication binds tighter than addition; use parentheses:
  `tbabs*(apec + powerlaw)` absorbs both, `tbabs*apec + powerlaw` does not.
- Convolution acts on **everything to its right within its parentheses**:
  `gsmooth*(apec+powerlaw)` broadens both; `cflux*powerlaw` sets the power-law
  flux. Place `cflux`/`cpflux` carefully — they set the flux of what they wrap.
- Check a name's type in `manifest.json` before composing.

## Common building blocks (present in this corpus)

- **Absorption (`mul`):** `tbabs` (ISM, modern; assumes `abund wilm`), `phabs`
  (simpler), `wabs` (legacy — avoid for new work), `ztbabs`/`zphabs`
  (redshifted), `pcfabs`/`zxipcf` (partial covering / ionized), `cabs`
  (Compton).
- **Continuum (`add`):** `powerlaw`, `cutoffpl` (cut-off PL), `bbody`/`bbodyrad`
  (blackbody), `diskbb` (multicolor disk), `bremss` (thermal brems),
  `nthComp`/`comptt` (Comptonization).
- **Plasma / lines (`add`):** `apec`/`vapec`/`vvapec` (CIE, AtomDB), `mekal`,
  `gaussian`/`zgauss` (line), `bapec` (velocity-broadened).
- **Convolution (`con`):** `cflux`/`cpflux` (set flux/photon-flux), `gsmooth`
  (Gaussian broaden), `zashift`/`vashift` (redshift/velocity shift), `kdblur`
  (relativistic blur), `partcov` (turn a `mul` into partial-covering), `thcomp`
  (Comptonization convolution), `reflect` (reflection).

## Picking a starting model by source class

| Source | Reasonable first model |
|---|---|
| AGN / X-ray binary (power-law-like) | `tbabs*powerlaw` (+ `zgauss` for Fe Kα) |
| Cut-off / Comptonized corona | `tbabs*nthComp` or `tbabs*cutoffpl` |
| Thermal accretion disk | `tbabs*diskbb` (+ `powerlaw`) |
| Cluster / diffuse hot gas | `tbabs*apec` (or `vapec` for abundances) |
| Supernova remnant (NEI) | `tbabs*(vnei/vpshock)` |
| Absorbed + reflection | `tbabs*(powerlaw + reflect*powerlaw)` or `relxill` family |

## Workflow

1. Identify the physical regime → pick one additive continuum.
2. Prepend absorption (`tbabs`) almost always (Galactic column at minimum).
3. Add lines/reflection/extra continua as additive terms as residuals demand.
4. Use convolution models (`cflux`, `gsmooth`, blurring) for derived quantities
   or physical broadening — not as standalone components.
5. Compare alternatives with `Fit.ftest(...)` / `Fit.compare(...)` rather than
   eyeballing the statistic; watch for degeneracies (`fit global` reports
   competitive basins).
