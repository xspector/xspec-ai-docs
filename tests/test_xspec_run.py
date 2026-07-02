"""Tier B (execution) proof-of-concept test.

Drives the runner against the manual's walkthrough datasets. The runner
bootstraps HEADAS itself, so this test only needs the HEADAS install to exist;
it is skipped otherwise. Verifies a real end-to-end fit through the
worker-subprocess protocol, and that the path allowlist rejects outside paths.

Run:  python tests/test_xspec_run.py
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "server"))
from runner import XspecRunner, DEFAULT_HEADAS  # noqa: E402

DATA = Path("/Users/kaa/software/Xspec-aux/doc/manual/walkthrough")

if not Path(DEFAULT_HEADAS).exists():
    print(f"SKIPPED: HEADAS not found at {DEFAULT_HEADAS}")
    sys.exit(0)

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


r = XspecRunner(data_root=str(DATA))
try:
    r.start()

    # path allowlist rejects a file outside the data root
    try:
        r.load_data("/etc/hosts")
        fails.append("allowlist did NOT reject /etc/hosts")
    except ValueError:
        pass

    check(r.reset_session().get("ok"), "reset_session ok")

    ld = r.load_data("s54405.pha", ignore_bad=True, energy_range="**-0.5 8.0-**")
    check(ld["ok"], f"load_data ok: {ld}")
    check(ld["result"]["nSpectra"] == 1, "one spectrum loaded")
    check(ld["result"]["exposure"] > 0, "exposure > 0")

    dm = r.define_model("tbabs*powerlaw")
    check(dm["ok"], f"define_model ok: {dm}")
    check(dm["result"]["components"] == ["TBabs", "powerlaw"],
          f"components: {dm['result'].get('components')}")

    ft = r.fit("cstat")
    check(ft["ok"], f"fit ok: {ft}")
    res = ft["result"]
    check(res["statistic"] > 0 and res["dof"] > 0, "fit produced stat/dof")
    check(any(p["name"] == "PhoIndex" for p in res["params"]),
          "PhoIndex in fitted params")

    st = r.get_state()["result"]
    check(st["nSpectra"] == 1 and st["model"]["components"] == ["TBabs",
          "powerlaw"], "get_state reflects session")

    # ---- B2: set_parameter, error, flux, lumin, steppar, plot ----
    pho_idx = next(p["index"] for p in res["params"] if p["name"] == "PhoIndex")
    sp = r.set_parameter(pho_idx, freeze=True)
    check(sp["ok"] and sp["result"]["param"]["frozen"], "set_parameter freeze")
    r.set_parameter(pho_idx, thaw=True)
    r.fit("cstat")   # freeze/thaw changes the model -> refit before error()

    er = r.error("2.706 %d" % pho_idx)
    check(er["ok"], f"error ok: {er}")
    ep = next(p for p in er["result"]["params"] if p["index"] == pho_idx)
    check(ep["low"] < ep["high"], "error interval low<high")

    fx = r.calc_flux("0.5 8.0")
    check(fx["ok"] and fx["result"]["spectra"][0]["flux"][0] > 0, "calc_flux")
    lm = r.calc_lumin("0.5 8.0 0.01")
    check(lm["ok"] and lm["result"]["spectra"][0]["lumin"][0] > 0, "calc_lumin")

    stp = r.steppar("%d 1.8 2.2 6" % pho_idx)
    check(stp["ok"] and len(stp["result"]["delstat"]) == 7, "steppar grid")
    capped = r.steppar("%d 1 2 100000" % pho_idx)
    check(not capped["ok"] and capped["category"] == "capped", "steppar cap")

    pl_ = r.plot("ldata delchi")
    check(pl_["ok"] and len(pl_["result"]["x"]) > 0 and "model" in pl_["result"],
          "plot arrays")

    # ---- B3: fakeit, mcmc, save/restore ----
    fk = r.fakeit(nSpectra=1, applyStats=True, seed=42)
    check(fk["ok"] and fk["result"]["nSpectra"] == 1, "fakeit")
    # fakeit replaced the spectrum; reload real data for a current fit
    r.reset_session()
    r.load_data("s54405.pha", energy_range="**-0.5 8.0-**")
    r.define_model("tbabs*powerlaw")
    r.fit("cstat")

    mc = r.run_mcmc("poc_chain.fits", burn=50, runLength=200, walkers=8)
    check(mc["ok"], f"run_mcmc: {mc}")

    sv = r.save_session("poc_session.xcm")
    check(sv["ok"], f"save_session: {sv}")
    r.reset_session()
    rs = r.restore_session("poc_session.xcm")
    check(rs["ok"] and rs["result"]["nSpectra"] == 1, "restore_session")

    # write allowlist: saving outside the output root is rejected
    try:
        r.save_session("/etc/poc.xcm")
        fails.append("write allowlist did NOT reject /etc")
    except ValueError:
        pass

    if not fails:
        pl = next(p for p in res["params"] if p["name"] == "PhoIndex")
        print(f"Tier B PoC OK: stat={res['statistic']:.1f}/{res['dof']} "
              f"PhoIndex={pl['value']:.2f} err=[{ep['low']:.2f},{ep['high']:.2f}] "
              f"flux={fx['result']['spectra'][0]['flux'][0]:.2e} "
              f"steppts={len(stp['result']['delstat'])} "
              f"plotpts={len(pl_['result']['x'])}")
        print("B2/B3 tools verified: set_parameter, error, calc_flux, "
              "calc_lumin, steppar(+cap), plot, fakeit, save/restore, mcmc")
finally:
    r.close()

if fails:
    print("FAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("all Tier B PoC checks passed")
