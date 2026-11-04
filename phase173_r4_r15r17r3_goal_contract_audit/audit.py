"""Audit typed open-goal identities and historical public display contracts.

No proof states, proof steps, goals, citations, or production files are modified.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
R2_STATE = ROOT / "phase173_r4_r15r17r2_unsupported_given_clean" / "installed_state.json"
R2_RENDERER = ROOT / "phase168_r3_5_model_renderer.py"
OLD_HEADINGS = ("検証済みの途中経過", "証明済みの抽象群構造", "検証済み証明木の Reference")
HISTORICAL_TESTS = (
    "phase173_r4_r15r9_shared_abstract_renderer/tests/test_projection.py",
    "phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py",
    "phase173_r4_r15r12_reference_correction/tests/test_integration.py",
    "phase173_r4_r15r13_unified_presentation/tests/test_integration.py",
    "phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py",
    "phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py",
    "phase173_r4_r15r15r2_head_guard_fix/tests/test_integration.py",
    "phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py",
    "phase173_r4_r15r16r2_shared_tree_narrative/tests/test_integration.py",
    "phase173_r4_r15r16r3_staged_guard_fix/tests/test_integration.py",
)


def stable_equal(left: object, right: object) -> bool:
    """Match exact typed values. A shared LaTeX string is not proof identity."""
    if type(left) is not type(right):
        return False
    try:
        return bool(left == right)
    except (TypeError, ValueError):
        return False


def reversed_relation(left: object, right: object) -> bool:
    """Report reversed equations, without treating them as the same Goal."""
    if type(left) is not type(right):
        return False
    names = ("lhs", "rhs", "relation_type")
    if not all(hasattr(left, name) and hasattr(right, name) for name in names):
        return False
    return (getattr(left, "relation_type") == getattr(right, "relation_type")
            and getattr(left, "lhs") == getattr(right, "rhs")
            and getattr(left, "rhs") == getattr(right, "lhs"))


def inspect_goal_pairs(goals: tuple[object, ...], display: Callable[[object], str]) -> dict[str, Any]:
    """Only report visually/structurally equal pairs; never coalesce goals."""
    if not isinstance(goals, tuple):
        raise TypeError("open_goals must be a tuple")
    rendered = [display(goal) for goal in goals]
    members = [
        {"index": i + 1,
         "type": f"{type(goal).__module__}.{type(goal).__qualname__}",
         "display": rendered[i],
         "repr": repr(goal)[:700]}
        for i, goal in enumerate(goals)
    ]
    collisions = []
    for i in range(len(goals)):
        for j in range(i + 1, len(goals)):
            same_display = rendered[i] == rendered[j]
            same_typed = stable_equal(goals[i], goals[j])
            reverse = reversed_relation(goals[i], goals[j])
            if same_display or same_typed or reverse:
                collisions.append({
                    "first": i + 1, "second": j + 1,
                    "same_display": same_display,
                    "same_type_and_equal": same_typed,
                    "reversed_relation": reverse,
                    "same_object": goals[i] is goals[j],
                })
    return {"count": len(goals), "goals": members, "paired_observations": collisions}


def historical_contract_locations() -> list[dict[str, Any]]:
    """Locate stale-display candidates in existing tests, do not edit them."""
    output = []
    for relative in HISTORICAL_TESTS:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"historical test missing: {relative}")
        source = path.read_text(encoding="utf-8")
        parsed = ast.parse(source, filename=relative)
        for node in ast.walk(parsed):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.name.startswith("test_"):
                continue
            for assertion in ast.walk(node):
                if not isinstance(assertion, ast.Assert):
                    continue
                snippet = ast.get_source_segment(source, assertion) or ""
                headings = [text for text in OLD_HEADINGS if text in snippet]
                if not headings:
                    continue
                # A negative assertion of absence is already the new contract.
                # Determine this syntactically only for a plain `not in`.
                negative = isinstance(assertion.test, ast.Compare) and any(
                    isinstance(op, ast.NotIn) for op in assertion.test.ops
                )
                classification = (
                    "ALREADY_NEGATIVE_EXPECTATION" if negative else
                    "PUBLIC_VIEW_REVIEW" if any(word in snippet for word in
                                             ("rendered_lines", "headings", "view", "text")) else
                    "HELPER_OR_INDIRECT_REVIEW"
                )
                output.append({
                    "file": relative, "test": node.name, "line": assertion.lineno,
                    "heading": headings, "classification": classification,
                    "assertion": " ".join(snippet.split())[:260],
                })
    return sorted(output, key=lambda item: (item["file"], item["line"]))


def check_r2_installation() -> None:
    """Verify actual R2 bytes before trusting the exported runtime behavior."""
    if not R2_STATE.is_file():
        raise RuntimeError("R15R17-R2 installed_state.json is missing")
    state = json.loads(R2_STATE.read_text(encoding="utf-8"))
    if state.get("target") != "phase168_r3_5_model_renderer.py":
        raise RuntimeError("R2 state targets an unexpected source")
    actual = sha256(R2_RENDERER.read_bytes()).hexdigest()
    if actual != state.get("installed_sha256"):
        raise RuntimeError("R2 renderer differs from the installed audited source")
    print("R15R17R3_R2_SOURCE_INTEGRITY=PASS")


def count_canonical_reference_headings(markdown: str, *, complete: bool) -> int:
    """Count the Reference heading emitted by the unchanged common renderer.

    Completed proof Markdown uses an undecorated heading, whereas incomplete
    proof Markdown uses a second-level Markdown heading. Do not mistake zero
    occurrences of the *wrong* heading for duplicate References.
    """
    if not isinstance(markdown, str):
        raise TypeError("rendered Markdown must be a string")
    if type(complete) is not bool:
        raise TypeError("complete must be a bool")
    expected = "使用する結果" if complete else "## 使用する結果"
    other = "## 使用する結果" if complete else "使用する結果"
    lines = tuple(line.strip() for line in markdown.splitlines())
    if other in lines:
        raise ValueError("unexpected Reference heading for the proof status")
    return lines.count(expected)


def audit_real_cases() -> None:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from web_group_proof_common import _group_proof_statement_latex

    def display(goal: object) -> str:
        if isinstance(goal, str):
            return goal
        latex, fallback = _group_proof_statement_latex(goal)
        return f"${latex}$" if latex is not None and fallback is None else f"<{type(goal).__name__}>"

    for n, k in ((4, 8), (4, 9), (5, 3), (4, 4)):
        typed_goal = exact_prior_database_result(n, k)
        result = search_group_from_registered_goal(n=n, k=k, goal=typed_goal)
        model = build_proof_narrative_model(result)
        markdown = render_model_backed_narrative_markdown(result, model)
        if model.open_goals != result.open_goals or model.status is not result.status:
            raise RuntimeError("model changed the original goal/status state")
        if model.abstract_structure is not result.abstract_structure:
            raise RuntimeError("model lost certificate identity")
        if result.status is ProofSearchStatus.COMPLETE:
            if result.open_goals or model.root_index is None:
                raise RuntimeError("completed proof lost its certified root")
        elif result.conclusion is not None or not result.open_goals:
            raise RuntimeError("incomplete proof has an invalid named-goal status")
        if model.abstract_structure is not None:
            if not any(step is model.abstract_structure.proof_step for step in model.steps):
                raise RuntimeError("certified abstract root missing from unified model")
        if any("## " + old in markdown for old in OLD_HEADINGS):
            raise RuntimeError("obsolete separate public section in canonical renderer")
        reference_sections = count_canonical_reference_headings(
            markdown, complete=result.status is ProofSearchStatus.COMPLETE,
        )
        if reference_sections != 1:
            raise RuntimeError(
                f"canonical Reference heading count is {reference_sections} "
                f"for n={n}, k={k}, status={result.status.value}"
            )
        if result.abstract_structure is not None and "\\cong" not in markdown:
            raise RuntimeError("certified abstract result not displayed")
        pair_report = inspect_goal_pairs(result.open_goals, display)
        output = {
            "n": n, "k": k, "status": result.status.value,
            "proven_steps": len(result.proven_steps),
            "model_steps": len(model.steps),
            "citations": len(model.citations),
            "abstract_certificate": result.abstract_structure is not None,
            "has_named_conclusion": result.conclusion is not None,
            "reference_sections": reference_sections,
            "open_goals": pair_report,
        }
        print("R15R17R3_GOAL_CASE=" + json.dumps(output, ensure_ascii=False, sort_keys=True))
    print("R15R17R3_RUNTIME_AUDIT=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    check_r2_installation()
    contracts = historical_contract_locations()
    for item in contracts:
        print("R15R17R3_CONTRACT=" + json.dumps(item, ensure_ascii=False, sort_keys=True))
    print("R15R17R3_CONTRACT_CANDIDATES=" + str(len(contracts)))
    if args.dry_run:
        print("R15R17R3_DRY_RUN=PASS")
    else:
        audit_real_cases()
        print("R15R17R3_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
