"""Prototype corpus generator.

Slice: models {powerlaw, TBabs, apec} + a Tcl<->PyXspec map for {data,model,fit}.
Emits corpus/models/<name>.{md,json}, corpus/manifest.json,
corpus/recipes/tcl_pyxspec_map.md, and llms.txt.

Run:  python generator/generate.py
"""
import json
import re
from pathlib import Path

import api
import config
import grounding
import intents
import modeldat
import texmacros

# Set to a list to restrict output (prototype slice), or None for all models.
SLICE_MODELS = None


def _fmt(x):
    if x is None:
        return ""
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)


def param_table(model) -> str:
    rows = ["| # | param | unit | default | soft min | soft max | "
            "hard min | hard max | delta | note |",
            "|---|-------|------|---------|----------|----------|"
            "----------|----------|-------|------|"]
    for i, p in enumerate(model.params, 1):
        note = []
        if p.kind == "switch":
            note.append("switch (not fitted)")
        if p.kind == "scale":
            note.append("scale (not fitted)")
        if p.kind == "norm":
            note.append("implicit norm")
        if p.frozen and p.kind == "fit":
            note.append("frozen by default")
        rows.append("| {i} | {n} | {u} | {d} | {smin} | {smax} | "
                    "{hmin} | {hmax} | {dl} | {note} |".format(
                        i=i, n=p.name, u=p.unit or "—",
                        d=_fmt(p.default), smin=_fmt(p.softmin),
                        smax=_fmt(p.softmax), hmin=_fmt(p.hardmin),
                        hmax=_fmt(p.hardmax),
                        dl=_fmt(abs(p.delta)) if p.delta is not None else "",
                        note="; ".join(note)))
    return "\n".join(rows)


TYPE_WORD = {"add": "additive", "mul": "multiplicative", "con": "convolution",
             "mix": "mixing", "acn": "pile-up/acn"}


def pyxspec_usage(model) -> str:
    if model.type == "add":
        expr = model.name
    elif model.type == "mul":
        expr = f"{model.name}*powerlaw"
    elif model.type == "con":
        expr = f"{model.name}*powerlaw"
    else:
        expr = model.name
    return ("```python\n"
            "from xspec import Model\n"
            f'm = Model("{expr}")\n'
            f"# component: m.{re.sub(r'[^A-Za-z0-9]', '', model.name.lower())}"
            "  (params as attributes)\n"
            "```")


def emit_model(name, models, label_index, outdir):
    model = models[name]
    tex = texmacros.find_tex(name, label_index)
    title, desc, family = "", "", []
    if tex:
        txt = tex.read_text(errors="replace")
        title = texmacros.subsection_title(txt)
        desc = texmacros.extract_description(txt)
        family = re.findall(r"\\xslabel\{([^}]+)\}", txt)

    # ---- JSON (ground truth) ----
    j = model.to_dict()
    j["family"] = family
    j["title"] = title
    (outdir / f"{name}.json").write_text(json.dumps(j, indent=2))

    # ---- Markdown (prose + frontmatter) ----
    fm = [
        "---",
        f"name: {name}",
        f"type: {model.type}  # {TYPE_WORD.get(model.type, model.type)}",
        f"func: {model.func}",
        f"n_params: {len(model.params)}",
        f"family: [{', '.join(family)}]",
        f"energy_range: [{model.elo}, {model.ehi}]",
        "source: manager/model.dat + " + (tex.name if tex else "(no tex)"),
        "---",
    ]
    body = [
        f"# {name}",
        "",
        f"**{TYPE_WORD.get(model.type, model.type)} model** "
        f"(`{model.type}`), function `{model.func}`.",
    ]
    if family and len(family) > 1:
        body.append(f"\nVariants documented together: "
                    f"{', '.join('`%s`' % f for f in family)}.")
    if desc:
        body += ["", "## Description", "", desc]
    body += ["", "## Parameters", "",
             "_Authoritative from `model.dat`. Negative fit-delta = frozen; "
             "additive models carry an implicit `norm`._", "",
             param_table(model)]
    body += ["", "## PyXspec", "", pyxspec_usage(model)]
    (outdir / f"{name}.md").write_text("\n".join(fm) + "\n\n" +
                                       "\n".join(body) + "\n")
    return {"name": name, "type": model.type,
            "n_params": len(model.params), "family": family}


