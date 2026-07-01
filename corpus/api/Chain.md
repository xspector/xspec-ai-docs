---
class: Chain
module: chain.py
---

# Chain

**Monte Carlo Markov Chain class.**

## Attributes

| attribute | type | access | description |
|-----------|------|--------|-------------|
| burn | — | get/set | The number of steps that will be thrown |
| fileName | — | get | Chain output file name. |
| fileType | str | get | Output format of the chain file [string]. |
| runLength | int | get/set | The length of chain to be added during the next run [int]. |
| totalLength | int | get | The cumulative length of the chain [int]. |
| proposal | — | get/set | The proposal distribution and source of covariance |
| rand | — | get/set | Determines whether chain start point will be randomized |
| rescale | — | get/set | Determines whether a rescale fraction will be |
| temperature | — | get/set | The temperature parameter used in the Metropolis-Hastings |
| algorithm | — | get/set | The current chain algorithm.  Valid settings are 'gw' |
| walkers | int | get/set | The number of walkers to be used for 'gw' chains [int]. |

## Methods

- `__init__(fileName, fileType=None, burn=None, runLength=None, proposal=None, rand=None, rescale=None, temperature=None, algorithm=None, walkers=None)` — Construct a chain object, perform a run, and load into AllChains
- `run(append=True)` — Perform a new chain run, either appending to or overwriting an
- `show()` — Display current settings of Chain object's attributes.
