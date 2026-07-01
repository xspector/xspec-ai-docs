---
name: statistic
aliases: [xstatistic]
also_documents: []
source: XSstatistic.tex
---

# statistic

**change the objective function (statistic) for the fit**

Change the fit or test statistic in use, for one or more spectra.

}
**Syntax:** & **statistic** & `[chi | cstat[#[b]] |
lstat | pgstat | pstat | whittle[#] | chistokes | chicov]
[<weight method>] [<spectrum range>]`

& **statistic test** & `[ad | chi | cvm | ks |
 pchi | runs] [<weight method>] [<spectrum range>]`

The fit statistic options are chi-squared (`chi`), C statistic
(`cstat`, note that this is the W statistic if there is
background), Loredo statistic (`lstat`), a statistic for
Poisson data with assumed known background (`pstat`), a
statistic for Poisson data with Gaussian background (`pgstat`),
and the Whittle statistic (`whittle`) for power density
functions. If the statistic is given as `cstat` with a number
appended (e.g. cstat5) then the statistic is calculated after the data
are binned to contain a minimum number of counts in each channel where
the minimum number is the number appended. If the number is followed
by b then the binning is based on the minimum number of counts in the
background spectrum. Note that this binning only
occurs when calculating the statistic and has to be done every time so
it is much less efficent than using an external program (such as
ftgrouppha). If the statistic is given as `whittle` with a
number appended (e.g. whittle5) then the statistic is appropriate for
that number of power density functions averaged together.

The `chistokes` statistic (with the general alias
`chicov`) is a multivariate-Gaussian generalization of
chi-squared for spectra that are correlated bin-by-bin, such as the
Stokes I, Q and U spectra of a polarized source. It uses a per-bin
covariance *between* the spectra (carried in the data files)
rather than treating them as independent. The statistic acts on the
covariance-group members currently assigned `chistokes` or
`chicov` (the { active sub-block}); the given spectrum range
must cover every active member of a group, all of which must share an
identical grouping and be noticed identically. See
Appendix AppendixStatistics for the full description, the
non-positive-definite (shrinkage) handling and the file format.

The **test** statistic options are 
Anderson-Darling (`ad`), chi-squared (`chi`), Cramer-von Mises 
(`cvm`), CUSUM (`cusum`), Kolmogorov-Smirnov (`ks`), Pearson chi-square 
(`pchi`) and Runs (`runs`). 

All These statistics are described in more in detail in
Appendix AppendixStatistics.

If a weight method is specified then that will be used if appropriate
for the statistic. The weight options available are `standard`,
`gehrels`, `churazov`, and
`model`. `standard` weighting uses $\sqrt{N}$ or the
statistical error given in the input spectrum. `gehrels`
weighting uses $1+\sqrt{N+0.75}$, a better approximation when N is
small ([Gehrels 1986](https://ui.adsabs.harvard.edu/abs/1986ApJ...303..336G/abstract)).
`churazov` weighting uses the suggestion of [Churazov
  et al. (1996)](https://ui.adsabs.harvard.edu/abs/1996ApJ...471..673C/abstract) to estimate the weight
for a given channel by averaging the counts in surrounding
channels. `model` weighting uses the value of the model, not
the data, to estimate the weight.

If a spectrum number or spectrum range is
given, the chosen statistic will only apply to those spectra.  It is 
therefore possible for a multi-spectrum fit to use more than one fit or 
test statistic.  If no spectrum number or range is given, the chosen 
statistic will apply to all loaded spectra and will be the default statistic 
for any future loaded spectra.

**Examples:**
  
Assume 3 spectra are currently loaded, all using the chi-squared statistic, 
and that chi-squared is the default statistic.

```
XSPEC12>statistic cstat 2-3
   // Spectrum 1 continues to use chi-sq, 2 and 3 use cstat.
XSPEC12>statistic cstat5 3
   // Spectrum 3 uses cstat but with a binning to a minimum
   // number of 5 counts/bin.
XSPEC12>data 4 spec4.pha
   // New spectrum 4 will use chi-sq.
XSPEC12>statistic cstat
   // All 4 spectra now use cstat, cstat is the new default.
XSPEC12>data 5 spec5.pha
   // New spectrum 5 will use cstat.
XSPEC12>statistic test ks
   // All 5 spectra now use ks as the test statistic.
XSPEC12>statistic chi churazov 5
   // Spectrum 5 will use chi-sq using the churazov weighting
```
