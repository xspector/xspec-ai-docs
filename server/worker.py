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
import math
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

# session journal: every mutating op, so export_script can reproduce the session
_JOURNAL = []

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
    _JOURNAL.clear()
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


def h_assess_fit(a):
    """Composite quality check so the agent doesn't have to remember them all."""
    issues, kinds = [], []

    def flag(kind, msg):
        # kind is a stable category (casebook `assess_issue_kind` vocab) so
        # episodes/telemetry carry categories, not prose; msg is the human line.
        kinds.append(kind)
        issues.append(msg)

    stat, dof, sm = Fit.statistic, Fit.dof, Fit.statMethod
    reduced = stat / dof if dof else None

    # parameters pegged at a soft limit (values = [val,delta,hmin,smin,smax,hmax])
    m = AllModels(1)
    for i in range(1, m.nParameters + 1):
        p = AllModels(1)(i)
        if p.frozen or p.link:
            continue
        val, smin, smax = p.values[0], p.values[3], p.values[4]
        # "pegged" = clamped to a limit: closeness relative to the limit's own
        # scale, NOT the (possibly enormous) full range.
        if abs(val - smin) <= 1e-6 * max(1.0, abs(smin), abs(val)):
            flag("pegged_limit", f"par {i} ({p.name}) pegged at soft min {smin:g}")
        elif abs(val - smax) <= 1e-6 * max(1.0, abs(smax), abs(val)):
            flag("pegged_limit", f"par {i} ({p.name}) pegged at soft max {smax:g}")

    # residual correlation: Wald-Wolfowitz runs test on delchi
    runs_info = None
    try:
        Plot.device = "/null"
        Plot("delchi")
        res = []
        for g in range(1, max(1, AllData.nGroups) + 1):
            try:
                res += list(Plot.y(g, 1))
            except Exception:
                pass
        signs = [1 if v > 0 else -1 for v in res if v != 0]
        n1 = signs.count(1)
        n2 = signs.count(-1)
        n = n1 + n2
        if n > 10 and n1 and n2:
            runs = 1 + sum(signs[k] != signs[k - 1] for k in range(1, n))
            mu = 2 * n1 * n2 / n + 1
            var = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n * n * (n - 1))
            z = (runs - mu) / math.sqrt(var) if var > 0 else 0.0
            runs_info = {"runs": runs, "expected": round(mu, 1),
                         "z": round(z, 2), "nbins": n}
            if z < -2:
                flag("systematic_residual",
                     f"systematic residuals (runs test z={z:.1f}; "
                     "model likely missing structure)")
    except Exception:
        pass

    # reduced chi-square sanity (only meaningful for chi)
    if sm == "chi" and reduced is not None:
        if reduced > 1.5:
            flag("reduced_chi_high",
                 f"reduced chi-square high ({reduced:.2f}); poor fit")
        elif reduced < 0.5:
            flag("reduced_chi_low",
                 f"reduced chi-square low ({reduced:.2f}); "
                 "over-fit or over-estimated errors")

    # optional Monte-Carlo goodness (slow; opt-in)
    goodness = None
    sims = a.get("goodness_sims", 0)
    if sims and sm in ("cstat", "lstat", "pgstat", "pstat"):
        goodness = Fit.goodness(sims, sim=True)
        if goodness >= 95:
            flag("goodness_poor",
                 f"goodness {goodness:.0f}% of sims below observed; "
                 "fit worse than most simulations")

    return {"statistic": stat, "dof": dof, "statMethod": sm,
            "reduced": reduced, "runs_test": runs_info, "goodness": goodness,
            "acceptable": not issues, "issues": issues, "issue_kinds": kinds}


# file extension -> giza/PGPLOT device. This giza build's reliable hardcopy
# drivers in the persistent worker are the single-file vector formats /pdf and
# /ps (they write the exact filename and flush on device close). The raster/
# per-page drivers (/png, /svg) buffer to '<stem>_NNNN<ext>' and do NOT reliably
# materialize a file in the long-lived worker, and /gif is absent -- so they are
# deliberately not offered. PDF is the recommended "figure for a human".
_IMG_DEV = {".pdf": "/pdf", ".ps": "/ps"}


def h_plot_image(a):
    fn = a["fileName"]
    ext = os.path.splitext(fn)[1].lower()
    dev = _IMG_DEV.get(ext)
    if not dev:
        raise ValueError(f"unsupported image extension {ext!r}; use one of "
                         f"{sorted(_IMG_DEV)} (this giza build has no working "
                         "png/gif hardcopy driver in the worker; use .pdf)")
    try:
        os.remove(fn)                               # clear any stale output
    except OSError:
        pass
    # an unavailable device fails at Plot() time (often with an empty message),
    # not on assignment -> convert to a clear error.
    try:
        Plot.device = fn + dev
        Plot.xAxis = a.get("xAxis", "keV")
        Plot(*(a.get("types") or "ldata delchi").split())
    except Exception:
        Plot.device = "/null"
        raise ValueError(f"could not render {dev} ({ext}) in this giza/PGPLOT "
                         "build")
    Plot.device = "/null"                            # close/flush the hardcopy
    if not (os.path.exists(fn) and os.path.getsize(fn) > 0):
        raise ValueError(f"{dev} produced no output for {ext} in this "
                         "giza/PGPLOT build")
    return {"fileName": fn, "device": dev}


