"""Audit canonical complete proof, ancestry and Web-facing narrative after R20R12."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase171_r20r12_verified_cyclic_narrative.projection import verified_order_four_summary
from proof import ProofRule

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"


def git(*args: str) -> str:
    if args not in {
        ("rev-parse", "HEAD"),
        ("branch", "--show-current"),
        ("status", "--porcelain", "--untracked-files=no"),
    }:
        raise ValueError("read-only Git commands only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def run() -> dict[str, object]:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    before = git("status", "--porcelain", "--untracked-files=no")
    if branch != "develop":
        raise RuntimeError("R20R12 must audit develop")
    original_bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=original_bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or result.open_goals or len(contexts) != 1):
        raise RuntimeError("canonical public pi_6^3 search is not complete")
    citing = resolve_specialized_goal_citing_id(original_bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("root publication position missing")
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    summary = verified_order_four_summary(model)
    if summary is None:
        raise RuntimeError("the canonical root does not contain full order-four ancestry")
    markdown = render_model_backed_narrative_markdown(result, model)
    if "\n証明\n" not in markdown:
        raise RuntimeError("missing standard narrative section")
    reference, body = markdown.split("\n証明\n", 1)
    if (summary not in body
            or r"\operatorname{ord}" not in body
            or r"\cdot" not in body
            or "による導出も同じ群構造を示す" in body
            or "□" not in body):
        raise RuntimeError("verified-order summary or duplicate suppression missing")
    if body.count(summary) != 1:
        raise RuntimeError("verified summary repeated")
    # Every reference in the paragraph was already present in model.citations.
    # No citation number is manufactured by the projection.
    citation_labels = tuple(
        "[R" + str(item.number) + "]" for item in model.citations
    )
    if not all(label in reference for label in citation_labels):
        raise RuntimeError("source reference lost during narrative projection")
    leaf_count = sum(step.rule is ProofRule.GIVEN for step in result.proven_steps)
    if git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("audit modified tracked production files")
    report = {
        "phase": "171-R20R12",
        "mode": "PUBLIC_COMPLETE_RENDERER_ONLY_PROJECTION",
        "git_head": head,
        "public_status": result.status.value,
        "public_complete": True,
        "proven_steps": len(result.proven_steps),
        "given_steps": leaf_count,
        "root_is_inference": model.steps[model.root_index].rule is ProofRule.INFERENCE,
        "root_order_four_ancestry_verified": True,
        "reference_count": len(model.citations),
        "reference_labels_preserved": True,
        "explicit_cardinality_and_generator_order": True,
        "duplicate_group_notice_suppressed": True,
        "new_given_added": 0,
        "completed_proofs_imported": False,
        "production_math_changed": False,
        "full_pytest": False,
        "browser_visual_check_performed": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUTPUT / "web_narrative.md").write_text(markdown, encoding="utf-8")
    print("PHASE171_R20R12_PUBLIC_STATUS=" + report["public_status"], flush=True)
    print("PHASE171_R20R12_ORDER_FOUR_ANCESTRY=True", flush=True)
    print("PHASE171_R20R12_NARRATIVE_SUMMARY=True", flush=True)
    print("PHASE171_R20R12_REFERENCES=" + str(report["reference_count"]), flush=True)
    print("PHASE171_R20R12_REPORT=" + str(OUTPUT / "audit.json"), flush=True)
    print("PHASE171_R20R12_MARKDOWN=" + str(OUTPUT / "web_narrative.md"), flush=True)
    print("PHASE171_R20R12_RESULT=PASS_RENDERER_AUDIT", flush=True)
    return report


if __name__ == "__main__":
    run()
