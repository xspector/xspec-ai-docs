# Casebook roadmap — what to author next, and why

The casebook grows case-by-case (PLAN-C §4). This file is the authoring queue: a
ranked list of worked cases to write, each justified by *how often the real
literature does this analysis* and *what judgment trap it teaches*. It is a
living document — reorder as cases land and as new gaps surface.

## Where the priorities come from

The ranking is grounded in a survey of `xspecpapers.bib` — the 500 most recent
refereed papers that cite XSPEC (2025–2026; the bib file itself is kept local,
not tracked in this repo). That is a snapshot of **current practice**, which is
the right prior for what an agent will actually be asked to do. Tallying missions, source types, and analysis themes
(by title + keyword match) gives:

| Source types | n | | Missions | n | | Analysis themes | n |
|---|---:|---|---|---:|---|---|---:|
| AGN (Seyfert/quasar/NLS1) | 112 | | XRISM | 38 | | disk/accretion continuum | 88 |
| NS XRB (LMXB/HMXB/pulsar) | 86 | | XMM-Newton | 22 | | QPO / timing | 41 |
| cluster / ICM | 49 | | Swift | 22 | | winds / outflows / UFO | 37 |
| blazar / jet | 39 | | Chandra | 20 | | state transitions / outbursts | 32 |
| GRB | 32 | | IXPE | 19 | | polarimetry | 27 |
| CV / nova / WD | 22 | | NuSTAR | 18 | | obscuration / absorption | 21 |
| BH XRB | 20 | | Insight-HXMT | 18 | | reflection / Fe K | 20 |
| SN | 20 | | NICER | 16 | | spectral survey / population | 25 |
| SNR | 19 | | eROSITA / EP | 15 | | thermonuclear X-ray burst | 15 |
| TDE | 16 | | AstroSat | 12 | | cyclotron line (CRSF) | 7 |

Two findings the raw counts surface that intuition would miss:

- **XRISM is now the single most-cited mission.** Microcalorimeter judgment —
  *high total counts but few counts per bin* — is a regime the current schema
  (which keys on total counts) cannot express. See case 3 and the lesson it
  spawns.
- **Polarimetry (IXPE, `chistokes`) is mainstream** — 27 papers, a statistic in
  the schema vocabulary with zero cases. Case 7 fills it.

## Coverage state

Seed case: `nicer-lowcount-thermal-001` (isolated NS, `low`, cstat). The
counts-regime grid is otherwise empty; the cases below are chosen partly to fill
it (`vlow`, `mid`, `vhigh`) and to exercise statistics beyond cstat.

| status | meaning |
|---|---|
| ✅ done | authored, validated against a `fakeit` twin, committed |
| 🚧 wip | in progress |
| ⬜ planned | queued |

## Authoring queue

Each case is buildable from a `fakeit` twin using only **built-in** models
(grounding-set safe — deliberately avoiding relxill / MYTorus / borus, which are
external table/local models not in the corpus). Responses currently on hand:
`aciss_aimpt_cy15` (Chandra ACIS-S, soft band) and `ginga_lac` (hard band). Cases
needing other instruments note the response they will require.

1. **✅ Obscured AGN — the flat-Γ trap.** `agn / mid / cstat /
   tbabs*ztbabs*powerlaw`. Fitting an unabsorbed (Galactic-only) power law to an
   obscured Seyfert drives Γ implausibly flat — even *inverted* — to fake the
   low-energy turnover; the missing ingredient is intrinsic absorption, not a
   hard spectrum. Authored as `chandra-obscured-agn-001` (soft-band CCD, where
   the trap is cleanest). Spawns lesson `flat-photon-index-means-absorption`.
   *Fills `mid`.* (112 AGN papers; 21 obscuration.)

2. **✅ Transient afterglow follow-up.** `grb / low / cstat /
   tbabs*ztbabs*powerlaw`, z frozen. The highest-*volume* real workflow — every
   GRB / Einstein-Probe / eROSITA transient gets one. Two traps: chi on ~566
   counts halves the flux behind a spuriously good reduced chi-square; and
   thawing the Galactic column + redshift the data cannot constrain lands a
   false minimum (nH_Gal pegged 0, z wrong). Authored as
   `chandra-grb-afterglow-001` (Chandra ACIS-S soft-band response; workflow
   identical for Swift-XRT / EP / eROSITA). Adds a second evidence case to
   `cstat-below-1k-counts`. *Fills `low` with a non-thermal source.* (32 GRB + 15
   eROSITA/EP transient papers.)

