"""Validation harness for casebook lesson `single-temperature-fe-bias`.

Claim: fitting a single-temperature plasma to genuinely multi-temperature
cluster/group gas biases the fitted iron abundance (classically LOW -- the Fe
bias), and the tell is an elevated fit statistic; adding a second temperature
recovers the truth.

Ground-truth test (fakeit). The truth is a two-phase ICM (1.0 and 2.5 keV, same
iron abundance 0.5) on the Chandra ACIS-S response:
  * WRONG model (tbabs*apec, single temperature, abundance thawed) -> abundance
    driven well below 0.5 AND an elevated cstat/dof (the misfit is visible);
  * RIGHT model (tbabs*(apec+apec), abundance thawed and tied across phases) ->
    abundance recovered near 0.5 with a good cstat/dof.

A lesson earns `validated` only if the single-T fit biases the abundance where
the two-T fit recovers it -- both directions.

NOTE: apec's Abundanc parameter is FROZEN by default; the harness thaws it
explicitly (index 3), else the "fit" would just hold the abundance at its start.

Run:  python bench/lessons/single-temperature-fe-bias.py
Needs HEADAS/PyXspec (the runner bootstraps it); skips cleanly otherwise.
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
RMF, ARF = "aciss_aimpt_cy15.rmf", "aciss_aimpt_cy15.arf"
BAND = "**-0.5 7.0-**"
SEED, EXPO = 4401, 8000.0
NH, Z, AB = 0.02, 0.05, 0.5
TRUTH = [NH, 1.0, AB, Z, 1.0e-2, 2.5, AB, Z, 2.0e-2]   # tbabs*(apec+apec)


def sim(r):
    r.reset_session()
    r.define_model("tbabs*(apec+apec)")
    r.xcall("AllModels(1)", "setPars", TRUTH)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": EXPO},
                    seed=SEED).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [BAND])
    return True


def abund(fit_result):
    for p in fit_result["params"]:
        if p["index"] == 3 and p["name"] == "Abundanc":
            return p["value"]
    return None


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        # single temperature (the trap), abundance thawed, neutral (solar) start
        one = None
        if sim(r):
            r.define_model("tbabs*apec")
            r.xcall("AllModels(1)", "setPars", [NH, 2.0, 1.0, Z, 3.0e-2])
            r.set_parameter(1, value=NH, freeze=True)
            r.set_parameter(4, value=Z, freeze=True)
            r.set_parameter(3, thaw=True)
            one = r.fit("cstat", timeout=300).get("result")
        # two temperatures, abundance thawed and tied
        two = None
        if sim(r):
            r.define_model("tbabs*(apec+apec)")
            r.xcall("AllModels(1)", "setPars",
                    [NH, 1.0, 1.0, Z, 1.0e-2, 2.5, 1.0, Z, 2.0e-2])
            r.set_parameter(1, value=NH, freeze=True)
            r.set_parameter(4, value=Z, freeze=True)
            r.set_parameter(8, value=Z, freeze=True)
            r.set_parameter(3, thaw=True)
            r.set_parameter(7, link=3)
            two = r.fit("cstat", timeout=300).get("result")
    finally:
        r.close()

    if not one or not two:
        print(f"FAIL: could not fit (single={bool(one)} two={bool(two)})")
        return 1

    ab1, red1 = abund(one), one["statistic"] / one["dof"]
    ab2, red2 = abund(two), two["statistic"] / two["dof"]
    print(f"single-T: Abund={ab1:.3f}  cstat/dof={red1:.2f}  (truth {AB})")
    print(f"two-T   : Abund={ab2:.3f}  cstat/dof={red2:.2f}")

    fails = []
    if abs(ab2 - AB) > 0.1:
        fails.append(f"two-T did not recover the abundance ({ab2:.3f} vs {AB})")
    if not ab1 < AB - 0.15:
        fails.append(f"single-T did not bias the abundance low ({ab1:.3f})")
    if not ab1 < ab2 - 0.15:
        fails.append(f"single-T abundance not below two-T ({ab1:.3f} vs {ab2:.3f})")
    if not red1 > 2.0:
        fails.append(f"single-T fit statistic not elevated (cstat/dof={red1:.2f})")
    if not red2 < 1.5:
        fails.append(f"two-T fit not good (cstat/dof={red2:.2f})")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: single-T biases the iron abundance low behind an elevated "
          "statistic where two-T recovers it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
