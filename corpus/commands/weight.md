---
name: weight
aliases: [xweight]
also_documents: [weightgehrels, weightchurazov]
source: XSweight.tex
---

# weight

**change weighting used in computing statistic**

Change the weighting function used in the calculation of chi-squared.

**Syntax:** `weight` [standard  |  gehrels  |  churazov  |  model]

`standard` weighting uses $\sqrt{N}$ or the statistical error given in 
the input spectrum. `gehrels` weighting uses $1+\sqrt{N+0.75}$, 
a better approximation when N is small (Gehrels, N. 1986, ApJ 303, 336). 
`churazov` weighting uses the suggestion of Churazov et al. 
(1996, ApJ 471, 673) to estimate the weight for a given channel by averaging 
the counts in surrounding channels. `model` weighting uses the value of 
the model, not the data, to estimate the weight.
