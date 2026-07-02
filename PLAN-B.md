# Tier B — PyXspec execution MCP server (design)

Status: **B1 + B2 + B3 + generic dispatch implemented and verified** against
live data (`server/worker.py`, `server/runner.py`, `server/xspec_run.py`;
`tests/test_xspec_run.py`). 15 guarded tools + 3 generic tools giving **100%
object-model API coverage**. Remaining future item: multi-worker session pool.

## Full coverage (generic dispatch)

The 15 structured tools cover ~15% of the 230-member executable API (135 attrs +
95 methods across 15 classes). To reach **any** PyXspec operation without a
per-member tool explosion, three generic tools navigate the live object graph:

- `xspec_get(target)` — read any attribute by object-path
- `xspec_set(target, value)` — write any attribute
- `xspec_call(target, method, args, kwargs)` — call any method

A **target** is `ROOT (.attr | (int))*` resolved with `getattr`/`__call__(int)`
against a whitelist of roots (`AllData/AllModels/Fit/Xset/Plot/AllChains`) — NOT
`eval`. Examples: `Fit.covariance`, `AllModels(1)(2).values`,
`AllData(1).response.rmf`, `Xset.parallel.leven`. The resolver reaches every
attribute/method/nested-handler in the object model, so coverage is complete by
construction.

**Posture (chosen: full & unrestricted).** These tools deliberately do not
enforce the filesystem allowlist and can reach code-loading methods
(`lmod`/`initpackage`/`tclLoad`/`addPyMod`), Tcl-script `restore`, and (via
dunder navigation) arbitrary Python — i.e. effectively local RCE with XSPEC's
capabilities. This is appropriate for a trusted local single-user setup. The 15
structured tools remain the guarded, path-checked, ergonomic path; the generic
tools are the completeness escape hatch. For a less-trusted deployment, drop the
three generic tools (and keep the structured set) or gate them behind a flag.

Tier A (`server/server.py`) is stateless retrieval over the static corpus. Tier B
is a **stateful compute engine**: it drives a live PyXspec so an agent can load
data, define models, fit, error, and iterate — closing the analysis loop.

## The fact that shapes everything

`AllData`, `AllModels`, `Fit` are **process-global singletons** — one XSPEC
engine per Python process — and an analysis spans many calls (load → ignore →
statistic → model → fit → error → flux). So the server must hold a **persistent
session across tool calls**. Consequences:

1. **No true multi-session per process** — two analyses can't coexist in one
   interpreter. → one session per process, or one worker subprocess per session.
2. **Not thread-safe** — calls must be **serialized** (one op in flight).
3. **Can crash/hang** on pathological input → run PyXspec in a **worker
   subprocess** so a bad call kills/restarts the worker, not the server, and
   timeouts are enforceable by killing the worker.

## Architecture

```
MCP client ──stdio──> Tier B server ──pipe──> PyXspec worker subprocess
                       (serialize,            (HEADAS-initialized; holds
                        timeouts, guards)      AllData/AllModels/Fit)
```

- The server never imports `xspec`, so it survives worker restarts.
- The worker is launched through a shell that sources `headas-init.sh` before
  `import xspec`.
- **Protocol isolation:** XSPEC prints to stdout at the C++ level (uncatchable
  from Python), which would corrupt a stdout-based protocol. So the worker sends
  JSON responses on a **dedicated inherited fd** (number passed via
  `XSPEC_RESP_FD`); the worker's stdout/stderr (XSPEC noise) go to DEVNULL.
  Requests arrive on stdin (clean JSON we control).

## Tool surface (higher-level than raw PyXspec)

Composite, safe steps returning typed JSON (guide 01 patterns):

