---
name: ftest
aliases: [xftest]
also_documents: []
source: XSftest.tex
---

# ftest

**calculate the F-statistic from two chi-square values**

Calculate the F-statistic and its probability given new and old 
values of chi^2 and number of degrees of freedom (DOF).

**Syntax:** `ftest` chisq2 dof2 chisq1 dof1

The new chi^2 and DOF, chisq2 and dof2, should come from adding an extra model 
component to (or thawing a frozen parameter of) the model which gave chisq1 
and dof1. If the F-test probability is low then it is reasonable to add the 
extra model component. WARNING : it is not correct to use the F-test statistic 
to test for the presence of a line (see Protassov et al 2002, ApJ 571, 545). 
WARNING: this command can only be used if the extra model component is 
additive, this does not give the correct result if the component is 
multiplicative (see Orlandini et al. 2012, ApJ 748, 86).
