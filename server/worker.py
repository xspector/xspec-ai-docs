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
import sys

# protocol channel (inherited fd); responses go here, never to stdout
_resp = os.fdopen(int(os.environ["XSPEC_RESP_FD"]), "w")


def send(obj):
    _resp.write(json.dumps(obj) + "\n")
    _resp.flush()


from xspec import AllData, AllModels, Model, Fit, Xset  # noqa: E402

Xset.chatter = 0
Xset.logChatter = 0
Fit.query = "yes"

_ERROR_CATS = [
    ("no data loaded", "no_data"),
    ("default (unnamed) model is not defined", "no_model"),
    ("has no response", "no_response"),
    ("out of range", "param_range"),
    ("cannot be frozen", "link"),
    ("table model file not found", "table_file"),
    ("cannot find table model", "table_file"),
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
    Fit.query = "yes"
    Xset.chatter = 0
    return {"cleared": True}


def h_load_data(a):
    AllData(f"1:1 {a['pha']}")
    s = AllData(1)
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
    return {"nSpectra": AllData.nSpectra, "exposure": s.exposure,
            "response": rmf, "background": bkg}


def h_define_model(a):
    m = Model(a["expr"])
    return {"expression": a["expr"], "components": m.componentNames,
            "nParameters": m.nParameters, "params": _dump_params()}


def h_fit(a):
    if a.get("statistic"):
        Fit.statMethod = a["statistic"]
    Fit.perform()
    return {"statistic": Fit.statistic, "dof": Fit.dof,
            "statMethod": Fit.statMethod, "params": _dump_params()}


def h_get_state(a):
    st = {"nSpectra": AllData.nSpectra}
    try:
        m = AllModels(1)
        st["model"] = {"components": m.componentNames,
                       "nParameters": m.nParameters}
        st["params"] = _dump_params()
    except Exception:
        st["model"] = None
    try:
        st["statistic"] = Fit.statistic
        st["dof"] = Fit.dof
        st["statMethod"] = Fit.statMethod
    except Exception:
        pass
    return st


HANDLERS = {"reset_session": h_reset, "load_data": h_load_data,
            "define_model": h_define_model, "fit": h_fit,
            "get_state": h_get_state}


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
