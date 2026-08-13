"""Tier B worker manager (pure, MCP-free -> unit-testable).

Spawns the PyXspec worker in a HEADAS-initialized shell, serializes calls,
enforces per-call timeouts (kill on expiry), and applies the filesystem
allowlist -- the trust boundary. `xspec_run.py` wraps this as MCP tools.
"""
import json
import os
import re
import select
import shlex
import subprocess
from pathlib import Path

_HERE = Path(__file__).resolve().parent

HEASOFT_ROOT = Path("/Users/kaa/software/heasoft")


def _discover_headas():
    """Resolve HEADAS without hard-coding the OS version.

    The arch directory is named for the macOS release
    (aarch64-apple-darwin25.5.0) and is RENAMED by an OS update, so any
    pinned version silently rots: the previous default here still pointed at
    darwin25.4.0 long after that tree was gone, which does not raise -- it
    just yields a HEADAS path that does not exist, so the worker fails to
    bootstrap (or, worse, appears configured while being unusable).

    Order: explicit XSPEC_HEADAS, then an already-initialized $HEADAS, then
    the newest arch dir actually present on disk.  Returns a str for the
    callers that interpolate it into a shell command.
    """
    env = os.environ.get("XSPEC_HEADAS") or os.environ.get("HEADAS")
    if env and Path(env).is_dir():
        return env
    candidates = sorted(
        (p for p in HEASOFT_ROOT.glob("aarch64-apple-darwin*") if p.is_dir()),
        key=lambda p: p.name)
    if candidates:
        return str(candidates[-1])
    # Nothing usable: keep the env value (if any) so the failure names what
    # was asked for rather than an empty string.
    return env or ""


