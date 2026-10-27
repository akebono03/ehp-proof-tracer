"""Verify R10EB rendering against a searched, replayed direct-sum proof."""
from __future__ import annotations

import json
from pathlib import Path

from homotopy_groups import DirectSumGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from proof import Relation
from toda_human_readable_renderer import render_toda_public_group_relation_latex

OUTPUT = Path(__file__).resolve().parent / "output"
CASES = ((13, 9), (15, 8), (15, 9), (30, 9))


def inspect_case(bridge: object, n: int, k: int) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        raise ValueError(f"R10EB complete group/context missing: pi_{n+k}^{n}")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    args = {"citing_assertion_id": citing}
    if citing is None:
        if (not isinstance(result.conclusion, Relation)
                or result.conclusion.lhs != result.target):
            raise ValueError("R10EB uncited root is not typed")
        args["derived_target_without_citing_id"] = True
    inference_count, given_count = verify_proof_tree_for_narrative(
        result, contexts[-1], **args,
    )
    model = build_linked_proof_narrative_model(result, contexts[-1])
    body = render_model_backed_narrative_markdown(result, model)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rendered_file = f"pi_{n+k}_{n}.md"
    (OUTPUT / rendered_file).write_text(body, encoding="utf-8")
    summary = render_toda_public_group_relation_latex(result.conclusion)
    if n == 30 and k == 9 and r"\nu_{30}^{3}" not in summary:
        raise ValueError("R10EB nu-cube public group summary is not compressed")
    return {
        "group": f"pi_{n+k}^{n}",
        "status": result.status.value,
        "trust": "PASS",
        "inference_count": inference_count,
        "given_count": given_count,
        "direct_sum": (isinstance(result.conclusion, Relation)
                       and isinstance(result.conclusion.rhs, DirectSumGroup)),
        "rendered_chars": len(body),
        "duplicate_image_prose": count_rendered_image_equations(body)[
            "extra_duplicate_occurrences"
        ],
        "public_summary": summary,
        "rendered_file": rendered_file,
    }


def main() -> None:
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, n, k) for n, k in CASES]
    report = {"phase": "169 R10EB", "cases": cases,
              "proof_rules_changed": False, "full_pytest_run": False}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for case in cases:
        key = "R10EB_" + case["group"]
        print(key + "_STATUS=" + case["status"])
        print(key + "_TRUST=" + case["trust"])
        print(key + "_DUPLICATE_IMAGE_PROSE=" + str(case["duplicate_image_prose"]))
        print(key + "_CHARACTERS=" + str(case["rendered_chars"]))
        if case["group"] == "pi_39^30":
            print("R10EB_NU_CUBE_IN_GROUP_SUMMARY=PASS")
    print("R10EB_AUDIT_JSON=" + str(OUTPUT / "audit.json"))
    print("R10EB_PROOF_RULES_CHANGED=False")
    print("R10EB_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
