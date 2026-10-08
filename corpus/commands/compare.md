---
name: compare
aliases: [xcompare]
also_documents: []
source: XScompare.tex
---

# compare

**compare alternative models against the current one**

**Syntax:** `compare` [`global` | `nest`] <alt> [<alt> ...]

**Syntax:** `compare` `presets`

The `compare` command automates model selection.  It evaluates one
or more user-supplied alternative models against the *current* data,
ignore ranges and fit statistic --- carrying shared parameters over by
name from the current best fit --- and tabulates a model-comparison
statistic for each, with the current model included as a baseline row.
The original model is restored when the command completes (or on any
error), so `compare` is non-destructive: it does not change the
data, the responses, or the fitted model.  A valid `fit` is
required before it can be run.

Each <alt> is one of:

- [`{}<model-expr>`] an inline model expression,
exactly as it would be typed after the `model` command (for example
phabs*powerlaw), *surrounded by braces*.  The braces are
required: they group the expression --- which usually contains spaces and
operators --- into a single command argument; without them `compare`
would read its separate words as separate arguments.  Parameters whose names
match a uniquely named parameter of the current model are carried over from
the current best fit; everything else takes its model.dat default.

- [`@`<file.xcm>] a candidate read from a model file saved
earlier with the `save` `model` command.  The file builds that
candidate's full model *including its own parameter values, limits,
freezes and priors*, giving complete per-model control.
Sourcing is model-only: `data`, `response`, `statistic`
and `ignore` lines in the file are skipped so the noticed data and
statistic are left unchanged.

- [<family> {[}`component` <n>{]} {[}`only` <a,b,...>{]}]
a *preset*: one word that stands for several alternatives (see
*Presets* below).  `component` <n> picks the component the
family acts on when the model has more than one of its members;
`only` restricts the alternatives to the members or values listed.

Shared parameters are matched *by name*, and only names that are
unique within each model qualify --- the ambiguous norm carried
by every additive component is deliberately skipped.  A comparison is
meaningful only under a fixed statistic and identical noticed data, so an
alternative that changes the number of noticed channels is reported and
skipped.

**Presets.** A preset compares the model with its neighbours in
a family of components without typing each alternative.  A
*substitute* family finds the model's member and refits the model with
each other member *in its place*, the rest of the expression unchanged:
on tbabs(diskbb+powerlaw), `compare absorbers` fits
phabs(diskbb+powerlaw), wabs(diskbb+powerlaw), and so on.  A
*variant* family refits the model with each other value of one
parameter or session setting.  The shipped families are

family & kind & members or values 

`absorbers`      & substitute & `tbabs`, `phabs`, `wabs`, `tbfeo`, `tbgrain`, `tbvarabs` 

`zabsorbers`     & substitute & `ztbabs`, `zphabs`, `zwabs`, `zvphabs` 

`pcabsorbers`    & substitute & `pcfabs`, `tbpcf` 

`comptonization` & substitute & `nthcomp`, `comptt`, `compps`, `comptb` 

`disks`          & substitute & `diskbb`, `diskpn`, `ezdiskbb`, `kerrbb`, `kerrd` 

`reflection`     & substitute & `pexrav`, `pexriv`, `pexmon` 

`reflconv`       & substitute & `reflect`, `ireflect`, `rfxconv`, `xilconv` 

`atomic`         & variant    & switch = 1 (mekal), 2 (AtomDB), 3 (SPEX) 

`abund`          & variant    & `abund` `wilm`, `aspl`, `lpgs`, `angr` 

`relxill`        & template   & `relxill`, `relxillCp`, `relxillD` 

`torus`          & template   & MYTorus, borus02, UXClumpy, RXTorusD 

`atomic` acts on any plasma component with a switch
parameter, and on `apec`, which has none, by substituting
`mekal` and `cie`.  `abund` reruns the model under
each other abundance table and puts the session's table back afterwards.
The *template* families are for models XSPEC does not ship: a member
counts only when its local model is loaded (`lmod`) or a user registry
gives its table file; the others are reported as skipped.
`compare` `presets` lists the families and the component of the
current model each would act on.

