"""PyXspec execution worker (Tier B, B1).

Runs as a subprocess inside a HEADAS-initialized environment. Reads JSON request
lines from stdin, executes against a live PyXspec session, and writes JSON
responses on a DEDICATED fd (number in $XSPEC_RESP_FD) -- NOT stdout, because
XSPEC prints to stdout at the C++ level and would corrupt the protocol.

Request:  {"cmd": "<name>", "args": {...}}
Response: {"ok": true, "result": {...}} | {"ok": false, "error": "...",
          "category": "..."}
"""
import json
import os
import re
import sys

# protocol channel (inherited fd); responses go here, never to stdout
_resp = os.fdopen(int(os.environ["XSPEC_RESP_FD"]), "w")


def send(obj):
    _resp.write(json.dumps(obj) + "\n")
    _resp.flush()


from xspec import (AllData, AllModels, Model, Fit, Xset, Plot,  # noqa: E402
                   FakeitSettings, Chain, AllChains)


def _headless():
    """Global guards against every hidden interactive prompt (the systemic fix:
    allowPrompting=False is the kill-switch for the whole class of hangs)."""
    Xset.allowPrompting = False
    Xset.chatter = 0
    Xset.logChatter = 0
    Fit.query = "yes"


_headless()

_ERROR_CATS = [
    ("no data loaded", "no_data"),
    ("default (unnamed) model is not defined", "no_model"),
    ("has no response", "no_response"),
    ("out of range", "param_range"),
    ("cannot be frozen", "link"),
    ("table model file not found", "table_file"),
    ("cannot find table model", "table_file"),
    ("new minimum", "new_minimum"),
    ("reduced chi", "poor_fit"),
    ("not a recognised error type", "bad_arg"),
    ("non-monotonicity", "rough_surface"),
    ("cannot open", "file"),
    ("invalid", "bad_arg"),
]


def _classify(msg):
    low = msg.lower()
    for frag, cat in _ERROR_CATS:
        if frag in low:
            return cat
    return "error"


def _dump_params(source=1):
    m = AllModels(source)
    out = []
    for i in range(1, m.nParameters + 1):
        p = AllModels(source)(i)
        out.append({"index": i, "name": p.name, "value": p.values[0],
                    "frozen": p.frozen, "unit": p.unit, "link": p.link})
    return out


# ---- handlers ----

def h_reset(a):
    AllData.clear()
    AllModels.clear()
    _headless()
    return {"cleared": True}


def h_load_data(a):
    spec = a.get("spectrum", 1)
    group = a.get("group") or spec
    AllData(f"{spec}:{group} {a['pha']}")
    s = AllData(spec)
    if a.get("rmf"):
        s.response = a["rmf"]
    if a.get("arf"):
        s.response.arf = a["arf"]
    if a.get("back"):
        s.background = a["back"]
    if a.get("ignore_bad", True):
        AllData.ignore("bad")
    if a.get("energy_range"):
        AllData.ignore(a["energy_range"])
    rmf = bkg = None
    try:
        rmf = s.response.rmf
    except Exception:
        pass
    try:
        bkg = s.background.fileName
    except Exception:
        pass
    return {"spectrum": spec, "group": group, "nSpectra": AllData.nSpectra,
            "nGroups": AllData.nGroups, "exposure": s.exposure,
            "response": rmf, "background": bkg}


def h_define_model(a):
    m = Model(a["expr"], a.get("modName", ""), a.get("sourceNum", 1))
    return {"expression": a["expr"], "modName": a.get("modName", ""),
            "sourceNum": a.get("sourceNum", 1), "components": m.componentNames,
            "nParameters": m.nParameters, "params": _dump_params()}


def h_fit(a):
    if a.get("statistic"):
        Fit.statMethod = a["statistic"]
    Fit.perform()
    return {"statistic": Fit.statistic, "dof": Fit.dof,
            "statMethod": Fit.statMethod, "params": _dump_params()}


