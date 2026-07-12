"""Validation harness for casebook lesson `systematics-dominate-above-1e5-counts`.

Claim: above ~10^5 counts the statistical error bars shrink below the ~1-2%
calibration floor (so they no longer represent the real uncertainty), and a
few-percent feature that is invisible at lower counts becomes highly significant.

Ground-truth test (fakeit). One bright soft-state black-hole binary,
tbabs*(diskbb+powerlaw+gaussian) with a modest Fe Ka line, faked at two depths on
the Chandra ACIS-S response:
  * at ~10^6 counts: the disk-temperature 90% statistical interval is sub-percent
    (below any real calibration), AND the Fe line is highly significant
    (delta-chi from adding it >> a 5-sigma threshold);
  * at ~10^4 counts: the SAME line is insignificant (delta-chi ~ 0).

A lesson earns `validated` only if both hold: statistics have shrunk below the
calibration floor at high counts, and the feature's significance scales with
counts (present when deep, absent when shallow).

Run:  python bench/lessons/systematics-dominate-above-1e5-counts.py
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RMF, ARF = "aciss_aimpt_cy15.rmf", "aciss_aimpt_cy15.arf"
BAND = "**-0.5 8.0-**"
SEED = 20219
NH, GN = 0.5, 3.0e-4
# tbabs*(diskbb+powerlaw+gaussian): nH,Tin,dnorm,Gamma,plnorm,LineE,Sig,gnorm
TRUTH = [NH, 0.7, 1000.0, 2.5, 0.1, 6.4, 0.05, GN]


def fake(r, expo, seed):
    r.reset_session()
    r.define_model("tbabs*(diskbb+powerlaw+gaussian)")
    r.xcall("AllModels(1)", "setPars", TRUTH)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": expo},
                    seed=seed).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [BAND])
    return True


def rate(r, expo):
    return float(r.xget("AllData(1).rate")["result"]["value"][0])


def fit_cont(r):
    r.define_model("tbabs*(diskbb+powerlaw)")
    r.xcall("AllModels(1)", "setPars", [NH, 0.7, 1000.0, 2.5, 0.1])
    r.set_parameter(1, value=NH, freeze=True)
    return r.fit("chi", timeout=400)["result"]["statistic"]


def fit_full(r):
    r.define_model("tbabs*(diskbb+powerlaw+gaussian)")
    r.xcall("AllModels(1)", "setPars", TRUTH)
    r.set_parameter(1, value=NH, freeze=True)
    r.set_parameter(6, value=6.4, freeze=True)
    r.set_parameter(7, value=0.05, freeze=True)
    return r.fit("chi", timeout=400)["result"]["statistic"]


def line_dchi(r):
    return fit_cont(r) - fit_full(r)


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        fake(r, 500.0, 11)
        cps = rate(r, 500.0)
        e_hi = round(1.0e6 / cps)
        e_mid = round(1.0e4 / cps)

        # deep: sub-percent stat error on Tin, line highly significant
        fake(r, float(e_hi), SEED)
        fit_full(r)
        d = {x["index"]: x for x in r.error("2.706 2", timeout=400)["result"]["params"]}
        tin = d[2]
        tin_pct = 100.0 * (tin["high"] - tin["low"]) / 2.0 / tin["value"]
        dchi_hi = line_dchi(r)

        # shallow: same line insignificant
        fake(r, float(e_mid), SEED)
        dchi_mid = line_dchi(r)
    finally:
        r.close()

    print(f"deep  (~{e_hi} s, ~1e6 cts): Tin stat +/-{tin_pct:.2f}%   "
          f"Fe-line dChi={dchi_hi:.1f}")
    print(f"shallow(~{e_mid} s, ~1e4 cts):                    "
          f"Fe-line dChi={dchi_mid:.1f}")

    fails = []
    if not tin_pct < 1.0:
        fails.append(f"Tin statistical error not sub-percent at 1e6 ({tin_pct:.2f}%)")
    if not dchi_hi > 25.0:
        fails.append(f"Fe line not significant at 1e6 (dChi={dchi_hi:.1f}, need >25)")
    if not dchi_mid < 4.0:
        fails.append(f"Fe line not insignificant at 1e4 (dChi={dchi_mid:.1f}, need <4)")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: at 1e6 counts the stat error is sub-calibration-floor and a "
          "weak line is highly significant; at 1e4 the same line vanishes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
