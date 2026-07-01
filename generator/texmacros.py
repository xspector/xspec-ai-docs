"""LaTeX -> markdown for the XSPEC manual's custom macro set.

This is NOT a general LaTeX converter. The manual uses a small, stable set of
custom macros (defined in XspecManualDefinitions.tex); we translate exactly
those, expand a few text macros, and fall back to "drop the control sequence,
keep its argument" for anything unrecognized.
"""
import re
from pathlib import Path

# ---- model-name -> tex-file index (join key is \xslabel) -------------------

# model.dat uses fuller names than some \xslabel stems; explicit aliases where
# normalization alone can't bridge the gap (stem renames).
ALIASES = {
    "gaussian": "gauss", "vgaussian": "vgauss",
    "zvgaussian": "zvgauss", "rsgaussian": "rsgauss",
}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def build_label_index(manual_dir: Path) -> dict:
    """Map every \\xslabel{name} in XSmodel*.tex to its file path, keyed both
    lowercased and normalized (case- and punctuation-insensitive) so
    e.g. model.dat `SSS_ice` joins `\\xslabel{SSSice}`."""
    index = {}
    for tex in manual_dir.glob("XSmodel*.tex"):
        try:
            txt = tex.read_text(errors="replace")
        except Exception:
            continue
        for m in re.finditer(r"\\xslabel\{([^}]+)\}", txt):
            label = m.group(1)
            index.setdefault(label.lower(), tex)
            index.setdefault(_norm(label), tex)
    return index


def find_tex(name: str, index: dict):
    """Resolve a model.dat name to its tex file via lower / normalized / alias."""
    return (index.get(name.lower())
            or index.get(_norm(name))
            or index.get(ALIASES.get(name.lower(), "\0")))


def subsection_title(txt: str) -> str:
    m = re.search(r"\\subsection\{([^}]*)\}", txt)
    return _inline(m.group(1)) if m else ""


# ---- description extraction ------------------------------------------------

_STOP = re.compile(r"\\begin\{(xspartable|tabular)\}")


def _strip_heading(txt: str) -> str:
    txt = re.sub(r"\\subsection\{[^}]*\}", "", txt, count=1)
    txt = re.sub(r"(\\xslabel\{[^}]*\}\s*)+", "", txt)
    return txt


def extract_description(txt: str) -> str:
    """Prose from after the \\subsection line up to the first parameter/option
    table. Keeps displaymath (some models define themselves by a formula)."""
    txt = _strip_heading(txt)
    m = _STOP.search(txt)
    if m:
        txt = txt[:m.start()]
    return _block(txt).strip()


def extract_body(txt: str) -> str:
    """Full body after the heading (for command docs: syntax + examples)."""
    return _block(_strip_heading(txt)).strip()


def labels(txt: str) -> list:
    return re.findall(r"\\xslabel\{([^}]+)\}", txt)


# ---- macro translation -----------------------------------------------------

def _inline(s: str) -> str:
    # Shield math spans ($...$, $$...$$) so macro stripping never touches them
    # (LaTeX math like E^{-\alpha} must survive verbatim for the AI).
    math = []

    def _stash(m):
        math.append(m.group(0))
        return "\x00%d\x00" % (len(math) - 1)

    # Protect escaped dollars (\$, literal '$' as in \$xspec_tclout) so they are
    # NOT seen as math delimiters — otherwise text between two \$ is swallowed
    # as "math" and skips all macro conversion.
    s = s.replace(r"\$", "\x01")
    s = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", _stash, s, flags=re.S)
    s = _inline_nomath(s)
    for i, mtxt in enumerate(math):
        s = s.replace("\x00%d\x00" % i, mtxt)
    s = s.replace("\x01", "$")           # restore literal dollars
    return s


def _grab(s: str, i: int):
    """s[i] == '{'; return (inner_text, index_just_after_closing_brace),
    respecting nested braces."""
    depth = 0
    start = i
    while i < len(s):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    return s[start + 1:], len(s)  # unbalanced; take the rest


def _sub_macro(s: str, name: str, nargs: int, fmt):
    """Replace every \\name followed by `nargs` balanced-brace groups using
    fmt(*args). Robust to nested braces (unlike a flat [^}]* regex)."""
    pat = "\\" + name
    out = []
    i = 0
    while True:
        j = s.find(pat, i)
        if j < 0:
            out.append(s[i:])
            break
        k = j + len(pat)
        # don't match a longer control word (\emphasis when looking for \emph)
        if k < len(s) and s[k].isalpha():
            out.append(s[i:k])
            i = k
            continue
        out.append(s[i:j])
        args = []
        p = k
        ok = True
        for _ in range(nargs):
            while p < len(s) and s[p] in " \t\n":
                p += 1
            if p < len(s) and s[p] == "{":
                a, p = _grab(s, p)
                args.append(a)
            else:
                ok = False
                break
        if ok:
            out.append(fmt(*args))
            i = p
        else:
            out.append(pat)
            i = k
    return "".join(out)