# ---- session journal -> reproducible script ----

def _fmt_args(args, kwargs):
    parts = [repr(x) for x in (args or [])]
    parts += [f"{k}={v!r}" for k, v in (kwargs or {}).items()]
    return ", ".join(parts)


def _script_lines(rec):
    c, a = rec["cmd"], rec["args"]
    if c == "load_data":
        spec, grp = a.get("spectrum", 1), a.get("group") or a.get("spectrum", 1)
        out = [f'AllData("{spec}:{grp} {a["pha"]}")']
        s = f"AllData({spec})"
        if a.get("rmf"):
            out.append(f'{s}.response = "{a["rmf"]}"')
        if a.get("arf"):
            out.append(f'{s}.response.arf = "{a["arf"]}"')
        if a.get("back"):
            out.append(f'{s}.background = "{a["back"]}"')
        if a.get("ignore_bad", True):
            out.append('AllData.ignore("bad")')
        if a.get("energy_range"):
            out.append(f'AllData.ignore("{a["energy_range"]}")')
        return out
    if c == "define_model":
        extra = ""
        if a.get("modName"):
            extra = f', "{a["modName"]}", {a.get("sourceNum", 1)}'
        elif a.get("sourceNum", 1) != 1:
            extra = f', "", {a["sourceNum"]}'
        return [f'Model("{a["expr"]}"{extra})']
    if c == "set_parameter":
        p = f"AllModels(1)({a['index']})"
        out = []
        if a.get("values_string"):
            out.append(f'{p}.values = "{a["values_string"]}"')
        elif a.get("value") is not None:
            out.append(f"{p}.values = {a['value']!r}")
        if a.get("freeze"):
            out.append(f"{p}.frozen = True")
        if a.get("thaw"):
            out.append(f"{p}.frozen = False")
        if a.get("unlink"):
            out.append(f"{p}.untie()")
        elif a.get("link") is not None:
            lk = a["link"]
            out.append(f"{p}.link = AllModels(1)({lk})" if isinstance(lk, int)
                       else f'{p}.link = "{lk}"')
        return out
    if c == "fit":
        out = []
        if a.get("statistic"):
            out.append(f'Fit.statMethod = "{a["statistic"]}"')
        out.append("Fit.perform()")
        return out
    if c == "error":
        return [f'Fit.error("{a["spec"]}")']
    if c == "calc_flux":
        r = a["range"] + (" err" if a.get("err") else "")
        return [f'AllModels.calcFlux("{r}")']
    if c == "calc_lumin":
        return [f'AllModels.calcLumin("{a["range"]}")']
    if c == "steppar":
        return [f'Fit.steppar("{a["spec"]}")']
    if c == "fakeit":
        return [f"# fakeit({a.get('nSpectra', 1)} spectra, "
                f"settings={a.get('settings')})"]
    if c == "save_session":
        return [f'Xset.save("{a["fileName"]}", info="{a.get("info", "a")}")']
    if c == "restore_session":
        return [f'Xset.restore("{a["fileName"]}")']
    if c == "xset":
        return [f"{a['target']} = {a['value']!r}"]
    if c == "xcall":
        return [f"{a['target']}.{a['method']}({_fmt_args(a.get('args'), a.get('kwargs'))})"]
    return [f"# (unrepr) {c} {a}"]


def h_export_script(a):
    header = ["from xspec import *", "", "Xset.allowPrompting = False",
              'Fit.query = "yes"', "AllData.clear()", "AllModels.clear()", ""]
    body = []
    for rec in _JOURNAL:
        body += _script_lines(rec)
    return {"nOps": len(_JOURNAL), "script": "\n".join(header + body) + "\n"}


def h_journal(a):
    return {"nOps": len(_JOURNAL), "ops": list(_JOURNAL)}


HANDLERS = {"reset_session": h_reset, "load_data": h_load_data,
            "define_model": h_define_model, "fit": h_fit,
            "get_state": h_get_state, "set_parameter": h_set_parameter,
            "error": h_error, "calc_flux": h_calc_flux,
            "calc_lumin": h_calc_lumin, "steppar": h_steppar, "plot": h_plot,
            "fakeit": h_fakeit, "run_mcmc": h_run_mcmc,
            "save_session": h_save_session,
            "restore_session": h_restore_session,
            "xget": h_xget, "xset": h_xset, "xcall": h_xcall,
            "assess_fit": h_assess_fit, "plot_image": h_plot_image,
            "export_script": h_export_script, "journal": h_journal}

# ops that change session state -> recorded in the journal for export_script
_MUTATING = {"load_data", "define_model", "set_parameter", "fit", "error",
             "calc_flux", "calc_lumin", "steppar", "fakeit", "save_session",
             "restore_session", "xset", "xcall"}


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
            args = req.get("args") or {}
            result = h(args)
            if cmd in _MUTATING:
                _JOURNAL.append({"cmd": cmd, "args": args})
            send({"ok": True, "result": result})
        except Exception as e:
            send({"ok": False, "error": str(e), "category": _classify(str(e))})


if __name__ == "__main__":
    main()
