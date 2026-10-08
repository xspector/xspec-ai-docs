"""Authoritative grounding-set extractors.

Each function returns data pulled from a definitive source (XSPEC source or
data files), with the source recorded so the manifest can cite provenance.
Anything an AI could hallucinate (command, model, xset/tclout key, statistic,
plot type, abundance/xsect table) should be checkable here.
"""
import re
from pathlib import Path


def command_map(heasoft_src: Path):
    """Parse the CLI command table (XSCli/CliCommands.cxx, since the Tcl-free
    CLI; XSUser/Global/XSGlobal.cxx's createCommandMap before). Returns
    (tokens, groups):
      tokens  -- every valid command token (incl. x-prefixed aliases)
      groups  -- [{canonical, aliases}] grouped by handler
    TABLE rows {"name", &XSGlobal::doX, autosave, result} register an
    "x"+name twin for every name but "?"; the specials {"name", cmdX, xtwin}
    register one only when xtwin is true.
    """
    txt = (heasoft_src / "XSCli" / "CliCommands.cxx").read_text(
        errors="replace")
    pairs = []
    for name, handler in re.findall(
            r'\{\s*"([^"]+)"\s*,\s*&XSGlobal::(\w+)\s*,\s*(?:true|false)\s*,'
            r'\s*(?:true|false)\s*\}', txt):
        pairs.append((name, handler))
        if name != "?":
            pairs.append(("x" + name, handler))
    for name, handler, xtwin in re.findall(
            r'\{\s*"([^"]+)"\s*,\s*(cmd\w+)\s*,\s*(true|false)\s*\}', txt):
        pairs.append((name, handler))
        if xtwin == "true":
            pairs.append(("x" + name, handler))
    # real user commands are lowercase (or "?"); drop internal sentinels.
    pairs = [(n, h) for n, h in pairs if n == "?" or n[0].islower()]
    tokens = sorted({name for name, _ in pairs})
    by_handler = {}
    for name, handler in pairs:
        by_handler.setdefault(handler, []).append(name)
    groups = []
    for handler, names in by_handler.items():
        # canonical = shortest name not starting with 'x' (fallback: shortest)
        non_x = [n for n in names if not n.startswith("x")]
        canonical = min(non_x or names, key=len)
        aliases = sorted(n for n in names if n != canonical)
        groups.append({"canonical": canonical, "aliases": aliases,
                       "handler": handler})
    groups.sort(key=lambda g: g["canonical"])
    return tokens, groups


def command_doc_files(manual_dir: Path):
    """The XS<cmd>.tex files \\input by Commands.tex, in order."""
    txt = (manual_dir / "Commands.tex").read_text(errors="replace")
    return [manual_dir / (m + ".tex")
            for m in re.findall(r"\\input\{([^}]+)\}", txt)]


def abundances(heasoft_src: Path):
    """Table names from manager/abundances.dat (first token of each data row)."""
    txt = (heasoft_src / "manager" / "abundances.dat").read_text(errors="replace")
    names = []
    for line in txt.splitlines():
        if line.startswith("#") or line.startswith("References"):
            break  # stop at the references section (rows there repeat names)
        m = re.match(r"([a-z][a-z0-9]{2,4}):", line)
        if m and m.group(1) != "elts" and m.group(1) not in names:
            names.append(m.group(1))
    # plus the special user options the abund command accepts
    return names + ["file", "read"]


def xsect(heasoft_src: Path):
    """Photoionization cross-section tables (NeutralOpacity.cxx)."""
    p = heasoft_src / "XSFunctions" / "NeutralOpacity.cxx"
    txt = p.read_text(errors="replace")
    found = re.findall(r'"(vern|bcmc|obcm)"', txt)
    return sorted(set(found))


def plot_types(heasoft_src: Path):
    """Registered plot commands (PlotCommandCreator.cxx)."""
    p = heasoft_src / "XSPlot" / "Plot" / "PlotCommandCreator.cxx"
    txt = p.read_text(errors="replace")
    toks = re.findall(r'"([a-z][a-z0-9]{2,})"', txt)
    # keep plausible plot-type tokens; drop obvious non-types
    drop = {"the", "and", "for", "not", "use", "off"}
    return sorted({t for t in toks if t not in drop})


# Statistics: documented set (XSstatistic.tex / XSappendixStatistics.tex),
# cross-checked against StatManager.cxx.
STATISTICS = {
    "fit": ["chi", "cstat", "lstat", "pgstat", "pstat", "whittle",
            "chicov", "chistokes"],
    "test": ["chi", "pchi", "cstat", "runs"],
}


def tclout_keys(manual_dir: Path):
    """Documented tclout options: the leading token of each \\argval{...} row
    in XStclout.tex."""
    txt = (manual_dir / "XStclout.tex").read_text(errors="replace")
    toks = re.findall(r"\\argval\{([?a-zA-Z][a-zA-Z0-9_]*)", txt)
    return sorted(set(toks))


def xset_keys(manual_dir: Path):
    """Best-effort documented xset keywords (ALLCAPS tokens in XSxset.tex and
    model docs). NOTE: xset accepts arbitrary KEY VALUE pairs, so this is a
    documented subset, not an exhaustive validity list."""
    keys = set()
    files = [manual_dir / "XSxset.tex"] + list(manual_dir.glob("XSmodel*.tex"))
    for f in files:
        try:
            txt = f.read_text(errors="replace")
        except Exception:
            continue
        keys.update(re.findall(r"\b([A-Z][A-Z0-9_]{3,})\b", txt))
    # drop obvious non-keywords (LaTeX/ADS/journal noise)
    noise = {"HEADAS", "FITS", "ATOMDB", "AGN", "ISM", "XSPEC", "ACIS",
             "NASA", "HEASARC", "ASCII", "NULL", "TRUE", "FALSE"}
    return sorted(k for k in keys if k not in noise)
