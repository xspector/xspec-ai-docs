"""XSPEC execution MCP server (Tier B, B1) -- read/write, runs live PyXspec.

Thin FastMCP wrapper over runner.XspecRunner. Calls are serialized (XSPEC is
not thread-safe). Data paths are restricted to XSPEC_DATA_ROOT.

Run (stdio):  python server/xspec_run.py
Requires HEADAS + PyXspec installed; the worker bootstraps HEADAS itself.
"""
import threading
from typing import Any

from mcp.server.fastmcp import FastMCP

from runner import XspecRunner

_LOCK = threading.Lock()
_RUNNER = XspecRunner()
mcp = FastMCP("xspec-run")


@mcp.tool()
def reset_session() -> dict:
    """Clear all data and models and set headless defaults (query=yes,
    chatter=0). Call at the start of an analysis for a clean, reproducible
    state."""
    with _LOCK:
        return _RUNNER.reset_session()


@mcp.tool()
def load_data(pha: str, rmf: str = "", arf: str = "", back: str = "",
              ignore_bad: bool = True, energy_range: str = "",
              spectrum: int = 1, group: int = 0) -> dict:
    """Load a spectrum into slot `spectrum` (data group `group`, default =
    spectrum) and optionally attach response/arf/background, ignore bad
    channels, and restrict the energy range. Call repeatedly with increasing
    `spectrum` for joint fits. Paths must be inside the data root; energy_range
    is an XSPEC ignore expression, e.g. '**-0.5 8.0-**'."""
    with _LOCK:
        return _RUNNER.load_data(pha, rmf or None, arf or None, back or None,
                                 ignore_bad, energy_range or None,
                                 spectrum, group or None)


@mcp.tool()
def define_model(expr: str, modName: str = "", sourceNum: int = 1) -> dict:
    """Define a model from an XSPEC expression (e.g. 'tbabs*powerlaw'). Optional
    `modName` (named model) and `sourceNum` (>1 for background/multi-source
    models). Returns components, parameter count, and the parameter list."""
    with _LOCK:
        return _RUNNER.define_model(expr, modName or None, sourceNum)


@mcp.tool()
def fit(statistic: str = "", timeout_s: float = 0) -> dict:
    """Fit the current model to the data (optionally setting the fit statistic
    first, e.g. 'cstat'). `timeout_s` overrides the default per-call timeout for
    a long fit. Returns statistic, dof, and fitted parameters."""
    with _LOCK:
        return _RUNNER.fit(statistic or None, timeout_s or None)


@mcp.tool()
def get_state() -> dict:
    """Structured snapshot of the current session: loaded spectra, model
    components/parameters, and the current fit statistic/dof."""
    with _LOCK:
        return _RUNNER.get_state()


@mcp.tool()
def set_parameter(index: int, value: float = None, values_string: str = "",
                  freeze: bool = False, thaw: bool = False, link: int = None,
                  unlink: bool = False) -> dict:
    """Modify one parameter (by number). Set `value`, or `values_string`
    ('val,delta,min,bottom,top,max') for value+limits; `freeze`/`thaw`;
    `link` to another parameter number, or `unlink`."""
    with _LOCK:
        return _RUNNER.set_parameter(index, value, values_string or None,
                                     freeze, thaw, link, unlink)


@mcp.tool()
def error(spec: str, timeout_s: float = 0) -> dict:
    """Confidence intervals via the error command (e.g. '2.706 1-3'). Requires a
    current fit (freeze/thaw/newpar invalidates it -> re-fit first). Returns each
    parameter's (low, high, code); code 'FFFFFFFFF' means clean."""
    with _LOCK:
        return _RUNNER.error(spec, timeout_s or None)


@mcp.tool()
def calc_flux(energy_range: str, err: bool = False) -> dict:
    """Model flux over an energy range (e.g. '0.5 10.0'); err=True adds
    Monte-Carlo flux errors. Returns the per-spectrum flux tuple."""
    with _LOCK:
        return _RUNNER.calc_flux(energy_range, err)


@mcp.tool()
def calc_lumin(energy_range: str) -> dict:
    """Luminosity over an energy range with redshift (e.g. '0.5 10.0 0.01')."""
    with _LOCK:
        return _RUNNER.calc_lumin(energy_range)


@mcp.tool()
def steppar(spec: str, timeout_s: float = 0) -> dict:
    """Steppar scan (e.g. '2 1.5 2.5 20', or two triples for a 2-D grid).
    Returns the delta-statistic grid. Grid size is capped; `timeout_s` overrides
    the per-call timeout for a large scan."""
    with _LOCK:
        return _RUNNER.steppar(spec, timeout_s or None)


@mcp.tool()
def plot(types: str = "ldata", xAxis: str = "keV") -> dict:
    """Compute plot arrays (no GUI): returns x, y, model, yErr for the given
    plot types (e.g. 'ldata delchi'). Use this to 'see' a fit numerically."""
    with _LOCK:
        return _RUNNER.plot(types, xAxis)


