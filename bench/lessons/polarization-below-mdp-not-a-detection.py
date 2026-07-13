"""Validation harness for casebook lesson `polarization-below-mdp-not-a-detection`.

Claim: the polarization degree PD=sqrt(Q^2+U^2)/I is positive-definite, so an
unpolarized source returns a non-zero measured PD, and PD/sigma_PD over-states
significance; the honest threshold is the MDP (~3 sigma_PD). A genuinely polarized
source above the MDP is recovered cleanly.

Ground-truth test (fakeit) on the manual's toy IXPE Stokes responses:
  * UNPOLARIZED (A=0): over many realizations the measured PD is positive-biased
    (median > 0, never near 0), the 99th percentile (MDP99) is ~3 sigma_PD, and
    PD/sigma_PD exceeds 2 far more often than the Gaussian ~2.3%;
  * POLARIZED (A=0.10): recovered well above the MDP at high significance.

A lesson earns `validated` only if both hold. chi is used because the toy Stokes
spectra carry independent errors (no XCOV); the positive-bias is statistic-independent.

Run:  python bench/lessons/polarization-below-mdp-not-a-detection.py
Needs HEADAS/PyXspec AND the toy IXPE Stokes files in the manual walkthrough;
prints SKIPPED and exits 0 if either is absent. ~120 fits, a few minutes.
Exit non-zero on failure.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough"
W = DATA + "/"
RMF, ARF, MRF = (W + "toyteldu1fictionalv002.rmf",
                 W + "toyteldu1fictionalv002.arf",
                 W + "toyteldu1fictionalv002.mrf")
TOY_I = W + "toy_point_source_du1_pha1.fits"
NORM, EXPO, M = 10.0, 5000.0, 120


def setup(r):
    r.reset_session()
    r.load_data("toy_point_source_du1_pha1.fits",  spectrum=1, group=1)
    r.load_data("toy_point_source_du1_pha1q.fits", spectrum=1, group=2)
    r.load_data("toy_point_source_du1_pha1u.fits", spectrum=1, group=3)
    for i, (rf, af) in enumerate([(RMF, ARF), (RMF, MRF), (RMF, MRF)], 1):
        r.xset(f"AllData({i}).response", rf)
        r.xset(f"AllData({i}).response.arf", af)
    r.define_model("polconst*powerlaw")


def measure(r, a_true, seed):
    """fakeit a Stokes triplet at polarization a_true, fit, return (PD, sigma_PD)."""
    r.xcall("AllModels(1)", "setPars", [a_true, 30.0, 2.0, NORM])
    r.fakeit(settings={"exposure": EXPO}, seed=seed)
    r.xcall("AllData", "ignore", ["1-3:**-2.0 8.0-**"])
    r.xcall("AllModels(1)", "setPars", [0.05, 20.0, 2.0, NORM])
    r.set_parameter(1, values_string="0.05,0.001,0,0,1,1")   # A in [0,1]
    f = r.fit("chi", timeout=120)
    if not f.get("ok"):
        return None, None
    pd = {x["index"]: x for x in f["result"]["params"]}[1]["value"]
    sig = r.xget("AllModels(1)(1).sigma")["result"]["value"]
    return pd, sig


def main():
    if not Path(DEFAULT_HEADAS).exists():
        print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
        return 0
    if not Path(TOY_I).exists():
        print(f"SKIPPED: toy IXPE Stokes data not found at {TOY_I}")
        return 0

    import numpy as np
    r = XspecRunner(data_root=DATA)
    r.start()
    try:
        setup(r)
        pds, sigs = [], []
        for k in range(M):
            pd, sig = measure(r, 0.0, 700 + k)     # unpolarized
            if pd is not None and sig and sig > 0:
                pds.append(pd)
                sigs.append(sig)
        pol_pd, pol_sig = measure(r, 0.10, 999)    # genuinely polarized
    finally:
        r.close()

    pd = np.array(pds)
    s = np.array(sigs)
    ratio = pd / s
    med, mdp99, med_sig = np.median(pd), np.percentile(pd, 99), np.median(s)
    far2 = np.mean(ratio > 2)
    pol_ratio = pol_pd / pol_sig if pol_sig else 0.0
    print(f"unpolarized: median PD={med*100:.2f}% MDP99={mdp99*100:.2f}% "
          f"(MDP99/sigma={mdp99/med_sig:.2f})  P(PD/sig>2)={far2*100:.1f}%  min PD={pd.min()*100:.3f}%")
    print(f"polarized A=0.10: measured {pol_pd:.4f}  PD/sig={pol_ratio:.1f}")

    fails = []
    if not med > 0.5 * med_sig:
        fails.append(f"measured PD not positive-biased (median {med*100:.2f}%)")
    if not pd.min() > 0:
        fails.append("some measured PD reached 0 (should be strictly positive)")
    if not 2.5 < mdp99 / med_sig < 3.6:
        fails.append(f"MDP99 not ~3 sigma (MDP99/sigma={mdp99/med_sig:.2f})")
    if not far2 > 0.08:
        fails.append(f"PD/sigma>2 not over-represented ({far2*100:.1f}%, need >8%)")
    if not pol_ratio > 10:
        fails.append(f"genuine 10% polarization not recovered above the MDP (PD/sig={pol_ratio:.1f})")

    if fails:
        print("\nLESSON NOT VALIDATED:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nVALIDATED: unpolarized PD is positive-biased and PD/sigma over-claims "
          "(MDP99 ~ 3 sigma); a genuine 10% polarization is recovered far above the MDP")
    return 0


if __name__ == "__main__":
    sys.exit(main())
