---
class: ChainManager
singleton: AllChains
module: chain.py
---

# AllChains

Singleton instance `AllChains` (class `ChainManager`).

**Monte Carlo Markov Chain container.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| defBurn | — | get/set | Default burn length for new Chain objects (orig = 0). |
| defFileType | — | get/set | Default output file format (orig = 'fits'). |
| defLength | — | get/set | Default chain length (orig = 100). |
| defProposal | — | get/set | Default chain proposal (orig = 'gaussian fit'). |
| defRand | — | get/set | Default randomization setting (orig = False). |
| defRescale | — | get/set | Default covariance rescale fraction (orig = None). |
| defTemperature | — | get/set | Default chain temperature (orig = 1.0). |
| defAlgorithm | — | get/set | Default chain algorithm (orig = 'gw'). |
| defWalkers | — | get/set | Default walkers parameter for 'gw' chains (orig = 10). |

## Methods

- `__init__()`
- `__call__(index)` — Get a Chain object from the *AllChains* container.
- `best()` — Return the best-fit parameters and statistic in the loaded chains.
- `clear()` — Unload all chains from container
- `dic()` — Calculate the deviance information criterion from all chains
- `diagnostics()` — Return the Vehtari et al. (2021) MCMC diagnostic suite for all
- `diag()` — Run `chain diag`: print the diagnostic verdict + per-parameter table.
- `margin(argString)` — Calculate a multi-dimensional probability distribution.
- `marginResults(arg)` — Retrieve values from the most recent margin calculation.
- `show()` — Display information for current attributes and loaded chains.
- `stat(parIdx)` — Display statistical information on a particular chain parameter.
