"""Verification harness.

Two tiers:
  1. Corpus integrity (always runs): manifest ↔ files consistent, JSON valid,
     no empty math, params present.
  2. Recipe execution (runs only when HEADAS is initialized): executes recipes
     against the datasets shipped in the manual's walkthrough/ directory. A
     recipe that raises fails the build.

Exit non-zero on any failure so it can gate a build.
Run:  python tests/run_recipes.py
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CORPUS = REPO / "corpus"
WALKTHROUGH = Path(os.environ.get(
    "XSPEC_MANUAL_DIR",
    "/Users/kaa/software/Xspec-aux/doc/manual")) / "walkthrough"

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def tier1_corpus_integrity():
    manifest = json.loads((CORPUS / "manifest.json").read_text())
    check("xspec_version" in manifest["provenance"], "manifest missing version")
    for m in manifest["models"]:
        name = m["name"]
        md = CORPUS / "models" / f"{name}.md"
        js = CORPUS / "models" / f"{name}.json"
        check(md.exists(), f"{name}: markdown missing")
        check(js.exists(), f"{name}: json missing")
        if js.exists():
            d = json.loads(js.read_text())
            # model.dat declares the count; a mixing model may have none
            # (crossarf, mixmatrix), any other must match its declaration.
            check(len(d["params"]) == d["npars_declared"] + (d["type"] == "add"),
                  f"{name}: {len(d['params'])} params, model.dat declares "
                  f"{d['npars_declared']}")
            if d["type"] == "add":
                check(any(p["kind"] == "norm" for p in d["params"]),
                      f"{name}: additive model lacks implicit norm")
        if md.exists():
            body = md.read_text()
            check("$$$$" not in body and "^{-}" not in body,
                  f"{name}: empty/broken math (macro ate a math token)")
    print(f"tier1: checked {len(manifest['models'])} models")

    # grounding set present and non-empty
    for key in ("command_tokens", "commands", "plot_types", "tclout_keys",
                "xset_keys", "abundances", "xsect"):
        check(manifest.get(key), f"manifest.{key} missing/empty")
    for cmd in ("fit", "data", "model", "abund"):
        check(cmd in manifest["command_tokens"], f"token '{cmd}' missing")
    for tbl in ("wilm", "angr", "aspl"):
        check(tbl in manifest["abundances"], f"abundance '{tbl}' missing")
    check(set(manifest["xsect"]) >= {"vern", "bcmc", "obcm"}, "xsect incomplete")
    check("cstat" in manifest["statistics"]["fit"], "cstat not a fit statistic")
    # every command doc entry has a file on disk
    for c in manifest["commands"]:
        check((CORPUS / "commands" / f"{c['name']}.md").exists(),
              f"command doc missing: {c['name']}")
    print(f"tier1: checked grounding set "
          f"({len(manifest['command_tokens'])} tokens, "
          f"{len(manifest['commands'])} command docs)")

    # intent index: every API ref must exist in the extracted api.json
    api = json.loads((CORPUS / "api" / "api.json").read_text())

    def _members(cls):
        e = api.get(cls, {})
        return ({a["name"] for a in e.get("attributes", [])} |
                {m["name"] for m in e.get("methods", [])})

    intents = json.loads((CORPUS / "intent_index.json").read_text())
    for r in intents:
        for cls, member in r["refs"]:
            check(cls in api, f"intent '{r['intent']}': unknown class {cls}")
            check(member in _members(cls),
                  f"intent '{r['intent']}': {cls}.{member} not in api.json")
    print(f"tier1: checked intent index ({len(intents)} intents, all API "
          "refs resolve)")


# Recipes are (label, callable) pairs. Each callable runs a full PyXspec
# workflow against a shipped dataset and asserts on typed results.
def _recipe_powerlaw_fit():
    from xspec import AllData, Model, Fit, Xset, AllModels
    Xset.chatter = 0
    Fit.query = "yes"
    AllData.clear(); AllModels.clear()
    AllData(f"1:1 {WALKTHROUGH/'s54405.pha'}")
    AllData.ignore("bad")
    AllData.ignore("**-0.5 8.0-**")
    Fit.statMethod = "cstat"
    Model("tbabs*powerlaw")
    Fit.perform()
    assert Fit.dof > 0 and Fit.statistic > 0, "fit produced no statistic"
    return f"stat={Fit.statistic:.1f}/{Fit.dof}"


def _recipe_guide_surface():
    """Exercises every API surface asserted in guides 01 and 02."""
    from xspec import AllData, AllModels, Model, Fit, Xset, Plot
    Xset.chatter = 0
    Fit.query = "yes"                                     # guide 01 §1
    Xset.abund = "wilm"; Xset.xsect = "vern"             # guide 02 §5
    AllData.clear(); AllModels.clear()
    AllData(f"1:1 {WALKTHROUGH/'s54405.pha'}")            # load (returns None)
    s = AllData(1)                                        # get Spectrum object
    _ = s.exposure                                        # guide 02 §2
    rmf = s.response.rmf                                  # raises if none
    try:
        _ = s.background.fileName
    except Exception:
        pass
    AllData.ignore("bad"); AllData.ignore("**-0.5 8.0-**")  # guide 02 §4
    Fit.statMethod = "cstat"                              # guide 02 §3
    Model("tbabs*powerlaw")
    Fit.perform()
    stat, dof = Fit.statistic, Fit.dof                    # guide 01 §5
    val = AllModels(1)(2).values[0]                       # PhoIndex value
    frozen = AllModels(1)(2).frozen
    Fit.error("2.706 2")                                  # guide 01 errors
    lo, hi, code = AllModels(1)(2).error
    AllModels.calcFlux("0.5 8.0")                         # guide 01 flux
    flux_ergs = AllData(1).flux[0]
    Plot.device = "/null"; Plot.xAxis = "keV"            # guide 01 §6
    Plot("data", "resid")
    npts = len(Plot.x()), len(Plot.model())
    assert stat > 0 and dof > 0 and rmf and flux_ergs > 0 and npts[0] > 0
    return (f"stat={stat:.1f}/{dof} PhoIndex={val:.2f}[{lo:.2f},{hi:.2f}] "
            f"flux={flux_ergs:.2e} plotpts={npts[0]}")


def _recipe_recipes_surface():
    """Verify executable claims in guide 03 (recipes): named component/param
    access, error code, steppar, calcLumin, goodness, save/restore, chains."""
    import os as _os
    from xspec import (AllData, AllModels, Model, Fit, Xset, Chain, AllChains)
    Xset.chatter = 0
    Fit.query = "yes"; Xset.abund = "wilm"
    AllData.clear(); AllModels.clear()
    AllData(f"1:1 {WALKTHROUGH/'s54405.pha'}")
    AllData.ignore("bad"); AllData.ignore("**-0.5 8.0-**")
    Fit.statMethod = "cstat"
    m = Model("tbabs*powerlaw")
    comps = m.componentNames                         # R1/R8 named access
    m.TBabs.nH = 0.1                                  # component.parameter
    m.powerlaw.PhoIndex = 1.8
    Fit.perform()
    Fit.error("2.706 2")                             # R2
    code = AllModels(1)(2).error[2]
    Fit.steppar("2 1.8 2.2 8")                       # R4
    dstat = Fit.stepparResults("delstat")
    AllModels.calcLumin("0.5 10.0 0.01")            # R3
    lum = AllData(1).lumin[0]
    g = Fit.goodness(50, sim=True)                   # R9
    xcm = str(WALKTHROUGH.parent / "_probe_session.xcm")
    if _os.path.exists(xcm):
        _os.remove(xcm)
    Xset.save(xcm, info="a")                          # R10
    saved = _os.path.exists(xcm)
    _os.remove(xcm)
    chf = str(WALKTHROUGH.parent / "_probe_chain.fits")
    if _os.path.exists(chf):
        _os.remove(chf)
    AllChains.clear()
    Chain(chf, burn=50, runLength=200, algorithm="gw", walkers=8)  # R7 (runs)
    made_chain = _os.path.exists(chf)
    _os.remove(chf)
    assert comps == ["TBabs", "powerlaw"], f"component names: {comps}"
    assert len(dstat) == 9 and lum > 0 and saved and made_chain
    return (f"comps={comps} errcode={code} steppts={len(dstat)} "
            f"lumin={lum:.2e} goodness={g:.0f}% save={saved} chain={made_chain}")


def _recipe_link_fakeit():
    """Verify R8 link/untie (2 data groups) and R6 fakeit."""
    from xspec import (AllData, AllModels, Model, Fit, Xset, FakeitSettings)
    Xset.chatter = 0; Fit.query = "yes"
    AllData.clear(); AllModels.clear()
    p = str(WALKTHROUGH / "s54405.pha")
    AllData(f"1:1 {p} 2:2 {p}")                       # 2 spectra, 2 groups
    AllData.ignore("bad"); AllData.ignore("**-0.5 8.0-**")
    Fit.statMethod = "cstat"
    Model("tbabs*powerlaw")
    AllModels(2).powerlaw.PhoIndex.link = AllModels(1).powerlaw.PhoIndex
    linked = bool(AllModels(2).powerlaw.PhoIndex.link)
    AllModels(2)(3).untie()
    unlinked = not AllModels(2)(3).link
    Xset.seed = 12345
    fs = FakeitSettings(exposure=1000.0)
    AllData.fakeit(2, fs, applyStats=True, noWrite=True)  # reuse responses
    faked = AllData.nSpectra
    assert linked and unlinked and faked == 2
    return f"linked={linked} untied={unlinked} fakeit_nspec={faked}"


def _recipe_api_introspection():
    """Verify the extracted PyXspec API against live objects: every documented
    attribute/method must exist on the real object (no drift, no hallucination),
    and the critical return shapes must match the object-model primer."""
    import json as _json
    from xspec import (AllData, AllModels, Model, Fit, Xset, Plot, AllChains)
    api = _json.load(open(CORPUS / "api" / "api.json"))
    Xset.chatter = 0; Fit.query = "yes"
    AllData.clear(); AllModels.clear()
    AllData(f"1:1 {WALKTHROUGH/'s54405.pha'}")
    AllData.ignore("bad"); AllData.ignore("**-0.5 8.0-**")
    Fit.statMethod = "cstat"
    Model("tbabs*powerlaw")
    live = {
        "FitManager": Fit, "XspecSettings": Xset, "PlotManager": Plot,
        "DataManager": AllData, "ModelManager": AllModels,
        "ChainManager": AllChains, "Spectrum": AllData(1),
        "Model": AllModels(1), "Component": AllModels(1).TBabs,
        "Parameter": AllModels(1)(1), "Response": AllData(1).response,
    }
    checked = ghosts = 0
    problems = []
    for cls, obj in live.items():
        real = {a for a in dir(obj) if not a.startswith("_")}
        documented = {x["name"] for x in api[cls]["attributes"]} | \
                     {x["name"] for x in api[cls]["methods"] if not
                      x["name"].startswith("__")}
        missing = documented - real          # documented but not on object
        if missing:
            problems.append(f"{cls}: documented-but-absent {sorted(missing)}")
        checked += 1
        ghosts += len(missing)
    # critical shape checks from the primer
    Fit.perform()
    v = AllModels(1)(2).values
    e = AllModels(1)(2).error
    AllModels.calcFlux("0.5 8.0")
    fx = AllData(1).flux
    if not (isinstance(v, list) and len(v) == 6):
        problems.append(f"Parameter.values not list[6]: {type(v)},{len(v)}")
    if not (isinstance(e, tuple) and len(e) == 3):
        problems.append(f"Parameter.error not tuple[3]: {type(e)},{len(e)}")
    if not (isinstance(fx, tuple) and len(fx) == 6):
        problems.append(f"Spectrum.flux not tuple[6]: {type(fx)},{len(fx)}")
    assert not problems, "; ".join(problems)
    return f"introspected {checked} classes, 0 ghosts; shapes OK"


RECIPES = [("tbabs*powerlaw fit on s54405.pha", _recipe_powerlaw_fit),
           ("guide 01+02 API surface", _recipe_guide_surface),
           ("guide 03 recipes surface", _recipe_recipes_surface),
           ("guide 03 link/untie/fakeit", _recipe_link_fakeit),
           ("PyXspec API vs live introspection", _recipe_api_introspection)]


def tier2_recipe_execution():
    if not os.environ.get("HEADAS"):
        print("tier2: SKIPPED (HEADAS not initialized)")
        return
    try:
        import xspec  # noqa: F401
    except Exception as e:
        fails.append(f"tier2: cannot import xspec: {e}")
        return
    for label, fn in RECIPES:
        try:
            result = fn()
            print(f"tier2: OK   {label}  ->  {result}")
        except Exception as e:
            fails.append(f"tier2: FAIL {label}: {e}")


if __name__ == "__main__":
    tier1_corpus_integrity()
    tier2_recipe_execution()
    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("\nAll checks passed.")
