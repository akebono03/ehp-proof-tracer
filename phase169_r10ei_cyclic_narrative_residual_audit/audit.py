"""Inspect residual E-equation prose in two verified cyclic proof models.

The output is evidence for a future presentation-only change, not permission
for a new mathematical rule or for suppressing an independently cited step.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

from homotopy_groups import TodaSuspensionMap
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_29_order_projection import project_narrative_order
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase169_r10a_verified_stable_chain_projection.projection import (
    project_verified_stable_image_chain,
)
from phase169_r10ec_direct_sum_narrative_projection.projection import (
    project_verified_direct_sum_transport,
)
from proof import ProofRule
from toda_human_readable_renderer import render_toda_public_group_generator_latex

from .diagnostics import (
    CASES, assess_case, extra_duplicate_occurrences,
    image_formula_occurrences, validate_coverage,
)


def _source_citations(step: object, index_by_identity: dict[int, int],
                      model: object) -> tuple[int, ...]:
    """Read genuine cited GIVEN ancestors from this model without adding any."""
    found = set()
    seen = set()
    pending = [step]
    while pending:
        node = pending.pop()
        identity = id(node)
        if identity in seen:
            continue
        seen.add(identity)
        index = index_by_identity.get(identity)
        if index is not None and node.rule is ProofRule.GIVEN:
            found.update(model.step_citation_numbers[index])
        pending.extend(node.premises)
    return tuple(sorted(found))


def _typed_formula(step: object) -> tuple[str, str] | None:
    """Extract an E equation only from an actual GeneratorImage/Suspension."""
    conclusion = step.conclusion
    if not isinstance(conclusion, (GeneratorImage, GeneratorSuspension)):
        return None
    if not isinstance(conclusion.map, TodaSuspensionMap):
        return None
    source = render_toda_public_group_generator_latex(conclusion.source_generator)
    target = render_toda_public_group_generator_latex(conclusion.target_generator)
    if not source or not target:
        return None
    return source, target


def _typed_step_index(model: object, hidden: frozenset[int]) -> dict:
    """Inventory proof nodes and actual consumers, preserving step identity."""
    positions = {id(step): index for index, step in enumerate(model.steps)}
    if len(positions) != len(model.steps):
        raise ValueError("reused ProofStep identity prevents unambiguous audit")
    output = {}
    for index, step in enumerate(model.steps):
        formula = _typed_formula(step)
        if formula is None:
            continue
        consumers = tuple(
            consumer_index
            for consumer_index, consumer in enumerate(model.steps)
            if any(parent is step for parent in consumer.premises)
        )
        item = {
            "step_index": index,
            "statement_type": type(step.conclusion).__name__,
            "rule": step.rule.value,
            "premise_count": len(step.premises),
            "consumer_indices": list(consumers),
            "own_citation_numbers": list(model.step_citation_numbers[index]),
            "given_ancestor_citation_numbers": list(_source_citations(step, positions, model)),
            "hidden_by_r10a": index in hidden,
        }
        output.setdefault(formula, []).append(item)
    return output


def inspect_case(bridge: object, case: object) -> tuple[dict, str]:
    """Re-run and replay the real complete proof before examining prose."""
    screened = []
    result = search_group_from_registered_goal(
        n=case.n, k=case.k, bridge=bridge, context_sink=screened.append,
    )
    if result.status is not ProofSearchStatus.COMPLETE or len(screened) != 1:
        raise RuntimeError(f"{case.label}: complete searched proof not available")
    citing_id = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    inferred, given = verify_proof_tree_for_narrative(
        result, screened[0], citing_assertion_id=citing_id,
        derived_target_without_citing_id=citing_id is None,
    )
    model = build_linked_proof_narrative_model(result, screened[0])
    if model.steps != result.proven_steps:
        raise RuntimeError("narrative model changed the proof tree")
    order = tuple(entry.step_index for entry in project_narrative_order(model))
    stable = project_verified_stable_image_chain(model, order)
    direct_sum = project_verified_direct_sum_transport(model, order)
    text = render_model_backed_narrative_markdown(result, model)
    if not all(f"**[R{source.number}] " in text for source in model.citations):
        raise RuntimeError("a registered Reference disappeared")
    rows = image_formula_occurrences(text)
    duplicates = extra_duplicate_occurrences(rows)
    hidden = frozenset(stable.hidden_indices if stable is not None else ())
    typed_nodes = _typed_step_index(model, hidden)
    formula_records = []
    for formula in rows:
        key = formula["source_tex"], formula["target_tex"]
        observed = dict(formula)
        observed["matching_typed_step_indices"] = [
            item["step_index"] for item in typed_nodes.get(key, ())
        ]
        observed["matching_typed_steps"] = typed_nodes.get(key, ())
        observed["typed_match_is_diagnostic_only"] = True
        formula_records.append(observed)
    assessment = assess_case(
        result.status.value, "PASS", stable is not None, duplicates, case,
    )
    record = {
        "group": case.label, "stem": case.k,
        "search_status": result.status.value, "trust": "PASS",
        "inference_steps": inferred, "given_steps": given,
        "proof_step_count": len(result.proven_steps),
        "reference_count": len(model.citations),
        "reference_visible": True,
        "r10a_available": stable is not None,
        "r10a_hidden_indices": sorted(hidden),
        "r10a_hidden_count": len(hidden),
        "r10a_exponent": stable.exponent if stable is not None else None,
        "r10ec_available": direct_sum is not None,
        "one_step_equations_displayed": sum(item["copies"] for item in rows),
        "one_step_equations_distinct": len(rows),
        "duplicate_occurrences": duplicates,
        "formulae": formula_records,
        "assessment": assessment,
        "proof_and_source_unchanged": True,
        "mathematical_inference_added": False,
    }
    return record, text


def _markdown_report(rows: list[dict]) -> str:
    lines = [
        "# Phase 169 R10EI — 検証済み巡回群の表示残差監査", "",
        "AUDIT_ONLY。圧縮可能性を調べるが証明木・引用・表示は変更しない。", "",
        "| 群 | 証明 | R10A | 隠したステップ | 1段 E 式 | 重複 |",
        "|---|---|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['group']} | {row['search_status']} / {row['trust']} | "
            f"{row['r10a_available']} | {row['r10a_hidden_count']} | "
            f"{row['one_step_equations_displayed']} | {row['duplicate_occurrences']} |"
        )
        lines.extend(("", "## " + row["group"], ""))
        for formula in row["formulae"]:
            indices = formula["matching_typed_step_indices"]
            if formula["copies"] > 1 or row["r10a_available"]:
                lines.append(
                    f"- $E({formula['source_tex']})={formula['target_tex']}$: "
                    f"本文 {formula['copies']}回、型付き対応候補 {indices}"
                )
    lines.extend((
        "", "## 次工程への境界", "",
        "同一の表示文字列だけでは ProofStep の等価性も省略の安全性も証明しない。",
        "型付きステップの consumer・GIVEN ancestor・個別引用を比較してから、",
        "次の Phase の Renderer 修正可否を判断する。",
        "11-stem と14-stem の partial 結果に証明を追加する作業は含めない。",
        "全体 pytest は Phase 169 の最後まで実施しない。", "",
    ))
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phase169_r10ei_cyclic_narrative_residual_audit.audit OUTPUT_DIRECTORY")
    destination = Path(sys.argv[1]).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    if not validate_coverage():
        raise RuntimeError("R10EI cases lost the reviewed 6/10-stem coverage")
    bridge = build_shared_typed_bridge()
    cases = []
    for case in CASES:
        row, rendered = inspect_case(bridge, case)
        filename = case.label.replace("^", "_") + ".md"
        (destination / filename).write_text(rendered, encoding="utf-8")
        row["rendered_file"] = filename
        cases.append(row)
    report = {
        "phase": "169 R10EI",
        "mode": "AUDIT_ONLY",
        "cases": cases,
        "status": "PASS" if all(row["assessment"] == "PASS" for row in cases) else "REVIEW_REQUIRED",
        "application_source_changed": False,
        "full_pytest_run": False,
    }
    (destination / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (destination / "audit.md").write_text(_markdown_report(cases), encoding="utf-8")
    for row in cases:
        key = "R10EI_" + row["group"]
        print(key + "_STATUS=" + row["search_status"], flush=True)
        print(key + "_TRUST=" + row["trust"], flush=True)
        print(key + "_R10A_AVAILABLE=" + str(row["r10a_available"]), flush=True)
        print(key + "_HIDDEN=" + str(row["r10a_hidden_count"]), flush=True)
        print(key + "_ONE_STEP_E=" + str(row["one_step_equations_displayed"]), flush=True)
        print(key + "_DUPLICATES=" + str(row["duplicate_occurrences"]), flush=True)
        print(key + "_ASSESSMENT=" + row["assessment"], flush=True)
    print("R10EI_REPORT=" + str(destination / "audit.json"), flush=True)
    print("R10EI_FULL_PYTEST_RUN=False", flush=True)
    print("R10EI_AUDIT_STATUS=" + report["status"], flush=True)
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