TCL_PY_MAP = """\
# Tcl ↔ PyXspec map (prototype slice)

Bidirectional lookup between interactive XSPEC (Tcl) commands and the PyXspec
API. Agentic code should prefer PyXspec (typed returns, exceptions instead of
blocking prompts). Signatures taken from `XSUser/Python/xspec/*.py`.

| Interactive Tcl | PyXspec | Notes |
|-----------------|---------|-------|
| `data 1:1 src.pha` | `AllData("1:1 src.pha")` or `Spectrum("src.pha")` | RMF/ARF/back auto-loaded from PHA header if present |
| `response resp.rmf` | `AllData(1).response = "resp.rmf"` | only needed if not in PHA header |
| `arf arf.arf` | `AllData(1).response.arf = "arf.arf"` | |
| `backgrnd bkg.pha` | `AllData(1).background = "bkg.pha"` | |
| `ignore bad` | `AllData.ignore("bad")` | |
| `ignore **-0.5 10.0-**` | `AllData.ignore("**-0.5 10.0-**")` | energy range trim |
| `model tbabs*powerlaw` | `Model("tbabs*powerlaw")` | returns a `Model` |
| `newpar 1 0.1` | `AllModels(1)(1).values = 0.1` | one parameter |
| `freeze 1` / `thaw 1` | `AllModels(1)(1).frozen = True/False` | |
| `statistic cstat` | `Fit.statMethod = "cstat"` | choose before fitting |
| `query yes` | `Fit.query = "yes"` | **required for headless runs** |
| `fit` | `Fit.perform()` | |
| `error 1` | `Fit.error("1")` | confidence intervals |
| `tclout stat` | `Fit.statistic` | typed float, no string-scraping |
| `tclout dof` | `Fit.dof` | |
| `tclout param 1` | `AllModels(1)(1).values` | |
| `flux 0.5 10.0` | `AllModels.calcFlux("0.5 10.0")` then `AllData(1).flux` | |
| `plot data resid` | `Plot("data","resid")` then `Plot.x()/y()/model()` | extract arrays; no GUI needed |
"""


def emit_command(tex, tokens_by_name, outdir):
    """Emit one command doc from an XS<cmd>.tex file."""
    txt = tex.read_text(errors="replace")
    labs = texmacros.labels(txt)
    # primary command = first label that is a real command token, else first
    name = next((l for l in labs if l in tokens_by_name), labs[0] if labs
                else tex.stem[2:].lower())
    title = texmacros.subsection_title(txt)
    body = texmacros.extract_body(txt)
    group = tokens_by_name.get(name, [name])
    aliases = [t for t in group if t != name]
    others = [l for l in labs if l != name]
    fm = [
        "---",
        f"name: {name}",
        f"aliases: [{', '.join(aliases)}]",
        f"also_documents: [{', '.join(others)}]" if others else
        "also_documents: []",
        f"source: {tex.name}",
        "---",
    ]
    (outdir / f"{name}.md").write_text(
        "\n".join(fm) + "\n\n# " + (title or name) + "\n\n" + body + "\n")
    return {"name": name, "aliases": aliases,
            "doc": f"corpus/commands/{name}.md"}


