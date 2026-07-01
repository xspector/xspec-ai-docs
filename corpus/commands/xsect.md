---
name: xsect
aliases: [xxsect]
also_documents: []
source: XSxsect.tex
---

# xsect

**set the photoionization cross-sections**

Change the photoelectric absorption cross-sections in use.

**Syntax:** `xsect` [bcmc| obcm| vern]

The three options are: `bcmc`, from [Balucinska-Church & McCammon
(1992)](https://ui.adsabs.harvard.edu/abs/1992ApJ...400..699B/abstract) with a new He cross-section
based on [Yan et al. (1998)](https://ui.adsabs.harvard.edu/abs/1998ApJ...496.1044Y/abstract);
`obcm`, as `bcmc` but with the old He cross-section,
and, `vern`, from [Verner & Yakovlev
(1995)](https://ui.adsabs.harvard.edu/abs/1995A%26AS..109..125V/abstract) and [Verner et
al. (1996)](https://ui.adsabs.harvard.edu/abs/1996ApJ...465..487V/abstract).
This changes the cross-sections in use for all absorption models with the exception of
`wabs`, the `tbabs` family of models, amd `ismabs`.
