"""Validation harness for casebook lesson `below-100-counts-cannot-discriminate-models`.

Claim: below ~100 counts, continuum models of similar shape (blackbody vs
disk-blackbody) fit equally well and cannot be told apart; given enough counts
they separate.

Ground-truth test (fakeit). An absorbed blackbody (bbodyrad, kT=0.10 keV) on the
Chandra ACIS-S response:
  * faked at ~80 counts -> fitting bbodyrad and diskbb gives |delta-cstat| small
    (the wrong model can even fit better) -> indistinguishable;
  * faked at high counts -> diskbb is clearly worse (delta-cstat large) ->
    distinguishable.

A lesson earns `validated` only if both hold -- indistinguishable when
counts-starved AND distinguishable when rich.

Run:  python bench/lessons/below-100-counts-cannot-discriminate-models.py
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RMF, ARF = "aciss_aimpt_cy15.rmf", "aciss_aimpt_cy15.arf"
BAND = "**-0.3 1.5-**"
NH, SEED = 0.05, 7
TRUTH = [NH, 0.10, 1.0e3]   # tbabs*bbodyrad: nH, kT, norm


def fake(r, expo):
    r.reset_session()
    r.define_model("tbabs*bbodyrad")
    r.xcall("AllModels(1)", "setPars", TRUTH)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": expo},
                    seed=SEED).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [BAND])
    return True


def rate(r, expo):
    return float(r.xget("AllData(1).rate")["result"]["value"][0])


def fit_stat(r, model):
    r.define_model(model)
    r.xcall("AllModels(1)", "setPars", [NH, 0.10, 1.0e3])
    r.set_parameter(1, value=NH, freeze=True)
    return r.fit("cstat", timeout=200)["result"]["statistic"]


def dcstat(r, expo):
    """delta-cstat = cstat(diskbb) - cstat(bbodyrad) on the same faked data."""
    fake(r, expo)
    bb = fit_stat(r, "tbabs*bbodyrad")
    fake(r, expo)
    db = fit_stat(r, "tbabs*diskbb")
    return db - bb


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        fake(r, 1000.0)
        cps = rate(r, 1000.0)
        e_low = round(80.0 / cps)        # ~80 counts (vlow)
        e_high = round(40000.0 / cps)    # ~40000 counts (high)
        d_low = dcstat(r, float(e_low))
        d_high = dcstat(r, float(e_high))
    finally:
        r.close()

    print(f"~80 counts   : delta-cstat(diskbb - bbody) = {d_low:+.2f}  (indistinguishable)")
    print(f"~40000 counts: delta-cstat(diskbb - bbody) = {d_high:+.2f}  (should separate)")

    fails = []
    if not abs(d_low) < 5.0:
        fails.append(f"models distinguishable at ~80 counts (|delta-cstat|={abs(d_low):.1f}, "
                     f"expected < 5)")
    if not d_high > 25.0:
        fails.append(f"models not separated at high counts (delta-cstat={d_high:.1f}, "
                     f"expected > 25 with diskbb worse)")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: bbody and diskbb are indistinguishable at ~80 counts and "
          "clearly separated when counts are plentiful")
    return 0


if __name__ == "__main__":
    sys.exit(main())
