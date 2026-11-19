"""Read-only runtime trace of the actual pi_9^5 proof and citation projection."""
from __future__ import annotations

import argparse
from dataclasses import fields, is_dataclass
import json
from pathlib import Path
import subprocess
import sys
import traceback

TARGET = (5, 4)
LOCATORS = ("(5.11)", "(5.8)")


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return completed.stdout.strip()


def compact(value: object, limit: int = 1200) -> str:
    result = repr(value)
    return result if len(result) <= limit else result[:limit] + " [TRUNCATED]"


def step_details(step: object, index: int, numbers: tuple[int, ...]) -> dict[str, object]:
    rule = getattr(step, "inference_rule", None)
    reference = getattr(rule, "literature_reference", None)
    premises = getattr(step, "premises", ())
    return {
        "index": index,
        "rule_kind": getattr(getattr(step, "rule", None), "name", None),
        "rule_name": getattr(rule, "name", None),
        "source_locator": (getattr(reference, "locator", None) or getattr(reference, "label", None)),
        "citation_numbers": list(numbers),
        "conclusion_type": type(getattr(step, "conclusion", None)).__name__,
        "conclusion": compact(getattr(step, "conclusion", None)),
        "premise_count": len(premises),
        "premises": [compact(getattr(x, "conclusion", None), 350) for x in premises],
    }


def trace_model(model: object) -> dict[str, object]:
    steps = model.steps
    citations = []
    for item in model.citations:
        locator = item.reference.locator or item.reference.label
        citations.append({
            "number": item.number, "locator": locator,
            "step_indices": list(item.step_indices),
            "assertion_ids": list(item.assertion_ids),
            "reference_ids": list(item.reference_ids),
            "statement_bodies": list(item.statement_bodies),
        })
    return {
        "status": getattr(model.status, "name", str(model.status)),
        "root_index": model.root_index,
        "steps": [step_details(step, index, model.step_citation_numbers[index]) for index, step in enumerate(steps)],
        "citations": citations,
        "target_citations": [x for x in citations if x["locator"] in LOCATORS],
    }


def trace(root: Path) -> dict[str, object]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("EXPECTED_DEVELOP_BRANCH")
    sys.path.insert(0, str(root))
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase165_r52_r3_web_adapter import build_partial_web_group_proof_view
    from phase165_r52_partial_proof import ProofSearchStatus

    bridge = build_shared_typed_bridge()
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=TARGET[0], k=TARGET[1], bridge=bridge,
        context_sink=contexts.append,
    )
    context = contexts[-1] if contexts else bridge
    model = build_linked_proof_narrative_model(result, context)
    view = build_partial_web_group_proof_view(
        result, max_depth=2, mode="narrative", narrative_model=model,
    )
    fields_view = {}
    if is_dataclass(view) and not isinstance(view, type):
        for field in fields(view):
            value = getattr(view, field.name)
            fields_view[field.name] = (
                value if isinstance(value, (str, int, bool, type(None))) else compact(value)
            )
    elif hasattr(view, "__dict__"):
        fields_view = {key: compact(value) for key, value in vars(view).items()}
    report = {
        "phase": "175_R4R12R13R8R2", "mode": "READ_ONLY_LIVE_PROOF_TRACE",
        "head": git(root, "rev-parse", "HEAD"),
        "branch": "develop", "target_n": TARGET[0], "target_k": TARGET[1],
        "search_status": getattr(result.status, "name", str(result.status)),
        "search_complete": result.status is ProofSearchStatus.COMPLETE,
        "search_conclusion": compact(result.conclusion),
        "search_context_count": len(contexts),
        "model": trace_model(model), "web_view": fields_view,
        "new_given": 0, "new_mathematical_rules": 0,
        "production_files_modified_by_script": False,
        "full_pytest_executed": False,
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        report = trace(root)
        gate = "PASS_LIVE_TREE_CAPTURED_NOT_FIX_COMPLETE"
        if not report["search_complete"]:
            gate = "FAIL_TARGET_NOT_COMPLETE"
        if not report["model"]["target_citations"]:
            gate = "FAIL_TARGET_REFERENCES_MISSING"
        report["gate"] = gate
    except Exception as exc:
        report = {"gate": "FAIL_LIVE_TRACE", "error": type(exc).__name__ + ": " + str(exc),
                  "traceback": traceback.format_exc()[-10000:]}
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R13R8R2_GATE=" + report["gate"])
    print("PHASE175_R13R8R2_REPORT=" + str(output))
    if "model" in report:
        for c in report["model"]["target_citations"]:
            print("PHASE175_R13R8R2_CITATION=R" + str(c["number"]) + " " + c["locator"])
            print("PHASE175_R13R8R2_BODY_COUNT=" + str(len(c["statement_bodies"])))
            print("PHASE175_R13R8R2_SOURCE_STEP_INDICES=" + str(c["step_indices"]))
    if "error" in report:
        print("PHASE175_R13R8R2_ERROR=" + report["error"])
    return 0 if report["gate"] == "PASS_LIVE_TREE_CAPTURED_NOT_FIX_COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
