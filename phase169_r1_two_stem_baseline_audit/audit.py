"""Phase 169 R1: audit the live 2-stem search and public Web route.

AUDIT_ONLY: This file never patches production code, tests, or documents.
Run from the repository root. All outputs are written into the package folder.
"""
from __future__ import annotations

import json
import sys
import traceback
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import (
    resolve_specialized_goal_citing_id,
)
from proof import ProofRule, ProofStep
from web_group_proof import build_standard_web_group_proof_view


TARGETS = ((2, 2), (3, 2))


def describe_step(step: ProofStep, number: int) -> dict[str, object]:
    return {
        "index": number,
        "rule": step.rule.value,
        "inference_rule_name": (
            step.inference_rule.name
            if step.inference_rule is not None else None
        ),
        "conclusion_type": type(step.conclusion).__name__,
        "conclusion_repr": repr(step.conclusion),
        "premise_count": len(step.premises),
        "premises_repr": [
            repr(item.conclusion) if isinstance(item, ProofStep) else repr(item)
            for item in step.premises
        ],
        "note": step.note,
        "foundational_reference": (
            repr(step.foundational_reference)
            if step.foundational_reference is not None else None
        ),
    }


def audit_publication_order(result, bridge) -> dict[str, object]:
    givens = tuple(
        step for step in result.proven_steps
        if step.rule is ProofRule.GIVEN
    )
    if result.status is not ProofSearchStatus.COMPLETE:
        return {
            "status": "NOT_CERTIFIED_INCOMPLETE",
            "given_count": len(givens),
            "details": [],
        }
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing_id is None:
        return {
            "status": "NO_REGISTERED_CITING_ASSERTION",
            "given_count": len(givens),
            "details": [],
        }
    details = []
    for index, step in enumerate(givens, start=1):
        matched = []
        for assertion in bridge.registry._assertions.values():
            if assertion.content != step.conclusion:
                continue
            try:
                eligible = precedes_citing_assertion(
                    bridge, assertion.assertion_id, citing_id
                )
            except (ValueError, TypeError, KeyError):
                eligible = False
            if eligible:
                matched.append(assertion.assertion_id)
        details.append({
            "given_index": index,
            "conclusion_repr": repr(step.conclusion),
            "eligible_assertion_ids": matched,
            "eligible": bool(matched),
        })
    return {
        "status": (
            "ALL_PRECEDING"
            if all(item["eligible"] for item in details)
            else "UNVERIFIED_GIVEN"
        ),
        "citing_assertion_id": citing_id,
        "given_count": len(givens),
        "details": details,
    }


def audit_group(n: int, k: int, bridge) -> dict[str, object]:
    label = f"pi_{n + k}^{n}"
    data: dict[str, object] = {
        "target": label,
        "n": n,
        "k": k,
        "stage": "starting",
    }
    try:
        candidates = registered_group_goal_candidates(bridge, n=n, k=k)
        data["candidate_count"] = len(candidates)
        data["candidates"] = [repr(candidate) for candidate in candidates]
        contexts = []
        result = search_group_from_registered_goal(
            n=n,
            k=k,
            bridge=bridge,
            context_sink=contexts.append,
        )
        screened = contexts[-1] if contexts else bridge
        data["status"] = result.status.value
        data["structure_status"] = result.structure_status.value
        data["conclusion_repr"] = (
            repr(result.conclusion) if result.conclusion is not None else None
        )
        data["target_repr"] = repr(result.target)
        data["proven_step_count"] = len(result.proven_steps)
        data["rule_counts"] = dict(
            Counter(step.rule.value for step in result.proven_steps)
        )
        data["steps"] = [
            describe_step(step, i)
            for i, step in enumerate(result.proven_steps, start=1)
        ]
        data["open_goal_count"] = len(result.open_goals)
        data["open_goals"] = [
            {"type": type(goal).__name__, "repr": repr(goal)}
            for goal in result.open_goals
        ]
        data["diagnostics"] = list(result.diagnostics)
        data["screened_context_available"] = bool(contexts)
        data["publication_order"] = audit_publication_order(result, screened)

        web = build_standard_web_group_proof_view(
            n=n, k=k, mode="narrative", citation_source="model"
        )
        data["web_key"] = web.key
        data["web_partial_result"] = web.partial_result
        data["web_conclusion_latex"] = web.conclusion_latex
        data["web_step_count"] = len(web.steps)
        data["web_rendered_line_count"] = len(web.rendered_lines)
        data["web_rendered_lines"] = [
            {
                "kind": line.kind,
                "indent_level": line.indent_level,
                "prefix": line.prefix,
                "statement_latex": line.statement_latex,
                "suffix": line.suffix,
                "segments": [
                    {"kind": segment.kind, "value": segment.value}
                    for segment in line.segments
                ],
            }
            for line in web.rendered_lines
        ]
        data["search_web_consistent"] = (
            web.partial_result
            == (result.status is not ProofSearchStatus.COMPLETE)
        )
        data["stage"] = "success"
        if not data["search_web_consistent"]:
            data["stage"] = "mismatch"
        return data
    except Exception as error:
        data["stage"] = "error"
        data["error_type"] = type(error).__name__
        data["error"] = str(error)
        data["traceback"] = traceback.format_exc()
        return data


