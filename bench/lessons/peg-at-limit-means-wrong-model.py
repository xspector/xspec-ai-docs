"""Validation harness for casebook lesson `peg-at-limit-means-wrong-model`.

Claim: a thawed parameter pegged at a soft limit AND correlated residuals
(runs-test failure) together mean the model is structurally wrong -- the
minimiser is pushing a parameter to an extreme to compensate for missing
physics. Either flag alone is weaker; the pair is the signal.

Ground-truth test (fakeit). The truth is an absorption-free power law plus a
strong broad emission line:
  * WRONG model (tbabs*powerlaw), fit from defaults -> absorption cannot add a
    line, so nH is driven to its floor (pegged at soft min 0) while the missing
    line leaves correlated residuals -> assess_fit must raise BOTH
    `pegged_limit` and `systematic_residual`.
  * RIGHT model (powerlaw + gaussian), initialised at the known truth -> must
    raise NEITHER (the signal stays quiet when the model is right and properly
    specified).

A lesson earns `validated` only if the signal fires when the model is wrong AND
stays quiet when it is right -- both directions.

Run:  python bench/lessons/peg-at-limit-means-wrong-model.py
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RMF, ARF = "aciss_aimpt_cy15.rmf", "aciss_aimpt_cy15.arf"
EBAND = "**-0.5 9.0-**"
SEED = 73101

TRUTH_EXPR = "powerlaw + gaussian"
TRUTH_PARS = [1.8, 8.0e-3, 3.0, 0.6, 5.0e-3]   # Gamma, plNorm, LineE, sigma, gNorm
WRONG_EXPR = "tbabs*powerlaw"


def _sim(r):
    """fakeit one dataset from the truth (fixed seed) and trim to band."""
    r.reset_session()
    r.define_model(TRUTH_EXPR)
    r.xcall("AllModels(1)", "setPars", TRUTH_PARS)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": 50000.0},
                    seed=SEED).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [EBAND])
    return True


def _fit_assess(r, expr, init_pars=None):
    """Define expr (optionally initialised to init_pars), fit, return assess."""
    r.define_model(expr)
    if init_pars is not None:
        r.xcall("AllModels(1)", "setPars", init_pars)
    if not r.fit("cstat").get("ok"):
        return None
    a = r.assess_fit()
    return a["result"] if a.get("ok") else None


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        wrong = _sim(r) and _fit_assess(r, WRONG_EXPR)          # from defaults
        right = _sim(r) and _fit_assess(r, TRUTH_EXPR, TRUTH_PARS)  # at truth
    finally:
        r.close()

    if not wrong or not right:
        print(f"FAIL: could not simulate/fit (wrong={bool(wrong)} "
              f"right={bool(right)})")
        return 1

    wk, rk = set(wrong["issue_kinds"]), set(right["issue_kinds"])
    print(f"WRONG ({WRONG_EXPR}, from defaults): kinds={sorted(wk)}")
    for s in wrong["issues"]:
        print(f"    - {s}")
    print(f"RIGHT ({TRUTH_EXPR}, at truth):     kinds={sorted(rk)}")
    for s in right["issues"]:
        print(f"    - {s}")

    signal = {"pegged_limit", "systematic_residual"}
    fails = []
    if not signal <= wk:
        fails.append("signal did NOT fire on the wrong model "
                     "(need both pegged_limit + systematic_residual)")
    if signal & rk:
        fails.append(f"signal fired on the RIGHT model (false positive: "
                     f"{sorted(signal & rk)})")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: peg+residuals fires on the wrong model, "
          "stays quiet on the right")
    return 0


if __name__ == "__main__":
    sys.exit(main())
