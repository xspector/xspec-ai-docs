"""Tests for the MCP server's data layer (server/corpus.py).

Exercises the query functions directly -- no MCP runtime needed -- so the
server's behavior is verified against the real generated corpus.
Run:  python tests/test_server.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "server"))
from corpus import Corpus  # noqa: E402

C = Corpus()
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


# get_model: known model, case-insensitive, with params + prose
m = C.get_model("TBabs")
check(m["found"] and m["type"] == "mul", "get_model TBabs type")
check(any(p["name"] == "nH" for p in m["params"]), "get_model TBabs has nH")
check(C.get_model("tbabs")["found"], "get_model case-insensitive")
check(m["doc_markdown"].startswith("---"), "get_model includes prose")
# additive model carries implicit norm
pl = C.get_model("powerlaw")
check(any(p["kind"] == "norm" for p in pl["params"]), "powerlaw implicit norm")
# unknown -> suggestions
u = C.get_model("powerlawww")
check(not u["found"] and "powerlaw" in u["suggestions"], "get_model suggests")

# list_models by type
mul = C.list_models("mul")
check(mul["count"] == 75 and all(x["type"] == "mul" for x in mul["models"]),
      "list_models mul")
check(C.list_models()["count"] == 328, "list_models all = 328")

# get_command with alias resolution
fit = C.get_command("fit")
check(fit["found"] and "xfit" in fit["aliases"], "get_command fit + alias")
check(not C.get_command("notacommand")["found"], "get_command unknown")

# get_api by class AND by singleton
check(C.get_api("FitManager")["found"], "get_api by class")
fitapi = C.get_api("Fit")
check(fitapi["found"] and fitapi["class"] == "FitManager", "get_api by singleton")
check(any(a["name"] == "statistic" and a["access"] == "get"
          for a in fitapi["attributes"]), "get_api Fit.statistic get-only")
check(any(mm["name"] == "perform" for mm in fitapi["methods"]),
      "get_api Fit.perform method")

# lookup_intent
r = C.lookup_intent("confidence interval")
check(r["count"] > 0 and "error" in r["results"][0]["pyxspec"].lower(),
      "lookup_intent confidence -> Fit.error")
check(C.lookup_intent("run headless")["count"] > 0, "lookup_intent headless")

# validate (anti-hallucination)
check(C.validate("apec", "model")["valid"], "validate apec model")
check(C.validate("TBABS", "model")["valid"], "validate case-insensitive")
check(not C.validate("powerlaww", "model")["valid"], "validate typo invalid")
check("powerlaw" in C.validate("powerlaww", "model")["suggestions"],
      "validate typo suggests powerlaw")
check(C.validate("cstat", "statistic")["valid"], "validate cstat statistic")
check(C.validate("wilm", "abundance")["valid"], "validate wilm abundance")
check(C.validate("vern", "xsect")["valid"], "validate vern xsect")
check("error" in C.validate("x", "boguskind"), "validate bad kind errors")

# guides
check("00_object_model" in C.get_guide()["guides"], "get_guide lists")
check(C.get_guide("01")["found"], "get_guide by prefix")
check("07_intent_index" in [g for g in C.get_guide()["guides"]],
      "get_guide includes intent index")

# casebook retrieval (Tier C) -- needs pyyaml; skip cleanly if absent
fc = C.find_cases(mission="NICER")
if "error" in fc and "pyyaml" in fc["error"]:
    print("note: pyyaml absent -- skipped casebook checks")
else:
    seed = "nicer-lowcount-thermal-001"
    check(any(r["id"] == seed for r in fc["results"]), "find_cases by mission")
    # fingerprint filters: counts_regime and model (model_family)
    check(any(r["id"] == seed for r in
              C.find_cases(counts_regime="low")["results"]),
          "find_cases by counts_regime")
    check(any(r["id"] == seed for r in
              C.find_cases(model="nsatmos")["results"]),
          "find_cases by model_family")
    # combined filters rank the seed top; lessons summarized inline
    top = C.find_cases(mission="NICER", counts_regime="low",
                       source_type="isolated_ns")["results"][0]
    check(top["id"] == seed and top["score"] >= 9, "find_cases weighted score")
    check(any(l["id"] == "cstat-below-1k-counts" for l in top["lessons"]),
          "find_cases inlines lessons")
    # non-matching filter -> no results
    check(C.find_cases(mission="NoSuchMission")["count"] == 0,
          "find_cases empty on miss")
    # get_case: full study + cited lessons inlined with rule/applies_when
    gc = C.get_case(seed)
    check(gc["found"] and gc["doc_markdown"].startswith("---"),
          "get_case returns full doc")
    check(len(gc["lessons"]) == 2, "get_case inlines both lessons")
    check(all(l.get("applies_when") and l.get("not_when")
              for l in gc["lessons"]), "get_case lessons have conditions")
    # unknown case -> suggestions
    bad = C.get_case("nicer-lowcount-thermal-999")
    check(not bad["found"] and seed in bad["suggestions"],
          "get_case unknown suggests")

# provenance
info = C.info()
check("xspec_version" in info["provenance"], "info provenance")

if fails:
    print("FAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print(f"all server data-layer checks passed "
      f"(corpus: {info['counts']})")