In a substituted model every parameter outside the swapped component keeps
exactly what it had --- value, freeze, link, prior --- however the parameter
numbers move.  Inside it, parameters that play the same role (N_H, a
photon index, a temperature, a redshift) start from the replaced
component's values; the others start from their model.dat
defaults.  An additive member's normalization is scaled before the fit so
that its folded counts in the noticed band equal the replaced component's,
so every row starts near the data.  Each row is labelled
`<family>: <member>` (`atomic: switch=3 (SPEX)`,
`abund: wilm`); under the table XSPEC names the abundance table the
rows ran under and adds a note for each member whose authors recommend
another table, each member skipped, and each link that could not be carried
into the new component.  Presets and `{}<model-expr>`
or `@`<file.xcm> alternatives can be mixed freely; two presets
give the alternatives of each, not their combinations.

The families are read from compare_presets.dat in the
manager directory, then from $HOME/.xspec/compare_presets.dat
and from the file named by `xset COMPARE_PRESETS`, which can add
families, add members to a shipped one or replace a member.  The format and
the role maps are described in Appendix AppendixAlgorithmsComparePresets.

**Default (information criterion).** With no leading keyword,
each alternative is fit with the current `method` and ranked by
the Akaike and Bayesian information criteria,

$${\rm AIC} = {\rm stat} + 2k, \qquad
  {\rm BIC} = {\rm stat} + k\ln N,$$

where $k$ is the number of free parameters and $N$ the number of noticed
channels.  The table reports the statistic, degrees of freedom, and
$\Delta{\rm stat}$, $\Delta{\rm AIC}$, $\Delta{\rm BIC}$ *relative to
the best-fit (lowest-statistic) row*.  Because the information criteria
penalise free parameters, a simpler model with a comparable statistic can
have a *negative* $\Delta{\rm AIC}$/$\Delta{\rm BIC}$ --- i.e. it is
preferred despite a marginally worse fit.  A shared-parameter shift table
follows, showing how each common parameter moves between models.

**The `global` keyword** fits each alternative with
`fit global` (a derivative-free global optimisation by
Differential Evolution, followed by a polish with the current method)
instead of a plain local fit.  This guards against a stuck local minimum
in one candidate corrupting its AIC/BIC; the table is otherwise identical
to the default.

**The `nest` keyword** replaces the information-criterion
table with a ranking by Bayesian evidence (the marginal likelihood
$\log Z$, see Chapter BayesianMethods).  The current model and every
alternative are explored by nested sampling (`nest`), and the models
are ranked by $\log Z$ rather than by AIC/BIC.  Unlike AIC/BIC --- which
score each model at a single point (its best fit) plus a parameter-count
penalty --- the evidence integrates the likelihood over the prior, so the
Occam penalty is the prior volume itself rather than a count.  This is the
rigorous model-comparison quantity, at the cost of $N+1$ full nested-sampling
runs.

Bayesian inference must be switched on (`bayes` `on`) before
`compare` `nest`, and each model's parameters must have proper,
integrable priors.  Priors are supplied in two ways:

- [Carried by name (default)] the prior type, its hyper-parameters and
the soft limits set on the *current* model are copied by name onto each
inline alternative's matching parameters.  Set the priors you want on the
current model (with `bayes`) before running, and they propagate to the
shared physical parameters (N_H, kT, abundances, same-named norms).

- [Per-candidate via `@`<file.xcm>] a saved-model candidate
carries its own priors and limits, so it is the way to give a comparison
model priors that differ from the current one.  This is the recommended
route whenever the priors matter: define each candidate in its own
`save` `model` file with the priors already set.