def _inline_nomath(s: str) -> str:
    # line breaks and list environments (math already shielded by caller)
    s = re.sub(r"\\begin\{(itemize|enumerate|description)\}", "", s)
    s = re.sub(r"\\end\{(itemize|enumerate|description)\}", "", s)
    s = re.sub(r"\\item\s*", "\n- ", s)
    s = re.sub(r"\\\\", "\n", s)
    # links: resolve \adslink (may be nested inside a link's 2nd arg) first
    s = _sub_macro(s, "adslink", 1,
                   lambda a: "https://ui.adsabs.harvard.edu/abs/%s/abstract" % a)
    s = _sub_macro(s, "pubreflink", 2, lambda a, b: "[%s](%s)" % (a, b))
    s = _sub_macro(s, "htmladdnormallink", 2, lambda a, b: "[%s](%s)" % (a, b))
    s = _sub_macro(s, "href", 2, lambda a, b: "[%s](%s)" % (b, a))
    s = _sub_macro(s, "xscmdii", 2, lambda a, b: "`%s %s`" % (a, b))
    s = _sub_macro(s, "syn", 2, lambda a, b: "\n**Syntax:** `%s` %s\n" % (a, b))
    # code-like single-arg macros -> `arg`
    for mac in ("modname", "xscmd", "argval", "filename", "texttt"):
        s = _sub_macro(s, mac, 1, lambda a: "`%s`" % a)
    # placeholder args: \argdes / \brc render as <name>
    s = _sub_macro(s, "argdes", 1, lambda a: "`<%s>`" % a)
    s = _sub_macro(s, "brc", 1, lambda a: "<%s>" % a)
    s = _sub_macro(s, "emph", 1, lambda a: "*%s*" % a)
    s = _sub_macro(s, "textbf", 1, lambda a: "**%s**" % a)
    for mac in ("mbox", "text", "textrm", "textit"):
        s = _sub_macro(s, mac, 1, lambda a: a)
    s = _sub_macro(s, "url", 1, lambda a: a)
    # text macros
    repl = {
        r"\cgsflux": "ergs/cm^2/s",
        r"\NH": "N_H",
        r"\chisquared": "chi^2", r"\chsq": "chi^2",
        r"\deltachisquared": "Delta chi^2",
        r"\rowsp": "\n",
        r"\textbar": "|", r"\textless": "<", r"\textgreater": ">",
    }
    for k, v in repl.items():
        s = s.replace(k, v)
    s = re.sub(r"\\plasmanorm",
               "1e-14 / (4 pi [D_A (1+z)]^2) * integral(n_e n_H dV)", s)
    # escaped punctuation
    for a, b in ((r"\_", "_"), (r"\&", "&"), (r"\%", "%"), (r"\$", "$"),
                 (r"\#", "#"), (r"\{", "{"), (r"\}", "}")):
        s = s.replace(a, b)
    s = s.replace("~", " ")
    # literal caret/tilde escapes and forced spaces
    s = s.replace(r"\^{}", "^").replace(r"\~{}", "~")
    s = re.sub(r"\\ ", " ", s)
    # drop any remaining environment markers (center, flushleft, longtable,
    # description, ...) — including an optional {colspec} argument — keep content
    s = re.sub(r"\\(begin|end)\{[^}]*\}(\{[^}]*\})?", "", s)
    # generic fallback: \foo{bar} -> bar ; bare \foo -> ""
    s = re.sub(r"\\[a-zA-Z]+\*?\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)
    return s


def _block(txt: str) -> str:
    # verbatim -> fenced code
    txt = re.sub(r"\\begin\{[Vv]erbatim\}(.*?)\\end\{[Vv]erbatim\}",
                 lambda m: "\n```\n" + m.group(1).strip("\n") + "\n```\n",
                 txt, flags=re.S)
    # displaymath / equation -> $$ ... $$
    txt = re.sub(r"\\begin\{displaymath\}(.*?)\\end\{displaymath\}",
                 lambda m: "\n$$" + m.group(1).strip() + "$$\n", txt, flags=re.S)
    txt = re.sub(r"\\begin\{equation\*?\}(.*?)\\end\{equation\*?\}",
                 lambda m: "\n$$" + m.group(1).strip() + "$$\n", txt, flags=re.S)
    txt = _inline(txt)
    # collapse 3+ blank lines to 1 blank line
    txt = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", txt)
    return txt
