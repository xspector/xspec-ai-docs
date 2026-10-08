---
name: group
aliases: [xgroup]
also_documents: []
source: XSgroup.tex
---

# group

**regroup spectra at runtime**

**Syntax:** `group` [<spectrum range>]   `data`|`back`   <type>   [<param>]

The `group` command rebins one or more loaded spectra in memory,
without re-reading the files or running an external tool such as
ftgrouppha.  It works from the original, ungrouped channels held in
an internal raw-channel cache, so it can be issued repeatedly to try
different binnings on the same data, and it can also regroup spectra produced
by `fakeit`.  The resulting grouping is recorded in `save` files,
can be read back with `tclout` `group`, and is available from
PyXspec.

`<spectrum range>` selects the spectra to act on, given as a
comma-separated list of numbers and ranges (e.g. `1`, `2-4`,
`1,3,5`), or `all` (the default) for every loaded spectrum.

The `data`|`back` selector chooses which layer to
regroup, and one of the two is required:

- [`data`] rebuilds the source channel-to-bin mapping.  The same
grouping is propagated to the associated background and correction spectra so
that they stay aligned with the source.

- [`back`] lays a coarser ``super-bin'' grouping on top of the
current source binning, gathering whole source bins into super-bins over which
the background is pooled, and caches the request so that a subsequent source
regroup replays it.  `auto` is the recommended `<type>` here.  Each super-bin spans an integer number of source bins, so
the background grouping cannot cut across the source binning.  Its main purpose
is to reduce a bias in the C statistic, as described under *Background
grouping and the C statistic* below.

`<type>` is the grouping algorithm, with a `<param>` where noted:

- [`none`] one bin per channel (i.e. remove all grouping).

- [`original`] restore the GROUPING and QUALITY arrays read from the
original file.

- [`minsn` `<S>`] group so that each bin reaches a minimum
signal-to-noise `<S>`, equivalent to requiring at least $S^{2}$ counts
per bin (matching the convention used by ftgrouppha).

- [`mincounts` `<N>`] group so that each bin contains at least
`<N>` counts.

- [`const` `<N>`] combine every `<N>` channels into one
bin.

- [`file` `<path>`] read the binning factors from a
single-column ASCII file `<path>`.

- [`optbin` [`<minCounts>`]] optimal binning following the
resolution-based scheme of [Kaastra & Bleeker
(2016)](https://ui.adsabs.harvard.edu/abs/2016A%26A...587A.151K/abstract), which sets the bin width from the
spectral resolution (the per-channel FWHM read from the RMF).  The optional
`<minCounts>` additionally enforces a minimum number of counts per bin.
The RMF is taken from the spectrum's response, so `optbin` (and
likewise `back` `optbin`) requires an ordinary single or
multiple-binning response, not a diagonal or dummy response.  The other
`back` types pool on the background counts alone and need no RMF.

- [`auto` [`<counts>` [`<fwhm>`]]] `back` only: the
two-condition pooling rule, and the recommended choice for the C statistic.  A
super-bin is closed as soon as it has accumulated `<counts>` background
counts *or* reached a width of `<fwhm>` times the narrowest FWHM it
spans, whichever happens first.  The defaults are `<counts>` $=10$ and
`<fwhm>` $=2$, so plain `group` `back` `auto` is the
usual form; both arguments are positional and may be given to override them.
Like `optbin` it reads the FWHM from the response and so needs an
ordinary single or multiple-binning response.  *Why* two conditions rather
than one is set out under *Choosing the pooling* below.  Requesting
`auto` on the `data` side is an error --- the source spectrum has
no profiled background rate for a count target to bound, and its
resolution-driven rule is `optbin`.

Channels flagged with bad quality are honoured: the new grouping is
reconciled with the quality array exactly as it is when a file is first read.

**Background grouping and the C statistic.** The most important use
of `group` `back` is to reduce a bias in the C statistic when a
background spectrum is present.  In that case XSPEC minimises the W statistic
(see Appendix AppendixStatistics), which treats the true background rate
in each source channel as a nuisance parameter and profiles it out
analytically.  When the background spectrum has few counts per channel these
per-channel background estimates are very noisy and, because their number
grows with the data rather than staying fixed, they bias the fitted source
parameters --- the classic Neyman--Scott incidental-parameters problem.  For a
faint source on a sparse background the bias on quantities such as N_H can
reach tens of percent.

