"""Audit R20R13 Web narrative formatting over the canonical verified proof."""
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
from phase171_r20r13_eta_sentence_layout.projection import verified_eta_display_sentences
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
        raise ValueError("audit permits read-only Git commands only")
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def run() -> dict[str, object]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R20R13 audit requires develop")
    before = git("status", "--porcelain", "--untracked-files=no")
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=3, k=3, bridge=bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
            or len(contexts) != 1):
        raise RuntimeError("pi_6^3 public proof must stay complete")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("missing publication-order evidence")
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    if "\n証明\n" not in markdown:
        raise RuntimeError("proof body missing")
    references, body = markdown.split("\n証明\n", 1)
    eligible = verified_eta_display_sentences(model)
    grouped = tuple(
        line for line in body.splitlines()
        if line.startswith("[R3]より, $E(") and r",\quad E(" in line
    )
    if (len(model.citations) != 8
            or len(eligible) < 3
            or not grouped
            or not all(f"[R{item.number}]" in references for item in model.citations)
            or r"\operatorname{ord}" not in body
            or r"\neq0" not in body):
        raise RuntimeError("expected verified eta compaction or order-four proof lost")
    # The summary originally includes multiple sentences; a final Markdown
    # paragraph break ensures one period per displayed line.
    if "短完全列となる. 両端" in body or "位数はそれぞれ" not in body:
        raise RuntimeError("sentence-boundary formatting failed")
    if git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("read-only audit modified tracked files")
    report = {
        "phase": "171-R20R13",
        "mode": "PRESENTATION_ONLY_SOURCE_BOUND_ETA_LAYOUT",
        "git_head": git("rev-parse", "HEAD"),
        "public_status": result.status.value,
        "public_complete": True,
        "reference_count": len(model.citations),
        "verified_eta_sentences": len(eligible),
        "grouped_eta_lines": list(grouped),
        "period_sentence_breaks": True,
        "root_inferred": model.steps[model.root_index].rule is ProofRule.INFERENCE,
        "new_given_added": 0,
        "math_inference_modified": False,
        "completed_proofs_imported": False,
        "full_pytest": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "web_narrative.md").write_text(markdown, encoding="utf-8")
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("PHASE171_R20R13_PUBLIC_STATUS=" + str(report["public_status"]), flush=True)
    print("PHASE171_R20R13_ETA_GROUPED=" + str(len(grouped)), flush=True)
    print("PHASE171_R20R13_PERIOD_BREAKS=True", flush=True)
    print("PHASE171_R20R13_REFERENCES=" + str(len(model.citations)), flush=True)
    print("PHASE171_R20R13_REPORT=" + str(OUTPUT / "audit.json"), flush=True)
    print("PHASE171_R20R13_MARKDOWN=" + str(OUTPUT / "web_narrative.md"), flush=True)
    print("PHASE171_R20R13_RESULT=PASS_NARRATIVE_LAYOUT", flush=True)
    return report


if __name__ == "__main__":
    run()
