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
regroup replays it.  Each super-bin spans an integer number of source bins, so
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
automatically whenever the background carries a grouping --- whether read from
the file (for example a background grouped by ftgrouppha
`grouptype=optsnmin`) or applied at run time with
`group` `back` --- and otherwise the ordinary per-bin W statistic
is used unchanged.  Pooling the background to a modest minimum signal-to-noise
(e.g. `group` `back` `minsn` 5) is typically enough to
bring the bias down to a few percent without coarsening the source spectrum.
The exact form of the pooled W statistic is given in
Appendix AppendixStatistics; the other fit statistics that estimate a
background (such as `pgstat`) honour the same pooling.

**tclout.** `tclout` `group` <n> [`data`
| `back`] returns the current per-channel grouping flags for
the source ($1$ starts a bin, $-1$ continues it, $0$ marks a bad channel), or
the per-source-bin super-bin index for the background.  Appending
`intent` returns instead the grouping request that produced them (for
example `minsn 5` or `optbin 20`), which is the form written to
`save` files.

**Examples:**

```
XSPEC12> group data minsn 5
// Group every loaded spectrum to a minimum signal-to-noise of 5.

XSPEC12> group 1 data optbin 20
// Optimally bin spectrum 1 from its RMF resolution, requiring at
// least 20 counts per bin.

XSPEC12> group 2-3 data mincounts 25
// Group spectra 2 and 3 to at least 25 counts per bin.

XSPEC12> group 1 back minsn 5
// Pool the background of spectrum 1 to S/N 5, independently of the
// source channel grouping, to reduce the C-statistic (W-statistic)
// bias on a low-count background.

XSPEC12> group data original
// Restore the grouping originally read from the files.
```
