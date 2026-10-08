---
name: clmass
type: mix  # mixing
func: U_MIClusterMassModel(Potential)
n_params: 36
family: [clmass, nfwmass, monomass]
energy_range: [0.001, 1.0e20]
source: manager/model.dat + XSmodelClmass.tex
---

# clmass

**mixing model** (`mix`), function `U_MIClusterMassModel(Potential)`.

Variants documented together: `clmass`, `nfwmass`, `monomass`.

## Description

These models are for determining distributions of gravitating mass in spherical, hydrostatic atmospheres. A hot atmosphere is approximated as a set of concentric spherical shells, each containing isothermal gas. The mixing models combine thermal spectra for the shells, with weights determined by the gravitational potential for the model, to produce projected spectra for annular regions centered on a cluster. The models have much in common with the `projct` mixing model, but the gas density distribution is determined by the gravitational potential and the assumption of hydrostatic equilibrium. Details of the models are discussed in 
[Nulsen, Powell & Vikhlinin (2010)](https://ui.adsabs.harvard.edu/abs/2010ApJ...722...55N/abstract) and the `clmass` model explained fully. For the `clmass` model, the gravitating matter density is assumed to be constant in each spherical shell. The `monomass` model is physically identical to `clmass`, but parametrized by the differences in mass densities for adjacent shells to ensure that the gravitating mass density is a non-increasing function of the radius. The `nfwmass` model treats an atmosphere as a nested set of isothermal, spherical shells, but with the Navarro, Frenk & White form for the gravitational potential.

Spectra should be extracted from concentric, circular annuli centered on a cluster (elliptical annuli are rejected). All spectra for one annulus must belong to the same data group, while spectra for distinct annuli must belong to separate data groups. Spectra must be provided for a complete set of annuli filling the range between the innermost and outermost radius. For each model, the inner radius of the innermost annulus is specified as the first model parameter.

To handle cases where the observations do not cover the whole of a cluster, X-ray emission from beyond the inner edge of the outermost annulus may be modeled with an isothermal beta model. This feature is designed to deal with background X-ray emission from parts of a cluster outside the region that has been observed. It adds a model-dependent element to the mass models. When the beta model is used, the pressure is assumed to be continuous between the two outermost shells, but the gravitational potential is ignored for the outermost shell. If the beta model is disabled, the outermost shell is treated like any other.

**Using the models**

The models rely on the XFLT keywords in much the same way as `projct`. Each spectrum must include, at least, the XFLT0001 keyword specifying the outer radius of the corresponding annulus. If present, XFLT0002 must equal XFLT0001 (annuli must be circular). XFLT0003 is ignored. If present, the following pairs of keywords (XFLT0004/5, XFLT0006/7, etc) give ranges of angle that are summed and divided by 360 to determine the fraction of the total annulus covered by a spectrum. Note that the same effect can be achieved by specifying this fraction in the AREASCAL keyword and leaving XFLT0004/5, etc, undefined (this approach provides greater flexibility when there is more than one spectrum in each data group).

It is essential for the models to link the temperature of the thermal model for each shell to the corresponding temperature parameter of the model. All unused shell parameters must be frozen. The norms of the thermal model must be tied (equal) for all shells (which happens by default). The one free norm applies to gas occupying the intersection between the innermost spherical shell and the 3-dimensional cylinder corresponding to the innermost annulus.

The number of shells available in these models is determined solely by the number of entries in `model.dat`. If you need more shells, simply add more shell parameters to `model.dat` (being sure to add them in pairs for `clmass` and `monomass`) and rebuild the models.

**Units**

Lengths can be specified in any unit, but must be consistent. Internal units depend on the length unit. If the physical length corresponding to the unit in XFLT0001 is $u$, then the densities used by the model are in units of $keV / (G \mu m_H u^2)$, where $keV$ is the energy of 1 keV, $G$ is Newton's constant and $\mu m_H$ is the mean mass per particle in the gas.

For `nfwmass`, the normalization constant, `nfwpot`, is $4 \pi G \rho_0 a^2 \mu m_H$ in units of keV. Here, $a$ is the NFW scale length in physical units and $\rho_0$ is the normalizing density for the NFW potential (mass density is $\rho_0 /[r/a (1 + r/a)^2]$).

**Gas Density Note**

Setting `chatter` to 20 and computing the model (eg running `fit`) causes it to dump "squared densities" and "emission measures."  The squared densities apply to the inner edge of each shell and they are in units of the squared density at the inner edge of the innermost shell.

The "Emission measures" are \[ E_{i,j} = _{V_{i,j}} {n_e / n_{e,0}}^2 dV / (4 ) \] where $V_{ij}$ is the intersection between the $i$th shell and the
$j$th cylinder, and $n_{e,0}$ is the density at the inner edge of the innermost shell.  Distances in these integrals are in units of pixels (whatever value is used in the XFLT keywords).  Beware of the factor of $4\pi$ that is omitted from the emission measure integrals (see Atmosphere::tpinteg in Xspec/src/XSFunctions/Mixing/Atmosphere.cxx).

The one free norm, $N$, for the thermal models is the XSPEC norm for the whole of the innermost volume, $V_{0,0}$.  To compute the density at
the inner edge of the innermost shell, note that \[ N = n_{e,0} n_{H,0} 10^{-14} s^3 d_A E_{0,0} (1 + z)^{-2}, \] where $s$ is the pixel size in radians, $d_A$ is the angular diameter distance and $z$ is the redshift.

**Parameters**

The `clmass` model parameters are:

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | rinner | — | 0 |  |  |  |  |  | scale (not fitted) |
| 2 | a | — | 0 | 0 | 1e+20 | 0 | 1e+20 | 0.01 |  |
| 3 | beta | — | 0.7 | 0.17 | 10 | 0.17 | 10 | 0.02 |  |
| 4 | switch | — | 0 |  |  |  |  |  | switch (not fitted) |
| 5 | kTa | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 6 | kTb | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 7 | kTc | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 8 | kTd | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 9 | kTe | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 10 | kTf | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 11 | kTg | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 12 | kTh | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 13 | kTi | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 14 | kTj | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 15 | kTk | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 16 | kTl | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 17 | kTm | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 18 | kTn | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 19 | kTo | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 20 | kTp | keV | 1 | 0.0808 | 79.9 | 0.0808 | 79.9 | 0.01 |  |
| 21 | dena | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 22 | denb | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 23 | denc | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 24 | dend | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 25 | dene | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 26 | denf | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 27 | deng | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 28 | denh | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 29 | deni | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 30 | denj | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 31 | denk | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 32 | denl | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 33 | denm | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 34 | denn | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 35 | deno | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |
| 36 | denp | — | 1e-05 | 0 | 1e+20 | 0 | 1e+20 | 1e-06 |  |

## PyXspec

```python
from xspec import Model
m = Model("clmass")
# component: m.clmass  (params as attributes)
```