OBJECT_MODEL = """\
---
title: PyXspec object model and indexing contract
audience: agent
priority: 0
verified_against: live introspection (tests/run_recipes.py)
---

# PyXspec object model (load this first)

The API is a small object graph reached through six singletons. Get the graph
and the indexing right and most errors disappear.

## Singletons

| Singleton | Class | Role |
|---|---|---|
| `AllData` | DataManager | loaded spectra; `AllData("1:1 f.pha")` loads (returns None) |
| `AllModels` | ModelManager | active models; `AllModels(1)` is the model for source 1 |
| `Fit` | FitManager | fitting, errors, statistic |
| `Xset` | XspecSettings | global settings (abund, xsect, chatter, seed, logs) |
| `Plot` | PlotManager | plotting + array extraction |
| `AllChains` | ChainManager | MCMC chains |

## The graph

```
AllData(i)            -> Spectrum         # i = spectrum number (1-indexed)
  Spectrum.response   -> Response         # RAISES if none attached
    Response.arf      -> Arf
  Spectrum.background -> Background        # RAISES if none attached
AllModels(i)          -> Model            # i = source number (1-indexed)
  Model.<compName>    -> Component         # e.g. m.TBabs, m.powerlaw
    Component.<parName> -> Parameter
  AllModels(i)(n)     -> Parameter        # n = parameter number across the model
Model(exprString)     -> Model            # constructing loads the model
Chain(fileName, ...)  -> Chain            # constructing RUNS the chain
```

## Indexing rules

- Everything user-facing is **1-indexed**: `AllData(1)`, `AllModels(1)(1)`.
- `AllModels(src)(parNum)` numbers parameters across the **whole** model, not
  per component. Prefer named access: `m.powerlaw.PhoIndex`.
- Component attribute names are the **model.dat canonical names** (`m.TBabs`,
  not `m.tbabs`); read them from `Model.componentNames`.

## Behavioral quirks that bite (memorize these)

- `AllData("1:1 f.pha")` **returns None** — the load is a side effect; get the
  object with `AllData(1)`.
- `Spectrum.response` and `Spectrum.background` **raise** when none is attached
  — guard with try/except.
- `Parameter.values` is a **6-list** `[val, delta, min, bottom, top, max]`; the
  fitted value is `values[0]`.
- `Parameter.error` is a **3-tuple** `(low, high, code)`; `code == "FFFFFFFFF"`
  means clean, any other flags a problem (e.g. new minimum).
- `Spectrum.flux`/`lumin` are **6-tuples** (value, errLo, errHi in cgs, then the
  same triple in photons); populated only after `AllModels.calcFlux/calcLumin`.
- `AllModels.calcFlux(...)` **stores into** `Spectrum.flux`; it does not return.
- Constructing a `Chain(...)` **runs** it immediately.
- Read-only attributes raise "Cannot rebind ..." on assignment — see each
  class's attribute table (access = get).

Full per-class attribute/method tables: `corpus/api/<Class>.md`; machine form:
`corpus/api/api.json`.
"""


INTENT_CATEGORIES = [
    ("session", "Session / setup"), ("data", "Data"), ("model", "Model"),
    ("fit", "Fit"), ("errors", "Errors / confidence"),
    ("derived", "Derived quantities"), ("plot", "Plot / output"),
    ("sim", "Simulation / Bayesian"), ("save", "Save / restore"),
]


def emit_intents(recipes_dir, corpus):
    """Emit the intent->API reverse index as markdown + JSON."""
    rows = [{"category": c, "intent": i, "pyxspec": p, "tcl": t,
             "refs": [list(r) for r in refs], "note": n}
            for (c, i, p, t, refs, n) in intents.INTENTS]
    (corpus / "intent_index.json").write_text(json.dumps(rows, indent=2))

    lines = [
        "---", "title: Intent -> API reverse index (I want to X -> call Y)",
        "audience: agent", "priority: 4", "---", "",
        "# Intent -> API index", "",
        "Find the exact call from what you want to do. PyXspec-first; Tcl shown "
        "for cross-reference. Every call is validated against `corpus/api/"
        "api.json` (see tests).", "",
    ]
    for key, title in INTENT_CATEGORIES:
        group = [r for r in rows if r["category"] == key]
        if not group:
            continue
        lines += [f"## {title}", "",
                  "| I want to... | PyXspec | Tcl | Notes |",
                  "|--------------|---------|-----|-------|"]
        for r in group:
            py = r["pyxspec"].replace("|", "\\|")
            tcl = r["tcl"].replace("|", "\\|")
            lines.append(f"| {r['intent']} | `{py}` | "
                         f"{('`'+tcl+'`') if tcl != '-' else '—'} | "
                         f"{r['note']} |")
        lines.append("")
    (recipes_dir / "07_intent_index.md").write_text("\n".join(lines))
    return rows


