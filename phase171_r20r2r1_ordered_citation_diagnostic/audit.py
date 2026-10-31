"""Read-only R20R2R1 diagnostic for the existing ordered-reference tests.

The diagnostic neither installs a patch nor changes any production file.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TEST_PATH = ROOT / "phase165_r52_r15_ordered_citation" / "test_phase165_r52_r15_ordered_citation.py"
TRACKED_PATHS = (
    "phase165_r3_recursive_search.py",
    "phase165_r52_r15_ordered_citation.py",
    "phase163_r3_registry_validation.py",
    "unified_statement_registry.py",
    "phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py",
    "phase165_r52_r9_shared_math.py",
)


def git(*args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=True,
    )
    return process.stdout.decode("utf-8", errors="replace").strip()


def load_existing_fixture() -> Any:
    spec = importlib.util.spec_from_file_location("r20r2r1_existing_ordered_test", TEST_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load existing ordered citation test")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def blob_comparison(relative_path: str) -> dict[str, Any]:
    absolute_path = ROOT / relative_path
    return {
        "path": relative_path,
        "exists": absolute_path.is_file(),
        "working_tree_blob": git("hash-object", relative_path) if absolute_path.is_file() else None,
        "head_blob": git("rev-parse", "HEAD:" + relative_path),
    }


def describe_fixture(bridge: Any, goal: object, citing_id: str) -> dict[str, Any]:
    from phase163_r3_registry_validation import CitationDecision, assess_citation
    from proof import ProofRule, ProofStep
    from unified_statement_registry import AssertionOrigin

    result: dict[str, Any] = {
        "citing_assertion_id": citing_id,
        "citing_source_id": bridge.registry.reference(
            bridge.registry.assertion(citing_id).reference_id
        ).source_id,
        "citing_publication_position": bridge.registry.reference(
            bridge.registry.assertion(citing_id).reference_id
        ).publication_position,
        "candidates": [],
    }
    for assertion in bridge.registry._assertions.values():
        if type(assertion.content) is not type(goal) or assertion.content != goal:
            continue
        source = bridge.registry.reference(assertion.reference_id)
        links = [link for link in bridge.proof_links if link.assertion_id == assertion.assertion_id]
        decision = assess_citation(bridge.registry, assertion.assertion_id, citing_id)
        result["candidates"].append({
            "assertion_id": assertion.assertion_id,
            "origin": assertion.origin.value,
            "origin_is_fixed_statement": assertion.origin is AssertionOrigin.FIXED_STATEMENT,
            "source_id": source.source_id,
            "publication_position": source.publication_position,
            "available_after_position": assertion.available_after_position,
            "dependencies": list(assertion.dependencies),
            "citation_decision": decision.decision.value,
            "citation_reason": decision.reason,
            "citation_is_allowed": decision.decision is CitationDecision.ALLOWED,
            "link_count": len(links),
            "step_is_proof_step": len(links) == 1 and isinstance(links[0].step, ProofStep),
            "step_rule": (links[0].step.rule.value if len(links) == 1 and isinstance(links[0].step, ProofStep) else None),
            "step_is_given": len(links) == 1 and isinstance(links[0].step, ProofStep)
                and links[0].step.rule is ProofRule.GIVEN,
            "exact_conclusion": len(links) == 1 and isinstance(links[0].step, ProofStep)
                and type(links[0].step.conclusion) is type(goal)
                and links[0].step.conclusion == goal,
        })
    return result


def run() -> dict[str, Any]:
    if not (ROOT / ".git").exists():
        raise RuntimeError("Unpack under the EHP Proof Tracer repository root")
    sys.path.insert(0, str(ROOT))
    from phase165_r52_r15_ordered_citation import ordered_typed_reference_steps
    from phase163_r3_registry_validation import assess_citation
    import phase165_r52_r15_ordered_citation as ordered_module
    import phase163_r3_registry_validation as validation_module
    import unified_statement_registry as registry_module
    import phase165_r3_recursive_search as recursive_module
    from phase165_r3_recursive_search import reconstruct_registered_goal

    existing_test = load_existing_fixture()
    bridge, expected_step = existing_test._fixture()
    fixture = describe_fixture(bridge, "fact", "citing")
    direct_steps = ordered_typed_reference_steps(bridge, "fact", "citing")
    report: dict[str, Any] = {
        "mode": "AUDIT_ONLY",
        "branch": git("branch", "--show-current"),
        "head": git("rev-parse", "HEAD"),
        "working_tree_status": git("status", "--short", "--untracked-files=no"),
        "tracked_files": [blob_comparison(path) for path in TRACKED_PATHS],
        "module_locations": {
            "ordered": str(Path(ordered_module.__file__).resolve()),
            "validation": str(Path(validation_module.__file__).resolve()),
            "registry": str(Path(registry_module.__file__).resolve()),
            "recursive_search": str(Path(recursive_module.__file__).resolve()),
            "test_fixture": str(TEST_PATH.resolve()),
        },
        "assess_citation_identity": assess_citation is ordered_module.assess_citation,
        "fixture": fixture,
        "ordered_direct_step_count": len(direct_steps),
        "ordered_direct_step_is_expected": len(direct_steps) == 1 and direct_steps[0] is expected_step,
    }
    try:
        found = reconstruct_registered_goal(
            "fact", bridge, "citing", lambda goal: (),
            lookup_mode="typed_reference_ordered",
        )
        report["search_result"] = "PROVED"
        report["search_step_is_expected"] = found is expected_step
    except Exception as exc:
        report["search_result"] = "EXCEPTION"
        report["search_exception"] = type(exc).__name__ + ": " + str(exc)
    if report["ordered_direct_step_is_expected"]:
        report["classification"] = "DIRECT_ORDERED_REFERENCE_OK_IN_FRESH_PROCESS"
    elif not fixture["candidates"]:
        report["classification"] = "MISSING_TYPED_CANDIDATE"
    elif any(not item["citation_is_allowed"] for item in fixture["candidates"]):
        report["classification"] = "CITATION_ELIGIBILITY_REJECTED"
    elif any(not item["step_is_given"] or not item["exact_conclusion"] for item in fixture["candidates"]):
        report["classification"] = "PROOF_LINK_INCONSISTENT"
    else:
        report["classification"] = "ORDERED_LOOKUP_UNEXPECTED_EMPTY_OR_AMBIGUOUS"
    return report


def main() -> int:
    report = run()
    output = PACKAGE / "output" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output.mkdir(parents=True, exist_ok=False)
    path = output / "diagnostic.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R2R1_MODE=" + report["mode"])
    print("PHASE171_R20R2R1_BRANCH=" + report["branch"])
    print("PHASE171_R20R2R1_HEAD=" + report["head"])
    print("PHASE171_R20R2R1_CLASSIFICATION=" + report["classification"])
    print("PHASE171_R20R2R1_ORDERED_DIRECT_STEP_COUNT=" + str(report["ordered_direct_step_count"]))
    print("PHASE171_R20R2R1_SEARCH_RESULT=" + report["search_result"])
    print("PHASE171_R20R2R1_REPORT=" + str(path))
    for item in report["fixture"]["candidates"]:
        print("PHASE171_R20R2R1_CANDIDATE=" + json.dumps(item, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
