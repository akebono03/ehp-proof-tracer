"""Validate actual R5B root proof and Web narrative without forging source leaves."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def ancestors(step):
    seen = set()
    result = []
    stack = [step]
    while stack:
        item = stack.pop()
        if id(item) in seen:
            continue
        seen.add(id(item))
        result.append(item)
        stack.extend(item.premises)
    return tuple(result)


def main() -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=5, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE:
        raise RuntimeError("pi7_5 is not complete: " + repr(result.open_goals))
    if result.open_goals or len(contexts) != 1:
        raise RuntimeError("pi7_5 has unscreened steps or open goals")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("missing target citation")
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    if not isinstance(model, ProofNarrativeModel):
        raise RuntimeError("Narrative Model is missing")
    markdown = render_model_backed_narrative_markdown(result, model)
    view = build_standard_web_group_proof_view(5, 2, mode="narrative")
    if view.key != "generic-complete-proof" or view.partial_result:
        raise RuntimeError("standard Web route is not complete")
    if len(view.steps) != len(result.proven_steps):
        raise RuntimeError("Web ProofSteps differ from searched proof")
    root = result.proven_steps[model.root_index]
    if root.rule is not ProofRule.INFERENCE or len(root.premises) != 3:
        raise RuntimeError("transport root must have three proved premises")
    if any(parent.rule is not ProofRule.INFERENCE for parent in root.premises):
        raise RuntimeError("transport subgoals were not actually inferred")
    if root.premises[0].conclusion.lhs != TodaPrimaryGroup(6, 4):
        raise RuntimeError("transport source group mismatch")
    given_leaves = [item for item in ancestors(root) if item.rule is ProofRule.GIVEN]
    ref_heads = re.findall(r"\*\*\[R(\d+)\]", markdown)
    if not ref_heads or len(set(ref_heads)) != len(ref_heads):
        raise RuntimeError("Reference display has missing or duplicate items")
    if not markdown.rstrip().endswith("□"):
        raise RuntimeError("complete Narrative has no conclusion marker")
    report = {
        "phase": "169-R5B",
        "head": head,
        "status": result.status.value,
        "steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "proof_tree_verified": True,
        "root_rule": root.inference_rule.name if root.inference_rule else None,
        "root_premise_types": [type(p.conclusion).__name__ for p in root.premises],
        "root_premise_rules": [p.rule.value for p in root.premises],
        "given_leaf_types": sorted({type(step.conclusion).__name__ for step in given_leaves}),
        "web_key": view.key,
        "references": len(model.citations),
        "reference_headings": ref_heads,
        "reference_tags_in_body": sorted(set(re.findall(r"\[R(\d+)\]", markdown.split("\n証明\n", 1)[-1]))),
        "full_pytest_run": False,
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT / "web_narrative.md").write_text(markdown, encoding="utf-8")
    lines = [
        "# Phase 169 R5B — π₇⁵ cited Toda transport proof", "",
        f"- Git HEAD: `{head}`",
        f"- Search: `{result.status.value}`; steps `{len(result.proven_steps)}`; open goals `0`",
        f"- Proof Tree validated: `True`",
        f"- Transport root: `{report['root_rule']}`",
        f"- Premises: `{report['root_premise_types']}`",
        f"- Premise proof rules: `{report['root_premise_rules']}`",
        f"- Web: `{view.key}`",
        f"- Reference count: `{len(model.citations)}`", "",
        "DB relation remains a Goal, never an assumed GIVEN. The proof contains a positioned prior FIXED_STATEMENT leaf.",
        "The entire pytest suite was not run.", "",
    ]
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R5B_HEAD=" + head)
    print("R5B_PI75_STATUS=" + result.status.value)
    print("R5B_PI75_STEPS=" + str(len(result.proven_steps)))
    print("R5B_PI75_OPEN_GOALS=" + str(len(result.open_goals)))
    print("R5B_ROOT_THREE_INFERENCE_PREMISES=True")
    print("R5B_PROOF_TREE_VERIFIED=True")
    print("R5B_WEB_KEY=" + view.key)
    print("R5B_REFERENCES=" + str(len(model.citations)))
    print("R5B_FULL_PYTEST_RUN=False")
    print("R5B_REPORT=" + str(OUTPUT / "audit.md"))
    print("R5B_MARKDOWN=" + str(OUTPUT / "web_narrative.md"))


if __name__ == "__main__":
    main()
