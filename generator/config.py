"""Pinned source-tree paths and version stamping for the corpus generator.

The generator reads from two external trees:
  * heasoft  -- authoritative structured data (model.dat, PyXspec .py)
  * manual   -- human prose (.tex)
Paths are pinned here; override via environment variables for CI / other hosts.
"""
import os
import re
import subprocess
from pathlib import Path

HEASOFT_SRC = Path(os.environ.get(
    "XSPEC_HEASOFT_SRC", "/Users/kaa/software/heasoft/Xspec/src"))
MANUAL_DIR = Path(os.environ.get(
    "XSPEC_MANUAL_DIR", "/Users/kaa/software/Xspec-aux/doc/manual"))

MODEL_DAT = HEASOFT_SRC / "manager" / "model.dat"
PYXSPEC_DIR = HEASOFT_SRC / "PyXspec" / "xspec"   # XSUser/Python until 2026-09-06
DEFINITIONS_TEX = MANUAL_DIR / "XspecManualDefinitions.tex"

# Output
REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "corpus"


def _git_commit(tree: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(tree), "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return "unknown"


def xspec_version() -> str:
    try:
        txt = DEFINITIONS_TEX.read_text()
        m = re.search(r"\\newcommand\*?\\?\{?\\xspecversion\}?\{?([^}\s]+)\}?",
                      txt)
        if m:
            return m.group(1)
    except Exception:
        pass
    return "unknown"


def version_stamp() -> dict:
    """Provenance block embedded in manifest.json and llms.txt."""
    return {
        "xspec_version": xspec_version(),
        "heasoft_src": str(HEASOFT_SRC),
        "heasoft_commit": _git_commit(HEASOFT_SRC),
        "manual_dir": str(MANUAL_DIR),
        "manual_commit": _git_commit(MANUAL_DIR),
    }
