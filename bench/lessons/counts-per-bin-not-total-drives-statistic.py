"""Validation harness for casebook lesson `counts-per-bin-not-total-drives-statistic`.

Claim: the fit statistic is set by counts PER BIN, not total counts. A
high-resolution (microcalorimeter) spectrum can hold tens of thousands of counts
yet ~1 per fine bin; chi's Gaussian per-bin assumption then fails and biases the
line-to-continuum-sensitive parameters (iron abundance high, normalisation low)
behind a reduced chi-square below 1, while cstat recovers the truth.

Ground-truth test (fakeit) on the real XRISM/Resolve Hp response (60000 channels
at 0.5 eV). A bright, velocity-broadened thermal plasma (bapec):
  * establish the regime: high total counts but a low median counts/bin;
  * WRONG statistic (chi, same fine data) -> iron abundance biased high, away
    from truth, with a reduced chi-square below 1;
  * RIGHT statistic (cstat) -> abundance recovered near truth.

A lesson earns `validated` only if chi biases where cstat recovers -- both
directions -- in a regime that is genuinely high-total / low-per-bin.

Fit over the full 2-10 keV band so the regime is genuine -- the high-total /
low-per-bin contrast lives in the many empty continuum bins, which a narrow
Fe-K window (count-rich) would hide. Two bapec fits over ~16000 fine bins take
~2-3 min; this is HEADAS-only (not in CI) and self-skips without the RMF. Needs
HEADAS/PyXspec AND the 372 MB Resolve Hp RMF at the path below; prints SKIPPED
and exits 0 if either is absent.

Run:  python bench/lessons/counts-per-bin-not-total-drives-statistic.py
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/Data/XRISM"
RMF, ARF = "rsl_Hp_L_2025.rmf", "rsl_pntsrc_GVC_2025.arf"
RMF_PATH = str(Path(DATA) / RMF)
BAND = "**-2.0 10.0-**"         # full band: the empty continuum bins ARE the point
SEED = 907
EXPO = 100000.0

TRUTH = [5.0, 0.7, 0.02, 200.0, 2.0e-2]   # kT, Abund, z, Velocity(km/s), norm
Z, ABUND_TRUE = 0.02, 0.7


def build(r):
    r.reset_session()
    r.define_model("bapec")
    r.xcall("AllModels(1)", "setPars", TRUTH)
    if not r.fakeit(settings={"response": RMF, "arf": ARF, "exposure": EXPO},
                    seed=SEED).get("ok"):
        return False
    r.xcall("AllData", "ignore", ["bad"])
    r.xcall("AllData", "ignore", [BAND])
    # neutral start; z frozen (optical); abundance + velocity free
    r.xcall("AllModels(1)", "setPars", [4.0, 0.5, Z, 100.0, 2.0e-2])
    r.set_parameter(2, thaw=True)
    r.set_parameter(4, thaw=True)
    r.set_parameter(3, value=Z, freeze=True)
    return True


def abund(fit_result):
    for p in fit_result["params"]:
        if p["index"] == 2:
            return p["value"]
    return None


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    if not Path(RMF_PATH).exists():
        print(f"SKIPPED: Resolve RMF not found at {RMF_PATH}")
        return 0

    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        if not build(r):
            print("FAIL: fakeit failed")
            return 1
        import numpy as np
        vals = np.array(r.xget("AllData(1).values")["result"]["value"]) * EXPO
        total = float(r.xget("AllData(1).rate")["result"]["value"][0] * EXPO)
        median_pb = float(np.median(vals))

        fc = r.fit("cstat", timeout=600)["result"]
        abund_cstat = abund(fc)

        if not build(r):
            print("FAIL: fakeit failed (chi pass)")
            return 1
        fchi = r.fit("chi", timeout=600)["result"]
        abund_chi = abund(fchi)
        chi_red = fchi["statistic"] / fchi["dof"]
    finally:
        r.close()

    print(f"regime : total~{total:.0f} counts, median {median_pb:.1f} count/bin "
          f"(band {BAND})")
    print(f"cstat  : Abund={abund_cstat:.3f} (truth {ABUND_TRUE})")
    print(f"chi    : Abund={abund_chi:.3f}, reduced chi={chi_red:.3f}")

    fails = []
    # the regime must actually be high-total / low-per-bin
    if not (total > 8000 and median_pb <= 3.0):
        fails.append(f"not a high-total/low-per-bin regime "
                     f"(total={total:.0f}, median/bin={median_pb:.1f})")
    # cstat must recover the abundance
    if abs(abund_cstat - ABUND_TRUE) > 0.15:
        fails.append(f"cstat did not recover the abundance "
                     f"({abund_cstat:.3f} vs {ABUND_TRUE})")
    # chi must bias it high, away from truth and from cstat
    if not (abund_chi > abund_cstat + 0.12):
        fails.append(f"chi did not bias the abundance above cstat "
                     f"({abund_chi:.3f} vs {abund_cstat:.3f})")
    # ...behind a spuriously low reduced chi-square
    if not (chi_red < 0.9):
        fails.append(f"chi reduced-statistic not spuriously low ({chi_red:.3f})")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: at ~1 count/bin, chi biases the iron abundance high behind "
          "a reduced chi < 1 where cstat recovers it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