def h_get_state(a):
    st = {"nSpectra": AllData.nSpectra, "nGroups": AllData.nGroups,
          "query": Fit.query}
    spectra = []
    for i in range(1, AllData.nSpectra + 1):
        s = AllData(i)
        d = {"index": i, "exposure": s.exposure}
        try:
            d["fileName"] = s.fileName
        except Exception:
            pass
        try:
            d["response"] = s.response.rmf
        except Exception:
            d["response"] = None
        spectra.append(d)
    st["spectra"] = spectra
    try:
        m = AllModels(1)
        st["model"] = {"expression": m.expression,
                       "components": m.componentNames,
                       "nParameters": m.nParameters}
        st["params"] = _dump_params()
    except Exception:
        st["model"] = None
    for key, get in (("statistic", lambda: Fit.statistic),
                     ("dof", lambda: Fit.dof),
                     ("statMethod", lambda: Fit.statMethod),
                     ("testStatistic", lambda: Fit.testStatistic)):
        try:
            st[key] = get()
        except Exception:
            pass
    return st


def _one_param(index, source=1):
    p = AllModels(source)(index)
    return {"index": index, "name": p.name, "value": p.values[0],
            "frozen": p.frozen, "unit": p.unit, "link": p.link}


def h_set_parameter(a):
    idx = a["index"]
    p = AllModels(1)(idx)
    if a.get("values_string"):
        p.values = a["values_string"]
    elif a.get("value") is not None:
        p.values = a["value"]
    if a.get("freeze"):
        p.frozen = True
    if a.get("thaw"):
        p.frozen = False
    if a.get("unlink"):
        p.untie()
    elif a.get("link") is not None:
        lk = a["link"]
        p.link = AllModels(1)(lk) if isinstance(lk, int) else lk
    return {"param": _one_param(idx)}


def h_error(a):
    Fit.error(a["spec"])
    m = AllModels(1)
    out = []
    for i in range(1, m.nParameters + 1):
        p = AllModels(1)(i)
        lo, hi, code = p.error
        out.append({"index": i, "name": p.name, "value": p.values[0],
                    "low": lo, "high": hi, "code": code})
    return {"spec": a["spec"], "params": out}


def h_calc_flux(a):
    spec = a["range"] + (" err" if a.get("err") else "")
    AllModels.calcFlux(spec)
    return {"range": a["range"],
            "spectra": [{"spectrum": i, "flux": list(AllData(i).flux)}
                        for i in range(1, AllData.nSpectra + 1)]}


def h_calc_lumin(a):
    AllModels.calcLumin(a["range"])
    return {"range": a["range"],
            "spectra": [{"spectrum": i, "lumin": list(AllData(i).lumin)}
                        for i in range(1, AllData.nSpectra + 1)]}


def h_steppar(a):
    Fit.steppar(a["spec"])
    return {"spec": a["spec"],
            "delstat": list(Fit.stepparResults("delstat"))}


def h_plot(a):
    Plot.device = "/null"
    Plot.xAxis = a.get("xAxis", "keV")
    types = (a.get("types") or "ldata").split()
    Plot(*types)
    ngroups = max(1, AllData.nGroups)
    panels = []
    for w, t in enumerate(types, 1):          # one plot window per plot type
        groups = []
        for g in range(1, ngroups + 1):       # one group per data group
            try:
                d = {"group": g, "x": list(Plot.x(g, w)),
                     "y": list(Plot.y(g, w))}
            except Exception:
                continue
            for key, fn in (("model", Plot.model), ("yErr", Plot.yErr)):
                try:
                    d[key] = list(fn(g, w))
                except Exception:
                    pass
            groups.append(d)
        panels.append({"window": w, "type": t, "groups": groups})
    return {"types": types, "xAxis": Plot.xAxis, "nGroups": ngroups,
            "panels": panels}


def h_fakeit(a):
    if a.get("seed") is not None:
        Xset.seed = a["seed"]
    # drop None/empty so FakeitSettings gets '' (its "use current") default
    # rather than the literal string "None"
    s = {k: v for k, v in (a.get("settings") or {}).items()
         if v is not None and v != ""}
    fs = FakeitSettings(response=s.get("response", ""), arf=s.get("arf", ""),
                        background=s.get("background", ""),
                        exposure=s.get("exposure", ""))
    AllData.fakeit(a.get("nSpectra", 1), fs,
                   applyStats=a.get("applyStats", True),
                   noWrite=a.get("noWrite", True))
    return {"nSpectra": AllData.nSpectra}


def h_run_mcmc(a):
    AllChains.clear()
    if os.path.exists(a["fileName"]):
        os.remove(a["fileName"])           # fresh chain (Chain appends otherwise)
    Chain(a["fileName"], burn=a.get("burn", 1000),
          runLength=a.get("runLength", 10000), walkers=a.get("walkers", 10),
          algorithm=a.get("algorithm", "gw"))
    return {"fileName": a["fileName"], "runLength": a.get("runLength", 10000)}


