#!/usr/bin/env python
"""Single entry point for the repo's checks.

    python tests/run_all.py          # fast: corpus-only, no HEADAS
    python tests/run_all.py --live   # also the HEADAS-dependent Tier B suite

The FAST set is corpus-only and safe to run anywhere (it is what CI runs):
macro audit, Tier A data layer, casebook validation, corpus integrity +
recipes (tier1), and the generator drift check (which self-skips if the
heasoft/manual source trees are absent). --live adds the live PyXspec suite
(test_xspec_run.py), which the runner bootstraps against a HEADAS install and
which skips cleanly if HEADAS is not present.

Ground-truth calibration (bench/benchmark.py) is a separate tool with its own
verdict semantics -- run it directly, it is not part of this gate.

Runs every selected suite (does not stop at the first failure) and exits
non-zero if any failed.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

# (label, args-after-interpreter). Paths are repo-relative.
FAST = [
    ("macro audit", ["tests/audit_macros.py"]),
    ("Tier A data layer", ["tests/test_server.py"]),
    ("casebook validation", ["tests/validate_casebook.py"]),
    ("corpus integrity + recipes", ["tests/run_recipes.py"]),
    ("corpus drift (--check)", ["generator/generate.py", "--check"]),
]
LIVE = [
    ("Tier B live (xspec-run)", ["tests/test_xspec_run.py"]),
]


def run(label, args):
    print(f"\n{'=' * 60}\n=== {label}\n{'=' * 60}")
    r = subprocess.run([PY, str(ROOT / args[0]), *args[1:]], cwd=ROOT)
    return r.returncode == 0


def main():
    live = "--live" in sys.argv
    suites = FAST + (LIVE if live else [])
    results = [(label, run(label, args)) for label, args in suites]

    print(f"\n{'=' * 60}\nSUMMARY\n{'=' * 60}")
    for label, passed in results:
        print(f"  {'PASS' if passed else 'FAIL'}  {label}")
    if not live:
        print("  ....  Tier B live suite skipped (run with --live)")
    ok = all(passed for _, passed in results)
    print(f"\n{'ALL PASSED' if ok else 'FAILURES ABOVE'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
