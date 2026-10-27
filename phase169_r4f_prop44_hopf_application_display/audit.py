"""Read the real completed proof and projected web narrative after R4F."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from web_group_proof import build_standard_web_group_proof_view

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    bridge = build_shared_typed_bridge()
    contexts = []
    proof = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if (proof.status is not ProofSearchStatus.COMPLETE
            or len(proof.proven_steps) != 18 or proof.open_goals
            or len(contexts) != 1):
        raise RuntimeError("R4F pi6_4 proof is not complete with 18 steps")
    citing = resolve_specialized_goal_citing_id(bridge, proof.conclusion)
    if citing is None:
        raise RuntimeError("R4F group goal is not linked to literature position")
    verify_proof_tree_for_narrative(
        proof, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(proof, contexts[0])
    narrative = render_model_backed_narrative_markdown(proof, model)
    if "\n証明\n" not in narrative:
        raise RuntimeError("R4F no proof section")
    reference, body = narrative.split("\n証明\n", 1)
    citations = {c.number for c in model.citations}
    used = {int(v) for v in re.findall(r"\[R(\d+)\]", body)}
    if citations != used or len(citations) != 5:
        raise RuntimeError("R4F Reference and body citations are not aligned")
    prop44 = [c.number for c in model.citations
              if (c.reference.locator or c.reference.label) == "Proposition 4.4"]
    if len(prop44) != 1:
        raise RuntimeError("R4F no unique Prop4.4 citation")
    required = (
        "Hopf fibration", r"$\alpha=h\in\pi_7^4$",
        r"$H(\alpha)=\pm\iota_7$",
        f"[R{prop44[0]}]を $(n,i)=(4,6)$ に適用できる",
        f"[R{prop44[0]}]より, " + r"$E: \pi_{5}^{3}\to \pi_{6}^{4}$ は単射.",
    )
    if not all(item in body for item in required):
        raise RuntimeError("R4F missing cited and dimension-bound Hopf application")
    if r"\nu_4" in body or "Lemma 5.4" in body:
        raise RuntimeError("R4F incorrectly uses post-target Lemma 5.4")
    view = build_standard_web_group_proof_view(4, 2, mode="narrative")
    if view.key != "generic-complete-proof" or view.partial_result:
        raise RuntimeError("R4F Web proof completeness regressed")
    head = subprocess.run(("git", "rev-parse", "HEAD"), cwd=ROOT,
                          check=True, capture_output=True, text=True).stdout.strip()
    report = {
        "phase": "169-R4F", "head": head,
        "pi64_status": proof.status.value,
        "pi64_steps": len(proof.proven_steps),
        "pi64_open_goals": len(proof.open_goals),
        "prop44_hopf_application_displayed": True,
        "alpha": "h (n=4 Hopf fibration, not post-target Lemma5.4)",
        "prop44_citation": prop44[0],
        "references": len(citations),
        "all_reference_tags_in_body": True,
        "narrative_ends_with_proof_box": body.rstrip().endswith("□"),
        "web_key": view.key,
        "full_pytest_run": False,
    }
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (output / "web_narrative.md").write_text(narrative, encoding="utf-8")
    (output / "audit.md").write_text(
        "# Phase 169 R4F — Proposition 4.4 の適用条件表示\n\n"
        "- π₆⁴: complete (18 steps, 未解決 0)\n"
        "- n=4 Hopf fibration h による条件確認: True\n"
        "- α=h, (n,i)=(4,6) の適用表示: True\n"
        "- 後続 Lemma 5.4 の使用: False\n"
        "- Reference 5件、本文タグ全対応: True\n"
        "- Proof Tree trust boundary: PASS\n"
        "- 全体 pytest: 未実施\n", encoding="utf-8",
    )
    for name, value in report.items():
        if name in ("head", "pi64_status", "pi64_steps", "pi64_open_goals",
                    "prop44_hopf_application_displayed", "all_reference_tags_in_body", "web_key"):
            print("R4F_" + name.upper() + "=" + str(value))
    print("R4F_FULL_PYTEST_RUN=False")
    print("R4F_MARKDOWN=" + str(output / "web_narrative.md"))
    print("R4F_REPORT=" + str(output / "audit.md"))


if __name__ == "__main__":
    main()
