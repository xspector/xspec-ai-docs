"""Validation harness for casebook lesson `ftest-invalid-for-line-significance`.

Claim: the F-test / naive delta-chi-square OVER-states the significance of a
searched line, because the line's depth is bounded at 0 and its energy/width are
unidentified under the no-line null (Protassov et al. 2002).

Ground-truth test (Monte-Carlo). Simulate many LINE-FREE cutoffpl spectra on the
Ginga LAC response; fit each with cutoffpl and with cutoffpl*gabs (line energy and
width free, depth >= 0); collect delta-chi-square. If the F-test were valid, the
naive chi-square_1 "p=0.01" threshold (delta-chi-square > 6.63) would be exceeded
by ~1% of line-free simulations. The lesson holds if it is exceeded by SEVERAL
times that -- the test is anti-conservative -- while the bulk of the null
distribution stays small (a sane, not always-huge, statistic).

Run:  python bench/lessons/ftest-invalid-for-line-significance.py
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
~150 line-free fits; a couple of minutes. Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RSP = "ginga_lac.rsp"
BAND = "**-2.0 28.0-**"
NORM = 1.0
CHI2_1_P01 = 6.63          # chi-square_1, p=0.01 ("2.6 sigma")
M = 150


def fake(r, expo, seed):
    r.reset_session()
    r.define_model("cutoffpl")
    r.xcall("AllModels(1)", "setPars", [1.0, 15.0, NORM])
    r.fakeit(settings={"response": RSP, "exposure": expo}, seed=seed)
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [BAND])


def dchi_one(r, expo, seed):
    fake(r, expo, seed)
    r.define_model("cutoffpl")
    r.xcall("AllModels(1)", "setPars", [1.0, 15.0, NORM])
    c0 = r.fit("chi", timeout=120)["result"]["statistic"]
    r.define_model("cutoffpl*gabs")
    r.xcall("AllModels(1)", "setPars", [1.0, 15.0, NORM, 15.0, 2.0, 0.1])
    r.set_parameter(4, values_string="15,0.1,5,5,28,28")    # LineE searched
    r.set_parameter(5, values_string="2,0.05,0.5,0.5,8,8")  # Sigma free (broad ok)
    r.set_parameter(6, values_string="0.1,0.01,0,0,50,50")  # Strength >= 0
    c1 = r.fit("chi", timeout=120)["result"]["statistic"]
    return max(c0 - c1, 0.0)


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    dchis = []
    try:
        fake(r, 1000.0, 1)
        rate = float(r.xget("AllData(1).rate")["result"]["value"][0])
        expo = round(20000.0 / rate)
        for i in range(M):
            try:
                dchis.append(dchi_one(r, float(expo), 5000 + i))
            except Exception:
                pass
    finally:
        r.close()

    n = len(dchis)
    if n < M * 0.8:
        print(f"FAIL: too many simulations failed ({n}/{M})")
        return 1
    dchis.sort()
    far = sum(d > CHI2_1_P01 for d in dchis) / n     # false-alarm at naive threshold
    median = dchis[n // 2]
    p99 = dchis[min(n - 1, int(0.99 * n))]
    print(f"M={n} line-free sims. null delta-chi^2: median={median:.2f} "
          f"99th={p99:.2f}")
    print(f"P(dChi > {CHI2_1_P01}) = {far*100:.1f}%   (nominal 1% if F-test valid)")

    fails = []
    if not far > 0.03:
        fails.append(f"false-alarm rate at the naive threshold not inflated "
                     f"({far*100:.1f}%, need > 3%)")
    if not median < 5.0:
        fails.append(f"null distribution not sane (median={median:.2f}, expected small)")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: a searched line clears the naive chi2_1 1% bar several times "
          "too often -- the F-test is anti-conservative; use Monte-Carlo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
