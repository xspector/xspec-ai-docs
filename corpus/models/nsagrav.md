---
name: nsagrav
type: add  # additive
func: nsagrav
n_params: 4
family: [nsagrav]
energy_range: [.05, 10.]
source: manager/model.dat + XSmodelNsagrav.tex
---

# nsagrav

**additive model** (`add`), function `nsagrav`.

## Description

This model provides the spectra emitted from a nonmagnetic hydrogen
atmosphere of a neutron star with surface gravitational acceleration
$g$ ranging from $10^{13}$ to $10^{15}$ cm/s$^2$, allowed by equations
of state for the neutron star matter (the `nsa` model gives
the spectra calculated for $g = 2.43\times 10^{14}$ cm/s$^2$). The
uniform surface (effective) temperature is in the range of $\log
T_{eff}(K) = 5.5 - 6.5$. The atmosphere is in radiative and
hydrostatic equilibrium; sources of heat are well below the
atmosphere. The radiative force and electron heat conduction are
included in the models, but they are of no importance in the specified
ranges of $T_{eff}$ and $g$. The model spectra are provided as seen by
a distant observer, with allowance for the GR effects.

The neutron star mass $M$ and radius $R$ determine the redshift parameter,

$$g_r = \\sqrt{1-2.952\times M/R}$$

and the gravitational acceleration at the surface,

$$g = 1.33\times10^{16}\times M/R^2/g_r$$

cm/s$^2$, where $M$ is in units of solar mass, and $R$ is in km. 

The allowed domain in the $M$--$R$ plane corresponds to $g_r^2 > 1/3$
and $10^{13} < g < 10^{15}$ cm/s$^2$. (This domain is restricted by
the solid curves in the figure). If chosen $M$ and $R$ values
correspond to $g_r$ or/and $g$ values outside the allowed domain, then
the code sets the latter to be the closest limiting values (e.g., if
one chooses $M = 2$, $R = 8$, then the code will use $g_r = 3 - 1/2 =
0.578$ instead of $g_r = 0.512$ corresponding to the $M$ and $R$
chosen), which would lead to unphysical results.

The values of the effective temperature and radius as measured by a
distant observer (``values at infinity'') are:

$$T_{inf} = g_r\times T_{eff}, R_{inf} = R/g_r$$

The `nsagrav` model may be useful for putting constraints on $M$
and $R$ from spectral fits to thermal emission detected from neutron
stars, provided the quality of the observational data are good enough
to warrant a detailed analysis. The parameters $M$ and $R$ can be fixed at
specific values or allowed to vary within a reasonable range (see the
note above). For example, one can run spectral fits on a $M$--$R$ grid
(using the `steppar` command) within the allowed parameter domain (see
above).

Please send your comments/questions (if any) to Slava Zavlin
([vyacheslav.zavlin@msfc.nasa.gov](mailto:vyacheslav.zavlin@msfc.nasa.gov)) and/or George Pavlov
([pavlov@astro.psu.edu](mailto:pavlov@astro.psu.edu)). If you publish results obtained using this
model please reference [Zavlin et al. (1996)](https://ui.adsabs.harvard.edu/abs/1996A%26A...315..141Z/abstract).

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | LogT_eff | K | 6 | 5.5 | 6.5 | 5.5 | 6.5 | 0.001 |  |
| 2 | NSmass | Msun | 1.4 | 0.3 | 2.5 | 0.3 | 2.5 | 0.001 |  |
| 3 | NSrad | km | 10 | 6 | 20 | 6 | 20 | 0.001 |  |
| 4 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("nsagrav")
# component: m.nsagrav  (params as attributes)
```
