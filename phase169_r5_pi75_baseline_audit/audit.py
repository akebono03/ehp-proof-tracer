"""Phase 169 R5: read-only pi7^5 typed-search baseline and Toda (4.5) audit.

Never adds a GIVEN source or changes the proof search, public entry or Renderer.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r3o_stable_composite_rule import expand_cited_toda45_composite_transport
from proof import ProofRule, Relation
from toda_rules import Toda45IsomorphismStatement
from web_group_proof import build_standard_web_group_proof_view

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
OUTPUT = PACKAGE / "output"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()


def _record_steps(result) -> list[dict]:
    return [
        {
            "index": index,
            "rule": step.rule.value,
            "inference_name": step.inference_rule.name if step.inference_rule else None,
            "statement_type": type(step.conclusion).__name__,
            "conclusion": repr(step.conclusion),
            "premise_types": [type(parent.conclusion).__name__ for parent in step.premises],
        }
        for index, step in enumerate(result.proven_steps)
    ]


def _inspect() -> tuple[dict, str]:
    bridge = build_shared_typed_bridge()
    lower = database_structured_group_goal_candidates(n=4, k=2)
    candidates = registered_group_goal_candidates(bridge, n=5, k=2)
    contexts: list = []
    search = search_group_from_registered_goal(
        n=5, k=2, bridge=bridge, context_sink=contexts.append,
    )
    screened = contexts[-1] if contexts else None
    citing = (resolve_specialized_goal_citing_id(bridge, candidates[0])
              if len(candidates) == 1 else None)
    if len(lower) == 1 and isinstance(lower[0], Relation):
        base = lower[0].lhs
        lower_n = base.sphere_dimension
        lower_k = base.group_dimension - base.sphere_dimension
        stable_range = type(lower_n) is int and type(lower_k) is int and lower_n >= lower_k + 2
    else:
        stable_range = False
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    ) if screened is not None else ()
    cited_lower = any(x == lower[0] for x in available) if len(lower) == 1 else False
    cited_45 = any(isinstance(x, Toda45IsomorphismStatement) for x in available)
    root_options = ()
    toda45_options = ()
    if screened is not None and len(candidates) == 1:
        provider = shared_expansion_provider(screened, proof_target=candidates[0])
        root_options = provider(candidates[0])
        toda45_options = expand_cited_toda45_composite_transport(candidates[0], available)

    verified_tree = False
    verification_error = None
    model = None
    markdown = ""
    if screened is not None:
        model = build_linked_proof_narrative_model(search, screened)
        if search.status is ProofSearchStatus.COMPLETE:
            if citing is None:
                verification_error = "complete search has no positioned citing assertion"
            else:
                try:
                    verify_proof_tree_for_narrative(
                        search, screened, citing_assertion_id=citing,
                    )
                except Exception as error:
                    verification_error = f"{type(error).__name__}: {error}"
                else:
                    verified_tree = True
        try:
            markdown = render_model_backed_narrative_markdown(search, model)
        except Exception as error:
            markdown = f"Rendering failed: {type(error).__name__}: {error}\n"

    web_key = None
    web_error = None
    web_partial = None
    try:
        view = build_standard_web_group_proof_view(n=5, k=2, mode="narrative")
        web_key = view.key
        web_partial = view.partial_result
    except Exception as error:
        web_error = f"{type(error).__name__}: {error}"

    status = search.status.value
    report = {
        "phase": "169-R5",
        "mode": "AUDIT_ONLY",
        "git_head": _git("rev-parse", "HEAD"),
        "target": "pi_7^5",
        "target_group": repr(TodaPrimaryGroup(7, 5)),
        "candidate_count": len(candidates),
        "candidate_goals": [repr(goal) for goal in candidates],
        "citing_assertion_id": citing,
        "lower_goal_count": len(lower),
        "lower_goals": [repr(item) for item in lower],
        "toda45_stable_range_n4_k2": stable_range,
        "citation_screened_context": screened is not None,
        "screened_lower_relation_available": cited_lower,
        "screened_toda45_available": cited_45,
        "root_expansion_rule_names": [option.rule.name for option in root_options],
        "cited_toda45_root_options": len(toda45_options),
        "cited_toda45_subgoal_types": [
            [type(goal).__name__ for goal in option.subgoals]
            for option in toda45_options
        ],
        "search_status": status,
        "proof_steps": len(search.proven_steps),
        "open_goals": [repr(goal) for goal in search.open_goals],
        "diagnostics": list(search.diagnostics),
        "proof_step_records": _record_steps(search),
        "proof_tree_verified": verified_tree,
        "verification_error": verification_error,
        "citations": [] if model is None else [
            {"number": citation.number,
             "locator": citation.reference.locator or citation.reference.label,
             "statement_bodies": list(citation.statement_bodies)}
            for citation in model.citations
        ],
        "web_key": web_key,
        "web_partial": web_partial,
        "web_error": web_error,
        "full_pytest_run": False,
        "production_modified": False,
    }
    return report, markdown


def _format_report(report: dict) -> str:
    lines = [
        "# Phase 169 R5 — π₇⁵ 現状監査", "",
        "- 監査方式：AUDIT_ONLY（本番コード変更なし）",
        f"- Git HEAD：`{report['git_head']}`",
        f"- 登録 Goal 候補：{report['candidate_count']} 件",
        f"- 下位群 π₆⁴ 候補：{report['lower_goal_count']} 件",
        f"- Toda (4.5) 安定範囲 n=4,k=2：`{report['toda45_stable_range_n4_k2']}`",
        f"- 文献順に選別済み下位群 Relation：`{report['screened_lower_relation_available']}`",
        f"- 文献順に選別済み (4.5)：`{report['screened_toda45_available']}`",
        f"- (4.5) 直接候補数：{report['cited_toda45_root_options']}",
        f"- 検索状態：`{report['search_status']}`",
        f"- ProofStep：{report['proof_steps']} 件",
        f"- 未解決 Goal：{len(report['open_goals'])} 件",
        f"- Proof Tree 検証済み：`{report['proof_tree_verified']}`",
        f"- Web key：`{report['web_key']}`",
        "", "## 未解決 Goal", "",
    ]
    lines.extend((f"- `{item}`" for item in report["open_goals"]))
    if not report["open_goals"]:
        lines.append("- なし")
    lines.extend(("", "## 根拠・制約", ""))
    for name in report["root_expansion_rule_names"]:
        lines.append(f"- 規則候補：`{name}`")
    lines.extend(("", "## 引用", ""))
    for item in report["citations"]:
        lines.append(f"- [R{item['number']}] {item['locator']}")
    lines.extend((
        "", "この監査は Goal を GIVEN として導入せず、complete を先取りしない。",
        "Toda (4.5) は n≥k+2 の条件を維持する。", "",
    ))
    if report["verification_error"]:
        lines.append("Proof Tree 検証エラー：" + report["verification_error"])
    if report["web_error"]:
        lines.append("Web 検証エラー：" + report["web_error"])
    return "\n".join(lines)


def main() -> None:
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("Phase 169 R5 requires develop")
    before = _git("status", "--porcelain", "--untracked-files=no")
    report, markdown = _inspect()
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUTPUT / "audit.md").write_text(_format_report(report), encoding="utf-8")
    (OUTPUT / "web_narrative.md").write_text(markdown, encoding="utf-8")
    after = _git("status", "--porcelain", "--untracked-files=no")
    if after != before:
        raise RuntimeError("tracked Git status changed during read-only audit")
    for key in (
        "git_head", "candidate_count", "lower_goal_count", "toda45_stable_range_n4_k2",
        "screened_lower_relation_available", "screened_toda45_available",
        "cited_toda45_root_options", "search_status", "proof_steps",
        "proof_tree_verified", "web_key", "web_partial",
    ):
        print(f"R5_{key.upper()}={report[key]}")
    print("R5_OPEN_GOALS=" + str(len(report["open_goals"])))
    print("R5_TRACKED_STATUS_UNCHANGED=True")
    print("R5_PRODUCTION_MODIFIED=False")
    print("R5_FULL_PYTEST_RUN=False")
    print("R5_REPORT=" + str(OUTPUT / "audit.md"))
    print("R5_MARKDOWN=" + str(OUTPUT / "web_narrative.md"))
    if report["verification_error"]:
        raise RuntimeError(report["verification_error"])


if __name__ == "__main__":
    main()
