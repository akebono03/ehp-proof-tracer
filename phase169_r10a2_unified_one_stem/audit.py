"""Check R10A2 final proof/Reference/1-stem Web display without full pytest."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10a2_unified_one_stem.one_stem_projection import (
    project_verified_one_stem_notation_chain,
)
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def main() -> None:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          text=True, check=True, capture_output=True).stdout.strip()
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=8, k=1, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise RuntimeError("pi_9^8 not complete or missing citation-screened context")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("1-stem goal lacks positioned literature assertion")
    verified = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    display = project_verified_one_stem_notation_chain(
        model, tuple(range(len(model.steps))),
    )
    if display is None or display.exponent != 5 or len(display.hidden_indices) < 2:
        raise RuntimeError("1-stem verified display is incomplete")
    narrative = render_model_backed_narrative_markdown(result, model)
    if (narrative.count(r"$E^{5}(\eta_{3})=\eta_{8}$") != 1
            or r"E(\eta_{7})=\eta_{8}" in narrative
            or r"\mathbb{Z}/2\{E^{5}" in narrative
            or not narrative.rstrip().endswith("□")):
        raise RuntimeError("1-stem transport was not compressed to one named equation")
    view = build_standard_web_group_proof_view(8, 1, mode="narrative")
    if (view.key != "generic-complete-proof" or view.partial_result
            or len(view.steps) != len(result.proven_steps)):
        raise RuntimeError("canonical 1-stem Web lost a completed proof")
    report = {
        "phase": "169-R10A2",
        "head": head,
        "status": result.status.value,
        "proof_steps": len(model.steps),
        "reference_count": len(model.citations),
        "root_index": model.root_index,
        "compressed_exponent": display.exponent,
        "suppressed_prose_step_indices": list(display.hidden_indices),
        "source_citation_numbers": list(display.citation_numbers),
        "one_stem_generator_identity_equation_count": 1,
        "verified_proof_counts": list(verified),
        "web_key": view.key,
        "full_pytest_run": False,
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUTPUT / "pi9_8_narrative.md").write_text(narrative, encoding="utf-8")
    print("R10A2_PI9_8_STATUS=" + result.status.value)
    print("R10A2_STEPS=" + str(len(model.steps)))
    print("R10A2_REFERENCES=" + str(len(model.citations)))
    print("R10A2_E5_ETA_NORMALIZATION=1")
    print("R10A2_HIDDEN_PROSE_STEPS=" + str(len(display.hidden_indices)))
    print("R10A2_PROOF_TREE_VERIFIED=True")
    print("R10A2_WEB_KEY=" + view.key)
    print("R10A2_REPORT=" + str(OUTPUT / "audit.json"))
    print("R10A2_NARRATIVE=" + str(OUTPUT / "pi9_8_narrative.md"))
    print("R10A2_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
