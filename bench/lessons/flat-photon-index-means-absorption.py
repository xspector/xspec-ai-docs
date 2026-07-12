"""Validation harness for casebook lesson `flat-photon-index-means-absorption`.

Claim: on soft-band data, unmodelled intrinsic absorption does not fail loudly --
it is absorbed into the continuum slope. The minimiser flattens the photon index
(sometimes past 1, even to an unphysical negative/rising value) to fake the soft
turnover it cannot bend a power law into, and leaves a soft residual deficit. The
signal is the implausibly flat Gamma AND a systematic residual -- and NOT a
pegged parameter (that is the sibling lesson `peg-at-limit-means-wrong-model`;
here Gamma flattens without hitting a limit).

Ground-truth test (fakeit). The truth is an obscured Seyfert -- Galactic plus a
heavy intrinsic column on a normal coronal power law:
  * WRONG model (tbabs*powerlaw, nH frozen at the Galactic value), the careless
    "source is unobscured" fit -> Gamma driven flat/inverted AND a systematic
    residual, but NO pegged_limit.
  * RIGHT model (tbabs*ztbabs*powerlaw, Galactic + redshift frozen, initialised
    at truth) -> a normal Gamma and no systematic residual.

A lesson earns `validated` only if the signal fires when the absorber is omitted
AND stays quiet when it is restored -- both directions.

Run:  python bench/lessons/flat-photon-index-means-absorption.py
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RMF, ARF = "aciss_aimpt_cy15.rmf", "aciss_aimpt_cy15.arf"
EBAND = "**-0.5 8.0-**"
SEED = 51841
EXPOSURE = 40000.0

# Truth: obscured Seyfert -- Galactic + heavy intrinsic absorption on a coronal PL
TRUTH_EXPR = "tbabs*ztbabs*powerlaw"
TRUTH_PARS = [0.03, 8.0, 0.05, 1.8, 3.0e-3]   # nH_gal, nH_z, z, Gamma, norm
NH_GAL, Z = 0.03, 0.05

# Careless model: Galactic absorption only (the source assumed unobscured)
WRONG_EXPR = "tbabs*powerlaw"

FLAT = 1.0            # a coronal Gamma below this is implausible -> absorption tell
NORMAL = (1.4, 2.4)   # a believable coronal slope


def _sim(r):
    """fakeit the obscured truth (fixed seed) and trim to the calibrated band."""
    r.reset_session()
    r.define_model(TRUTH_EXPR)
    r.xcall("AllModels(1)", "setPars", TRUTH_PARS)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": EXPOSURE},
                    seed=SEED).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [EBAND])
    return True


def _gamma(params):
    for p in params:
        if p["name"] == "PhoIndex":
            return p["value"]
    return None


def _fit(r, expr, frozen, init_pars=None):
    """Define expr (optionally initialised to truth), freeze the (index, value)
    pairs in `frozen`, fit cstat; return (gamma, issue_kinds) or (None, None)."""
    r.define_model(expr)
    if init_pars is not None:
        r.xcall("AllModels(1)", "setPars", init_pars)
    for idx, val in frozen:
        r.set_parameter(idx, value=val, freeze=True)
    f = r.fit("cstat")
    if not f.get("ok"):
        return None, None
    g = _gamma(f["result"]["params"])
    a = r.assess_fit()
    if not a.get("ok"):
        return None, None
    return g, set(a["result"]["issue_kinds"])


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        wrong_g, wrong_k = (_fit(r, WRONG_EXPR, [(1, NH_GAL)])
                            if _sim(r) else (None, None))
        right_g, right_k = (_fit(r, TRUTH_EXPR, [(1, NH_GAL), (3, Z)], TRUTH_PARS)
                            if _sim(r) else (None, None))
    finally:
        r.close()

    if wrong_g is None or right_g is None:
        print(f"FAIL: could not simulate/fit (wrong={wrong_g} right={right_g})")
        return 1

    print(f"WRONG ({WRONG_EXPR}, Galactic nH only): Gamma={wrong_g:+.2f} "
          f"kinds={sorted(wrong_k)}")
    print(f"RIGHT ({TRUTH_EXPR}, at truth):          Gamma={right_g:+.2f} "
          f"kinds={sorted(right_k)}")

    fails = []
    # signal must FIRE when the absorber is omitted: flat Gamma + soft residual...
    if not wrong_g < FLAT:
        fails.append(f"Gamma not flat on the wrong model (got {wrong_g:+.2f}, "
                     f"need < {FLAT})")
    if "systematic_residual" not in wrong_k:
        fails.append("no systematic residual on the wrong model")
    # ...and it must be the FLAT-index signature, not the pegged-parameter one
    if "pegged_limit" in wrong_k:
        fails.append("Gamma pegged on the wrong model -- that is the "
                     "peg-at-limit signature, not this one")
    # ...and stay QUIET when the absorber is restored
    if not NORMAL[0] <= right_g <= NORMAL[1]:
        fails.append(f"Gamma not normal on the right model (got {right_g:+.2f}, "
                     f"need {NORMAL})")
    if "systematic_residual" in right_k:
        fails.append("systematic residual on the RIGHT model (false positive)")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: omitting the absorber flattens Gamma and leaves a soft "
          "residual; restoring it recovers a normal Gamma and clears the residual")
    return 0


if __name__ == "__main__":
    sys.exit(main())
