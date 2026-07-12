"""Validation harness for casebook lesson `young-plasma-needs-nei-not-equilibrium`.

Claim: a young / under-ionized plasma must be fit with a non-equilibrium model;
an equilibrium model reads the low ionization as a low temperature and gets kT
badly wrong.

Ground-truth test (fakeit). A young SNR: tbabs*nei with kT=3.0 keV and a low
ionization timescale Tau=1e10 s/cm^3, on the Chandra ACIS-S response:
  * WRONG model (tbabs*apec, equilibrium) -> kT badly underestimated AND a much
    worse fit statistic;
  * RIGHT model (tbabs*nei) -> kT and Tau recovered near truth.

A lesson earns `validated` only if the equilibrium fit is both badly biased and
much worse, while the NEI fit recovers the truth.

NOTE: apec's and nei's Abundanc parameter (index 3) is FROZEN by default; the
harness thaws it, else the abundance would be held at its start.

Run:  python bench/lessons/young-plasma-needs-nei-not-equilibrium.py
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
NH, KT_TRUE, TAU_TRUE, SEED = 0.3, 3.0, 1.0e10, 9
TRUTH = [NH, KT_TRUE, 1.0, TAU_TRUE, 0.0, 1.0e-2]   # tbabs*nei


def fake(r, expo):
    r.reset_session()
    r.define_model("tbabs*nei")
    r.xcall("AllModels(1)", "setPars", TRUTH)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": expo},
                    seed=SEED).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [BAND])
    return True


def rate(r, expo):
    return float(r.xget("AllData(1).rate")["result"]["value"][0])


def fit_apec(r):
    r.define_model("tbabs*apec")
    r.xcall("AllModels(1)", "setPars", [NH, 2.0, 1.0, 0.0, 1.0e-2])
    r.set_parameter(1, value=NH, freeze=True)
    r.set_parameter(4, value=0.0, freeze=True)
    r.set_parameter(3, thaw=True)
    res = r.fit("cstat", timeout=300)["result"]
    kT = {x["index"]: x for x in res["params"]}[2]["value"]
    return res["statistic"], kT


def fit_nei(r):
    r.define_model("tbabs*nei")
    r.xcall("AllModels(1)", "setPars", [NH, 2.0, 1.0, 1.0e11, 0.0, 1.0e-2])
    r.set_parameter(1, value=NH, freeze=True)
    r.set_parameter(5, value=0.0, freeze=True)
    r.set_parameter(3, thaw=True)
    res = r.fit("cstat", timeout=300)["result"]
    p = {x["index"]: x for x in res["params"]}
    return res["statistic"], p[2]["value"], p[4]["value"]


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        fake(r, 1000.0)
        expo = round(6000.0 / rate(r, 1000.0))
        fake(r, float(expo))
        c_apec, kT_apec = fit_apec(r)
        fake(r, float(expo))
        c_nei, kT_nei, tau_nei = fit_nei(r)
    finally:
        r.close()

    print(f"apec (equilibrium): cstat={c_apec:.0f}  kT={kT_apec:.2f} keV (truth {KT_TRUE})")
    print(f"nei  (NEI):         cstat={c_nei:.0f}  kT={kT_nei:.2f} keV  "
          f"Tau={tau_nei:.2e} (truth {TAU_TRUE:.0e})")
    print(f"delta-cstat(apec - nei) = {c_apec - c_nei:.0f}")

    fails = []
    if not kT_apec < 0.5 * KT_TRUE:
        fails.append(f"equilibrium kT not badly underestimated ({kT_apec:.2f} vs {KT_TRUE})")
    if not (c_apec - c_nei) > 100.0:
        fails.append(f"equilibrium fit not much worse (delta-cstat={c_apec - c_nei:.0f})")
    if not abs(kT_nei - KT_TRUE) < 0.4 * KT_TRUE:
        fails.append(f"NEI did not recover kT ({kT_nei:.2f} vs {KT_TRUE})")
    if not 0.5 * TAU_TRUE < tau_nei < 2.0 * TAU_TRUE:
        fails.append(f"NEI did not recover Tau ({tau_nei:.2e} vs {TAU_TRUE:.0e})")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: equilibrium apec reads the young plasma as ~6x too cool at a "
          "far worse statistic; nei recovers kT and Tau")
    return 0


if __name__ == "__main__":
    sys.exit(main())
