---
name: stdisc
type: add  # additive
func: c_stokesnidisc
n_params: 9
family: [stdisc]
energy_range: [0., 1.0e20]
source: manager/model.dat + XSmodelStokesdisc.tex
---

# stdisc

**additive model** (`add`), function `c_stokesnidisc`.

## Description

This additive model computes the spectral and polarization (Stokes $I$,
$Q$, $U$) properties of a power-law X-ray source of arbitrary incident
polarization that is reprocessed by distant, nearly neutral, equatorial
regions of a geometrically thin, optically thick accretion disc around a
black hole. The local reflection was precomputed with the { STOKES}
code and is interpolated from FITS tables for any primary polarization
state. No relativistic effects are included and all components are static.

The model is designed for joint fitting of the three Stokes spectra. With
the { Stokes} selector (par8) set to $-1$, the quantity returned for
each spectrum is taken from its { Stokes} XFLT keyword
(``Stokes:0''$\,=I$, ``Stokes:1''$\,=Q$, ``Stokes:2''$\,=U$), the same
convention used by the { polconst} model and the { chistokes}
statistic. Setting par8 to an integer $0$--$10$ instead returns a single
quantity ($I$, $Q$, $U$, $V$, polarization degree or angle, or a
normalized Stokes ratio), which is convenient for plotting the model
against a dummy response. When par8 is $5$--$10$ the normalization (par9)
should be frozen at unity.

After evaluation the derived inclination { inc_degrees}
($\arccos(\mathtt{cos\_incl})$ in degrees) can be retrieved with the
`xset` command. The reflection tables
({ stokes-neutral-iso-*-disc.fits}) are installed in the standard
model-data directory.

References: Podgorn\'y et al. 2022, MNRAS 510, 4723; Podgorn\'y et al.\
2024, MNRAS 530, 2608.

The parameters are :

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Size | — | 0.3 | 0.1 | 1 | 0.1 | 1 | 0.01 |  |
| 2 | PhoIndex | — | 2 | 1.4 | 3 | 1.4 | 3 | 0.1 |  |
| 3 | cos_incl | — | 0.775 | 0.025 | 0.975 | 0.025 | 0.975 | 0.01 |  |
| 4 | pol_deg | — | 0 | 0 | 1 | 0 | 1 | 0.01 |  |
| 5 | chi | deg | 0 | -90 | 90 | -90 | 90 | 5 |  |
| 6 | pos_ang | deg | 0 | -90 | 90 | -90 | 90 | 5 | frozen by default |
| 7 | zshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.1 | frozen by default |
| 8 | Stokes | — | 1 | -1 | 10 | -1 | 10 | 1 | frozen by default |
| 9 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("stdisc")
# component: m.stdisc  (params as attributes)
```
