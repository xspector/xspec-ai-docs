"""Tier B worker manager (pure, MCP-free -> unit-testable).

Spawns the PyXspec worker in a HEADAS-initialized shell, serializes calls,
enforces per-call timeouts (kill on expiry), and applies the filesystem
allowlist -- the trust boundary. `xspec_run.py` wraps this as MCP tools.
"""
import json
import os
import select
import subprocess
from pathlib import Path

_HERE = Path(__file__).resolve().parent
DEFAULT_HEADAS = os.environ.get(
    "XSPEC_HEADAS", "/Users/kaa/software/heasoft/aarch64-apple-darwin25.4.0")
DEFAULT_PYTHON = os.environ.get("XSPEC_PYTHON", "/opt/miniconda3/bin/python")
DEFAULT_DATA_ROOT = os.environ.get(
    "XSPEC_DATA_ROOT",
    "/Users/kaa/software/Xspec-aux/doc/manual/walkthrough")
DEFAULT_OUTPUT_ROOT = os.environ.get(
    "XSPEC_OUTPUT_ROOT", str(Path.home() / ".xspec-run-out"))

# resource caps (B2)
MAX_STEPPAR_GRID = 20000     # product of steps across all stepped params
MAX_CHAIN_LENGTH = 1_000_000
MAX_FAKE_SPECTRA = 100