# ---- generic dispatch: reach 100% of the PyXspec object-model API ----
# A target is  ROOT ( .attr | (int) )*  resolved against the live objects with
# getattr / __call__(int) -- NOT eval. Covers e.g. "Fit.covariance",
# "AllModels(1)(2).values", "AllData(1).response.rmf", "Xset.parallel.leven".
_ROOTS = {"AllData": AllData, "AllModels": AllModels, "Fit": Fit,
          "Xset": Xset, "Plot": Plot, "AllChains": AllChains}
_STEP = re.compile(r"\.([A-Za-z_]\w*)|\((-?\d+)\)")


def _parse_target(target):
    m = re.match(r"\s*([A-Za-z_]\w*)\s*", target)
    if not m or m.group(1) not in _ROOTS:
        raise ValueError(f"target must start with one of {sorted(_ROOTS)}")
    root, rest, i, steps = m.group(1), target[m.end():], 0, []
    for tm in _STEP.finditer(rest):
        if tm.start() != i:
            raise ValueError(f"cannot parse target near: {rest[i:]!r}")
        i = tm.end()
        steps.append(("attr", tm.group(1)) if tm.group(1) is not None
                     else ("call", int(tm.group(2))))
    if rest[i:].strip():
        raise ValueError(f"trailing characters in target: {rest[i:]!r}")
    return root, steps


def _walk(root, steps):
    obj = _ROOTS[root]
    for kind, val in steps:
        obj = getattr(obj, val) if kind == "attr" else obj(val)
    return obj


def _safe(v):
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, (list, tuple)):
        return [_safe(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _safe(x) for k, x in v.items()}
    return {"_type": type(v).__name__, "repr": repr(v)[:500]}


def h_xget(a):
    root, steps = _parse_target(a["target"])
    return {"target": a["target"], "value": _safe(_walk(root, steps))}


def h_xset(a):
    root, steps = _parse_target(a["target"])
    if not steps or steps[-1][0] != "attr":
        raise ValueError("set target must end in an attribute")
    parent = _walk(root, steps[:-1])
    setattr(parent, steps[-1][1], a["value"])
    return {"target": a["target"],
            "value": _safe(getattr(parent, steps[-1][1]))}


def h_xcall(a):
    root, steps = _parse_target(a["target"])
    obj = _walk(root, steps)
    method = getattr(obj, a["method"])
    result = method(*(a.get("args") or []), **(a.get("kwargs") or {}))
    return {"target": a["target"], "method": a["method"],
            "result": _safe(result)}


def h_save_session(a):
    # save to an existing file otherwise prompts "overwrite?" and blocks
    if os.path.exists(a["fileName"]):
        os.remove(a["fileName"])
    Xset.save(a["fileName"], info=a.get("info", "a"))
    return {"fileName": a["fileName"]}


def h_restore_session(a):
    Xset.restore(a["fileName"])
    _headless()          # an .xcm is a Tcl script; it may have re-enabled prompts
    return h_get_state({})


HANDLERS = {"reset_session": h_reset, "load_data": h_load_data,
            "define_model": h_define_model, "fit": h_fit,
            "get_state": h_get_state, "set_parameter": h_set_parameter,
            "error": h_error, "calc_flux": h_calc_flux,
            "calc_lumin": h_calc_lumin, "steppar": h_steppar, "plot": h_plot,
            "fakeit": h_fakeit, "run_mcmc": h_run_mcmc,
            "save_session": h_save_session,
            "restore_session": h_restore_session,
            "xget": h_xget, "xset": h_xset, "xcall": h_xcall}


def main():
    send({"ready": True})
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            send({"ok": False, "error": "invalid JSON request",
                  "category": "protocol"})
            continue
        cmd = req.get("cmd")
        if cmd == "shutdown":
            send({"ok": True, "result": {"bye": True}})
            break
        h = HANDLERS.get(cmd)
        if not h:
            send({"ok": False, "error": f"unknown command '{cmd}'",
                  "category": "protocol"})
            continue
        try:
            send({"ok": True, "result": h(req.get("args") or {})})
        except Exception as e:
            send({"ok": False, "error": str(e), "category": _classify(str(e))})


if __name__ == "__main__":
    main()
