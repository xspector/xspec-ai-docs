"""Ground-truth calibration benchmark for xspec-run.

Generates synthetic spectra with KNOWN parameters via fakeit, recovers them
through the Tier B server (the same tools an agent uses), and scores:

  * coverage -- fraction of realizations whose 1-sigma CI contains the truth
                (nominal 68.3%). Under- or over-coverage means the errors are
                mis-sized.
  * pull     -- (recovered - truth) / sigma across realizations; should be
                ~N(0,1): mean ~0 (unbiased), std ~1 (errors correctly sized).

Trap cases use the SAME simulated data (same seed) fit two ways to show the
statistic choice matters: cstat is calibrated on low counts, chi is not.

This validates that the tooling produces statistically trustworthy results and
guards against regressions. It is tool-level (deterministic); an agent-in-the-
loop layer could reuse this scoring later.

Run:  python bench/benchmark.py [N_realizations]   (default 40)
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RMF, ARF = "aciss_aimpt_cy15.rmf", "aciss_aimpt_cy15.arf"
EBAND = "**-0.5 8.0-**"
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40

# each case: model, true parameter vector, exposure, fit statistic, and which
# parameter (1-based) to score. Cases sharing (expr, pars, exposure) and seeds
# see identical simulated data -> a fair statistic comparison.
CASES = [
    dict(name="powerlaw bright  (cstat)", expr="powerlaw", pars=[2.0, 1e-3],
         exposure=20000.0, stat="cstat", score=1, truth=2.0),
    dict(name="powerlaw faint   (cstat)", expr="powerlaw", pars=[2.0, 1e-4],
         exposure=3000.0, stat="cstat", score=1, truth=2.0),
    dict(name="powerlaw faint   (chi)  TRAP", expr="powerlaw", pars=[2.0, 1e-4],
         exposure=3000.0, stat="chi", score=1, truth=2.0),
    dict(name="tbabs*powerlaw nH (cstat)", expr="tbabs*powerlaw",
         pars=[0.5, 1.8, 1e-3], exposure=20000.0, stat="cstat", score=1,
         truth=0.5),
]


def realize(r, case, seed):
    """One synthetic dataset -> recovered value + CI, or None on failure."""
    r.reset_session()
    r.define_model(case["expr"])
    r.xcall("AllModels(1)", "setPars", case["pars"])
    fk = r.fakeit(settings={"response": RMF, "arf": ARF,
                            "exposure": case["exposure"]}, seed=seed)
    if not fk.get("ok"):
        return None
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [EBAND])
    if not r.fit(case["stat"]).get("ok"):
        return None
    er = r.error("1.0 %d" % case["score"])
    if not er.get("ok"):
        return None
    p = next((x for x in er["result"]["params"]
              if x["index"] == case["score"]), None)
    if not p or p["high"] <= p["low"]:
        return None
    sigma = (p["high"] - p["low"]) / 2.0
    return {"val": p["value"], "covered": p["low"] <= case["truth"] <= p["high"],
            "pull": (p["value"] - case["truth"]) / sigma}


def score(case, results):
    ok = [x for x in results if x]
    n = len(ok)
    if n < 5:
        return {"name": case["name"], "n": n, "note": "too few good fits"}
    cov = sum(x["covered"] for x in ok) / n
    pulls = [x["pull"] for x in ok]
    return {"name": case["name"], "n": n, "coverage": cov,
            "pull_mean": statistics.mean(pulls),
            "pull_std": statistics.pstdev(pulls),
            "failed": len(results) - n}


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    rows = []
    try:
        for case in CASES:
            res = [realize(r, case, seed) for seed in range(N)]
            rows.append(score(case, res))
            s = rows[-1]
            if "coverage" in s:
                print(f"  {s['name']:<32} n={s['n']:>3}  "
                      f"cov={s['coverage']*100:5.1f}%  "
                      f"pull mean={s['pull_mean']:+.2f} std={s['pull_std']:.2f}"
                      f"  (failed {s['failed']})")
            else:
                print(f"  {s['name']:<32} {s['note']}")
    finally:
        r.close()

    # ---- verdict ----
    print(f"\n1-sigma nominal coverage = 68.3%  (N={N} per case)")
    fails = []
    by = {s["name"]: s for s in rows if "coverage" in s}
    for s in by.values():
        if "TRAP" in s["name"]:
            continue
        # coverage is a noisy binomial estimate at small N -> wide band; the
        # pull mean/std checks below carry the real weight. Raise N to tighten.
        if not 0.50 <= s["coverage"] <= 0.85:
            fails.append(f"{s['name']}: coverage {s['coverage']*100:.0f}% off 68%")
        if abs(s["pull_mean"]) > 0.4:
            fails.append(f"{s['name']}: biased (pull mean {s['pull_mean']:+.2f})")
        if not 0.6 <= s["pull_std"] <= 1.5:
            fails.append(f"{s['name']}: pull std {s['pull_std']:.2f} off 1.0")

    # trap: chi on faint data should be measurably worse than cstat on the same data
    cstat = by.get("powerlaw faint   (cstat)")
    chi = by.get("powerlaw faint   (chi)  TRAP")
    if cstat and chi:
        degraded = (chi["coverage"] < cstat["coverage"] - 0.05
                    or abs(chi["pull_mean"]) > abs(cstat["pull_mean"]) + 0.2)
        print(f"trap: cstat cov {cstat['coverage']*100:.0f}% / pull "
              f"{cstat['pull_mean']:+.2f}  vs  chi cov {chi['coverage']*100:.0f}%"
              f" / pull {chi['pull_mean']:+.2f}  -> "
              f"{'chi degraded (expected)' if degraded else 'no clear degradation'}")

    if fails:
        print("\nCALIBRATION FAILURES:")
        for f in fails:
            print("  -", f)
        return 1
    print("\ncalibration OK: cstat cases are well-covered and unbiased")
    return 0


if __name__ == "__main__":
    sys.exit(main())
