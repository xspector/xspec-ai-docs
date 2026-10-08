---
name: datascan
aliases: [xdatascan]
also_documents: []
source: XSdatascan.tex
---

# datascan

**refit the model to other data setups and see how far it drifts**

Refit the current model to each of several alternative data setups -- the
same source extracted in another annulus partition, other annuli or
sectors, another grouping of the same spectrum -- and report how far each
parameter moves from the current fit.

**Syntax:** `datascan` [global] `<@setup1.xcm>` [`<@setup2.xcm>` ]
  [par `<p1>`,`<p2>`,] [coord xflt:`<key>`]
  [file `<name>`]

XSPEC cannot move an annulus boundary or re-extract a spectrum, so every
setup is data you have prepared: a script, in the grammar of a
`save` file, that loads spectra (`data`, `backgrnd`,
`response`, `arf`, `ignore`, ).  The current data
and fit are the first setup; a valid fit is required.  For each setup the
session's spectra are replaced by the setup's, the model is refitted, and
the session is put back afterwards: its data, models, parameter values,
links, priors, error bounds, $\sigma$s, covariance and fit status are all as
they were.  Results stored with the spectra themselves (the last
`flux`, `lumin` and `eqwidth`) go with them, as on any
reload.

Unless the setup script defines a model of its own, the current model is
rebuilt on the setup's data groups and every parameter keeps its role: a
parameter frozen, or linked to its data group 1 copy, in every data group
stays so in every new one, a link within a data group is rewritten for each
new group, and a parameter free in every group is free in every new one.
Priors, the statistic and the fit method carry over, and a
`bayes smooth` prior over every data group is re-made over the
setup's groups at the $\lambda$ in force.  A setup that defines a model is
fitted exactly as it defines it.

There are two ways to compare, chosen from the setups:

- [Profiles.] When a setup has other data groups than the session -- a
  different number, or the same number at other radii -- each per-group
  parameter is a profile against a coordinate.  With `projct` in the
  model the coordinate is the shell's mid-radius, from the XFLT
  `major` keys; otherwise, or to choose another,
  `coord xflt:``<key>` reads the XFLT keyword `<key>` of
  each data group's first spectrum (an annular profile with no
  deprojection, a phase or a time slice).  Each setup starts from the
  current fit interpolated onto its own coordinates, so that it does not
  find a different local minimum instead of a different answer.  Without a
  coordinate such a setup is refused.

- [Group for group.] When every setup has the session's data groups at
  the session's coordinates -- a regrouping, say -- the parameters are
  compared one to one, starting from the current fit's values.

For each setup the report gives its number of data groups, the largest
`projct` condition number and most negative adjacent-shell
correlation (each marked `!` past `xset PROJCT_COND_WARN`
or `PROJCT_CORR_WARN`: an ill-conditioned partition) and its fit
statistic.  It then lists
each reported parameter's value and $1\sigma$ (from the fit covariance) at
each data group, and the drift table: for each parameter and setup, the
largest $|\Delta|/\sigma$ between that setup's values and the current fit's,
where $\sigma$ combines both $1\sigma$s.  In profile mode the coarser of the
two profiles is interpolated onto the finer one's coordinates, inside their
common range.  A drift above 2 is marked `***`: the answer depends
on how the data were set up.  It measures resolution as well as
conditioning -- a coarse partition that cannot follow a steep gradient
drifts where the gradient is -- so read it with the profiles beside it.

`par` names the parameters to report, by name (`kT`),
number within the model (`3`) or either with a model name
(`clus:kT`); the default is every parameter free in every data group
except the normalizations.  A parameter with a single value (tied across
the data groups) is compared as one number per setup.  `global` fits
each setup with `fit global`.  `file` writes every
profile point -- setup, parameter, data group, coordinate, value and
$\sigma$ -- one per line.  The drift table can be read with
`tclout datascan`, and `tclout projct` gives the
conditioning of the current `projct` deprojection.

A setup that will not load or fit is reported as failed and the scan
continues.  The session's spectra must be files on disk, since they are
reloaded at the end, and a `backmodel` must be removed first.

**Examples:**

```
XSPEC> @med.xcm
XSPEC> model projct*apec & 0 & 0 & 0 & 4 & 0.3 & 0.05 & 1
// ... untie kT and norm in data groups 2-6, then
XSPEC> fit
XSPEC> datascan @coarse.xcm @fine.xcm
// The deprojected kT profile from 6 annuli, refitted to 3 and 12
// annuli of the same cluster; drifts above 2 sigma are marked.
XSPEC> datascan @sectors.xcm coord xflt:radius par kT,Abundanc
// An annular profile (no deprojection) against XFLT key radius.
XSPEC> datascan @grouped25.xcm file drift.txt
// The same spectra grouped another way, compared group for group.
```

where coarse.xcm holds, for instance,

```
data 1:1 coarse_a1.pha 2:2 coarse_a2.pha 3:3 coarse_a3.pha
ignore **:**-0.5 8.0-**
```
