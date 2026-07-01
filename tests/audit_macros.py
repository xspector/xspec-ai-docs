"""Macro-dictionary gap auditor.

Scans corpus/models/*.md for signs the LaTeX->markdown pass fell short:
  * residual LaTeX control sequences (\\foo) outside math/code
  * broken/empty math ($$$$, ^{-}, $$ $$)
  * leftover table/env plumbing (\\begin, \\end, & , \\rowsp, dangling \\\\)
  * failed tex join (no description AND empty family)

Prints a frequency-ranked report of residual macros (the actionable output:
which macros to add to the dictionary next) plus per-file flags.
Run:  python tests/audit_macros.py
"""
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCAN_DIRS = [REPO / "corpus" / "models", REPO / "corpus" / "commands"]

# spans to exclude before hunting for residual control sequences.
# display math ($$...$$) may contain single-$ inline math (e.g. \mbox{if $E$}),
# so match content that is any non-$ char or a lone $ not starting a $$.
MATH = re.compile(r"\$\$(?:[^$]|\$(?!\$))*\$\$|\$[^$]*\$", re.S)
CODE = re.compile(r"```.*?```", re.S)
CTRL = re.compile(r"\\[a-zA-Z]+")

residual = Counter()
broken_math = []
env_plumbing = []
no_join = []


def strip_protected(text):
    text = CODE.sub(" ", text)
    text = MATH.sub(" ", text)
    return text


def body_of(md):
    # everything after the closing frontmatter '---'
    parts = md.split("---", 2)
    return parts[2] if len(parts) >= 3 else md


total = 0
for d in SCAN_DIRS:
    is_models = d.name == "models"
    for f in sorted(d.glob("*.md")):
        total += 1
        md = f.read_text()
        body = body_of(md)
        scan = strip_protected(body)

        for m in CTRL.findall(scan):
            residual[m] += 1

        # empty math or a stripped exponent (e.g. E^{-} from an eaten \alpha)
        if "$$$$" in body or re.search(r"\^\{-?\}|_\{\}", body):
            broken_math.append(f.name)

        # genuine LaTeX residue only (prose '&' from \& is legitimate)
        if re.search(r"\\begin\{|\\end\{|\\rowsp|\\\\", scan):
            env_plumbing.append(f.name)

        # join check only applies to model docs (they carry family/description)
        if is_models:
            fam = re.search(r"family: \[([^\]]*)\]", md)
            has_desc = "## Description" in md
            if (not fam or not fam.group(1).strip()) and not has_desc:
                no_join.append(f.name)


def section(title, items, limit=40):
    print(f"\n== {title}: {len(items)} ==")
    for x in items[:limit]:
        print("   ", x)
    if len(items) > limit:
        print(f"    ... (+{len(items) - limit} more)")


print(f"audited {total} docs (models + commands)")

print("\n== residual LaTeX control sequences (freq-ranked) ==")
if not residual:
    print("    none")
for mac, n in residual.most_common(40):
    print(f"    {n:4d}  {mac}")

section("broken/empty math", broken_math)
section("leftover env/table plumbing", env_plumbing)
section("failed tex join (no family & no description)", no_join)
