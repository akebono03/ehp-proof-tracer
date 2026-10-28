"""Production search and trust replay; do not modify mathematical sources."""
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
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10eq_r1_universal_stable_definition.definition import (
    is_defined_stable_image,
)
from proof import ProofRule


def inspect(bridge, n: int, k: int, output: Path) -> dict:
    contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    name = f"pi_{n+k}^{n}"
    record = {
        "group": name,
        "status": result.status.value,
        "open_goals": [type(g).__name__ for g in result.open_goals],
        "proof_steps": len(result.proven_steps),
        "definition_images": sum(
            isinstance(p.conclusion, GeneratorImage)
            and p.rule is ProofRule.INFERENCE
            and p.inference_rule is not None
            and p.inference_rule.name == "stable representative definitional suspension"
            and is_defined_stable_image(p.conclusion)
            for p in result.proven_steps
        ),
    }
    if result.status is ProofSearchStatus.COMPLETE:
        if result.open_goals or len(contexts) != 1:
            raise RuntimeError(f"unscreened complete target: {name}")
        citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
        infer_count, given_count = verify_proof_tree_for_narrative(
            result, contexts[0], citing_assertion_id=citing,
            derived_target_without_citing_id=citing is None,
        )
        record.update({"trust": "PASS", "inferences": infer_count, "givens": given_count})
        model = build_linked_proof_narrative_model(result, contexts[0])
        rendered = render_model_backed_narrative_markdown(result, model)
        dest = output / f"pi_{n+k}_{n}.md"
        dest.write_text(rendered, encoding="utf-8")
        record["narrative"] = str(dest)
    else:
        record["trust"] = "NOT_APPLICABLE_INCOMPLETE"
    return record


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        raise SystemExit("Usage: python -m phase169_r10eq_r1_universal_stable_definition.audit OUTPUT")
    output = Path(args[0]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    bridge = build_shared_typed_bridge()
    cases = [inspect(bridge, *pair, output) for pair in ((30, 11), (30, 14))]
    report = {"phase": "169 R10EQ-R1", "cases": cases,
              "mode": "FOCUSED_DEFINITION_INFERENCE", "full_pytest_run": False}
    target = output / "audit.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in cases:
        tag = "R10EQ_" + item["group"]
        print(tag + "_STATUS=" + item["status"], flush=True)
        print(tag + "_OPEN_GOALS=" + repr(item["open_goals"]), flush=True)
        print(tag + "_DEFINITION_IMAGES=" + str(item["definition_images"]), flush=True)
        print(tag + "_TRUST=" + item["trust"], flush=True)
    print("R10EQ_AUDIT=" + str(target), flush=True)
    if any(item["status"] != "complete" or item["trust"] != "PASS" for item in cases):
        raise RuntimeError("expected both representative stable proof cases COMPLETE/TRUST PASS")
    print("R10EQ_LIVE_AUDIT=PASS", flush=True)


if __name__ == "__main__":
    main()
