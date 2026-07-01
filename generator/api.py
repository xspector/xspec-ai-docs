"""PyXspec class-API extractor.

Parses XSUser/Python/xspec/*.py with `ast` and emits, per public class:
  * attributes (name, type-from-docstring, read-only?, one-line doc)
  * methods   (name, full signature, one-line doc)
The reference an agent consumes when driving PyXspec: "what can I call on this
object, and what comes back."

Read-only is detected structurally: a property whose setter body is just a
`raise` (the "Cannot rebind ..." pattern) is get-only.
"""
import ast
import re

# manager class -> the singleton instance name users actually call
SINGLETON = {
    "DataManager": "AllData", "ModelManager": "AllModels",
    "FitManager": "Fit", "XspecSettings": "Xset",
    "PlotManager": "Plot", "ChainManager": "AllChains",
}
SKIP = {"_AttrRestrictor", "_ParallelHandler", "_DetArrayEmulator",
        "_ModParam", "_RespParam", "BaseResult"}
KEEP_DUNDER = {"__init__", "__call__"}

_TYPE_RE = re.compile(
    r"\[(int(?:eger)?|str(?:ing)?|float|bool(?:ean)?|list|tuple)\]", re.I)
_NORM = {"integer": "int", "string": "str", "boolean": "bool"}


def _first_line(doc):
    if not doc:
        return ""
    for ln in doc.splitlines():
        ln = ln.strip()
        if ln:
            return ln
    return ""


def _type_from_doc(doc):
    """Best-effort type from the docstring's FIRST line only. Using the whole
    docstring mis-fires (e.g. a setter's '[string]' overriding a getter that
    returns an object, or a later 'tuple' overriding a 'list' first line)."""
    fl = _first_line(doc)
    if not fl:
        return ""
    m = _TYPE_RE.search(fl)
    if m:
        t = m.group(1).lower()
        return _NORM.get(t, t)
    low = fl.lower()
    if low.startswith(("a tuple", "tuple")) or "tuple of" in low:
        return "tuple"
    if low.startswith(("a list", "list")) or "list of" in low:
        return "list"
    if low.startswith("bool") or "boolean" in low:
        return "bool"
    return ""


def _is_raiser(func):
    """True if a FunctionDef body is only a raise (read-only setter pattern)."""
    body = [n for n in func.body if not isinstance(n, ast.Expr)  # skip docstring
            or not isinstance(getattr(n, "value", None), ast.Constant)]
    return len(body) == 1 and isinstance(body[0], ast.Raise)


def _signature(func):
    a = func.args
    parts = []
    posonly = getattr(a, "posonlyargs", [])
    allpos = list(posonly) + list(a.args)
    defaults = list(a.defaults)
    ndef = len(defaults)
    nnodef = len(allpos) - ndef
    for i, arg in enumerate(allpos):
        if arg.arg == "self":
            continue
        if i >= nnodef:
            d = defaults[i - nnodef]
            try:
                parts.append(f"{arg.arg}={ast.unparse(d)}")
            except Exception:
                parts.append(f"{arg.arg}=...")
        else:
            parts.append(arg.arg)
    if a.vararg:
        parts.append("*" + a.vararg.arg)
    for i, arg in enumerate(a.kwonlyargs):
        d = a.kw_defaults[i]
        if d is not None:
            try:
                parts.append(f"{arg.arg}={ast.unparse(d)}")
            except Exception:
                parts.append(f"{arg.arg}=...")
        else:
            parts.append(arg.arg)
    if a.kwarg:
        parts.append("**" + a.kwarg.arg)
    return "(" + ", ".join(parts) + ")"


def _init_attrs(funcs):
    """Public instance attributes assigned as self.X = ... in __init__ (these
    are real attributes but not declared via property(), e.g.
    Model.componentNames)."""
    init = funcs.get("__init__")
    names = []
    if not init:
        return names
    for node in ast.walk(init):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if (isinstance(tgt, ast.Attribute)
                        and isinstance(tgt.value, ast.Name)
                        and tgt.value.id == "self"
                        and not tgt.attr.startswith("_")):
                    if tgt.attr not in names:
                        names.append(tgt.attr)
    return names


def _class_entry(cls):
    funcs = {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}
    attributes, methods = [], []
    for node in cls.body:
        # properties: NAME = property(fget, fset, ...)
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "property"
                and node.targets and isinstance(node.targets[0], ast.Name)):
            call = node.value
            name = node.targets[0].id
            fset = call.args[1] if len(call.args) > 1 else None
            read_only = True
            if fset is not None and not (isinstance(fset, ast.Constant)
                                         and fset.value is None):
                if isinstance(fset, ast.Name) and fset.id in funcs:
                    read_only = _is_raiser(funcs[fset.id])
                else:
                    read_only = False
            # doc: keyword 'doc' or 4th positional
            doc = None
            for kw in call.keywords:
                if kw.arg == "doc" and isinstance(kw.value, ast.Constant):
                    doc = kw.value.value
            if doc is None and len(call.args) >= 4 and isinstance(
                    call.args[3], ast.Constant):
                doc = call.args[3].value
            attributes.append({
                "name": name,
                "type": _type_from_doc(doc),
                "access": "get" if read_only else "get/set",
                "doc": _first_line(doc),
            })
        # methods
        elif isinstance(node, ast.FunctionDef):
            if node.name.startswith("_") and node.name not in KEEP_DUNDER:
                continue
            methods.append({
                "name": node.name,
                "signature": _signature(node),
                "doc": _first_line(ast.get_docstring(node)),
            })
    # instance attributes from __init__ not already declared as properties
    prop_names = {a["name"] for a in attributes}
    for nm in _init_attrs(funcs):
        if nm not in prop_names:
            attributes.append({"name": nm, "type": "", "access": "instance",
                               "doc": ""})
    return attributes, methods


def extract(pyxspec_dir):
    """Return {class_name: entry} for every public class in the package."""
    out = {}
    for py in sorted(pyxspec_dir.glob("*.py")):
        try:
            tree = ast.parse(py.read_text(errors="replace"))
        except SyntaxError:
            continue
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if node.name in SKIP or node.name.startswith("_"):
                continue
            attrs, meths = _class_entry(node)
            out[node.name] = {
                "class": node.name,
                "module": py.name,
                "singleton": SINGLETON.get(node.name),
                "summary": _first_line(ast.get_docstring(node)),
                "attributes": attrs,
                "methods": meths,
            }
    return out
