---
name: sttorus
type: add  # additive
func: c_stokesxitorus
n_params: 13
family: [sttorus]
energy_range: [0., 1.0e20]
source: manager/model.dat + XSmodelStokestorus.tex
---

# sttorus

**additive model** (`add`), function `c_stokesxitorus`.

## Description

This additive model (version 2.0) computes the $0.1$--$100$ keV spectral
and polarization (Stokes $I$, $Q$, $U$) properties of a power-law X-ray
source of arbitrary incident polarization that is reprocessed by an
optically thick, axially symmetric elliptical or circular torus --
representing, e.g., an opaque AGN torus, a broad-line region, or a
super-Eddington accretion funnel around an accreting stellar-mass black
hole or neutron star. The local reflection was precomputed with the
{ STOKES} code for partially ionized, fully neutral, or fully ionized
(Chandrasekhar electron-scattering) surfaces and is interpolated from FITS
tables. No relativistic effects are included and all components are static.

As with the other polarization models, the { Stokes} selector (par12)
set to $-1$ returns, for each spectrum, the quantity named by its
{ Stokes} XFLT keyword (``Stokes:0''$\,=I$, ``Stokes:1''$\,=Q$,
``Stokes:2''$\,=U$); this is the mode used for joint $I,Q,U$ fitting with
the { chistokes} statistic. Setting par12 to $0$--$10$ returns a single
quantity ($I$, $Q$, $U$, $V$, polarization degree or angle, or a normalized
ratio); when par12 is $5$--$10$ the normalization (par13) should be frozen
at unity.

{ Caution.} The public tables have low resolution in the reprocessing
parameters. { beta} (par6) must be held at one of $-2$, $2$, $6$ and not
fitted, and one should not switch between those discrete values, between
the { xi0} regimes ($<0$, $0$--$5$, $\ge5$), between { rhorhoin}
$=-1$ and $1$--$2$, or between { pol_deg} $=-1$ and $0$--$1$ within a
single XSPEC session, as new tables are accumulated in memory at each
switch.

After a fit the `xset` command reports the derived quantities
{ Theta_degrees} (true half-opening angle), { inc_degrees}
(inclination) and { RF} (reflection fraction); and, given the XSET
inputs { NORMVAL}, { D_MPC}, { NH0} and { MASS}, the
$2$--$10$ keV luminosity { L} and the inner-torus distance
{ rho_in_pc} / { rho_in_r_g}. The reflection tables
({ stokes-*-torus.fits}, { stokes-*-ctorus.fits}) and the visibility
files ({ visibility_line*.txt}) are installed in the standard
model-data directory.

References: Podgorn\'y et al. 2022, MNRAS 510, 4723; Podgorn\'y et al.\
2024, MNRAS 530, 2608; Podgorn\'y 2025, A&A 702, A43.

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | PhoIndex | — | 2 | 1.4 | 3 | 1.4 | 3 | 0.05 |  |
| 2 | cos_incl | — | 0.775 | 0.025 | 0.975 | 0.025 | 0.975 | 0.01 |  |
| 3 | trTheta | — | 0.5 | 0 | 1 | 0 | 1 | 0.05 |  |
| 4 | rhorhoin | — | 1.5 | -1 | 2 | -1 | 2 | 0.2 | frozen by default |
| 5 | xi0 | — | 100 | -1000000 | 10000 | -1000000 | 10000 | 5 |  |
| 6 | beta | — | 2 | -2 | 6 | -2 | 6 | 0.5 | frozen by default |
| 7 | N_p | — | 0 | 0 | 1 | 0 | 1 | 0.2 | frozen by default |
| 8 | pol_deg | — | 0 | -1 | 1 | -1 | 1 | 0.005 | frozen by default |
| 9 | chi | deg | 0 | -90 | 90 | -90 | 90 | 1 | frozen by default |
| 10 | pos_ang | deg | 0 | -90 | 90 | -90 | 90 | 1 | frozen by default |
| 11 | zshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.1 | frozen by default |
| 12 | Stokes | — | 1 | -1 | 10 | -1 | 10 | 1 | frozen by default |
| 13 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("sttorus")
# component: m.sttorus  (params as attributes)
```
