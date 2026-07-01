"""Read-only data-access layer over the generated corpus.

Pure functions with no MCP dependency so they can be unit-tested directly.
`server.py` wraps these as MCP tools. Everything here is lookups over the JSON
and markdown the generator already produced.
"""
import difflib
import json
import re
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent / "corpus"

# kind -> function returning the authoritative list of valid names
_VALIDATE_KINDS = {
    "model": lambda m: [x["name"] for x in m["models"]],
    "command": lambda m: m["command_tokens"],
    "statistic": lambda m: m["statistics"]["fit"] + m["statistics"]["test"],
    "plot_type": lambda m: m["plot_types"],
    "tclout_key": lambda m: m["tclout_keys"],
    "xset_key": lambda m: m["xset_keys"],
    "abundance": lambda m: m["abundances"],
    "xsect": lambda m: m["xsect"],
}


class Corpus:
    def __init__(self, root=DEFAULT_ROOT):
        self.root = Path(root)
        self.manifest = self._json("manifest.json")
        self.api = self._json("api/api.json")
        self.intents = self._json("intent_index.json")
        # case-insensitive filename indexes
        self._models = {p.stem.lower(): p
                        for p in (self.root / "models").glob("*.json")}
        self._commands = {p.stem.lower(): p
                          for p in (self.root / "commands").glob("*.md")}
        self._recipes = {p.stem.lower(): p
                         for p in (self.root / "recipes").glob("*.md")}
        # api: allow lookup by class OR singleton name
        self._api_alias = {}
        for cls, e in self.api.items():
            self._api_alias[cls.lower()] = cls
            if e.get("singleton"):
                self._api_alias[e["singleton"].lower()] = cls

    def _json(self, rel):
        return json.loads((self.root / rel).read_text())

    # ---- models ----
    def get_model(self, name):
        key = name.lower()
        if key not in self._models:
            return {"found": False, "query": name,
                    "suggestions": self._close(key, self._models)}
        data = json.loads(self._models[key].read_text())
        md = self._models[key].with_suffix(".md")
        data["found"] = True
        data["doc_markdown"] = md.read_text() if md.exists() else ""
        return data

    def list_models(self, type=None):
        ms = self.manifest["models"]
        if type:
            ms = [m for m in ms if m["type"] == type]
        return {"count": len(ms), "type": type or "all",
                "models": [{"name": m["name"], "type": m["type"],
                            "n_params": m["n_params"]} for m in ms]}

    # ---- commands ----
    def get_command(self, name):
        key = name.lower()
        if key not in self._commands:
            return {"found": False, "query": name,
                    "suggestions": self._close(key, self._commands)}
        text = self._commands[key].read_text()
        fm = _frontmatter(text)
        return {"found": True, "name": fm.get("name", key),
                "aliases": _listval(fm.get("aliases", "")),
                "doc_markdown": text}

    # ---- api ----
    def get_api(self, class_name):
        key = class_name.lower()
        if key not in self._api_alias:
            return {"found": False, "query": class_name,
                    "suggestions": self._close(key, self._api_alias)}
        entry = dict(self.api[self._api_alias[key]])
        entry["found"] = True
        return entry

    # ---- intents ----
    def lookup_intent(self, query, limit=10):
        q = query.lower()
        terms = [t for t in re.split(r"\W+", q) if t]
        scored = []
        for r in self.intents:
            hay = " ".join([r["intent"], r["note"], r["pyxspec"],
                            r["category"]]).lower()
            score = sum(t in hay for t in terms) + (2 if q in hay else 0)
            if score:
                scored.append((score, r))
        scored.sort(key=lambda s: -s[0])
        return {"query": query, "count": len(scored[:limit]),
                "results": [r for _, r in scored[:limit]]}

    # ---- validate (anti-hallucination) ----
    def validate(self, name, kind):
        if kind not in _VALIDATE_KINDS:
            return {"error": f"unknown kind '{kind}'",
                    "valid_kinds": sorted(_VALIDATE_KINDS)}
        names = _VALIDATE_KINDS[kind](self.manifest)
        lower = {n.lower(): n for n in names}
        key = name.lower()
        if key in lower:
            return {"name": name, "kind": kind, "valid": True,
                    "canonical": lower[key]}
        return {"name": name, "kind": kind, "valid": False,
                "suggestions": difflib.get_close_matches(key, list(lower), 5,
                                                         0.6),
                "note": "xset_key is a documented subset; xset accepts "
                        "arbitrary keys" if kind == "xset_key" else ""}

    # ---- guides ----
    def get_guide(self, name=None):
        if not name:
            return {"guides": sorted(self._recipes)}
        key = name.lower()
        # tolerate "01" / "01_headless_and_output" / full stem
        match = next((k for k in self._recipes
                      if k == key or k.startswith(key) or key in k), None)
        if not match:
            return {"found": False, "query": name,
                    "available": sorted(self._recipes)}
        return {"found": True, "name": match,
                "doc_markdown": self._recipes[match].read_text()}

    # ---- provenance ----
    def info(self):
        return {"provenance": self.manifest["provenance"],
                "counts": self.manifest["counts"]}

    @staticmethod
    def _close(key, index, n=5):
        return difflib.get_close_matches(key, list(index), n, 0.5)


def _frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def _listval(s):
    return [x.strip() for x in s.strip("[]").split(",") if x.strip()]
