"""XSPEC execution MCP server (Tier B, B1) -- read/write, runs live PyXspec.

Thin FastMCP wrapper over runner.XspecRunner. Calls are serialized (XSPEC is
not thread-safe). Data paths are restricted to XSPEC_DATA_ROOT.

Run (stdio):  python server/xspec_run.py
Requires HEADAS + PyXspec installed; the worker bootstraps HEADAS itself.
"""
import threading

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
              ignore_bad: bool = True, energy_range: str = "") -> dict:
    """Load a spectrum (and optionally attach response/arf/background), ignore
    bad channels, and restrict the energy range. Paths must be inside the
    configured data root. energy_range is an XSPEC ignore expression, e.g.
    '**-0.5 8.0-**'."""
    with _LOCK:
        return _RUNNER.load_data(pha, rmf or None, arf or None, back or None,
                                 ignore_bad, energy_range or None)


@mcp.tool()
def define_model(expr: str) -> dict:
    """Define the model from an XSPEC expression (e.g. 'tbabs*powerlaw').
    Returns component names, parameter count, and the parameter list."""
    with _LOCK:
        return _RUNNER.define_model(expr)


@mcp.tool()
def fit(statistic: str = "") -> dict:
    """Fit the current model to the data (optionally setting the fit statistic
    first, e.g. 'cstat'). Returns statistic, dof, and fitted parameters."""
    with _LOCK:
        return _RUNNER.fit(statistic or None)


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
def error(spec: str) -> dict:
    """Confidence intervals via the error command (e.g. '2.706 1-3'). Returns
    each parameter's (low, high, code); code 'FFFFFFFFF' means clean."""
    with _LOCK:
        return _RUNNER.error(spec)


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
def steppar(spec: str) -> dict:
    """Steppar scan (e.g. '2 1.5 2.5 20', or two triples for a 2-D grid).
    Returns the delta-statistic grid. Grid size is capped."""
    with _LOCK:
        return _RUNNER.steppar(spec)


@mcp.tool()
def plot(types: str = "ldata", xAxis: str = "keV") -> dict:
    """Compute plot arrays (no GUI): returns x, y, model, yErr for the given
    plot types (e.g. 'ldata delchi'). Use this to 'see' a fit numerically."""
    with _LOCK:
        return _RUNNER.plot(types, xAxis)


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
             walkers: int = 10, algorithm: str = "gw") -> dict:
    """Run an MCMC chain, written under the output root. runLength is capped."""
    with _LOCK:
        return _RUNNER.run_mcmc(fileName, burn, runLength, walkers, algorithm)


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


if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        _RUNNER.close()
