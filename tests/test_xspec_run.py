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

    if not fails:
        pl = next(p for p in res["params"] if p["name"] == "PhoIndex")
        print(f"Tier B PoC OK: stat={res['statistic']:.1f}/{res['dof']} "
              f"PhoIndex={pl['value']:.2f} statMethod={res['statMethod']}")
finally:
    r.close()

if fails:
    print("FAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("all Tier B PoC checks passed")
