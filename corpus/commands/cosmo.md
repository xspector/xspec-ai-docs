---
name: cosmo
aliases: [xcosmo]
also_documents: []
source: XScosmo.tex
---

# cosmo

**set the cosmology**

Set the cosmology used (i.e., $H_0$, $q_0$, and $\Lambda_0$).

**Syntax:** `cosmo` <$H_0$> <$q_0$> <$\Lambda_0$>

where `<$H_0$>` is the Hubble constant in km/s/Mpc, `<$q_0$>`
is the deceleration parameter, and `<$\Lambda_0$>` is the cosmological constant.
If the cosmological constant is non-zero then at present XSPEC requires that 
the universe is flat. In this case the value of `<$q_0$>` will be ignored
and XSPEC will assume that $\Omega_{matter}\geq 1-\Lambda_0$.  The default values
are `<$H_0$>` = 70, `<$q_0$>` = 0.0, and `<$\Lambda_0$>` = 0.73

**Examples:**
  
`XSPEC12> cosmo 100`
`// Set <$H_0$> = 100 km/s/Mpc`
`XSPEC12> cosmo ,0`
`// Set <$q_0$> = 0`
`XSPEC12> cosmo ,,0.7`
`// Set a flat universe with <$\Lambda_0$> = 0.7`