def emit_api(pyxspec_dir, outdir):
    data = api.extract(pyxspec_dir)
    manifest = []
    for name, e in sorted(data.items()):
        # name the doc by the user-facing singleton where one exists (an agent
        # looks for Fit.md / AllData.md, not FitManager.md)
        docname = e["singleton"] or name
        lines = ["---", f"class: {name}"]
        if e["singleton"]:
            lines.append(f"singleton: {e['singleton']}")
        lines += [f"module: {e['module']}", "---", "", f"# {docname}"]
        if e["singleton"]:
            lines.append(f"\nSingleton instance `{e['singleton']}` "
                         f"(class `{name}`).")
        if e["summary"]:
            lines += ["", e["summary"]]
        if e["attributes"]:
            lines += ["", "## Attributes", "",
                      "| attribute | type | access | description |",
                      "|-----------|------|--------|-------------|"]
            for a in e["attributes"]:
                lines.append(f"| {a['name']} | {a['type'] or '—'} | "
                             f"{a['access']} | {a['doc']} |")
        elif name == "Component":
            lines += ["", "## Attributes", "",
                      "Attributes are **dynamic**: one per parameter, named by "
                      "the parameter (e.g. `m.powerlaw.PhoIndex`), each a "
                      "`Parameter`. See `corpus/recipes/00_object_model.md`."]
        elif e["methods"] and any(m["name"] == "__init__" for m in e["methods"]):
            lines += ["", "## Attributes", "",
                      "Set via the constructor (see `__init__` below); no "
                      "get/set property attributes."]
        if e["methods"]:
            lines += ["", "## Methods", ""]
            for m in e["methods"]:
                doc = f" — {m['doc']}" if m["doc"] else ""
                lines.append(f"- `{m['name']}{m['signature']}`{doc}")
        (outdir / f"{docname}.md").write_text("\n".join(lines) + "\n")
        manifest.append({"class": name, "singleton": e["singleton"],
                         "doc": f"corpus/api/{docname}.md",
                         "n_attributes": len(e["attributes"]),
                         "n_methods": len(e["methods"])})
    (outdir / "api.json").write_text(json.dumps(data, indent=2))
    return manifest, data


def casebook_index(repo_root):
    """Light regex index of the casebook (id + label + status) for the manifest
    and llms.txt. Deliberately yaml-free so indexing works even without the
    validation deps; full schema validation is the separate gate
    (tests/validate_casebook.py). Returns (cases, lessons) lists of dicts."""
    cb = repo_root / "casebook"
    if not cb.exists():
        return [], []

    def field(fm, key, default):
        m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        return m.group(1).strip().strip('"').strip("'") if m else default

    def entries(subdir, label_key):
        out = []
        for p in sorted((cb / subdir).glob("*.md")):
            txt = p.read_text(errors="replace")
            m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
            fm = m.group(1) if m else ""
            out.append({"id": field(fm, "id", p.stem),
                        "label": field(fm, label_key, p.stem),
                        "status": field(fm, "status", ""),
                        "doc": f"casebook/{subdir}/{p.name}"})
        return out

    return entries("cases", "title"), entries("lessons", "one_line")


