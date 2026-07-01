"""XSPEC/PyXspec AI docs — MCP server (Tier A: read-only retrieval).

Exposes the generated corpus as MCP tools so an agent can look up models,
commands, the PyXspec class API, task recipes, and validate names against the
authoritative grounding set — all without reading files directly.

Run (stdio):   python server/server.py
Corpus path:   $XSPEC_AI_CORPUS  (defaults to ../corpus relative to this file)
"""
import os

from mcp.server.fastmcp import FastMCP

from corpus import Corpus, DEFAULT_ROOT

C = Corpus(os.environ.get("XSPEC_AI_CORPUS") or DEFAULT_ROOT)
mcp = FastMCP("xspec-ai-docs")


@mcp.tool()
def get_model(name: str) -> dict:
    """Full reference for an XSPEC model: component type, every parameter with
    units/defaults/hard+soft limits/frozen flag (authoritative from model.dat),
    plus prose. Case-insensitive. Returns suggestions if not found."""
    return C.get_model(name)


@mcp.tool()
def list_models(type: str = "") -> dict:
    """List models, optionally filtered by component type: 'add' (additive),
    'mul' (multiplicative), 'con' (convolution), 'acn'."""
    return C.list_models(type or None)


@mcp.tool()
def get_command(name: str) -> dict:
    """Reference for an interactive XSPEC (Tcl) command: syntax + examples.
    Case-insensitive; accepts aliases. Returns suggestions if not found."""
    return C.get_command(name)


@mcp.tool()
def get_api(class_name: str) -> dict:
    """PyXspec class API: attributes (type, get/get-set, description) and method
    signatures. Accepts the class name or its singleton (e.g. 'Fit' or
    'FitManager', 'AllData' or 'DataManager')."""
    return C.get_api(class_name)


@mcp.tool()
def lookup_intent(query: str, limit: int = 10) -> dict:
    """'How do I X?' -> the exact PyXspec call (and Tcl equivalent). Searches
    the intent index, e.g. 'confidence interval', 'set parameter limit',
    'flux', 'run headless'."""
    return C.lookup_intent(query, limit)


@mcp.tool()
def validate(name: str, kind: str) -> dict:
    """Check a name against the authoritative grounding set before using it
    (anti-hallucination). kind is one of: model, command, statistic, plot_type,
    tclout_key, xset_key, abundance, xsect. Returns valid + canonical form, or
    close suggestions."""
    return C.validate(name, kind)


@mcp.tool()
def get_guide(name: str = "") -> dict:
    """Task-layer guides (PyXspec-first). With no name, lists available guides;
    e.g. '00_object_model', '01' (headless+output), '02' (data ingestion),
    '03' (recipes), '04' (anti-patterns), '05' (errors), '06' (model selection),
    '07' (intent index)."""
    return C.get_guide(name or None)


@mcp.tool()
def corpus_info() -> dict:
    """Provenance (XSPEC version + source commits) and item counts for the
    corpus this server is serving."""
    return C.info()


if __name__ == "__main__":
    mcp.run()
