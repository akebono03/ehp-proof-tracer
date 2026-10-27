"""After-test evidence report; report does not replace pytest or trust replay."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def main() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=8, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or len(contexts) != 1:
        raise RuntimeError("pi_10^8 must remain complete")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("unpositioned target")
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    image_equation = r"$E^{4}(\eta_{4}^{2})=\eta_{8}^{2}$"
    iso_prefix = "$E^{4}:"
    if markdown.count(image_equation) != 1:
        raise RuntimeError("the 4-fold generator image must appear exactly once")
    if markdown.count(iso_prefix) != 1:
        raise RuntimeError("the cited 4-fold isomorphism must remain visible")
    view = build_standard_web_group_proof_view(8, 2, mode="narrative")
    if view.key != "generic-complete-proof" or view.partial_result:
        raise RuntimeError("standard Web result changed")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout.strip()
    report = {
        "phase": "169-R10A", "head": head,
        "status": result.status.value,
        "proof_steps": len(result.proven_steps),
        "model_steps": len(model.steps),
        "open_goals": len(result.open_goals),
        "compressed_image_equations": markdown.count(image_equation),
        "stable_isomorphism_occurrences": markdown.count(iso_prefix),
        "reference_count": len(model.citations),
        "proof_tree_verified": True,
        "web_key": view.key,
        "production_files_changed": ["phase168_r3_5_model_renderer.py"],
        "full_pytest_run": False,
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUTPUT / "pi10_8_narrative.md").write_text(markdown, encoding="utf-8")
    print("R10A_PI10_8_STATUS=" + result.status.value)
    print("R10A_PROOF_STEPS=" + str(len(result.proven_steps)))
    print("R10A_IMAGE_EQUATIONS=" + str(report["compressed_image_equations"]))
    print("R10A_REFERENCES=" + str(len(model.citations)))
    print("R10A_PROOF_TREE_VERIFIED=True")
    print("R10A_WEB_KEY=" + view.key)
    print("R10A_AUDIT=" + str(OUTPUT / "audit.json"))
    print("R10A_NARRATIVE=" + str(OUTPUT / "pi10_8_narrative.md"))


if __name__ == "__main__":
    main()
