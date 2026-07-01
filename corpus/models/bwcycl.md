---
name: bwcycl
type: add  # additive
func: c_beckerwolff
n_params: 13
family: [bwcycl]
energy_range: [0., 1.e20]
source: manager/model.dat + XSmodelBwcycl.tex
---

# bwcycl

**additive model** (`add`), function `c_beckerwolff`.

## Description

This is the implementation by Carlo Ferrigno of the model by Becker & Wolff (2007). 
This implementation has been validated in Ferrigno, Becker et al. (2009) 

The original model is described in 
[P. A. Becker & M. Wolff *Thermal and Bulk Comptonization in Accretion-powered X-Ray Pulsars* 2007, ApJ 654, 435B](https://ui.adsabs.harvard.edu/abs/2007ApJ...654..435B/abstract). 

The application details are reported in
[C. Ferrigno, P. A. Becker, A. Segreto, T. Mineo & A. Santangelo, *Study of the accreting pulsar 4U 0115+63 using a bulk and thermal Comptonization model*, 2009, A&A, 498, 825](https://ui.adsabs.harvard.edu/abs/2009A%26A...498..825F/abstract).

This package is also under version control at https://gitlab.astro.unige.ch/ferrigno/bwmodel.

It is mandatory to:

- freeze the model normalization to one;

- set the source distance in kpc;

- set and freeze the neutron star parameters (default values are a good choice);

- select which source terms should be computed.

The computation of the black-body source term is time consuming, because it involves the numerical solution of an integral. Since the contribution of this component is generally negligible, the parameter `BBnorm` should be set to zero and then fixed to one for the final runs. The parameters `FFnorm` and `CYCnorm` should be fixed to one.In principle, it is possible to use untested versions of the model with the `CYCnorm` forced to negative values to mimic an emission around the sonic point.

The mass accretion rate $\dot M$ is strongly degenerate with the accretion column radius and the parameter $\xi$; it is therefore advisable to fix $\dot M$ to a suitable value, which can be derived by equaling the X-ray luminosity to the accretion luminosity or a fraction of it. For a source in which the magnetic field is well above the plasma temperature and the contribution by the cyclotron emission term is minor, it is suggested to link the magnetic field of the continuum model to the one derived by the cyclotron scattering absorption feature(s).

For particular combinations of the parameters, the special functions used in the GSL libraries do not provide a finite value and a ``Not a number'' (`NAN`) is returned to Xspec.
The following parameter constraints avoid most of `NAN` occurrences:

- $\xi\delta<63.7$,
	
- $\xi,\delta < \sim 20$,
	
- $\xi,\delta>\sim0.01$,
	
- $\delta>\sim0.03$ for $\xi>\sim5$,
	
- $T_e > 1.3\,\mathrm{keV}$.

Finally, large values of $r_0>1000$\,km should be avoided.
When a `NAN` is returned the program prints out the parameter values for which this occurred and the contraints can be refined.

It is important to limit the parameter ranges in a customary way and maybe tune the mass accretion rate to a value which keeps these parameters in the range suggested by physical considerations. Equaling the accretion and the X-ray luminosities is not guaranteed to yield meaningful results for all sources.

It is possible to define a derived model as:

`mdefine newbw bwcycl(Radius,Mass,csi,csiDel/(csi+10.85)**1.63,
B,Mdot,Te,r0,D,BBnorm,CYCnorm,FFnorm)`.

in the Xspec prompt or:

`xspec.AllModels.mdefine('newbw bwcycl(Radius,Mass,csi,
csiDel/(csi+10.85)**1.63,B,Mdot,Te,r0,D,BBnorm,CYCnorm,FFnorm)')`

in pyXspec, with the parameter `csiDel` limited between $\sim10^{-4}$ and $\sim10^3$ and $\xi$ from 0.01 to 20.
However, for $\xi>\sim5$, the lower limit of `csiDel` should be increased to about 3. 

This complex setting could permit a safe exploration of the parameter space, while avoiding most of `NAN` in the model computation.

## Parameters

_Authoritative from `model.dat`. Negative fit-delta = frozen; additive models carry an implicit `norm`._

| # | param | unit | default | soft min | soft max | hard min | hard max | delta | note |
|---|-------|------|---------|----------|----------|----------|----------|-------|------|
| 1 | Radius | km | 10 | 5 | 20 | 5 | 20 | 1 | frozen by default |
| 2 | Mass | Solar | 1.4 | 1 | 3 | 1 | 3 | 1 | frozen by default |
| 3 | csi | — | 3 | 0.01 | 20 | 0.01 | 20 | 0.01 |  |
| 4 | delta | — | 1 | 0.01 | 20 | 0.01 | 20 | 0.01 |  |
| 5 | B | 1e12G | 4 | 0.01 | 100 | 0.01 | 100 | 0.01 |  |
| 6 | Mdot | 1e17g/s | 1 | 1e-06 | 1000000 | 1e-06 | 1000000 | 0.01 |  |
| 7 | Te | keV | 5 | 1.3 | 100 | 1.3 | 100 | 0.01 |  |
| 8 | r0 | m | 44 | 10 | 1000 | 10 | 1000 | 0.01 |  |
| 9 | D | kpc | 5 | 1 | 20 | 1 | 20 | 1 | frozen by default |
| 10 | BBnorm | — | 0 | 0 | 100 | 0 | 100 | 1 | frozen by default |
| 11 | CYCnorm | — | 1 | -1 | 100 | -1 | 100 | 1 | frozen by default |
| 12 | FFnorm | — | 1 | -1 | 100 | -1 | 100 | 1 | frozen by default |
| 13 | norm | — | 1 | 0 | 1e+24 | 0 | 1e+24 | 0.01 | implicit norm |

## PyXspec

```python
from xspec import Model
m = Model("bwcycl")
# component: m.bwcycl  (params as attributes)
```