def main():
    stamp = config.version_stamp()
    models = modeldat.parse(config.MODEL_DAT)
    label_index = texmacros.build_label_index(config.MANUAL_DIR)

    mdir = config.CORPUS / "models"
    mdir.mkdir(parents=True, exist_ok=True)
    names = SLICE_MODELS if SLICE_MODELS else sorted(models, key=str.lower)
    manifest_models = []
    for name in names:
        if name not in models:
            print(f"  WARN: {name} not in model.dat")
            continue
        manifest_models.append(emit_model(name, models, label_index, mdir))
    print(f"  emitted {len(manifest_models)} models")

    rdir = config.CORPUS / "recipes"
    rdir.mkdir(parents=True, exist_ok=True)
    (rdir / "tcl_pyxspec_map.md").write_text(TCL_PY_MAP)
    (rdir / "00_object_model.md").write_text(OBJECT_MODEL)
    intent_rows = emit_intents(rdir, config.CORPUS)
    print(f"  emitted recipes/tcl_pyxspec_map.md + 00_object_model.md + "
          f"07_intent_index.md ({len(intent_rows)} intents)")

    # ---- PyXspec class-API reference ----
    adir = config.CORPUS / "api"
    adir.mkdir(parents=True, exist_ok=True)
    manifest_api, _ = emit_api(config.PYXSPEC_DIR, adir)
    print(f"  emitted {len(manifest_api)} API class docs")

    # ---- commands: docs + token/alias grounding ----
    tokens, groups = grounding.command_map(config.HEASOFT_SRC)
    tokens_by_name = {}
    for g in groups:
        allnames = sorted([g["canonical"]] + g["aliases"])
        for n in allnames:
            tokens_by_name[n] = allnames
    cdir = config.CORPUS / "commands"
    cdir.mkdir(parents=True, exist_ok=True)
    manifest_cmds = []
    for tex in grounding.command_doc_files(config.MANUAL_DIR):
        if not tex.exists():
            print(f"  WARN: command doc missing: {tex.name}")
            continue
        manifest_cmds.append(emit_command(tex, tokens_by_name, cdir))
    print(f"  emitted {len(manifest_cmds)} command docs")

    # ---- casebook index (Tier C judgment layer) ----
    cb_cases, cb_lessons = casebook_index(config.REPO_ROOT)

    # ---- full grounding manifest ----
    manifest = {
        "provenance": stamp,
        "counts": {
            "models": len(manifest_models),
            "pyxspec_api_classes": len(manifest_api),
            "command_tokens": len(tokens),
            "command_docs": len(manifest_cmds),
            "intents": len(intent_rows),
            "casebook_cases": len(cb_cases),
            "casebook_lessons": len(cb_lessons),
        },
        "models": manifest_models,
        "pyxspec_api": manifest_api,
        "command_tokens": tokens,
        "commands": manifest_cmds,
        "statistics": grounding.STATISTICS,
        "plot_types": grounding.plot_types(config.HEASOFT_SRC),
        "tclout_keys": grounding.tclout_keys(config.MANUAL_DIR),
        "xset_keys": grounding.xset_keys(config.MANUAL_DIR),
        "abundances": grounding.abundances(config.HEASOFT_SRC),
        "xsect": grounding.xsect(config.HEASOFT_SRC),
        "provenance_notes": {
            "models": "manager/model.dat + XSmodel*.tex",
            "pyxspec_api": "ast extraction of XSUser/Python/xspec/*.py",
            "command_tokens": "XSGlobal.cxx createCommandMap (authoritative)",
            "commands": "Commands.tex \\input list",
            "statistics": "XSstatistic.tex / XSappendixStatistics.tex",
            "plot_types": "XSPlot/Plot/PlotCommandCreator.cxx",
            "tclout_keys": "XStclout.tex (documented options)",
            "xset_keys": "documented subset; xset accepts arbitrary KEY VALUE",
            "abundances": "manager/abundances.dat",
            "xsect": "XSFunctions/NeutralOpacity.cxx",
            "casebook": "casebook/ (hand-authored + distilled; schema-gated by "
                        "tests/validate_casebook.py)",
        },
    }
    (config.CORPUS / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"  emitted manifest.json "
          f"({len(tokens)} cmd tokens, {len(manifest_models)} models)")

    # ---- llms.txt root index ----
    lines = [
        "# XSPEC / PyXspec AI docs",
        f"> XSPEC {stamp['xspec_version']} | manual@{stamp['manual_commit']} "
        f"| heasoft@{stamp['heasoft_commit']}",
        "",
        "## Models",
    ]
    for m in manifest_models:
        lines.append(f"- [{m['name']}](corpus/models/{m['name']}.md): "
                     f"{TYPE_WORD.get(m['type'], m['type'])} model, "
                     f"{m['n_params']} params")
    lines += ["", f"## PyXspec API ({len(manifest_api)} classes)"]
    for a in sorted(manifest_api, key=lambda a: a["singleton"] or a["class"]):
        label = a["singleton"] or a["class"]
        sg = f" (class `{a['class']}`)" if a["singleton"] else ""
        lines.append(f"- [{label}]({a['doc']}){sg}: "
                     f"{a['n_attributes']} attrs, {a['n_methods']} methods")
    lines += ["", f"## Commands ({len(manifest_cmds)} docs, "
              f"{len(tokens)} valid tokens incl. aliases)"]
    for c in sorted(manifest_cmds, key=lambda c: c["name"]):
        al = f" (aliases: {', '.join(c['aliases'])})" if c["aliases"] else ""
        lines.append(f"- [{c['name']}]({c['doc']}){al}")
    lines += ["", "## Recipes / guides"]
    for rec in sorted((config.CORPUS / "recipes").glob("*.md")):
        first = rec.read_text().splitlines()
        # prefer YAML frontmatter `title:`, else first heading
        title = next((l.split("title:", 1)[1].strip()
                      for l in first[:8] if l.startswith("title:")), rec.stem)
        lines.append(f"- [{title}](corpus/recipes/{rec.name})")
    lines += ["", "## Grounding", "- [manifest.json](corpus/manifest.json)"]
    if cb_cases or cb_lessons:
        lines += ["", "## Casebook (judgment layer)",
                  f"> {len(cb_cases)} case(s), {len(cb_lessons)} lesson(s) — "
                  "worked studies + reusable lessons; retrieve by data "
                  "fingerprint. See [SCHEMA.md](casebook/SCHEMA.md)."]
        for c in cb_cases:
            st = f" ({c['status']})" if c["status"] else ""
            lines.append(f"- [{c['label']}]({c['doc']}){st}")
        if cb_lessons:
            lines += ["", "### Lessons"]
            for les in cb_lessons:
                st = f" ({les['status']})" if les["status"] else ""
                lines.append(f"- [{les['label']}]({les['doc']}){st}")
    (config.REPO_ROOT / "llms.txt").write_text("\n".join(lines) + "\n")
    print("  emitted llms.txt")

    # ---- casebook gate (Tier C) --------------------------------------------
    # Validate the casebook against its schemas + refs + grounding set, so a
    # broken casebook fails the regen -- same anti-drift discipline as the rest
    # of the corpus. Runs last: the grounding check reads the manifest just
    # written above. Loaded by file path to avoid a hard tests/ import coupling.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "validate_casebook",
        str(config.REPO_ROOT / "tests" / "validate_casebook.py"))
    cbmod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cbmod)
    try:
        n_cases, n_lessons, cb_errors = cbmod.validate_casebook(config.REPO_ROOT)
    except RuntimeError as e:
        print(f"  WARN: casebook not gated ({e}); "
              "pip install -r generator/requirements.txt")
    else:
        if cb_errors:
            print(f"  FAIL: casebook invalid ({len(cb_errors)}):")
            for err in cb_errors:
                print("    -", err)
            raise SystemExit(1)
        print(f"  casebook OK: {n_cases} case(s), {n_lessons} lesson(s) gated")


if __name__ == "__main__":
    main()