As with a standalone `nest` run, if any parameter would be sampled
under a flat prior spanning more than four decades (typical of an
unconstrained normalisation with its default limits) `compare` %
`nest` refuses to run and names the offending parameters.  Give each
a prior (e.g. `bayes` <par> `jeffreys` on a same-named
current-model parameter, or an `@`<file.xcm> candidate that sets
it) or tighten its limits, then retry.  `compare` `nest` uses
the current `nest` settings (`nest live`, `nest tol`,
etc.); `nest live` $200$ trades $\log Z$ precision for speed when
scanning many models, and `parallel nest` $N$ parallelises each run.

The evidence table reports, for each model, $\log Z$ and its uncertainty,
$\Delta\log Z = \log Z - \log Z_{\rm best} \le 0$ relative to the best
(highest-evidence) model, $2\,\Delta\log Z$ on the Kass & Raftery
(1995) scale ($>2$ positive, $>6$ strong, $>10$ decisive evidence against
the model), and the posterior model probability $P(M|D) = Z_i / \sum_j Z_j$
under equal model priors.  The reference row (flagged `*`) is the
highest-evidence model.

**Examples:**

```
XSPEC> compare {powerlaw + gaussian} {bbody}
```

Fit powerlaw+gaussian and bbody against the current data and
compare them to the current model by $\Delta{\rm AIC}$/$\Delta{\rm BIC}$:

```
Model comparison (statistic = cstat, N = 1024 noticed channels):
   #  model                                 stat    dof       dStat        dAIC        dBIC
   1  powerlaw + gaussian                 434.22   1019        0.00       +0.00       +0.00  *
   2  powerlaw (current)                  434.22   1022        0.00       -6.00      -20.79
   3  bbody                            3.472e+07   1022   3.472e+07  +3.472e+07  +3.472e+07
```

Here the added Gaussian does not improve the fit, so the simpler current
powerlaw has the lower (better) AIC and BIC despite the identical
statistic.

```
XSPEC> compare global {tbabs(diskbb+comptt)} {tbabs*relxilllpCp}
```

The same comparison, but each alternative is fit with a global optimiser so
a poor local minimum cannot bias the result.

```
XSPEC> bayes on
XSPEC> bayes 2 jeffreys
XSPEC> fit
XSPEC> nest live 400
XSPEC> compare nest {powerlaw} @bbody_prior.xcm
```

Rank the current model and two candidates by Bayesian evidence.  The inline
powerlaw inherits the current model's Jeffreys prior on the
normalisation by name; the bbody_prior.xcm candidate supplies its
own priors:

```
Model comparison by evidence (nested sampling, statistic = cstat):
   #  model                                ln Z       +/-       dlnZ     2 dlnZ   P(M|D)
   1  powerlaw                          -238.27     0.636      +0.00      -0.00    0.750  *
   2  powerlaw (current)                -239.37     0.652      -1.10       2.20    0.250
   3  @bbody_prior.xcm               -1.736e+07     0.634 -1.736e+07  3.472e+07    0.000
```

The blackbody is decisively rejected and the two power-law fits share the
posterior probability.

```
XSPEC> model tbabs(diskbb+powerlaw)
XSPEC> fit
XSPEC> compare absorbers only phabs,TBfeo
XSPEC> compare disks
XSPEC> compare atomic {tbabs*apec}
```

Refit with `phabs` and `tbfeo` in place of `tbabs`,
then with each other disk model in place of `diskbb` (each started at
`diskbb`'s folded counts).  On a `vmekal` model,
`compare atomic` gives the AtomDB and SPEX rows.

**PyXspec.** The same harness is available as
`Fit.compare(alternatives, method=``'lm'``|`%
`'global'``|``'nest'``)`, which returns
the per-model table as a list of dictionaries (the `nest` method adds
`logZ`, `logZerr`, `deltaLogZ` and `postProb` to
each row).  A preset is given as a string, `"absorbers only phabs,wabs"`,
or as `xspec.ComparePreset("absorbers", component=None, only=["phabs","wabs"])`;
`Fit.comparePresets()` lists the families and
`Fit.loadComparePresets(path)` adds a registry file.
