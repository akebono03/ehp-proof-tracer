"""R10EJ focused live regression: verified cyclic display compression only."""
from __future__ import annotations

import argparse
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
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from proof import Relation

CASES = (
    (22, 6, 14, "cyclic_nu_square"),
    (22, 10, 10, "cyclic_eta_mu"),
    (8, 2, 4, "existing_eta_square"),
    (15, 8, None, "direct_sum_control"),
    (4, 1, None, "one_stem_control"),
)


def inspect_case(bridge, n: int, k: int, exponent: int | None, label: str) -> tuple[dict, str]:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise AssertionError(f"{label}: previously completed proof became incomplete")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    derived = citing is None
    if derived and not (isinstance(result.conclusion, Relation)
                        and result.conclusion.lhs == result.target):
        raise AssertionError(f"{label}: unpositioned result lacks typed conclusion")
    inferred, given = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=derived,
    )
    previous_steps = result.proven_steps
    model = build_linked_proof_narrative_model(result, contexts[0])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    display = project_verified_stable_image_chain(model, order)
    narrative = render_model_backed_narrative_markdown(result, model)
    if result.proven_steps != previous_steps or model.steps != previous_steps:
        raise AssertionError(f"{label}: proof steps changed during presentation")
    if any(f"**[R{citation.number}] " not in narrative
           for citation in model.citations):
        raise AssertionError(f"{label}: reference lost during presentation")
    metrics = count_rendered_image_equations(narrative)
    if exponent is not None:
        if display is None or display.exponent != exponent:
            raise AssertionError(f"{label}: certified E^{exponent} projection unavailable")
        expected_formula = (
            f"$E^{{{exponent}}}({display.source_tex})={display.target_tex}$"
        )
        if narrative.count(expected_formula) != 1:
            raise AssertionError(f"{label}: aggregate source-target formula missing or duplicated")
        if metrics["total_occurrences"] != 0:
            raise AssertionError(f"{label}: residual one-step image display remains")
        if len(display.hidden_indices) <= exponent:
            raise AssertionError(f"{label}: nested typed inference steps were not suppressed")
    if label == "direct_sum_control" and display is not None:
        raise AssertionError("direct sum must not use cyclic compression")
    record = {
        "goal": f"pi_{n+k}^{n}",
        "label": label,
        "status": result.status.value,
        "trust": "PASS",
        "inferred_steps": inferred,
        "given_steps": given,
        "proof_steps": len(previous_steps),
        "reference_count": len(model.citations),
        "cyclic_projection": display is not None,
        "compressed_exponent": display.exponent if display is not None else None,
        "hidden_display_indices": len(display.hidden_indices) if display is not None else 0,
        "one_step_equations": metrics["total_occurrences"],
        "duplicate_equations": metrics["extra_duplicate_occurrences"],
        "rendered_characters": len(narrative),
    }
    return record, narrative


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    bridge = build_shared_typed_bridge()
    cases = []
    for n, k, exponent, label in CASES:
        record, narrative = inspect_case(bridge, n, k, exponent, label)
        (args.output / f"pi_{n+k}_{n}.md").write_text(narrative, encoding="utf-8")
        cases.append(record)
        prefix = f"R10EJ_pi_{n+k}^{n}"
        print(f"{prefix}_STATUS={record['status']}", flush=True)
        print(f"{prefix}_TRUST={record['trust']}", flush=True)
        print(f"{prefix}_HIDDEN_DISPLAY_ONLY={record['hidden_display_indices']}", flush=True)
        print(f"{prefix}_ONE_STEP_E={record['one_step_equations']}", flush=True)
        print(f"{prefix}_DUPLICATES={record['duplicate_equations']}", flush=True)
    report = {"phase": "169 R10EJ", "scope": "PRESENTATION_ONLY",
              "cases": cases, "production_rule_changes": False,
              "proof_tree_changes": False, "full_pytest_run": False, "status": "PASS"}
    (args.output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("R10EJ_AUDIT_STATUS=PASS", flush=True)
    print("R10EJ_FULL_PYTEST_RUN=False", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
