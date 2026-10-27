"""R6A canonical pi_8^6 proof and standard-Web evidence audit."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from proof import ProofRule
from toda_rules import Toda45IsomorphismStatement
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"


def main() -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=6, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE:
        raise RuntimeError("pi_8^6 incomplete: " + repr(result.open_goals))
    if result.open_goals or len(contexts) != 1:
        raise RuntimeError("complete pi_8^6 missing screened context or has open goals")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("no positioned pi_8^6 source citation")
    verified = verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
    )
    model = build_linked_proof_narrative_model(result, contexts[0])
    if model.root_index is None:
        raise RuntimeError("missing root ProofStep")
    root = model.steps[model.root_index]
    if root.rule is not ProofRule.INFERENCE or len(root.premises) != 4:
        raise RuntimeError("root must have four actual proof premises")
    lower, iso, image1, image2 = root.premises
    if not (
        lower.conclusion.lhs == TodaPrimaryGroup(6, 4)
        and isinstance(iso.conclusion, Toda45IsomorphismStatement)
        and iso.conclusion.map.exponent == 2
        and isinstance(image1.conclusion, GeneratorImage)
        and isinstance(image2.conclusion, GeneratorImage)
        and all(parent.rule is ProofRule.INFERENCE for parent in root.premises[1:])
        and image1.conclusion.target_generator == image2.conclusion.source_generator
    ):
        raise RuntimeError("real root premises do not certify E^2 eta-square transport")
    narrative = render_model_backed_narrative_markdown(result, model)
    view = build_standard_web_group_proof_view(6, 2, mode="narrative")
    if (
        view.key != "generic-complete-proof"
        or view.partial_result
        or len(view.steps) != len(result.proven_steps)
        or not narrative.rstrip().endswith("□")
    ):
        raise RuntimeError("canonical Web did not render a complete cited proof")
    headers = re.findall(r"\*\*\[R(\d+)\]", narrative)
    if not headers or len(set(headers)) != len(headers):
        raise RuntimeError("missing or duplicated Reference headings")
    if "\n証明\n" not in narrative:
        raise RuntimeError("Narrative proof body missing")
    used = set(re.findall(r"\[R(\d+)\]", narrative.split("\n証明\n", 1)[1]))
    report = {
        "phase": "169-R6A",
        "head": head,
        "status": result.status.value,
        "steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "root_inference_premises": len(root.premises),
        "root_premise_rules": [step.rule.value for step in root.premises],
        "root_premise_types": [type(step.conclusion).__name__ for step in root.premises],
        "verified_inference_and_given_counts": list(verified),
        "proof_tree_verified": True,
        "web_key": view.key,
        "reference_count": len(model.citations),
        "reference_headings": headers,
        "proof_citation_numbers": sorted(used),
        "untagged_references": sorted(set(headers) - used),
        "full_pytest_run": False,
    }
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUTPUT / "web_narrative.md").write_text(narrative, encoding="utf-8")
    lines = [
        "# Phase 169 R6A — π₈⁶ の2回懸垂証明", "",
        f"- Git HEAD: `{head}`",
        f"- 証明状態: `{result.status.value}`",
        f"- ProofStep: `{len(result.proven_steps)}`",
        "- 未解決 Goal: `0`",
        "- Proof Tree / publication trust boundary: 検証済み",
        f"- Root premise types: `{report['root_premise_types']}`",
        f"- Root premise rules: `{report['root_premise_rules']}`",
        f"- Web key: `{view.key}`",
        f"- Reference: `{len(model.citations)}`",
        f"- 証明本文で未使用の Reference: `{report['untagged_references']}`", "",
        "π₇⁵ の群構造を GIVEN として利用していない。",
        "先行した π₆⁴ と Toda (4.5)、2つの生成元写像を実際に証明する。",
        "全体 pytest は実行していない。", "",
    ]
    (OUTPUT / "audit.md").write_text("\n".join(lines), encoding="utf-8")
    print("R6A_GIT_HEAD=" + head)
    print("R6A_PI86_STATUS=" + result.status.value)
    print("R6A_PI86_STEPS=" + str(len(result.proven_steps)))
    print("R6A_PI86_OPEN_GOALS=" + str(len(result.open_goals)))
    print("R6A_ROOT_FOUR_PROVED_PREMISES=True")
    print("R6A_PROOF_TREE_VERIFIED=True")
    print("R6A_WEB_KEY=" + view.key)
    print("R6A_REFERENCES=" + str(len(model.citations)))
    print("R6A_UNTAGGED_REFERENCES=" + repr(report["untagged_references"]))
    print("R6A_FULL_PYTEST_RUN=False")
    print("R6A_REPORT=" + str(OUTPUT / "audit.md"))
    print("R6A_MARKDOWN=" + str(OUTPUT / "web_narrative.md"))


if __name__ == "__main__":
    main()
