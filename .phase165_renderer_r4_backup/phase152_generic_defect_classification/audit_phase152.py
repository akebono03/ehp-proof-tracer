from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_arguments import (
    build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
    TodaGroupProofNarrativeMathematicalBlockRole,
    build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_reason_renderer import (
    render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
    build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
    build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
    build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
    build_toda_group_result_proof_replay,
)

N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2

EXPECTED_GROUPS = 112
EXPECTED_NODES = 713
EXPECTED_BLOCKS = 559
EXPECTED_ARGUMENTS = 129
EXPECTED_OTHER_BLOCKS = 126
EXPECTED_OTHER_STEPS = 144
EXPECTED_FALLBACK_STEPS = 166
EXPECTED_RULE_NAME = 115
EXPECTED_TYPE_NAME = 51
EXPECTED_RAW = 0
EXPECTED_OVERLAP = 125
EXPECTED_TYPED_REASONS = 146

OUTPUT_DIR = Path(__file__).resolve().parent / "audit_output"


def _group_label(n: int, k: int) -> str:
    return f"pi_{n + k}^{n}"


def _fallback_kind(step, rendered: str) -> str | None:
    rule = step.inference_rule
    if rule is not None and rendered == rule.name:
        return "rule_name"
    if rendered == "`" + type(step.conclusion).__name__ + "`":
        return "type_name"
    if rendered == repr(step.conclusion):
        return "raw_repr"
    if rendered == str(step.conclusion):
        return "raw_str"
    return None


def _context(n: int, k: int):
    report = build_standard_toda_report(n=n, k=k)
    if not report.candidates:
        raise AssertionError(f"no report candidate for n={n}, k={k}")

    group_result = report.candidates[0].source_candidate.group_result
    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=MAX_DEPTH,
    )
    presentation = build_toda_group_proof_presentation(replay)
    presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            presentation
        )
    )
    sidecar = build_toda_group_proof_narrative_semantic_sidecar(
        presentation
    )
    blocks = build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=sidecar,
    )
    arguments = build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=sidecar,
    )
    reasons = build_toda_group_proof_narrative_reason_sidecar(
        presentation,
        sidecar,
    )
    return presentation, blocks, arguments, reasons


