"""Read-only R10EH audit: two complete cyclic narratives and two open goals.

Neither a CSV generator symbol nor a renderer formula is mathematical evidence.
Only actual searched ProofSteps can be given to the trust-boundary verifier.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from expression import Composition, HomotopyElement, IteratedSuspension, Multiple, Sum
from homotopy_groups import FiniteCyclicGroup
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3t_goal_source_binding.goal_source import (
    resolve_specialized_goal_citing_id,
)
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase168_r3_27_typed_statement_projection import element_tex
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from phase169_r10ea_direct_sum_narrative_audit.prose_metrics import (
    count_rendered_image_equations,
)
from phase169_r10b_registered_stable_family_binding.family_registry import (
    registered_family_of,
)
from phase169_r10d2_general_family_definition.family_citation import (
    SOURCE_RECORDS,
)
from phase169_r10e8_hyoujigen_generic_suspension.source_records import (
    CHAPTER_VI_SOURCE_RECORDS,
)
from toda_human_readable_renderer import render_toda_public_group_generator_latex
from proof import ProofRule, Relation

from .policy import CASES, classify_observation, expected_coverage, source_record_status


REVIEWED_IDS = frozenset(
    row.family_id for row in SOURCE_RECORDS + CHAPTER_VI_SOURCE_RECORDS
)


def _typed_family_members(value: object) -> list[dict]:
    """Describe only registered metadata; a family ID is not a proof source."""
    if isinstance(value, HomotopyElement):
        registered = registered_family_of(value)
        return [{
            "element": repr(value)[:600],
            "family_id": registered.family_id if registered else None,
            "family_display": registered.display if registered else None,
            "source_status": (
                source_record_status(registered.family_id, REVIEWED_IDS)
                if registered else "NOT_AN_EXACT_REGISTERED_MEMBER"
            ),
        }]
    if isinstance(value, Composition):
        return _typed_family_members(value.left) + _typed_family_members(value.right)
    if isinstance(value, (Sum,)):
        return _typed_family_members(value.left) + _typed_family_members(value.right)
    if isinstance(value, Multiple):
        return _typed_family_members(value.expression)
    if isinstance(value, IteratedSuspension):
        return _typed_family_members(value.expression)
    return [{"element": repr(value)[:600], "source_status": "UNSUPPORTED_TYPED_SHAPE"}]


def _generator_profile(goal: object) -> dict:
    structure = getattr(goal, "rhs", None)
    if not isinstance(structure, FiniteCyclicGroup):
        return {"structure": type(structure).__name__, "members": []}
    generator = structure.generator
    return {
        "structure": "FiniteCyclicGroup",
        "order": structure.order,
        "generator_type": type(generator).__name__,
        "generator_repr": repr(generator)[:1000],
        "element_tex_supported": bool(element_tex(generator)),
        "public_tex_supported": bool(render_toda_public_group_generator_latex(generator)),
        "members": _typed_family_members(generator),
    }


def inspect_case(bridge: object, n: int, k: int) -> dict:
    """Audit current backward result; verify ONLY complete searched Proof Trees."""
    contexts: list[object] = []
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    record = {
        "group": f"pi_{n+k}^{n}", "n": n, "k": k,
        "status": result.status.value,
        "goal_candidates": len(goals),
        "proof_steps": len(result.proven_steps),
        "open_goal_types": [type(goal).__name__ for goal in result.open_goals],
        "open_goal_examples": [repr(goal)[:1200] for goal in result.open_goals[:8]],
        "diagnostics": list(result.diagnostics),
        "given_steps": sum(step.rule is ProofRule.GIVEN for step in result.proven_steps),
        "inference_steps": sum(step.rule is ProofRule.INFERENCE for step in result.proven_steps),
        "goal_generator": _generator_profile(goals[0]) if len(goals) == 1 else None,
        "trust": "NOT_APPLICABLE_INCOMPLETE",
        "narrative_file": None,
    }
    if result.status is not ProofSearchStatus.COMPLETE:
        return record
    if not contexts or result.conclusion is None:
        record["trust"] = "MISSING_VERIFICATION_CONTEXT"
        return record
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    try:
        inference, given = verify_proof_tree_for_narrative(
            result, contexts[-1], citing_assertion_id=citing_id,
            derived_target_without_citing_id=citing_id is None,
        )
    except (ValueError, TypeError) as error:
        record["trust"] = type(error).__name__ + ": " + str(error)
        return record
    record["trust"] = "PASS"
    record["verified_inference_steps"] = inference
    record["verified_given_steps"] = given
    model = build_linked_proof_narrative_model(result, contexts[-1])
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    r10a = project_verified_stable_image_chain(model, order)
    r10ec = project_verified_direct_sum_transport(model, order)
    narrative = render_model_backed_narrative_markdown(result, model)
    metrics = count_rendered_image_equations(narrative)
    record.update({
        "narrative_characters": len(narrative),
        "narrative_E_image_metrics": metrics,
        "r10a_cyclic_projection": r10a is not None,
        "r10ec_direct_sum_projection": r10ec is not None,
        "proof_tree_preserved": model.steps == result.proven_steps,
        "reference_count": len(model.citations),
        "references_displayed": all(
            f"**[R{item.number}] " in narrative for item in model.citations
        ),
        "root_premise_types": (
            [type(step.conclusion).__name__ for step in model.steps[model.root_index].premises]
            if model.root_index is not None else []
        ),
    })
    # No outputs in this module are written to a fixed tracked filename.
    record["_rendered_text"] = narrative
    return record


def _report_text(rows: list[dict]) -> str:
    parts = [
        "# R10EH — 6/10/11/14-stem 表示・証明境界監査", "",
        "AUDIT_ONLY。DB の表示名と文献に基づく証明を区別する。", "",
        "| 群 | 探索 | 信頼境界 | 1段 E 等式 | 重複 | R10A | R10EC |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for row in rows:
        metric = row.get("narrative_E_image_metrics", {})
        parts.append(
            f"| {row['group']} | {row['status']} | {row['trust']} | "
            f"{metric.get('total_occurrences', '—')} | "
            f"{metric.get('extra_duplicate_occurrences', '—')} | "
            f"{row.get('r10a_cyclic_projection', '—')} | "
            f"{row.get('r10ec_direct_sum_projection', '—')} |"
        )
    for row in rows:
        parts.extend(("", "## " + row["group"], ""))
        parts.append("- 型付き Goal 候補: " + str(row["goal_candidates"]))
        parts.append("- ProofStep: " + str(row["proof_steps"]))
        if row.get("goal_generator"):
            for member in row["goal_generator"]["members"]:
                parts.append(
                    "- 生成元 ID と文献の区別: "
                    + str(member.get("family_id")) + " / "
                    + member["source_status"]
                )
        for item in row["open_goal_types"]:
            parts.append("- 未解決型: " + item)
        for diag in row["diagnostics"][:3]:
            parts.append("- 探索診断: `" + diag.replace("`", "'")[:500] + "`")
        if row["narrative_file"]:
            parts.append("- 完成本文: " + row["narrative_file"])
    parts.extend((
        "", "## 次工程との境界", "",
        "完成群については検証済み Proof Tree に基づく cyclic projection を別工程で検討する。",
        "未完成群は不足する GeneratorImage と source-backed family definition の有無を監査し、",
        "メタデータの存在だけで GIVEN を増やさない。",
        "本監査は証明木、推論規則、文献、既存テスト、DB、本番 Renderer を変更しない。",
        "全体 pytest は Phase 169 の終了時に実施する。", "",
    ))
    return "\n".join(parts)


def main() -> None:
    args = sys.argv[1:]
    if len(args) != 1:
        raise SystemExit("Usage: python -m phase169_r10eh_stem6_10_11_14_audit.audit OUTPUT_DIRECTORY")
    destination = Path(args[0]).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    if not expected_coverage():
        raise RuntimeError("R10EH audit case definition lost intended coverage")
    bridge = build_shared_typed_bridge()
    results = [inspect_case(bridge, case.n, case.k) for case in CASES]
    for record in results:
        text = record.pop("_rendered_text", None)
        if text is not None:
            filename = record["group"].replace("^", "_") + ".md"
            (destination / filename).write_text(text, encoding="utf-8")
            record["narrative_file"] = filename
    classifications = [
        classify_observation(case.expected_status, row["status"], row["trust"])
        for case, row in zip(CASES, results)
    ]
    report = {
        "phase": "169 R10EH", "mode": "AUDIT_ONLY", "cases": results,
        "classifications": classifications,
        "production_files_changed": False,
        "mathematical_inference_rules_added": False,
        "full_pytest_run": False,
        "audit_pass": all(item in ("PASS", "EXPECTED_INCOMPLETE")
                          for item in classifications),
    }
    (destination / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (destination / "audit.md").write_text(_report_text(results), encoding="utf-8")
    for row, status in zip(results, classifications):
        label = "R10EH_" + row["group"]
        print(label + "_STATUS=" + row["status"], flush=True)
        print(label + "_TRUST=" + row["trust"], flush=True)
        print(label + "_ASSESSMENT=" + status, flush=True)
        print(label + "_PROOF_STEPS=" + str(row["proof_steps"]), flush=True)
        if row.get("narrative_E_image_metrics"):
            metric = row["narrative_E_image_metrics"]
            print(label + "_DISPLAY_IMAGE_EQUATIONS="
                  + str(metric["total_occurrences"]), flush=True)
            print(label + "_DUPLICATES="
                  + str(metric["extra_duplicate_occurrences"]), flush=True)
            print(label + "_R10A_AVAILABLE="
                  + str(row["r10a_cyclic_projection"]), flush=True)
            print(label + "_R10EC_AVAILABLE="
                  + str(row["r10ec_direct_sum_projection"]), flush=True)
        else:
            print(label + "_OPEN_GOAL_TYPES="
                  + ",".join(row["open_goal_types"]), flush=True)
        if row.get("goal_generator"):
            print(label + "_FAMILY_SOURCE_STATUS=" + ",".join(
                member["source_status"]
                for member in row["goal_generator"]["members"]
            ), flush=True)
    print("R10EH_REPORT=" + str(destination / "audit.json"))
    print("R10EH_PRODUCTION_CHANGED=False")
    print("R10EH_FULL_PYTEST_RUN=False")
    print("R10EH_AUDIT_STATUS=" + ("PASS" if report["audit_pass"] else "REVIEW_REQUIRED"))
    if not report["audit_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