| Tool | Does | Phase |
|---|---|---|
| `reset_session` | clear all; force `Fit.query="yes"`, `chatter=0` | B1 ✅ |
| `load_data(pha, rmf?, arf?, back?, ...)` | load + attach + verify | B1 ✅ |
| `define_model(expr)` | `Model(...)`; return components + params | B1 ✅ |
| `fit(statistic?)` | `Fit.perform()`; return stat/dof/params | B1 ✅ |
| `get_state()` | structured snapshot of data + model + fit | B1 ✅ |
| `set_parameter(index, ...)` | value/limits/freeze/thaw/link/unlink | B2 ✅ |
| `error(spec)` | confidence intervals per parameter | B2 ✅ |
| `calc_flux` / `calc_lumin` | derived quantities per spectrum | B2 ✅ |
| `steppar(spec)` | Δstat scan (grid size capped) | B2 ✅ |
| `plot(types)` | plot arrays (x/y/model/yErr), no GUI | B2 ✅ |
| `fakeit(...)` | simulate spectra (seeded) | B3 ✅ |
| `run_mcmc(...)` | MCMC chain (length capped, overwrites) | B3 ✅ |
| `save_session` / `restore_session` | .xcm persistence | B3 ✅ |

**Blocking-prompt guards proven necessary during B2/B3:** beyond the fit query,
two more prompts would hang a headless run and are now handled by overwriting
first — `run_mcmc` and `save_session` both prompt when their output file already
exists. `error`/`steppar` also require a *current* fit (freeze/thaw invalidates
it), which surfaces as a structured error the agent can act on.

**No generic `exec(code)` tool.** PyXspec can run shell (Tcl `syscall`) and
arbitrary Python — an eval tool is effectively RCE. Excluded by default.

## Guardrails (why Tier B is higher-risk)

- **Filesystem allowlist** — data paths must resolve inside a configured
  `data_root`; anything outside is rejected. (B1: enforced in the runner, the
  trust boundary.)
- **No blocking prompts** — the systemic guard is `Xset.allowPrompting=False`
  (the kill-switch for the whole class), plus `Fit.query="yes"` and `chatter=0`,
  re-asserted at session init AND after every `restore` (an `.xcm` is a Tcl
  script that can re-enable prompts). This subsumes the per-command overwrite
  workarounds for `save`/`run_mcmc`.
- **Crash/timeout are structured, not fatal** — a worker that dies mid-call
  (segfault, CPU-limit) returns `{ok:false, category:"crashed"|"timeout",
  session_lost:true}`; the next call auto-restarts a fresh worker and flags
  `session_restarted:true` so the agent knows prior state is gone.
- **Per-call timeouts** — long ops (`fit`/`error`/`steppar`/`run_mcmc`/
  `xspec_call`) accept a `timeout_s` override so a legitimate long run isn't
  killed at the default.
- **Timeouts** — every call has a deadline; on expiry the worker is killed and
  the response flags `session_lost` so the agent knows state was cleared.
  (B2: auto-restart + `ulimit` resource caps.)
- **Output caps** — plot arrays / chains can be huge → cap or write-to-file +
  handle (B2/B3).
- **Structured errors** — PyXspec exceptions mapped to
  `{ok:false, error, category}` using the guide-05 catalog, for in-loop
  recovery.

## Relationship to Tier A

Keep them **separate servers**: Tier A (`xspec-ai-docs`) stays read-only and
always-on for "what/how" lookups; Tier B (`xspec-run`) is the opt-in engine that
"does it". An agent validates names and reads models via A, then executes via B.

## Deployment

Local only: needs HEADAS + PyXspec installed and data files on the same machine.
The worker must be launched with HEADAS initialized before `import xspec`.

## Phasing

- **B1 (this PoC):** single session; worker subprocess with fd-isolated
  protocol; tools `reset_session`, `load_data`, `define_model`, `fit`,
  `get_state`; filesystem allowlist; query/chatter enforcement; per-call
  select-based timeout. Verified against the manual's `walkthrough/` datasets.
- **B2:** kill-on-timeout auto-restart, `ulimit`, resource caps, `set_parameter`
  / `error` / `flux` / `steppar` / `plot`, richer error mapping.
- **B3:** fakeit, MCMC, save/restore, optional multi-worker session pool.

## Testing

`tests/test_xspec_run.py` drives the runner against the walkthrough data (the
runner bootstraps HEADAS itself, so the test needs only the HEADAS install to
exist). Asserts a real fit result and that the path allowlist rejects outside
paths. Same "verify against live data" principle as the rest of the repo.
