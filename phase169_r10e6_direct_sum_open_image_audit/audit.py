"""Phase 169 R10E6: read-only diagnosis of unresolved direct-sum images.

This module does not add facts, proof rules, registry entries or ProofSteps.
Reported search steps are observations, not independent trust-boundary verification.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from expression import Composition, HomotopyElement
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e1_general_group_transport.transport import (
    generator_images_for_group_transport,
)
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step,
    exact_prior_database_result,
)
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
    expand_composite_generator_image,
)
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    SOURCE_RECORDS,
    expand_cited_stable_family,
)
from phase169_r10b_registered_stable_family_binding.family_registry import (
    read_registered_stable_families,
    registered_stable_family_pair,
)
from proof import ProofRule, Relation


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
TARGETS = ((15, 8), (15, 9))


def _element_name(item: object) -> str:
    """Use typed expression structure for display, never for evidence."""
    if isinstance(item, HomotopyElement):
        return item.name
    if isinstance(item, Composition):
        return f"({_element_name(item.left)} ∘ {_element_name(item.right)})"
    return repr(item)


def _component_generators(statement: object) -> tuple[object, ...]:
    if not isinstance(statement, Relation):
        return ()
    structure = statement.rhs
    if isinstance(structure, (FiniteCyclicGroup, FreeCyclicGroup)):
        return (structure.generator,)
    if isinstance(structure, DirectSumGroup):
        if all(isinstance(x, (FiniteCyclicGroup, FreeCyclicGroup)) for x in structure.summands):
            return tuple(x.generator for x in structure.summands)
    return ()


def _observed_inferred(image: GeneratorImage, steps: tuple) -> bool:
    """Search-engine observation; does not construct a new verified proof."""
    return any(step.rule is ProofRule.INFERENCE and step.conclusion == image for step in steps)


def _cited_families(screened: object) -> tuple[object, ...]:
    """Return only screened fixed source statements as candidate metadata."""
    if screened is None:
        return ()
    sources = []
    for link in screened.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        statement = link.step.conclusion
        if isinstance(statement, CitedStableFamilyDefinition):
            sources.append(statement)
    return tuple(sources)


def _candidate_profile(image: GeneratorImage, available: tuple[object, ...]) -> dict[str, Any]:
    """Classify proposals without treating a proposal as a discharged goal."""
    factors = component_image_obligations(image)
    family = registered_stable_family_pair(image.source_generator, image.target_generator)
    reviewed_ids = {record.family_id for record in SOURCE_RECORDS}
    screened_ids = {item.family_id for item in available if isinstance(item, CitedStableFamilyDefinition)}
    cited_options = expand_cited_stable_family(image, available)
    composite_options = expand_composite_generator_image(image)
    return {
        "family_id_from_name_metadata": family.family_id if family is not None else None,
        "family_has_reviewed_source": family is not None and family.family_id in reviewed_ids,
        "family_source_in_screened_context": family is not None and family.family_id in screened_ids,
        "cited_family_proposals": len(cited_options),
        "composition_proposals": len(composite_options),
        "composition_factor_goals": [
            {"source": _element_name(part.source_generator),
             "target": _element_name(part.target_generator)}
            for part in factors
        ] if factors is not None else [],
        "scope": "These are possible rule expansions, not verified proofs",
    }


def _expected_component_audit(
    source: object, goal: object, steps: tuple,
    open_goals: tuple, available: tuple[object, ...],
) -> dict[str, Any]:
    source_gens = _component_generators(source)
    target_gens = _component_generators(goal)
    source_group = source.lhs if isinstance(source, Relation) else None
    target_group = goal.lhs if isinstance(goal, Relation) else None
    expected = generator_images_for_group_transport(source, goal)
    if expected is None:
        return {
            "typed_transport_compatible": False,
            "source_generators": [_element_name(x) for x in source_gens],
            "target_generators": [_element_name(x) for x in target_gens],
            "component_reports": [],
        }
    if source_group is None or target_group is None:
        return {"typed_transport_compatible": True, "component_reports": [],
                "note": "non-Relation source/target requires separate handling"}
    folds = target_group.sphere_dimension - source_group.sphere_dimension
    components = []
    for i, (earlier, later) in enumerate(zip(source_gens, target_gens)):
        images = expected[i * folds:(i + 1) * folds]
        observations = []
        for j, image in enumerate(images):
            in_steps = _observed_inferred(image, steps)
            is_open = image in open_goals
            row = {
                "suspension_index": j + 1,
                "source_generator": _element_name(image.source_generator),
                "target_generator": _element_name(image.target_generator),
                "in_search_proven_steps_as_inference": in_steps,
                "exact_open_goal": is_open,
            }
            if not in_steps:
                row["candidate_diagnosis"] = _candidate_profile(image, available)
            observations.append(row)
        components.append({
            "index": i + 1,
            "source_generator": _element_name(earlier),
            "target_generator": _element_name(later),
            "expected_image_count": len(images),
            "inferred_image_count": sum(x["in_search_proven_steps_as_inference"] for x in observations),
            "images": observations,
        })
    return {
        "typed_transport_compatible": True,
        "suspension_exponent": folds,
        "expected_image_count": len(expected),
        "source_generators": [_element_name(x) for x in source_gens],
        "target_generators": [_element_name(x) for x in target_gens],
        "component_reports": components,
    }


def _unresolved(goal: object) -> dict[str, Any]:
    item = {"type": type(goal).__name__, "repr": repr(goal)}
    if isinstance(goal, GeneratorImage):
        item["source_generator"] = _element_name(goal.source_generator)
        item["target_generator"] = _element_name(goal.target_generator)
        item["factors"] = [
            {"source": _element_name(g.source_generator),
             "target": _element_name(g.target_generator)}
            for g in (component_image_obligations(goal) or ())
        ]
    return item


def audit_case(bridge: object, n: int, k: int) -> dict[str, Any]:
    goals = registered_group_goal_candidates(bridge, n=n, k=k)
    base_n = k + 2
    source = exact_prior_database_result(base_n, k)
    contexts: list[object] = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=contexts.append,
    )
    goal = goals[0] if len(goals) == 1 else None
    admitted = (
        admitted_db_step(source, proof_target=goal, bridge=bridge)
        if source is not None and goal is not None else None
    )
    steps = tuple(result.proven_steps)
    open_goals = tuple(result.open_goals)
    available = _cited_families(contexts[-1] if contexts else None)
    target = f"pi_{n+k}^{n}"
    report = {
        "target": target,
        "stable_base": f"pi_{2*k+2}^{k+2}",
        "source_explicit_in_db": source is not None,
        "source_admitted_as_ordered_db_given": admitted is not None,
        "target_goal_candidates": len(goals),
        "status": result.status.value,
        "diagnostics": list(result.diagnostics),
        "open_goals": [_unresolved(x) for x in open_goals],
        "search_inferred_generator_images": sum(
            1 for step in steps
            if step.rule is ProofRule.INFERENCE and isinstance(step.conclusion, GeneratorImage)
        ),
        "screened_family_source_ids": sorted({x.family_id for x in available}),
        "screened_context_captured": bool(contexts),
    }
    if source is not None and goal is not None:
        report["transport"] = _expected_component_audit(
            source, goal, steps, open_goals, available,
        )
    else:
        report["transport"] = None
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 169 R10E6 — 直和群の未解決生成元像監査",
        "", "AUDIT_ONLY：既存コード・既存テスト・証明台帳は変更しない。",
        "", f"- Git HEAD: `{report['head']}`",
        "- 監査は探索結果の観測であり、新規証明または Trust Boundary の代用ではない。",
        "- 生成元の DB 名称や型一致は懸垂像の証明ではない。", "",
    ]
    for item in report["cases"]:
        lines.extend([
            f"## {item['target']}", "",
            f"- 探索状態: `{item['status']}`",
            f"- 安定基点: `{item['stable_base']}`（DB 行: {item['source_explicit_in_db']}、先行前提: {item['source_admitted_as_ordered_db_given']}）",
            f"- 未解決目標: {', '.join(x['type'] for x in item['open_goals']) or 'なし'}",
            f"- 審査済み系列定義 ID: {item['screened_family_source_ids']}", "",
        ])
        transport = item["transport"]
        if transport is None:
            lines.extend(["輸送目標を一意に取得できない。", ""])
            continue
        if not transport.get("typed_transport_compatible", False):
            lines.extend(["型付き群構造の輸送候補が構築できない。", ""])
            continue
        lines.extend([
            f"期待される懸垂像: {transport.get('expected_image_count', 0)} 件", "",
            "| 成分 | 基点生成元 | 輸送先生成元 | INFERENCE として観測 | 期待数 |",
            "|---|---|---|---:|---:|",
        ])
        for component in transport["component_reports"]:
            lines.append(
                f"| {component['index']} | `{component['source_generator']}` | "
                f"`{component['target_generator']}` | {component['inferred_image_count']} | "
                f"{component['expected_image_count']} |"
            )
        lines.extend(["", "### 未導出の画像条件", ""])
        for component in transport["component_reports"]:
            for row in component["images"]:
                if row["in_search_proven_steps_as_inference"]:
                    continue
                profile = row["candidate_diagnosis"]
                lines.extend([
                    f"- 成分{component['index']}・第{row['suspension_index']}回: "
                    f"`{row['source_generator']}` → `{row['target_generator']}` "
                    f"(exact open={row['exact_open_goal']}; "
                    f"family_id={profile['family_id_from_name_metadata']}; "
                    f"cited proposals={profile['cited_family_proposals']}; "
                    f"composition proposals={profile['composition_proposals']})",
                ])
        lines.append("")
        for open_goal in item["open_goals"]:
            if open_goal["type"] == "GeneratorImage":
                lines.append(
                    f"探索が直接報告した GeneratorImage: "
                    f"`{open_goal['source_generator']}` → `{open_goal['target_generator']}`"
                )
        lines.append("")
    lines.extend([
        "## 判断基準", "",
        "- 未解決の GeneratorImage または Relation が残る場合、complete に変更しない。",
        "- 系列定義の追加は原典の記述・掲載位置・型・Trust Boundary を別途監査した後。",
        "- 合成規則が存在しても、その因子の像が両方証明されない限り complete としない。",
        "- 次の実装段階は、この監査による成分別未解決位置の確定後に限定する。",
        "- 全体 pytest は Phase 169 終了時のみ実施。", "",
    ])
    return "\n".join(lines)


def main() -> None:
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if branch != "develop":
        raise RuntimeError(f"AUDIT_ONLY requires develop; got {branch!r}")
    report = {
        "phase": "169 R10E6",
        "mode": "AUDIT_ONLY",
        "branch": branch,
        "head": head,
        "cases": [],
        "production_files_modified": [],
        "full_pytest_run": False,
    }
    bridge = build_shared_typed_bridge()
    for n, k in TARGETS:
        item = audit_case(bridge, n, k)
        report["cases"].append(item)
        print(f"R10E6_{item['target']}_STATUS={item['status']}")
        print(f"R10E6_{item['target']}_OPEN={','.join(x['type'] for x in item['open_goals'])}")
        transport = item["transport"]
        if transport is not None:
            for comp in transport["component_reports"]:
                missing = [x for x in comp["images"]
                           if not x["in_search_proven_steps_as_inference"]]
                print(f"R10E6_{item['target']}_COMP{comp['index']}_FROM={comp['source_generator']}")
                print(f"R10E6_{item['target']}_COMP{comp['index']}_TO={comp['target_generator']}")
                print(f"R10E6_{item['target']}_COMP{comp['index']}_MISSING={','.join(str(x['suspension_index']) for x in missing)}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT / "audit.json"
    md_path = OUTPUT / "audit.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(f"R10E6_AUDIT_JSON={json_path}")
    print(f"R10E6_AUDIT_MD={md_path}")
    print("R10E6_PRODUCTION_FILES_CHANGED=none")
    print("R10E6_FULL_PYTEST_RUN=False")


if __name__ == "__main__":
    main()
