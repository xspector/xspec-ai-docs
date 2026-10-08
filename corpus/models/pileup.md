---
name: pileup
type: acn  # pile-up/acn
func: C_pileup
n_params: 7
family: [pileup]
energy_range: [0.001, 1.0e20]
source: manager/model.dat + XSmodelPileup.tex
---

# pileup

**pile-up/acn model** (`acn`), function `C_pileup`.

## Description

CCD pile-up model used for brightish point sources observed by Chandra. This 
is an implementation of the fast pile-up algorithm proposed by John Davis 
(see http://space.mit.edu/ davis/papers/pileup2001.pdf). The frame time 
and maximum number of photons to pile up should be fixed. The grade morphing 
is expressed through a single parameter, alpha, which should be left as a free 
parameter.

`pileup` is a **pile-up** (`acn`) component: unlike a 
convolution model it does not act on the photon spectrum but on the count 
spectrum *after* it has been folded through the response, on the response 
file's ungrouped detector channel grid.  Two photons landing in channels with 
energies $E_1$ and $E_2$ during one frame produce a single event in the 
channel containing $E_1 + E_2$, and the series is summed over 2 to 
max_ph piled photons.  Ignored channels take part (the photons are 
still there), piles whose summed energy falls beyond the last channel are 
lost, and the model energy grid plays no role, so the `energies` command 
is not needed.  The component acts on the sum of the components it 
multiplies: `pileup*wabs*pow + gauss` piles the power law only, 
`pileup*wabs*(pow + gauss)` both.  Only one `pileup` 
component is allowed in a model, it must be the first component of its term 
(nothing may multiply the piled count spectrum), and the spectrum it applies 
to must use an ordinary RMF (with or without an ARF); a dummy response is 
refused.

Because the pile-up is applied after folding, `flux`, `lumin` and 
`eqwidth` report the unpiled source model and the component need not 
be removed to use them.  `renorm` is skipped for a model containing 
`pileup`, since the predicted count rate is not linear in the 
normalizations.  Additive components shown by `setplot add` are 
the unpiled contributions; only the total model is piled.  When table-model 
uncertainties are in use, each grouped bin's model variance is scaled by the 
square of its piled-to-unpiled ratio.

After every evaluation the model publishes two diagnostics as model strings 
(see `xset`): `PILEUP_$n$_PILEFRAC`, the fraction of the 
observed events in spectrum $n$ that are piles of two or more photons, and 
`PILEUP_$n$_FRAMEOCC`, the mean number of detected photons per 
region per frame.

Versions before 13.0.1 applied the series to the photon spectrum multiplied 
by the effective area, assuming a uniform model energy grid.  On the 
non-uniform energy grids of real response matrices that mis-binned the piled 
photons and lost a large fraction of the piled hard tail (25% of the 
5--7 keV band at 0.6 photons per frame on an ACIS response), and a linear 
grid set with `energies` gave undefined results; fits with the old 
model should be repeated.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | fr_time | s | 3.2 | 0 | 100 | 0 | 100 | 0.01 | frozen by default |
| 2 | max_ph | — | 5 | 1 | 20 | 1 | 20 | 0.01 | frozen by default |
| 3 | g0 | — | 1 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 4 | alpha | — | 1 | 0 | 1 | 0 | 1 | 0.01 |  |
| 5 | psffrac | — | 0.95 | 0 | 1 | 0 | 1 | 0.01 | frozen by default |
| 6 | nregions | — | 1 |  |  |  |  |  | scale (not fitted) |
| 7 | fracexpo | — | 1 |  |  |  |  |  | scale (not fitted) |

## PyXspec

```python
from xspec import Model
m = Model("pileup")
# component: m.pileup  (params as attributes)
```