`group` `back` addresses this by gathering several source bins
into a single background super-bin that shares *one* nuisance background
rate, so the number of profiled parameters shrinks from one per source bin to
one per super-bin.  The grouping is hierarchical, laid *on top of* the
source binning: each super-bin is a contiguous block of whole source bins, so
the source spectrum keeps its own (finer) binning while the background is
pooled over the coarser super-bins above it --- the two binnings are nested,
not independent.  XSPEC selects this pooled-background calculation
automatically whenever a background super-bin grouping has been set up at run
time with `group` `back`, and otherwise the ordinary per-bin W
statistic is used unchanged.  Note that a `GROUPING` column carried by
the background *file* (for example one written by ftgrouppha
`grouptype=optsnmin`) does not by itself select the pooled calculation:
on input XSPEC applies the source spectrum's grouping to the background and
ignores the background file's own grouping, so the super-bins must be requested
with `group` `back`.  Pooling the background to a modest minimum signal-to-noise
(e.g. `group` `back` `minsn` 5) is typically enough to
bring the bias down to a few percent without coarsening the source spectrum.
The exact form of the pooled W statistic is given in
Appendix AppendixStatistics; the other fit statistics that estimate a
background (such as `pgstat`) honour the same pooling.

**Choosing the pooling.** How coarsely to pool is not a one-number
question, because what is left of the bias after pooling has two halves that
answer to *different* variables.  The incidental-parameter half is a
function of the expected background counts in a super-bin, and falls away once
that number is of order a few.  The other half is the price of making one rate
stand for a stretch of spectrum over which the background is not in fact flat;
it is a function of the super-bin's width in *resolution elements*, is
negligible below about $2$ FWHM, and grows to $\sim$10% by $20$.  Neither is a
function of the other, because the conversion between counts and width runs
through the background exposure: a rule that sets a count target and lets the
width fall where it may (`minsn`, `mincounts`) pools four times as
many channels when the background exposure is four times shorter --- and does so
silently, since nothing in the fit output reports how wide a super-bin became.
A rule that fixes the width alone has the opposite failure, leaving the count
target unmet wherever the background is sparse.

`auto` imposes both conditions and closes a super-bin at whichever is
reached first.  With its defaults --- $10$ counts, $2$ FWHM --- the bias on the
fitted parameters stays within about $2\%$ and the nominal $90\%$ confidence
intervals keep $\sim$90% coverage across background exposures ranging from half
the source exposure to a hundred times it, a range over which every
single-condition rule fails at one end or the other.  The count target is
deliberately larger than the $\sim$1 count at which the incidental-parameter
bias dies for *predetermined* bin edges, because choosing the edges from
the same counts that are then fitted costs a few percent of extra bias at a
target of $2$ counts (bins tend to close on upward fluctuations); that penalty
has decayed by $5$--$10$ counts.  Where the background is too sparse for both
conditions to be met the width cap wins, and `auto` then accepts some
residual bias rather than smearing the background over a resolution element ---
which is the honest behaviour, since no grouping of a background that sparse can
remove the bias without incurring a worse systematic in its place.

**Fit quality will not tell you whether to pool.** The W
statistic *falls* when the per-channel background estimates are biasing
the fit, because assigning background counts to the source improves the very
likelihood being profiled.  A biased ungrouped fit therefore returns a
*better*-looking statistic than the pooled fit that corrects it: in one
XRISM Resolve example a fit whose temperature was wrong by $-35\%$ gave
$W/\nu = 0.75$, against $1.07$ for the same data after
`group` `back` `minsn` 3.  The `goodness` Monte
Carlo inherits this, since it compares the observed statistic against
simulations of the same model, and so would any comparison of $W$ with an
expected value.  Neither can be used to decide whether pooling was needed, nor
whether the rule chosen was adequate --- a rule that leaves background
super-bins empty scores *lower* than one that does not.  Note also that
for a sparse background $W$ falls well short of the number of degrees of
freedom, values near $0.6\nu$ being unremarkable, because the large-count
chi^2 limit given in Appendix AppendixStatistics is not reached;
``$W/\nu\approx1$'' is not a check in this regime.

**tclout.** `tclout` `group` <n> [`data`
| `back`] returns the current per-channel grouping flags for
the source ($1$ starts a bin, $-1$ continues it, $0$ marks a bad channel), or
the per-source-bin super-bin index for the background.  Appending
`intent` returns instead the grouping request that produced them (for
example `minsn 5`, `optbin 20` or `auto 10 2`), which is
the form written to `save` files.

**Examples:**

```
XSPEC> group data minsn 5
// Group every loaded spectrum to a minimum signal-to-noise of 5.

XSPEC> group 1 data optbin 20
// Optimally bin spectrum 1 from its RMF resolution, requiring at
// least 20 counts per bin.

XSPEC> group 2-3 data mincounts 25
// Group spectra 2 and 3 to at least 25 counts per bin.

XSPEC> group back auto
// Pool the background of every spectrum with the recommended
// two-condition rule: close a super-bin at 10 background counts or
// 2 resolution elements of width, whichever comes first.

XSPEC> group 1 back auto 25 1.5
// The same rule on spectrum 1 with a higher count target and a
// tighter width cap.

XSPEC> group 1 back minsn 5
// Pool the background of spectrum 1 to S/N 5, independently of the
// source channel grouping, to reduce the C-statistic (W-statistic)
// bias on a low-count background.

XSPEC> group data original
// Restore the grouping originally read from the files.
```
