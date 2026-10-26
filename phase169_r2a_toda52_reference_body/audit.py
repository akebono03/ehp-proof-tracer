"""Audit the real pi_4^2 citation binding before and after the local change."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

BODY = (
    r"$i\ge 3$ に対し, "
    r"$\eta_2\circ(-):\pi_i^3\xrightarrow{\cong}\pi_i^2$ は同型."
)


def audit(mode: str) -> dict:
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r27_r5_literature import Toda52UniversalStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=2, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or not contexts:
        raise AssertionError(f"pi_4^2 proof is not complete: {result.status}")
    model = build_linked_proof_narrative_model(result, contexts[-1])
    if len(model.steps) != 3:
        raise AssertionError(f"pi_4^2 step count changed: {len(model.steps)}")
    matches = tuple(item for item in model.citations if item.reference.locator == "(5.2)")
    if len(matches) != 1:
        raise AssertionError("Expected exactly one live (5.2) citation")
    citation = matches[0]
    if not citation.assertion_ids or not citation.reference_ids:
        raise AssertionError("(5.2) has no live registered assertion source; patch not justified")
    if not any(
        step.rule is ProofRule.GIVEN
        and isinstance(step.conclusion, Toda52UniversalStatement)
        and index in citation.step_indices
        for index, step in enumerate(model.steps)
    ):
        raise AssertionError("(5.2) has no actual typed GIVEN in the proof tree")

    markdown = render_model_backed_narrative_markdown(result, model)
    present = BODY in citation.statement_bodies and BODY in markdown
    if mode == "after" and not present:
        raise AssertionError("(5.2) statement body missing after patch")
    record = {
        "mode": mode,
        "target": "pi_4^2",
        "status": result.status.value,
        "proofsteps": len(model.steps),
        "given": sum(step.rule is ProofRule.GIVEN for step in model.steps),
        "citation_locator": citation.reference.locator,
        "citation_assertion_ids": list(citation.assertion_ids),
        "citation_reference_ids": list(citation.reference_ids),
        "citation_step_indices": list(citation.step_indices),
        "citation_bodies": list(citation.statement_bodies),
        "reference_body_rendered": present,
    }
    path = PACKAGE / "output" / ("pi42_before.json" if mode == "before" else "pi42_after.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PI42_STATUS:", record["status"])
    print("PI42_STEPS:", record["proofsteps"])
    print("PI42_GIVEN:", record["given"])
    print("TODA52_ASSERTION_IDS:", record["citation_assertion_ids"])
    print("TODA52_REFERENCE_BODIES:", record["citation_bodies"])
    print("TODA52_BODY_RENDERED:", present)
    print("REPORT:", path)
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("before", "after"))
    args = parser.parse_args()
    audit(args.mode)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"R2A AUDIT ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