3. **✅ Microcalorimeter line spectroscopy.** `cluster / high-total-vlow-per-bin
   / cstat / bapec`. Trap: "bright source ⇒ chi" is wrong — 27k counts but ~1 per
   bin; chi biases the Fe abundance +40% and the flux −35% behind a reduced χ² of
   0.67, and grouping to rescue chi erases the turbulent-velocity signal. Authored
   as `xrism-cluster-turbulence-001` on the real Resolve Hp response (60000 ch @
   0.5 eV, gate-valve-closed). Spawns lesson
   `counts-per-bin-not-total-drives-statistic`. **Concrete evidence for the
   schema gap** already flagged in [SCHEMA.md](SCHEMA.md) (`counts_regime` is
   total-counts only): this spectrum keys as `high` while the judgment context is
   ~1 count/bin. A per-bin refinement is now motivated, not hypothetical. (XRISM =
   top mission, 38 papers.)

4. **⬜ Cluster ICM abundance.** `cluster / high / chi / tbabs*apec` (or
   `vapec`). Trap: a single-temperature fit to multi-phase gas biases the Fe
   abundance low (the classic "Fe bias"); background *modelling* vs. subtraction
   matters in the outskirts. Spawns `single-temperature-fe-bias`. *Fills part of
   `high`.* (49 cluster papers.)

5. **⬜ BH-XRB state decomposition.** `xrb / vhigh / chi + systematics /
   tbabs*(diskbb+powerlaw)`. Two traps: an additive power law diverging below the
   disk is unphysical (use a convolution — `thcomp`/`simpl`); and at ~10⁶ counts
   *calibration beats statistics* — without a systematic error the χ² is
   meaningless. Spawns `systematics-dominate-above-1e5-counts`. *Fills `vhigh`.*
   (20 BH-XRB + 32 state-transition papers.)

6. **⬜ Cyclotron-line significance.** `xrb / high / chi / cutoffpl*gabs` (Ginga
   or NuSTAR band). Trap: CRSF "detections" that are really continuum curvature —
   and the **F-test is invalid for line significance** (Protassov et al. 2002);
   significance must come from `fakeit` simulations. Spawns
   `ftest-invalid-for-line-significance`. (7 CRSF papers; a live literature
   debate — "the elusive cyclotron line in 4U 1901+03".)

7. **⬜ Spectro-polarimetry.** `xrb / mid / chistokes / polconst*(...)`. Joint
   I,Q,U fitting; trap: fitting Stokes spectra with plain chi, or claiming a
   polarization detection without checking it against the MDP. Fills the
   `chistokes` vocabulary slot. Needs an IXPE response set. (27 polarimetry
   papers.)

8. **⬜ Super-soft TDE, very low counts.** `tde / vlow / cstat /
   tbabs*zashift(bbody)`. Trap: below ~100 counts, bbody vs. diskbb is
   *undecidable* — report kT with honest non-parabolic intervals and refuse the
   model comparison; goodness only via Monte Carlo. *Fills `vlow`.* (16 TDE
   papers.)

9. **⬜ Young SNR — non-equilibrium plasma.** `snr / mid / cstat / tbabs*vnei`.
   Trap: fitting a collisional-*equilibrium* apec to a young remnant misreads kT;
   the ionization timescale τ is a physical parameter, not a nuisance. (19 SNR +
   eROSITA remnant-survey papers.)

10. **⬜ Blazar curvature — nested-model significance.** `agn / high / chi /
    logpar vs. powerlaw`. The other half of the F-test teaching: when the
    F-test *is* admissible (nested, parameter not on a boundary) and when it is
    not. (39 blazar papers.)

Cases 1, 8, and 5 close the counts-regime grid (`mid`, `vlow`, `vhigh`); case 3
exposes the per-bin subtlety the grid cannot express.

## Lessons this queue spawns

Each is a promotable unit that will need a `bench/lessons/<id>.py` harness to
graduate `candidate → validated` (PLAN-C §4, the `fakeit` gate):

| Lesson | From case | Status |
|---|---|---|
| `flat-photon-index-means-absorption` | 1 | **validated** (`bench/lessons/…`) |
| `counts-per-bin-not-total-drives-statistic` | 3 | candidate (harness pending) |
| `single-temperature-fe-bias` | 4 | not yet authored |
| `systematics-dominate-above-1e5-counts` | 5 | not yet authored |
| `ftest-invalid-for-line-significance` | 6, 10 | not yet authored |

## Method

Author top-down; cases 1–3 cover the three most common real requests. Every case
is grounded in a `fakeit` twin with **known truth**, fit both the careless way
and the correct way through the `xspec-run` server, so the numbers in the case
are real fit output and `assess_fit`'s verdict is reproducible — not asserted.
Record the twin recipe in `provenance.synthetic_twin` so anyone can rebuild it.
