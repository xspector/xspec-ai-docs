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


if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        _RUNNER.close()