class XspecRunner:
    def __init__(self, data_root=DEFAULT_DATA_ROOT, headas=DEFAULT_HEADAS,
                 python=DEFAULT_PYTHON, worker=str(_HERE / "worker.py"),
                 output_root=DEFAULT_OUTPUT_ROOT, timeout=180,
                 start_timeout=90, cpu_limit=600, mem_mb=None):
        self.data_root = Path(data_root).resolve()
        self.output_root = Path(output_root).resolve()
        self.output_root.mkdir(parents=True, exist_ok=True)
        self.headas = headas
        self.python = python
        self.worker = worker
        self.timeout = timeout
        self.start_timeout = start_timeout
        self.cpu_limit = cpu_limit          # CPU seconds; kills a wedged engine
        self.mem_mb = mem_mb                # virtual mem (best-effort; ignored on macOS)
        self.proc = None
        self._resp = None

    # ---- lifecycle ----
    def start(self):
        r_fd, w_fd = os.pipe()          # child writes responses on w_fd
        env = dict(os.environ)
        env["HEADAS"] = self.headas
        env["XSPEC_RESP_FD"] = str(w_fd)
        env["PATH"] = "/opt/homebrew/bin:" + env.get("PATH", "")
        # resource caps (best-effort; -v is ignored on macOS). A CPU-time cap
        # kills a wedged C++ engine even if the pipe never closes.
        limits = f"ulimit -t {self.cpu_limit} 2>/dev/null; "
        if self.mem_mb:
            limits += f"ulimit -v {self.mem_mb * 1024} 2>/dev/null; "
        bash = (limits + 'source "$HEADAS/headas-init.sh" >/dev/null 2>&1; '
                f'exec "{self.python}" "{self.worker}"')
        self.proc = subprocess.Popen(
            ["bash", "-c", bash], stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            env=env, pass_fds=(w_fd,), text=True)
        os.close(w_fd)
        self._resp = os.fdopen(r_fd, "r")
        ready = self._read(self.start_timeout)
        if not ready or not json.loads(ready).get("ready"):
            self.kill()
            raise RuntimeError("worker failed to start (HEADAS/PyXspec?)")
        return self

    def _read(self, timeout):
        if not self._resp:
            return None
        r, _, _ = select.select([self._resp], [], [], timeout)
        if not r:
            return None
        return self._resp.readline()

    def alive(self):
        return self.proc is not None and self.proc.poll() is None

    def kill(self):
        if self.proc and self.proc.poll() is None:
            self.proc.kill()
            self.proc.wait(timeout=5)
        self.proc = None

    def close(self):
        try:
            if self.alive():
                self.proc.stdin.write(json.dumps({"cmd": "shutdown"}) + "\n")
                self.proc.stdin.flush()
                self._read(5)
        except Exception:
            pass
        self.kill()

    # ---- protocol ----
    def _call(self, cmd, args=None, timeout=None):
        if not self.alive():
            self.start()
        self.proc.stdin.write(json.dumps({"cmd": cmd, "args": args or {}}) + "\n")
        self.proc.stdin.flush()
        line = self._read(timeout or self.timeout)
        if line is None:                # timeout -> engine may be wedged
            self.kill()
            return {"ok": False, "error": "operation timed out",
                    "category": "timeout", "session_lost": True}
        return json.loads(line)

    # ---- filesystem allowlist (trust boundary) ----
    def _resolve(self, p):
        path = Path(p)
        if not path.is_absolute():
            path = self.data_root / p
        path = path.resolve()
        if not (path == self.data_root or self.data_root in path.parents):
            raise ValueError(f"path outside data root ({self.data_root}): {p}")
        if not path.exists():
            raise FileNotFoundError(str(path))
        return str(path)

    def _resolve_write(self, p):
        """Output paths must live under output_root (write allowlist)."""
        path = Path(p)
        if not path.is_absolute():
            path = self.output_root / p
        path = path.resolve()
        if not (path == self.output_root or self.output_root in path.parents):
            raise ValueError(
                f"output path outside output root ({self.output_root}): {p}")
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)

    def _resolve_readable(self, p):
        """Readable from either the data root or the output root."""
        path = Path(p)
        roots = [self.data_root, self.output_root]
        cands = ([path.resolve()] if path.is_absolute()
                 else [(r / p).resolve() for r in roots])
        for c in cands:
            if any(c == r or r in c.parents for r in roots) and c.exists():
                return str(c)
        raise FileNotFoundError(f"not found under data/output root: {p}")

    # ---- tools ----
    def reset_session(self):
        return self._call("reset_session")

    def load_data(self, pha, rmf=None, arf=None, back=None,
                  ignore_bad=True, energy_range=None):
        args = {"pha": self._resolve(pha), "ignore_bad": ignore_bad}
        if rmf:
            args["rmf"] = self._resolve(rmf)
        if arf:
            args["arf"] = self._resolve(arf)
        if back:
            args["back"] = self._resolve(back)
        if energy_range:
            args["energy_range"] = energy_range
        return self._call("load_data", args)

    def define_model(self, expr):
        return self._call("define_model", {"expr": expr})

    def fit(self, statistic=None):
        return self._call("fit", {"statistic": statistic} if statistic else {})

    def get_state(self):
        return self._call("get_state")

    # ---- B2: parameters, errors, derived quantities, scans, plots ----
    def set_parameter(self, index, value=None, values_string=None,
                      freeze=False, thaw=False, link=None, unlink=False):
        return self._call("set_parameter", {
            "index": index, "value": value, "values_string": values_string,
            "freeze": freeze, "thaw": thaw, "link": link, "unlink": unlink})

    def error(self, spec):
        return self._call("error", {"spec": spec})

    def calc_flux(self, energy_range, err=False):
        return self._call("calc_flux", {"range": energy_range, "err": err})

    def calc_lumin(self, energy_range):
        return self._call("calc_lumin", {"range": energy_range})

    def steppar(self, spec):
        # cap the grid size (product of the 'steps' token of each param)
        toks = spec.split()
        steps = toks[3::4]
        grid = 1
        for s in steps:
            try:
                grid *= int(s)
            except ValueError:
                pass
        if grid > MAX_STEPPAR_GRID:
            return {"ok": False, "category": "capped",
                    "error": f"steppar grid {grid} exceeds cap "
                             f"{MAX_STEPPAR_GRID}"}
        return self._call("steppar", {"spec": spec})

    def plot(self, types="ldata", xAxis="keV"):
        return self._call("plot", {"types": types, "xAxis": xAxis})

    # ---- B3: fakeit, MCMC, save/restore ----
    def fakeit(self, settings=None, nSpectra=1, applyStats=True, seed=None):
        if nSpectra > MAX_FAKE_SPECTRA:
            return {"ok": False, "category": "capped",
                    "error": f"nSpectra {nSpectra} exceeds cap "
                             f"{MAX_FAKE_SPECTRA}"}
        s = dict(settings or {})
        for k in ("response", "arf", "background"):
            if s.get(k):
                s[k] = self._resolve(s[k])
        return self._call("fakeit", {"settings": s, "nSpectra": nSpectra,
                                     "applyStats": applyStats, "seed": seed})

    def run_mcmc(self, fileName, burn=1000, runLength=10000, walkers=10,
                 algorithm="gw"):
        if runLength > MAX_CHAIN_LENGTH:
            return {"ok": False, "category": "capped",
                    "error": f"runLength {runLength} exceeds cap "
                             f"{MAX_CHAIN_LENGTH}"}
        return self._call("run_mcmc", {
            "fileName": self._resolve_write(fileName), "burn": burn,
            "runLength": runLength, "walkers": walkers,
            "algorithm": algorithm}, timeout=self.timeout)

    def save_session(self, fileName, info="a"):
        return self._call("save_session",
                          {"fileName": self._resolve_write(fileName),
                           "info": info})

    def restore_session(self, fileName):
        return self._call("restore_session",
                          {"fileName": self._resolve_readable(fileName)})
