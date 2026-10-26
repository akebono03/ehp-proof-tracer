"""Read-only verification of the R4G source-linked Reference in public narrative."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r27_r5_literature import verify_prop44_hopf_fibration_source
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent


def main() -> None:
    verify_prop44_hopf_fibration_source()
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=4, k=2, bridge=bridge, context_sink=contexts.append)
    if result.status is not ProofSearchStatus.COMPLETE or len(result.proven_steps) != 18 or result.open_goals:
        raise RuntimeError("pi6_4 original completion was not retained")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None or len(contexts) != 1:
        raise RuntimeError("screened source context missing")
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    reference, body = markdown.split("\n証明\n", 1)
    if (len(model.citations) != 5
            or "Proposition 4.4 直前の記述" not in reference
            or r"$h:S^7\to S^4$" not in body
            or set(int(n) for n in re.findall(r"\[R(\d+)\]", body)) != set(range(1, 6))):
        raise RuntimeError("R4G Reference or body citation contract failed")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                          check=True, capture_output=True).stdout.strip()
    report = {
        "phase": "169 R4G",
        "head": head,
        "source_verified": True,
        "source_locator": "Toda Chapter IV, immediately before Proposition 4.4",
        "printed_original_cites": "Steenrod1951",
        "reference_locator": "Proposition 4.4",
        "reference_body_includes_prior_hopf_fibration": True,
        "separate_new_given_created": False,
        "proof_status": result.status.value,
        "proof_steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "citation_count": len(model.citations),
        "all_citations_in_body": True,
        "full_pytest_run": False,
    }
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (output / "web_narrative.md").write_text(markdown, encoding="utf-8")
    (output / "audit.md").write_text(
        "# Phase 169 R4G — Hopf fibration の出典を Reference に表示\n\n"
        "- 認証済み原文: Toda_04_2.tex の Proposition 4.4 直前（Steenrod1951 を引用）\n"
        "- 既存 [R2] に前段落を明示: True\n"
        "- 別の未認証 GIVEN を追加: False\n"
        "- 既存の完成証明: 18ステップ・未解決0\n"
        "- Reference: 5件を維持\n"
        "- 全体 pytest: 未実施\n", encoding="utf-8")
    print("R4G_GIT_HEAD=" + head)
    print("R4G_PI64_STATUS=" + result.status.value)
    print("R4G_PI64_STEPS=" + str(len(result.proven_steps)))
    print("R4G_PI64_OPEN_GOALS=" + str(len(result.open_goals)))
    print("R4G_REF_PROP44_PRELUDE_VERIFIED=True")
    print("R4G_REFERENCES=" + str(len(model.citations)))
    print("R4G_ALL_TAGS_IN_BODY=True")
    print("R4G_FULL_PYTEST_RUN=False")
    print("R4G_REPORT=" + str(output / "audit.md"))
    print("R4G_WEB_NARRATIVE=" + str(output / "web_narrative.md"))

if __name__ == "__main__":
    main()
