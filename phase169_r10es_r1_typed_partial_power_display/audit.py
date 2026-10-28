"""R10ES post-patch live search, provenance and renderer validation."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from web_group_proof import build_standard_web_group_proof_view


CASES = ((30, 26), (30, 14), (30, 16), (30, 9))
EXPECTED = (
    r"\nu_{28}^{2}\bar{\kappa}_{34}",
    r"\nu_{30}^{2}\bar{\kappa}_{36}",
    r"E^{2}(\nu_{28}^{2}\bar{\kappa}_{34})=\nu_{30}^{2}\bar{\kappa}_{36}",
)


def inspect_case(bridge: object, n: int, k: int, output: Path) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
            or len(contexts) != 1):
        raise AssertionError(f"incomplete group pi_{n+k}^{n}")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferences, givens = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    before = tuple(id(step) for step in model.steps), model.step_citation_numbers
    markdown = render_model_backed_narrative_markdown(result, model)
    after = tuple(id(step) for step in model.steps), model.step_citation_numbers
    if before != after:
        raise AssertionError("renderer modified Proof Tree or citations")
    if k == 26:
        if any(markdown.count(item) != 1 for item in EXPECTED[2:]):
            raise AssertionError("mixed typed ν power absent or duplicated")
        if r"\nu_{30}\nu_{33}\bar{\kappa}_{36}" in markdown:
            raise AssertionError("uncompressed ν composition remains")
        if not all(item in markdown for item in EXPECTED[:2]):
            raise AssertionError("source or target mixed generator missing")
    if not markdown.rstrip().endswith("□"):
        raise AssertionError("completed proof lost termination")
    view = build_standard_web_group_proof_view(n, k, mode="narrative")
    if view.key != "generic-complete-proof" or view.partial_result:
        raise AssertionError("web proof regressed")
    filename = f"pi_{n+k}_{n}.md"
    (output / filename).write_text(markdown, encoding="utf-8")
    print(f"R10ES_pi_{n+k}^{n}_STATUS=complete", flush=True)
    print(f"R10ES_pi_{n+k}^{n}_TRUST=PASS", flush=True)
    return {
        "group": f"pi_{n+k}^{n}",
        "status": "complete",
        "trust": "PASS",
        "inference_steps": inferences,
        "given_steps": givens,
        "references": len(model.citations),
        "proof_steps_unchanged": True,
        "source_and_target_compressed": k == 26,
        "narrative_file": filename,
    }


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10es_r1_typed_partial_power_display.audit OUTPUT_DIR")
    output = Path(sys.argv[1]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    records = [inspect_case(bridge, n, k, output) for n, k in CASES]
    path = output / "audit.json"
    path.write_text(json.dumps({
        "phase": "169 R10ES-R1",
        "mode": "FOCUSED_PRESENTATION_ONLY",
        "cases": records,
        "proof_rules_modified": False,
        "full_pytest_run": False,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("R10ES_REPORT=" + str(path), flush=True)
    print("R10ES_LIVE_AUDIT=PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
