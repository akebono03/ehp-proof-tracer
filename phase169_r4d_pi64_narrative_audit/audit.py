"""Audit the genuine pi6_4 Web narrative without changing proof or renderer code."""
from __future__ import annotations

import json
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
from phase169_r4d_pi64_narrative_audit.checks import (
    citation_usage, split_narrative, visual_findings,
)

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def main() -> None:
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=ROOT, text=True,
    ).strip()
    if branch != "develop":
        raise RuntimeError("R4D requires the develop branch")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    provider_source = (ROOT / "phase165_r52_r9_shared_math.py").read_text(encoding="utf-8")
    for required in (
        "options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))",
        "options.extend(expand_pi64_suspension_isomorphism(goal))",
    ):
        if provider_source.count(required) != 1:
            raise RuntimeError("R4B or R4C provider missing or duplicated: " + required)

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(
        n=4, k=2, bridge=bridge, context_sink=contexts.append,
    )
    if (result.status is not ProofSearchStatus.COMPLETE
            or len(result.proven_steps) != 18
            or result.open_goals
            or len(contexts) != 1):
        raise RuntimeError("R4C 18-step pi6_4 proof baseline is not complete")
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    if citing is None:
        raise RuntimeError("no positioned citation target for pi6_4")
    verify_proof_tree_for_narrative(result, contexts[0], citing_assertion_id=citing)
    model = build_linked_proof_narrative_model(result, contexts[0])
    markdown = render_model_backed_narrative_markdown(result, model)
    header, body = split_narrative(markdown)

    web = build_standard_web_group_proof_view(
        n=4, k=2, max_depth=2, mode="narrative", citation_source="model",
    )
    if web.partial_result or web.key != "generic-complete-proof" or len(web.steps) != 18:
        raise RuntimeError("Web route does not preserve pi6_4 complete proof")
    citations = [
        {
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "step_indices": list(citation.step_indices),
            "assertion_ids": list(citation.assertion_ids),
            "statement_bodies": list(citation.statement_bodies),
        }
        for citation in model.citations
    ]
    usage = citation_usage(markdown, tuple(citation.number for citation in model.citations))
    findings = visual_findings(markdown, usage)
    rendered = [
        {
            "kind": line.kind,
            "indent_level": line.indent_level,
            "prefix": line.prefix,
            "statement_latex": line.statement_latex,
            "suffix": line.suffix,
            "segments": [{"kind": s.kind, "value": s.value} for s in line.segments],
        }
        for line in web.rendered_lines
    ]
    report = {
        "phase": "169-R4D",
        "mode": "AUDIT_ONLY",
        "head": head,
        "proof_status": result.status.value,
        "proof_steps": len(result.proven_steps),
        "open_goals": len(result.open_goals),
        "proof_tree_verified": True,
        "model_root_index": model.root_index,
        "web_key": web.key,
        "web_partial": web.partial_result,
        "web_steps": len(web.steps),
        "web_rendered_lines": len(rendered),
        "unsupported_step_types": sorted(set(
            step.fallback_type_name for step in web.steps
            if step.fallback_type_name is not None
        )),
        "citations": citations,
        "citation_usage": usage,
        "visual_findings": findings,
        "reference_text": header,
        "proof_text": body,
        "web_rendered_content": rendered,
        "production_modified": False,
        "full_pytest_run": False,
    }
    output = PACKAGE / "output"
    output.mkdir(exist_ok=True)
    (output / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (output / "web_narrative.md").write_text(markdown, encoding="utf-8")
    summary = [
        "# Phase 169 R4D — π₆⁴ Web Narrative / Reference 監査", "",
        "- mode: AUDIT_ONLY",
        f"- Git HEAD: `{head}`",
        "- 証明状態: complete (18 ProofSteps, 未解決 0)",
        "- Proof Tree / publication trust boundary: 検証済み",
        f"- Web 公開状態: `{web.key}` / partial={web.partial_result}",
        f"- Reference 件数: {len(citations)}",
        f"- Web rendered lines: {len(rendered)}",
        f"- 証明本文で参照されない引用番号: {usage['uncited_in_proof']}",
        f"- Citation に対応しない本文タグ: {usage['unknown_in_proof']}",
        f"- 表示上の検討事項: {findings}", "",
        "## 引用一覧", "",
    ]
    for citation in citations:
        summary.append(f"- [R{citation['number']}] {citation['locator']} (step={citation['step_indices']})")
    summary.extend([
        "", "## 判定", "",
        "証明の complete 判定は既存 Proof Tree による。表示上の検討事項は証明を偽装して自動解消しない。",
        "`web_narrative.md` の本文と Reference を人手で確認する。", "",
    ])
    (output / "audit.md").write_text("\n".join(summary), encoding="utf-8")
    print("R4D_GIT_HEAD=" + head)
    print("R4D_PROOF_TREE_VERIFIED=True")
    print("R4D_PI64_STATUS=complete")
    print("R4D_PI64_STEPS=18")
    print("R4D_PI64_OPEN_GOALS=0")
    print("R4D_WEB_KEY=" + web.key)
    print("R4D_CITATIONS=" + str(len(citations)))
    print("R4D_VISUAL_FINDINGS=" + ",".join(findings or ["NONE"]))
    print("R4D_AUDIT_ONLY=True")
    print("R4D_FULL_PYTEST_RUN=False")
    print("R4D_MARKDOWN=" + str(output / "web_narrative.md"))
    print("R4D_REPORT=" + str(output / "audit.md"))


if __name__ == "__main__":
    main()
