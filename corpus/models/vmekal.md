---
name: vmekal
type: add  # additive
func: C_vmekal
n_params: 19
family: [mekal, vmekal]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelMekal.tex
---

# vmekal

**additive model** (`add`), function `C_vmekal`.

Variants documented together: `mekal`, `vmekal`.

## Description

An emission spectrum from hot diffuse gas based on the model
calculations of Mewe and Kaastra with Fe L calculations by
Liedahl. The model includes line emissions from several elements. The
switch parameter determines whether spectrum is calculated by
running the mekal code, by interpolating on a pre-calculated mekal
table, or using the AtomDB data. Relative abundances are set by the
`abund` command for the `mekal` model. The
`vmekal` variant allows the user to set the individual
abundances for the model.

For the `mekal` model the parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | kT | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 2 | nH | cm-3 | 1 | 1e-05 | 1e+19 | 1e-06 | 1e+20 | 0.01 | frozen by default |
| 3 | He | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 4 | C | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 5 | N | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 6 | O | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 7 | Ne | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 8 | Na | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 9 | Mg | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 10 | Al | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 11 | Si | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 12 | S | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 13 | Ar | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 14 | Ca | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 15 | Fe | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 16 | Ni | — | 1 | 0 | 1000 | 0 | 1000 | 0.01 | frozen by default |
| 17 | Redshift | — | 0 | -0.999 | 10 | -0.999 | 10 | 0.01 | frozen by default |
| 18 | switch | — | 1 |  |  |  |  |  | switch (not fitted) |
| 19 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("vmekal")
# component: m.vmekal  (params as attributes)
```
