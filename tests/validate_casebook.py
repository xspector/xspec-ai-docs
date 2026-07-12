#!/usr/bin/env python
"""Validate the casebook against its JSON Schemas + referential integrity +
the grounding set. This is the build-time gate SCHEMA.md refers to: a bad enum
value, an unknown model/abundance/xsect name, a dangling lesson/case reference,
or a missing validation path fails the run.

No HEADAS needed (static corpus only). Needs pyyaml + jsonschema.

    python tests/validate_casebook.py
"""
import json
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CB = os.path.join(ROOT, "casebook")

try:
    import yaml
except ImportError:
    print("SKIP: pyyaml not installed")
    sys.exit(0)
try:
    import jsonschema
except ImportError:
    print("SKIP: jsonschema not installed")
    sys.exit(0)

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(path):
    txt = open(path).read()
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    if not m:
        raise ValueError(f"{path}: no YAML frontmatter")
    return yaml.safe_load(m.group(1))


def load_schema(name):
    return json.load(open(os.path.join(CB, "schema", name)))


def grounding():
    """model / abundance / xsect names from the corpus manifest, if present."""
    mpath = os.path.join(ROOT, "corpus", "manifest.json")
    if not os.path.exists(mpath):
        return None
    man = json.load(open(mpath))

    def lower_names(v):
        out = set()
        for x in (v.values() if isinstance(v, dict) else v):
            out.add((x.get("name") if isinstance(x, dict) else str(x)).lower())
        return out

    return {
        "models": lower_names(man.get("models", [])),
        "abund": lower_names(man.get("abundances", [])),
        "xsect": lower_names(man.get("xsect", [])),
    }


def main():
    case_schema = load_schema("case.schema.json")
    lesson_schema = load_schema("lesson.schema.json")
    ground = grounding()
    errors = []
    cases, lessons = {}, {}

    for p in sorted(glob.glob(os.path.join(CB, "cases", "*.md"))):
        stem = os.path.splitext(os.path.basename(p))[0]
        fm = frontmatter(p)
        cases[stem] = fm
        if fm.get("id") != stem:
            errors.append(f"case {stem}: id {fm.get('id')!r} != filename")
        for e in jsonschema.Draft7Validator(case_schema).iter_errors(fm):
            errors.append(f"case {stem}: {e.message} at {list(e.path)}")

    for p in sorted(glob.glob(os.path.join(CB, "lessons", "*.md"))):
        stem = os.path.splitext(os.path.basename(p))[0]
        fm = frontmatter(p)
        lessons[stem] = fm
        if fm.get("id") != stem:
            errors.append(f"lesson {stem}: id {fm.get('id')!r} != filename")
        for e in jsonschema.Draft7Validator(lesson_schema).iter_errors(fm):
            errors.append(f"lesson {stem}: {e.message} at {list(e.path)}")

    # referential integrity
    for cid, fm in cases.items():
        for lid in fm.get("lessons", []):
            if lid not in lessons:
                errors.append(f"case {cid}: dangling lesson ref {lid!r}")
    for lid, fm in lessons.items():
        for cid in fm.get("evidence_cases", []):
            if cid not in cases:
                errors.append(f"lesson {lid}: dangling evidence_case {cid!r}")
        v = fm.get("validation")
        if v and not os.path.exists(os.path.join(ROOT, v)):
            errors.append(f"lesson {lid}: validation path missing: {v}")

    # grounding: names must exist in the corpus
    if ground:
        for cid, fm in cases.items():
            ctx = fm.get("context", {})
            for mf in ctx.get("model_family", []):
                if ground["models"] and mf.lower() not in ground["models"]:
                    errors.append(f"case {cid}: model_family {mf!r} not in grounding set")
            for key in ("abund", "xsect"):
                val = ctx.get(key)
                if val and ground[key] and val.lower() not in ground[key]:
                    errors.append(f"case {cid}: {key} {val!r} not in grounding set")
    else:
        print("note: corpus/manifest.json absent -- skipped grounding checks")

    if errors:
        print(f"FAIL ({len(errors)}):")
        for e in errors:
            print("  -", e)
        return 1
    print(f"OK: {len(cases)} case(s), {len(lessons)} lesson(s) "
          "valid; refs + grounding consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