def render_report(results: list[dict[str, object]]) -> str:
    lines = [
        "Phase 169 R1 — 2-stem live search and Web baseline",
        "AUDIT_ONLY: no production application/test/document changes",
        "",
    ]
    for result in results:
        lines.extend([
            f"TARGET {result['target']}",
            f"STAGE {result['stage']}",
            f"CANDIDATES {result.get('candidate_count', 'unavailable')}",
            f"SEARCH_STATUS {result.get('status', 'unavailable')}",
            f"PROVEN_STEPS {result.get('proven_step_count', 'unavailable')}",
            f"RULE_COUNTS {result.get('rule_counts', {})}",
            f"OPEN_GOALS {result.get('open_goal_count', 'unavailable')}",
            f"WEB_KEY {result.get('web_key', 'unavailable')}",
            f"WEB_PARTIAL {result.get('web_partial_result', 'unavailable')}",
            f"SEARCH_WEB_CONSISTENT {result.get('search_web_consistent', 'unavailable')}",
            f"PUBLICATION {result.get('publication_order', {}).get('status', 'unavailable')}",
            "",
            "CANDIDATE GOALS",
        ])
        lines.extend(result.get("candidates", []))
        lines.append("")
        lines.append("PROVEN PROOFSTEPS")
        for step in result.get("steps", []):
            lines.extend([
                f"STEP {step['index']} RULE={step['rule']} INFERENCE={step['inference_rule_name']}",
                f"  CONCLUSION: {step['conclusion_repr']}",
                f"  PREMISES: {step['premise_count']}",
            ])
            lines.extend(
                f"    {premise}"
                for premise in step["premises_repr"]
            )
        lines.append("")
        lines.append("OPEN GOALS")
        for goal in result.get("open_goals", []):
            lines.append(f"  {goal['type']}: {goal['repr']}")
        lines.append("")
        lines.append("DIAGNOSTICS")
        lines.extend(f"  {diagnostic}" for diagnostic in result.get("diagnostics", []))
        if result.get("error"):
            lines.append(f"ERROR {result['error_type']}: {result['error']}")
            lines.append(result.get("traceback", ""))
        lines.extend(["", "-" * 72, ""])
    return "\n".join(lines)


def main() -> int:
    package_dir = Path(__file__).resolve().parent
    output = package_dir / "output"
    output.mkdir(exist_ok=True)
    try:
        bridge = build_shared_typed_bridge()
    except Exception:
        (output / "bridge_error.txt").write_text(
            traceback.format_exc(), encoding="utf-8"
        )
        print("BRIDGE_BUILD_ERROR: see output/bridge_error.txt", flush=True)
        return 2

    results = [audit_group(n, k, bridge) for n, k in TARGETS]
    (output / "two_stem_baseline.json").write_text(
        json.dumps(
            {"phase": 169, "audit": "R1", "results": results},
            ensure_ascii=False, indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    (output / "two_stem_baseline.txt").write_text(
        render_report(results), encoding="utf-8"
    )
    for result in results:
        print(
            f"{result['target']}: stage={result['stage']}"
            f" status={result.get('status', 'unavailable')}"
            f" steps={result.get('proven_step_count', 'unavailable')}"
            f" open={result.get('open_goal_count', 'unavailable')}"
            f" web={result.get('web_key', 'unavailable')}",
            flush=True,
        )
        if result.get("error"):
            print(f"  ERROR: {result['error']}", flush=True)
    print("REPORT:", output / "two_stem_baseline.txt", flush=True)
    print("JSON:", output / "two_stem_baseline.json", flush=True)
    return 1 if any(
        result["stage"] != "success" for result in results
    ) else 0


if __name__ == "__main__":
    sys.exit(main())
