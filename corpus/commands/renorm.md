---
name: renorm
aliases: [xrenorm]
also_documents: [renormauto, renormprefit, renormnone]
source: XSrenorm.tex
---

# renorm

**renormalize model to minimize statistic with current parameters**

Renormalize model, or change renorm conditions.

**Syntax:** `renorm` [auto| none| prefit]

The `renorm` command will adjust the normalizations of the model 
by a single multiplication factor, which is chosen to minimize the fit 
statistic.  Such a renorm will be performed explicitly whenever the command 
is used without a key-word, or during certain XSPEC commands, as determined 
by the following key-words:

 p{0.61}}
`auto`& Renormalize after a `model` or `newpar` command, 
and at the beginning of a fit.

`prefit`& Renormalize only at the beginning of a fit.

`none`& Perform no automatic renormalizations, i.e., only perform them 
when a `renorm` command is given explicitly.

This command works by doing an analytic calculation to change the
normalizations of all additive components in the model to minimize the
fit statistic. The relative normalizations of the components will not
be changed. This analytic calculation cannot be performed for all the
fit statistics, in particular it will not work for cstat if there is a
background file. If the analytic calculation is not possible this
command will have no effect.
