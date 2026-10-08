---
name: zTBred
type: mul  # multiplicative
func: C_ztbred
n_params: 5
family: [tbred, ztbred]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelTbred.tex
---

# zTBred

**multiplicative model** (`mul`), function `C_ztbred`.

Variants documented together: `tbred`, `ztbred`.

## Description

The `tbabs` X-ray absorption multiplied by IR/optical/UV
extinction from the same column, so a fit to X-ray and optical/UV data
(Swift UVOT, XMM-Newton OM, or flux points loaded as spectra) constrains one
absorber rather than two. The visual extinction is
\[
A_V = N_H{NH_AV},  E(B-V) = A_V{R_V},
\]
with $N_H$ the `tbabs` column and NH_AV the gas-to-dust ratio
$N_H/A_V$ in units of $10^{21}$ cm$^{-2}$ mag$^{-1}$. NH_AV is frozen by
default but can be fitted, which measures the ratio along the line of sight.
The *law* switch selects the extinction curve:
1 = [Cardelli, Clayton & Mathis (1989)](https://ui.adsabs.harvard.edu/abs/1989ApJ...345..245C/abstract)
(the `redden` curve, here with $R_V$ free: $A_\lambda = A_V\,(a(x) +
b(x)/R_V)$), and 2, 3, 4 = the Milky Way, LMC and SMC curves of
[Pei (1992)](https://ui.adsabs.harvard.edu/abs/1992ApJ...395..130P/abstract) (the `zdust`
curves). With $R_V = 3.1$ and law 1 the model is exactly
`tbabs`$\times$`redden` with $E(B-V) = N_H/(\mathrm{NH\_AV}\,
R_V)$; with laws 2--4 it is exactly `tbabs`$\times$`zdust`.

The reddening factor is 1 shortward of each curve (wavelengths below
909  for Cardelli and 800  for Pei), so with X-ray data alone
`tbred` is identical to `tbabs` and NH_AV and $R_V$ have no
effect; the link matters only when optical/UV bins are in the fit.

**The NH_AV default assumes `abund wilm`.** The default,
2.87, is the ratio [Foight et al. (2016)](https://ui.adsabs.harvard.edu/abs/2016ApJ...826...66F/abstract)
measured with `tbabs` and Wilms abundances. A published ratio is
tied to the absorption model and abundance table used to measure $N_H$, so
set NH_AV to match the `abund` setting; when the table is not
`wilm` the model notes this once per table. Published values:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | nH | 10^22 | 1 | 0 | 100000 | 0 | 1000000 | 0.001 |  |
| 2 | NH_AV | 10^21 | 2.87 | 0.5 | 10 | 0.1 | 100 | 0.01 | frozen by default |
| 3 | R_V | — | 3.1 | 2 | 6 | 1 | 10 | 0.01 | frozen by default |
| 4 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 5 | law | — | 1 |  |  |  |  |  | switch (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("zTBred*powerlaw")
# component: m.ztbred  (params as attributes)
```