def _write_csv(path: Path, fieldnames, rows) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _step_defect_category(
    *,
    is_other: bool,
    fallback_kind: str | None,
) -> str:
    if is_other and fallback_kind is not None:
        return "semantic_classification_and_statement_rendering"
    if is_other:
        return "semantic_classification"
    if fallback_kind is not None:
        return "statement_rendering"
    return "none_observed"


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    step_rows = []
    reason_rows = []
    exceptions = []

    totals = Counter()

    for n in N_RANGE:
        for k in K_RANGE:
            group = _group_label(n, k)
            try:
                presentation, blocks, arguments, reasons = _context(n, k)
            except Exception as exc:
                exceptions.append(
                    {
                        "n": n,
                        "k": k,
                        "group": group,
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                    }
                )
                continue

            totals["groups"] += 1
            totals["nodes"] += len(presentation.nodes)
            totals["blocks"] += len(blocks)
            totals["arguments"] += len(arguments)

            other_blocks = tuple(
                block
                for block in blocks
                if block.role
                is TodaGroupProofNarrativeMathematicalBlockRole.OTHER
            )
            totals["other_blocks"] += len(other_blocks)

            block_role_by_step_id = {}
            for block in blocks:
                for step in block.steps:
                    block_role_by_step_id[id(step)] = block.role.value

            for node in presentation.nodes:
                step = node.proof_step
                block_role = block_role_by_step_id[id(step)]
                is_other = block_role == "other"
                rendered = _render_generic_narrative_step(step)
                fallback_kind = _fallback_kind(step, rendered)
                category = _step_defect_category(
                    is_other=is_other,
                    fallback_kind=fallback_kind,
                )

                if is_other:
                    totals["other_steps"] += 1
                if fallback_kind is not None:
                    totals["fallback_steps"] += 1
                    totals[f"fallback_{fallback_kind}"] += 1
                if is_other and fallback_kind is not None:
                    totals["overlap"] += 1

                step_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "stem": k,
                        "group": group,
                        "statement_type": type(step.conclusion).__name__,
                        "block_role": block_role,
                        "inference_rule_name": (
                            step.inference_rule.name
                            if step.inference_rule is not None
                            else ""
                        ),
                        "fallback_kind": fallback_kind or "",
                        "defect_category": category,
                    }
                )

            for reason in reasons.reasons:
                sentence = render_toda_group_proof_narrative_reason_sentence(
                    reason
                )
                totals["typed_reasons"] += 1
                reason_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "stem": k,
                        "group": group,
                        "reason_kind": reason.kind.value,
                        "conclusion_type": type(
                            reason.conclusion_step.conclusion
                        ).__name__,
                        "premise_count": len(reason.premise_steps),
                        "sentence_rendered": sentence is not None,
                    }
                )

    category_counts = Counter(
        row["defect_category"]
        for row in step_rows
        if row["defect_category"] != "none_observed"
    )
    category_statement_counts = Counter(
        (
            row["defect_category"],
            row["statement_type"],
        )
        for row in step_rows
        if row["defect_category"] != "none_observed"
    )
    category_group_sets = defaultdict(set)
    for row in step_rows:
        if row["defect_category"] == "none_observed":
            continue
        category_group_sets[
            row["defect_category"]
        ].add(row["group"])

    category_rows = []
    for category, count in sorted(
        category_counts.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        statement_types = {
            statement_type
            for (
                defect_category,
                statement_type,
            ), occurrence_count in category_statement_counts.items()
            if defect_category == category and occurrence_count > 0
        }
        category_rows.append(
            {
                "defect_category": category,
                "occurrences": count,
                "statement_types": len(statement_types),
                "affected_groups": len(category_group_sets[category]),
            }
        )

    statement_rows = [
        {
            "defect_category": category,
            "statement_type": statement_type,
            "occurrences": count,
        }
        for (
            category,
            statement_type,
        ), count in sorted(
            category_statement_counts.items(),
            key=lambda item: (
                item[0][0],
                -item[1],
                item[0][1],
            ),
        )
    ]

    reason_kind_counts = Counter(
        row["reason_kind"]
        for row in reason_rows
    )
    non_final_reason_count = sum(
        count
        for kind, count in reason_kind_counts.items()
        if kind != "final_result_derivation"
    )
    final_reason_count = reason_kind_counts[
        "final_result_derivation"
    ]

    reason_rows_summary = [
        {
            "reason_kind": kind,
            "occurrences": count,
            "coverage_class": (
                "final_result"
                if kind == "final_result_derivation"
                else "intermediate_specific"
            ),
        }
        for kind, count in sorted(reason_kind_counts.items())
    ]

    investigation_rows = [
        {
            "candidate_category": "reason_coverage",
            "status": "observed_cross_cutting_gap",
            "evidence": (
                f"typed reasons={totals['typed_reasons']}; "
                f"final_result_derivation={final_reason_count}; "
                f"intermediate_specific={non_final_reason_count}"
            ),
            "phase152_action": "classify_only",
            "future_boundary": (
                "A later phase may generalize intermediate mathematical "
                "reason kinds; Phase 152 does not add them."
            ),
        },
        {
            "candidate_category": "selection",
            "status": "not_determined_by_phase151_baseline",
            "evidence": (
                "Phase 151 measured selected generic presentation output, "
                "not counterfactual selection quality."
            ),
            "phase152_action": "do_not_classify_as_confirmed_defect",
            "future_boundary": "Requires a dedicated selection invariant audit.",
        },
        {
            "candidate_category": "ownership",
            "status": "not_determined_by_phase151_baseline",
            "evidence": (
                "Phase 151 measured rendered steps and blocks, not whether "
                "each contribution belongs to the mathematically correct argument."
            ),
            "phase152_action": "do_not_classify_as_confirmed_defect",
            "future_boundary": "Requires a dedicated ownership invariant audit.",
        },
        {
            "candidate_category": "ordering",
            "status": "not_determined_by_phase151_baseline",
            "evidence": (
                "Phase 151 counted outputs but did not compare contribution "
                "order against dependency constraints."
            ),
            "phase152_action": "do_not_classify_as_confirmed_defect",
            "future_boundary": "Requires a dedicated ordering invariant audit.",
        },
        {
            "candidate_category": "formatting",
            "status": "not_determined_by_phase151_baseline",
            "evidence": (
                "Fallback/OTHER counts do not establish punctuation, TeX, "
                "numbering, or layout defects."
            ),
            "phase152_action": "do_not_classify_as_confirmed_defect",
            "future_boundary": "Requires rendered-text formatting checks.",
        },
        {
            "candidate_category": "result_reuse",
            "status": "not_determined_by_phase151_baseline",
            "evidence": (
                "Phase 151 did not measure duplicate derivation or reusable "
                "result identity across arguments."
            ),
            "phase152_action": "do_not_classify_as_confirmed_defect",
            "future_boundary": "Requires a dedicated reuse/deduplication audit.",
        },
    ]

    _write_csv(
        OUTPUT_DIR / "confirmed_step_defect_categories.csv",
        (
            "defect_category",
            "occurrences",
            "statement_types",
            "affected_groups",
        ),
        category_rows,
    )
    _write_csv(
        OUTPUT_DIR / "defect_by_statement_type.csv",
        (
            "defect_category",
            "statement_type",
            "occurrences",
        ),
        statement_rows,
    )
    _write_csv(
        OUTPUT_DIR / "step_classification_inventory.csv",
        (
            "n",
            "k",
            "stem",
            "group",
            "statement_type",
            "block_role",
            "inference_rule_name",
            "fallback_kind",
            "defect_category",
        ),
        step_rows,
    )
    _write_csv(
        OUTPUT_DIR / "reason_coverage_classification.csv",
        (
            "reason_kind",
            "occurrences",
            "coverage_class",
        ),
        reason_rows_summary,
    )
    _write_csv(
        OUTPUT_DIR / "unresolved_candidate_categories.csv",
        (
            "candidate_category",
            "status",
            "evidence",
            "phase152_action",
            "future_boundary",
        ),
        investigation_rows,
    )
    _write_csv(
        OUTPUT_DIR / "exception_inventory.csv",
        (
            "n",
            "k",
            "group",
            "exception_type",
            "exception_message",
        ),
        exceptions,
    )

    summary = [
        "=" * 78,
        "Phase 152 — Generic Defect Classification",
        "=" * 78,
        f"groups: {totals['groups']}",
        f"exceptions: {len(exceptions)}",
        f"presentation nodes: {totals['nodes']}",
        f"blocks: {totals['blocks']}",
        f"arguments: {totals['arguments']}",
        f"OTHER blocks: {totals['other_blocks']}",
        f"OTHER steps: {totals['other_steps']}",
        f"fallback steps: {totals['fallback_steps']}",
        f"  rule-name: {totals['fallback_rule_name']}",
        f"  type-name: {totals['fallback_type_name']}",
        (
            "  raw: "
            f"{totals['fallback_raw_repr'] + totals['fallback_raw_str']}"
        ),
        f"OTHER ∩ fallback: {totals['overlap']}",
        f"typed reasons: {totals['typed_reasons']}",
        "",
        "Confirmed step-level defect categories:",
    ]

    for row in category_rows:
        summary.append(
            "  "
            f"{row['defect_category']}: "
            f"occurrences={row['occurrences']}, "
            f"statement_types={row['statement_types']}, "
            f"affected_groups={row['affected_groups']}"
        )

    summary.extend(
        [
            "",
            "Reason coverage:",
            (
                "  final_result_derivation: "
                f"{final_reason_count}"
            ),
            (
                "  intermediate-specific typed reasons: "
                f"{non_final_reason_count}"
            ),
            "",
            "Candidate categories not yet proven by Phase 151 data:",
            "  selection",
            "  ownership",
            "  ordering",
            "  formatting",
            "  result_reuse",
            "",
            "Classification rule:",
            (
                "  OTHER + fallback -> "
                "semantic_classification_and_statement_rendering"
            ),
            "  OTHER only -> semantic_classification",
            "  fallback only -> statement_rendering",
            (
                "  reason concentration -> reason_coverage "
                "(cross-cutting gap, not a step-level fallback category)"
            ),
            "",
            "Interpretation boundary:",
            "  No production behavior is changed.",
            "  No semantic role is reassigned.",
            "  No statement renderer is added.",
            "  No reason kind is added.",
            (
                "  Selection/ownership/ordering/formatting/result_reuse "
                "are not inferred without dedicated evidence."
            ),
            "",
            "Output files:",
            "  confirmed_step_defect_categories.csv",
            "  defect_by_statement_type.csv",
            "  step_classification_inventory.csv",
            "  reason_coverage_classification.csv",
            "  unresolved_candidate_categories.csv",
            "  exception_inventory.csv",
            "  defect_classification_summary.txt",
            "=" * 78,
        ]
    )

    summary_text = "\n".join(summary) + "\n"
    (
        OUTPUT_DIR / "defect_classification_summary.txt"
    ).write_text(summary_text, encoding="utf-8")
    print(summary_text)

    raw_count = (
        totals["fallback_raw_repr"]
        + totals["fallback_raw_str"]
    )
    baseline_ok = (
        totals["groups"] == EXPECTED_GROUPS
        and not exceptions
        and totals["nodes"] == EXPECTED_NODES
        and totals["blocks"] == EXPECTED_BLOCKS
        and totals["arguments"] == EXPECTED_ARGUMENTS
        and totals["other_blocks"] == EXPECTED_OTHER_BLOCKS
        and totals["other_steps"] == EXPECTED_OTHER_STEPS
        and totals["fallback_steps"] == EXPECTED_FALLBACK_STEPS
        and totals["fallback_rule_name"] == EXPECTED_RULE_NAME
        and totals["fallback_type_name"] == EXPECTED_TYPE_NAME
        and raw_count == EXPECTED_RAW
        and totals["overlap"] == EXPECTED_OVERLAP
        and totals["typed_reasons"] == EXPECTED_TYPED_REASONS
    )

    category_ok = (
        category_counts[
            "semantic_classification_and_statement_rendering"
        ] == EXPECTED_OVERLAP
        and category_counts["semantic_classification"]
        == EXPECTED_OTHER_STEPS - EXPECTED_OVERLAP
        and category_counts["statement_rendering"]
        == EXPECTED_FALLBACK_STEPS - EXPECTED_OVERLAP
    )

    if not baseline_ok:
        print("FAIL: Phase 151-3 baseline was not reproduced.")
        return 1

    if not category_ok:
        print("FAIL: defect category partition is inconsistent.")
        return 1

    print(
        "PASS: Phase 151 baseline reproduced and observed defects "
        "partitioned without changing production behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
