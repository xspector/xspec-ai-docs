"""Parser for XSPEC's manager/model.dat -- the authoritative parameter source.

Each model is a header line followed by `npars` parameter lines:

    <name> <npars> <elo> <ehi> <funcname> <type> <flag> [grad=...]
    <pname> <unit> <default> <hardmin> <softmin> <softmax> <hardmax> <delta>
    ...

Conventions handled:
  * type in {add, mul, con, mix, acn}
  * delta < 0  -> parameter frozen by default
  * a parameter name beginning with `$` is a switch/scale parameter (not fitted)
  * additive models get an implicit `norm` parameter appended
  * unit `" "` (quoted) means dimensionless / blank
"""
import shlex
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Param:
    name: str
    unit: str
    default: float
    hardmin: Optional[float]
    softmin: Optional[float]
    softmax: Optional[float]
    hardmax: Optional[float]
    delta: Optional[float]
    frozen: bool
    kind: str  # "fit" | "switch" | "norm"


@dataclass
class Model:
    name: str
    type: str            # add / mul / con / mix / acn
    func: str
    elo: str
    ehi: str
    npars_declared: int
    params: list = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        return d


def _num(tok):
    try:
        return float(tok)
    except ValueError:
        return None


def _parse_param(line: str) -> Param:
    toks = shlex.split(line)
    name = toks[0]
    if name[0] in "$*":
        # non-fit scale/switch param: "$name value", "$name unit value",
        # or "*name unit value". Value is the last token; a middle token
        # (when present) is the unit.
        unit = toks[1].strip() if len(toks) >= 3 else ""
        val = _num(toks[-1])
        return Param(name=name.lstrip("$*"), unit=unit, default=val,
                     hardmin=None, softmin=None, softmax=None, hardmax=None,
                     delta=None, frozen=True,
                     kind="switch" if name[0] == "$" else "scale")
    # normal: name unit default hardmin softmin softmax hardmax delta
    unit = toks[1].strip()
    if unit == "":
        unit = ""
    default, hardmin, softmin, softmax, hardmax, delta = (
        _num(t) for t in toks[2:8])
    frozen = delta is not None and delta < 0
    return Param(name=name, unit=unit, default=default, hardmin=hardmin,
                 softmin=softmin, softmax=softmax, hardmax=hardmax,
                 delta=delta, frozen=frozen, kind="fit")


def _norm_param() -> Param:
    return Param(name="norm", unit="", default=1.0, hardmin=0.0, softmin=0.0,
                 softmax=1e24, hardmax=1e24, delta=0.01, frozen=False,
                 kind="norm")


def parse(path) -> dict:
    """Return {model_name: Model} for every entry in model.dat."""
    with open(path) as fh:
        lines = fh.read().splitlines()

    models = {}
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        head = line.split()
        # header: name npars elo ehi func type flag ...
        if len(head) >= 6 and head[1].lstrip("-").isdigit():
            name = head[0]
            npars = int(head[1])
            elo, ehi, func = head[2], head[3], head[4]
            mtype = head[5]
            i += 1
            params = []
            read = 0
            while read < npars and i < n and lines[i].strip():
                params.append(_parse_param(lines[i]))
                i += 1
                read += 1
            if mtype == "add":
                params.append(_norm_param())
            models[name] = Model(name=name, type=mtype, func=func,
                                 elo=elo, ehi=ehi, npars_declared=npars,
                                 params=params)
        else:
            i += 1
    return models
