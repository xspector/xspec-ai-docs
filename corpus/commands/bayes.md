---
name: bayes
aliases: [xbayes]
also_documents: []
source: XSbayes.tex
---

# bayes

**set up for Bayesian inference**

 p{} p{---6}}
**Syntax:** & **bayes** & `<option>`

                 & **bayes** & `<mod par #>  <prior type>  [<hyperparameters>]`

                 & **bayes** & `smooth  <par>  [order `1|2`]  [space `lin| log`]  [lambda <value> | lcurve | discrep]  [radii <r$_1$> ... <r$_N$>]`

                 & **bayes** & `smooth clear`

                 & **bayes** & `fuzzy  <par>  <par> ...  [tolerance <t>]  [ratio <c>]`

                 & **bayes** & `fuzzy clear`

where `<option>` ::= `[off | on | cons]`. If a 
parameter number is given as the first argument then this command sets up 
the prior for the specified model parameter but does not turn Bayesian 
inference on.  A data parameter (see `dmodel`) is given as `d`$n$,
for example `bayes d1 lognormal 1 0.1`. If the first argument to the `bayes` command is not a 
parameter number then one of the options `off`, `on`, or 
`cons` is used.  The first two turn Bayesian inference off or on, 
while `cons` turns Bayesian inference on and gives all parameters a 
constant prior. The options for prior types are as follows:

 \

|}
Prior type & Log(prior)

cons & 0

exp & $-p/h_1-\ln{(h_1)}$

jeffreys & $-\ln{(p)}$

gauss & $-0.5\ln{(2\pi h_2)}-0.5(h_1-p)^{2}/h_2^{2}$

lognormal & $-\ln{(p \sqrt{2\pi} h_2)} -0.5(\ln{(p)}-\ln{(h_1)})^{2}/h_2^{2}$

gamma & $h_1\ln{(h_2)} + (h_1-1) \ln{p} - h_2 p -
\ln{\Gamma(h_1)}$

cauchy & $-\ln{(1+(p-h_1)^2/h_2^2)} - \ln{\pi} - \ln{h_2}$ 

beta & $(h_1-1)\ln{x} + (h_2-1)\ln{(1-x)} - \ln{\Gamma(h_1+h_2)} -
\ln{\Gamma(h_1)} - \ln{\Gamma(h_2)}$ 

studentst & $\ln{\Gamma((h_1+1)/2)} - 0.5\ln{(h_1\pi)} -
\ln{\Gamma(h_1/2)} - ((h_1+2)/2)\ln{(1+p^2/h_1)}$ 

halfnormal & $-0.5\ln{(h_1^2\pi/2)} - p^2/(2h_1^2)$ 

powerlaw & $-h_1\ln{(p)} - \ln{Z}$ for $h_2 \le p \le h_3$, where the prior
density is $p^{-h_1}/Z$ and $Z = (h_3^{1-h_1}-h_2^{1-h_1})/(1-h_1)$, or
$\ln{(h_3/h_2)}$ when $h_1=1$
 
isotropic & $\ln{(\sin{(p)})} + \ln{(\pi/360)}$, with p in
degrees over $[0,180]$
 
shiftedlognormal & $-\ln{((p-h_1) \sqrt{2\pi} h_3)} -0.5(\ln{(p-h_1)}-\ln{(h_2)})^{2}/h_3^{2}$

 \

Where p is the parameter value, h$_{\#}$ the
hyperparameter values, and for the beta prior x = (p-min)/(max-min)
where min and max are the parameter hard limits.

 \

**Multi-parameter smoothness prior.** The priors above act on one
parameter at a time. The `bayes` `smooth` subcommand instead
applies a single prior that *couples* a chosen model parameter
<par> (its local index within the model) across all datagroups, penalising
shell-to-shell roughness of that parameter. It is the in-engine regularizer for
`projct` de-projection, where the per-datagroup normalisations (or
temperatures) recovered by inverting the projection are noisy and
anti-correlated; see the `projct` model description for the underlying
failure modes. The prior is a correlated Gaussian

$$\ln p = -\tfrac{1}{2}\,\lambda\,\lVert L\,q\rVert^{2},
  \qquad q_k = p_k\ (\texttt{lin})\ \ \text{or}\ \ \ln p_k\ (\texttt{log}),$$

where the sum runs over the datagroups, L is a spacing-aware
finite-difference operator built from the shell radii, and $\lambda$ is the
regularisation strength. The options are:

- [`order` `1|2`] `1` penalises the gradient of
the profile (biasing towards a flat profile); `2` penalises the curvature
(biasing towards a power-law-like profile). Default `2`.

- [`space` `lin| log`] whether the operator acts on the
parameter (`lin`) or its logarithm (`log`). Default `log`,
appropriate for normalisations that vary over orders of magnitude.

- [`lambda` `<value>` | `lcurve` |\
`discrep`] a fixed strength `<value>`; or `lcurve` to select
it automatically at the corner of the misfit-versus-roughness L-curve; or
`discrep` to select it by the discrepancy principle (increase the
smoothing until the data misfit reaches the number of degrees of freedom). The
`lcurve` and `discrep` options refit the model over a grid of
$\lambda$ and leave the model fitted at the chosen value.

- [`radii` `<r$_1$>` ... `<r$_N$>`] the shell radii, one per
datagroup. If omitted they default to the XFLT `major` axis of each
datagroup (the `projct` convention), so cluster users need not re-enter
them.

The smoothness term is consumed by the same machinery as the per-parameter
priors, so it regularises Levenberg--Marquardt fits, the error calculation, and
all four samplers (under `nest` it is sampled through a spectral
transform of its rank-deficient precision). The members must be free,
unlinked, and free of a per-parameter prior. `bayes` `smooth clear`
removes all smoothness terms (as does `bayes` `cons`). Registered
terms are written to `save` files and listed by `show` `bayes`.

**Fuzzy links.** A hard link (`newpar` `5 = 2`) makes
two parameters identical. `bayes` `fuzzy` instead makes them equal
*to within a tolerance*: it is a joint prior under which each pair of the
listed parameters has a log ratio drawn from a Gaussian of standard deviation
$\sigma = \ln(1 + t)$, the common level being left free. The parameters are
named as for `newpar` (`5`, `mod:3`) and may belong to any
models and data groups, but each must be free, unlinked, positive, free of a
per-parameter prior and not already in another joint term.

- [`tolerance` $t$] relative; the default, 0.2, means ``equal to
  within 20%''.

- [`ratio` $c$] for exactly two parameters, the expected value of the
  first divided by the second (default 1).

For example `bayes` `fuzzy 4 8 12 tolerance 0.1` ties three
cross-normalisation constants to within 10% of one another, and
`bayes` `fuzzy 2 5 ratio 2` expects parameter 2 to be twice
parameter 5. Like `smooth`, adding a link turns Bayesian inference on,
and the link acts in fits, error calculations and all four samplers.
`bayes` `fuzzy clear` removes all fuzzy links and leaves smoothness
terms alone (`bayes` `smooth clear` likewise leaves fuzzy links);
`bayes` `cons` removes both.
