"""Compare verified root proof and displayed prose for four real groups."""
from __future__ import annotations

import json
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from proof import Relation

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
CASES = ((13, 9), (15, 8), (15, 9), (30, 9))


def inspect_case(bridge: object, n: int, k: int) -> dict:
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        raise RuntimeError(f"R10EC incomplete proof: pi_{n+k}^{n}")
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    derived = citing_id is None
    if derived and not (isinstance(result.conclusion, Relation)
                        and result.conclusion.lhs == result.target):
        raise RuntimeError("R10EC uncited root lacks typed group conclusion")
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[-1], citing_assertion_id=citing_id,
        derived_target_without_citing_id=derived,
    )
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    display = project_verified_direct_sum_transport(model, order)
    if display is None:
        raise RuntimeError(f"R10EC direct-sum projection unavailable: pi_{n+k}^{n}")
    body = render_model_backed_narrative_markdown(result, model)
    if display.statement not in body:
        raise RuntimeError(f"R10EC verified compression not rendered: pi_{n+k}^{n}")
    metrics = count_rendered_image_equations(body)
    if metrics["extra_duplicate_occurrences"]:
        raise RuntimeError(f"R10EC duplicate image prose remains: pi_{n+k}^{n}")
    if any(f"**[R{item.number}] " not in body for item in model.citations):
        raise RuntimeError("R10EC registered Reference disappeared")
    if n == 30 and k == 9 and (
        r"E^{19}(\nu_{11}^{3})=\nu_{30}^{3}" not in body
        or r"E^{19}(\mu_{11})=\mu_{30}" not in body
        or len(body) >= 4167
    ):
        raise RuntimeError("R10EC pi39 notation or compression regression")
    OUTPUT.mkdir(exist_ok=True)
    filename = f"pi_{n+k}_{n}.md"
    (OUTPUT / filename).write_text(body, encoding="utf-8")
    return {
        "group": f"pi_{n+k}^{n}", "status": result.status.value,
        "trust": "PASS", "inference_steps": inferred, "given_steps": given,
        "suppressed_display_steps": len(display.hidden_indices),
        "displayed_formulae": display.statement,
        "duplicate_image_prose": metrics["extra_duplicate_occurrences"],
        "rendered_characters": len(body), "reference_count": len(model.citations),
        "proof_step_count": len(result.proven_steps), "rendered_file": filename,
    }


def main() -> None:
    bridge = build_shared_typed_bridge()
    cases = [inspect_case(bridge, n, k) for n, k in CASES]
    report = {
        "phase": "169 R10EC", "cases": cases,
        "proof_rules_changed": False, "full_pytest_run": False,
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    for case in cases:
        key = "R10EC_" + case["group"]
        print(key + "_STATUS=" + case["status"])
        print(key + "_TRUST=" + case["trust"])
        print(key + "_DUPLICATES=" + str(case["duplicate_image_prose"]))
        print(key + "_CHARACTERS=" + str(case["rendered_characters"]))
        print(key + "_HIDDEN_DISPLAY_ONLY=" + str(case["suppressed_display_steps"]))
    print("R10EC_AUDIT_JSON=" + str(OUTPUT / "audit.json"))
    print("R10EC_PROOF_TREE_OR_RULES_CHANGED=False")
    print("R10EC_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