DEFAULT_HEADAS = _discover_headas()
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
        if self._resp:
            try:
                self._resp.close()      # avoid fd leak per restart
            except Exception:
                pass
            self._resp = None

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
    def _fail(self, error, category):
        self.kill()
        return {"ok": False, "error": error, "category": category,
                "session_lost": True}

    def _call(self, cmd, args=None, timeout=None):
        # (re)start the worker; flag a restart only if a prior one had died
        was_dead = self.proc is not None and self.proc.poll() is not None
        if not self.alive():
            self.start()
        try:
            self.proc.stdin.write(
                json.dumps({"cmd": cmd, "args": args or {}}) + "\n")
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError, ValueError):
            return self._fail("worker died before the request was sent",
                              "crashed")
        line = self._read(timeout or self.timeout)
        if line is None:                # select timed out -> engine wedged
            return self._fail("operation timed out", "timeout")
        if line == "":                  # EOF -> worker crashed mid-operation
            return self._fail("worker crashed during the operation "
                              "(segfault / CPU limit?)", "crashed")
        try:
            resp = json.loads(line)
        except json.JSONDecodeError:
            return self._fail(f"corrupt worker response: {line!r}", "crashed")
        if was_dead:
            resp["session_restarted"] = True   # prior session state was lost
        return resp

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
        """Readable from either the data root or the output root. Distinguishes
        an allowlist violation (ValueError) from within-root-but-missing
        (FileNotFoundError)."""
        path = Path(p)
        roots = [self.data_root, self.output_root]
        cands = ([path.resolve()] if path.is_absolute()
                 else [(r / p).resolve() for r in roots])
        within = [c for c in cands
                  if any(c == r or r in c.parents for r in roots)]
        if not within:
            raise ValueError(f"path outside data/output roots: {p}")
        for c in within:
            if c.exists():
                return str(c)
        raise FileNotFoundError(f"not found under data/output root: {p}")

    # ---- tools ----
    def reset_session(self):
        return self._call("reset_session")

    def load_data(self, pha, rmf=None, arf=None, back=None,
                  ignore_bad=True, energy_range=None, spectrum=1, group=None):
        # spectrum may be a grouped product under the output root
        args = {"pha": self._resolve_readable(pha), "ignore_bad": ignore_bad,
                "spectrum": spectrum, "group": group}
        if rmf:
            args["rmf"] = self._resolve(rmf)
        if arf:
            args["arf"] = self._resolve(arf)
        if back:
            args["back"] = self._resolve(back)
        if energy_range:
            args["energy_range"] = energy_range
        return self._call("load_data", args)

    def define_model(self, expr, modName=None, sourceNum=1):
        return self._call("define_model", {"expr": expr, "modName": modName or "",
                                           "sourceNum": sourceNum})

    def fit(self, statistic=None, timeout=None):
        a = {"statistic": statistic} if statistic else {}
        return self._call("fit", a, timeout=timeout)

    def get_state(self):
        return self._call("get_state")

    # ---- B2: parameters, errors, derived quantities, scans, plots ----
    def set_parameter(self, index, value=None, values_string=None,
                      freeze=False, thaw=False, link=None, unlink=False):
        return self._call("set_parameter", {
            "index": index, "value": value, "values_string": values_string,
            "freeze": freeze, "thaw": thaw, "link": link, "unlink": unlink})

    def error(self, spec, timeout=None):
        return self._call("error", {"spec": spec}, timeout=timeout)

    def calc_flux(self, energy_range, err=False):
        return self._call("calc_flux", {"range": energy_range, "err": err})

    def calc_lumin(self, energy_range):
        return self._call("calc_lumin", {"range": energy_range})

    def steppar(self, spec, timeout=None):
        # cap the grid (product of step-counts). Keep only numeric tokens so
        # keywords like 'log'/'best' don't shift the (par lo hi steps) grouping.
        nums = [t for t in spec.split()
                if re.match(r"-?[\d.]+([eE][-+]?\d+)?$", t)]
        grid = 1
        for s in nums[3::4]:
            try:
                grid *= int(float(s))
            except ValueError:
                pass
        if grid > MAX_STEPPAR_GRID:
            return {"ok": False, "category": "capped",
                    "error": f"steppar grid {grid} exceeds cap "
                             f"{MAX_STEPPAR_GRID}"}
        return self._call("steppar", {"spec": spec}, timeout=timeout)

    def plot(self, types="ldata", xAxis="keV"):
        return self._call("plot", {"types": types, "xAxis": xAxis})

    def plot_image(self, fileName, types="ldata delchi", xAxis="keV"):
        return self._call("plot_image", {
            "fileName": self._resolve_write(fileName), "types": types,
            "xAxis": xAxis})

    def assess_fit(self, goodness_sims=0, timeout=None):
        return self._call("assess_fit", {"goodness_sims": goodness_sims},
                          timeout=timeout)

    def export_script(self):
        return self._call("export_script")

    def journal(self):
        return self._call("journal")

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
                 algorithm="gw", timeout=None):
        if runLength > MAX_CHAIN_LENGTH:
            return {"ok": False, "category": "capped",
                    "error": f"runLength {runLength} exceeds cap "
                             f"{MAX_CHAIN_LENGTH}"}
        return self._call("run_mcmc", {
            "fileName": self._resolve_write(fileName), "burn": burn,
            "runLength": runLength, "walkers": walkers,
            "algorithm": algorithm}, timeout=timeout)

    def save_session(self, fileName, info="a"):
        return self._call("save_session",
                          {"fileName": self._resolve_write(fileName),
                           "info": info})

    def restore_session(self, fileName):
        return self._call("restore_session",
                          {"fileName": self._resolve_readable(fileName)})

    # ---- generic dispatch (full API coverage; unrestricted) ----
    def xget(self, target):
        return self._call("xget", {"target": target})

    def xset(self, target, value):
        return self._call("xset", {"target": target, "value": value})

    def xcall(self, target, method, args=None, kwargs=None, timeout=None):
        return self._call("xcall", {"target": target, "method": method,
                                    "args": args or [], "kwargs": kwargs or {}},
                          timeout=timeout)

    # ---- data prep (pre-analysis; no worker session needed) ----
    def _headas_python(self, code, extra_env=None, timeout=180):
        """Run a Python snippet in a HEADAS-initialized subprocess (so heasoftpy
        imports). HEADAS CLI tools prompt to /dev/tty with no terminal;
        heasoftpy runs them non-interactively, so we go through it."""
        env = dict(os.environ)
        env["HEADAS"] = self.headas
        env["PATH"] = "/opt/homebrew/bin:" + env.get("PATH", "")
        env.update(extra_env or {})
        cmd = ('source "$HEADAS/headas-init.sh" >/dev/null 2>&1; exec '
               + shlex.quote(self.python) + " -c " + shlex.quote(code))
        p = subprocess.run(["bash", "-c", cmd], env=env, capture_output=True,
                           text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr

    def pha_info(self, pha):
        """Inspect a PHA header: mission, exposure, linked RMF/ARF/background,
        grouping, total counts -- what the agent needs to decide how to proceed
        (guide 02). Reads the FITS header directly; no XSPEC session."""
        from astropy.io import fits
        path = self._resolve_readable(pha)   # data root or output (grouped) root
        info = {"file": path}
        with fits.open(path) as hdul:
            hdu = hdul["SPECTRUM"] if "SPECTRUM" in hdul else hdul[1]
            h, prim = hdu.header, hdul[0].header
            for key in ("TELESCOP", "INSTRUME", "FILTER", "EXPOSURE",
                        "RESPFILE", "ANCRFILE", "BACKFILE", "CORRFILE",
                        "CHANTYPE", "DETCHANS", "AREASCAL", "BACKSCAL",
                        "POISSERR", "HDUCLAS2"):
                v = h.get(key, prim.get(key))
                if v is not None:
                    info[key] = v
            cols = ([c.name.upper() for c in hdu.columns]
                    if getattr(hdu, "columns", None) else [])
            info["grouped"] = "GROUPING" in cols
            info["type2"] = "SPEC_NUM" in cols or h.get("HDUCLAS4") == "TYPE:II"
            try:
                import numpy as np
                if "COUNTS" in cols:
                    info["total_counts"] = float(np.sum(hdu.data["COUNTS"]))
                elif "RATE" in cols and info.get("EXPOSURE"):
                    info["total_counts"] = float(
                        np.sum(hdu.data["RATE"]) * info["EXPOSURE"])
            except Exception:
                pass
        return {"ok": True, "result": info}

    def group_spectrum(self, infile, outfile, grouptype="min", groupscale=25,
                       backfile=None, respfile=None, arffile=None):
        """Group a spectrum with ftgrouppha (grouptype: min/snmin/bmin/opt/
        optmin/const). opt/optmin need respfile. Writes under the output root.
        Any of respfile/arffile/backfile supplied are embedded as absolute paths
        in the output so the grouped file is self-contained (loads from any
        directory)."""
        outpath = self._resolve_write(outfile)
        params = {"infile": self._resolve(infile), "outfile": outpath,
                  "grouptype": grouptype, "groupscale": groupscale,
                  "clobber": "yes"}
        if backfile:
            params["backfile"] = self._resolve(backfile)
        if respfile:
            params["respfile"] = self._resolve(respfile)
        code = ("import os, json, sys, heasoftpy as hsp; "
                "p = json.loads(os.environ['XSPEC_GRP_PARAMS']); "
                "sys.exit(hsp.ftgrouppha(**p).returncode)")
        rc, out, err = self._headas_python(
            code, extra_env={"XSPEC_GRP_PARAMS": json.dumps(params)})
        if rc != 0 or not os.path.exists(outpath):
            return {"ok": False, "category": "prep",
                    "error": (err or out).strip()[-500:] or
                    f"ftgrouppha exited {rc}"}
        # make the grouped file self-contained: embed absolute RESPFILE/
        # ANCRFILE/BACKFILE so it loads from any directory. Caller-supplied
        # paths win; otherwise promote a real relative keyword to absolute.
        # (%match% / none are left alone -- there is no concrete file to embed.)
        rewritten = []
        supplied = {"RESPFILE": respfile, "ANCRFILE": arffile,
                    "BACKFILE": backfile}
        try:
            from astropy.io import fits
            indir = os.path.dirname(self._resolve(infile))
            with fits.open(outpath, mode="update") as hdul:
                hdu = hdul["SPECTRUM"] if "SPECTRUM" in hdul else hdul[1]
                for key, given in supplied.items():
                    if given:
                        hdu.header[key] = self._resolve(given)
                        rewritten.append(key)
                        continue
                    v = hdu.header.get(key)
                    if v and v.upper() != "NONE" and not os.path.isabs(v):
                        cand = os.path.join(indir, v)
                        if os.path.exists(cand):
                            hdu.header[key] = cand
                            rewritten.append(key)
                hdul.flush()
        except Exception:
            pass
        return {"ok": True, "result": {"outfile": outpath,
                                       "grouptype": grouptype,
                                       "groupscale": groupscale,
                                       "abspath_keywords": rewritten}}
