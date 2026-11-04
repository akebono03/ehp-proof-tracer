"""Read-only public proof projection diagnostic for Phase 173 R15R17.

No proof data, repository files, citations, or statuses are modified.
"""
from __future__ import annotations

import json

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import verified_tree_postorder
from web_group_proof import build_standard_web_group_proof_view
from web_group_proof_common import _group_proof_statement_latex


def _report_case(n: int, k: int) -> dict[str, object]:
    """Describe real search and Web paths without promoting any proof state."""
    result = search_group_from_registered_goal(n=n, k=k)
    view = build_standard_web_group_proof_view(
        n=n,
        k=k,
        mode="narrative",
        citation_source="model",
    )
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    text = "\n".join(
        " ".join(segment.value for segment in line.segments)
        for line in view.rendered_lines
    )
    structure = result.abstract_structure
    evidence: dict[str, object] | None = None
    if structure is not None:
        root = structure.proof_step
        latex, fallback = _group_proof_statement_latex(root.conclusion)
        evidence = {
            "verified_tree_steps": len(verified_tree_postorder(root)),
            "abstract_root_rule": root.rule.value,
            "abstract_root_type": type(root.conclusion).__name__,
            "abstract_root_formula_supported": latex is not None and fallback is None,
            "abstract_root_in_named_proven_steps": any(
                step is root for step in result.proven_steps
            ),
        }
    return {
        "n": n,
        "k": k,
        "status": result.status.value,
        "named_complete": result.status is ProofSearchStatus.COMPLETE,
        "named_proven_steps": len(result.proven_steps),
        "named_open_goals": len(result.open_goals),
        "abstract_certificate_present": structure is not None,
        "abstract_evidence": evidence,
        "view_key": view.key,
        "view_partial": view.partial_result,
        "web_headings": headings,
        "reference_heading_count": headings.count("使用する結果"),
        "separate_abstract_reference_heading_count": headings.count(
            "検証済み証明木の Reference"
        ),
        "separate_abstract_result_heading_count": headings.count(
            "証明済みの抽象群構造"
        ),
        "no_proofstep_reference_message": "参照情報を持つ ProofStep はありません" in text,
        "no_japanese_punctuation": "、" not in text and "。" not in text,
    }


def main() -> None:
    """Print three scoped observations, never a repository-wide test report."""
    for n, k in ((4, 8), (5, 3), (4, 4)):
        report = _report_case(n, k)
        print("R15R17_RUNTIME_CASE=" + json.dumps(report, ensure_ascii=False, sort_keys=True))
    print("R15R17_RUNTIME_PROBE=PASS")


if __name__ == "__main__":
    main()