@mcp.tool()
def plot_image(fileName: str, types: str = "ldata delchi",
               xAxis: str = "keV") -> dict:
    """Render a plot to an image file under the output root (for a human to look
    at). The device is inferred from the extension (.gif/.ps/.cps/.eps/.pdf;
    note this build has no PNG driver). Returns the file path. Use `plot` for
    numeric arrays instead."""
    with _LOCK:
        return _RUNNER.plot_image(fileName, types, xAxis)


@mcp.tool()
def assess_fit(goodness_sims: int = 0, timeout_s: float = 0) -> dict:
    """Composite fit-quality check: returns {acceptable, issues, ...} covering
    parameters pegged at soft limits, a runs test for systematic residuals,
    reduced chi-square sanity, and (if goodness_sims>0, cstat family) a
    Monte-Carlo goodness. Call after fit instead of remembering each check."""
    with _LOCK:
        return _RUNNER.assess_fit(goodness_sims, timeout_s or None)


@mcp.tool()
def export_script() -> dict:
    """Emit a standalone PyXspec script reproducing every mutating operation of
    the current session (a reproducible artifact for the result). Returns
    {nOps, script}."""
    with _LOCK:
        return _RUNNER.export_script()


@mcp.tool()
def journal() -> dict:
    """Return the raw list of mutating operations recorded this session."""
    with _LOCK:
        return _RUNNER.journal()


@mcp.tool()
def fakeit(response: str = "", arf: str = "", background: str = "",
           exposure: float = None, nSpectra: int = 1, applyStats: bool = True,
           seed: int = None) -> dict:
    """Simulate spectra. Paths must be inside the data root; seed for
    reproducibility. Simulated spectra are not written to disk."""
    settings = {"response": response, "arf": arf, "background": background,
                "exposure": exposure}
    with _LOCK:
        return _RUNNER.fakeit(settings, nSpectra, applyStats, seed)


@mcp.tool()
def run_mcmc(fileName: str, burn: int = 1000, runLength: int = 10000,
             walkers: int = 10, algorithm: str = "gw",
             timeout_s: float = 0) -> dict:
    """Run an MCMC chain, written under the output root (overwrites). runLength
    is capped; set `timeout_s` for a long chain (else it may hit the default
    timeout and lose the session)."""
    with _LOCK:
        return _RUNNER.run_mcmc(fileName, burn, runLength, walkers, algorithm,
                                timeout_s or None)


@mcp.tool()
def save_session(fileName: str, info: str = "a") -> dict:
    """Save the session (model+data+settings) to an .xcm under the output
    root."""
    with _LOCK:
        return _RUNNER.save_session(fileName, info)


@mcp.tool()
def restore_session(fileName: str) -> dict:
    """Restore a session from an .xcm (readable from the data or output root).
    Returns the resulting state."""
    with _LOCK:
        return _RUNNER.restore_session(fileName)


@mcp.tool()
def xspec_get(target: str) -> dict:
    """Read ANY PyXspec attribute by object-path. The path starts at a root
    (AllData, AllModels, Fit, Xset, Plot, AllChains) and navigates via .attr and
    (int) indexing. Examples: 'Fit.covariance', 'AllModels(1)(2).values',
    'AllData(1).response.rmf', 'Xset.abund', 'Xset.parallel.leven'."""
    with _LOCK:
        return _RUNNER.xget(target)


@mcp.tool()
def xspec_set(target: str, value: Any) -> dict:
    """Set ANY writable PyXspec attribute by object-path (must end in an
    attribute). Examples: xspec_set('Fit.nIterations', 100),
    xspec_set('Xset.abund', 'wilm'), xspec_set('AllModels(1)(2).frozen', true),
    xspec_set('Xset.cosmo', '70,0,0.73')."""
    with _LOCK:
        return _RUNNER.xset(target, value)


@mcp.tool()
def xspec_call(target: str, method: str, args: list = None,
               kwargs: dict = None, timeout_s: float = 0) -> dict:
    """Call ANY PyXspec method. `target` resolves to the object; `method` is the
    method name; `args`/`kwargs` are JSON; `timeout_s` overrides the per-call
    timeout for long methods (goodness, chains). Examples:
    xspec_call('Fit','goodness',[1000],{'sim':true});
    xspec_call('AllModels','setPars',[1.0,1.8,1e-3]);
    xspec_call('Xset','addModelString',['APECROOT','3.0.9']);
    xspec_call('AllChains','margin',['1 1.5 2.5 50']).

    NOTE: unrestricted -- this can reach code-loading (lmod/initpackage/tclLoad)
    and Tcl-script restore, and file-path args are not allowlisted."""
    with _LOCK:
        return _RUNNER.xcall(target, method, args, kwargs, timeout_s or None)


if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        _RUNNER.close()
