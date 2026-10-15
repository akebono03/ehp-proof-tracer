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
EXPECTED_GROUP_COUNT = 112
EXPECTED_NODES = 713
EXPECTED_BLOCKS = 559
EXPECTED_ARGUMENTS = 129
EXPECTED_OTHER_BLOCKS = 126
EXPECTED_RULE_NAME_FALLBACKS = 115
EXPECTED_TYPE_FALLBACKS = 51
OUTPUT_DIR = Path(__file__).resolve().parent / "audit_output"


def _label(n: int, k: int) -> str:
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
    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    step_rows = []
    reason_rows = []
    group_rows = []
    exceptions = []

    total_nodes = 0
    total_blocks = 0
    total_arguments = 0
    total_other_blocks = 0

    for n in N_RANGE:
        for k in K_RANGE:
            group = _label(n, k)
            try:
                presentation, blocks, arguments, reason_sidecar = _context(
                    n,
                    k,
                )
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

            total_nodes += len(presentation.nodes)
            total_blocks += len(blocks)
            total_arguments += len(arguments)
            other_blocks = tuple(
                block
                for block in blocks
                if block.role
                is TodaGroupProofNarrativeMathematicalBlockRole.OTHER
            )
            total_other_blocks += len(other_blocks)

            block_info_by_step_id = {}
            for block_index, block in enumerate(blocks):
                for step in block.steps:
                    block_info_by_step_id[id(step)] = (
                        block_index,
                        block.role.value,
                    )

            group_other_steps = 0
            group_fallback_steps = 0
            group_overlap_steps = 0

            for node_index, node in enumerate(presentation.nodes):
                step = node.proof_step
                block_index, block_role = block_info_by_step_id[id(step)]
                rendered = _render_generic_narrative_step(step)
                fallback_kind = _fallback_kind(step, rendered)
                is_other = block_role == "other"
                is_fallback = fallback_kind is not None
                overlap = is_other and is_fallback

                if is_other:
                    group_other_steps += 1
                if is_fallback:
                    group_fallback_steps += 1
                if overlap:
                    group_overlap_steps += 1

                step_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "stem": k,
                        "group": group,
                        "node_index": node_index,
                        "block_index": block_index,
                        "block_role": block_role,
                        "statement_type": type(step.conclusion).__name__,
                        "inference_rule_name": (
                            step.inference_rule.name
                            if step.inference_rule is not None
                            else ""
                        ),
                        "fallback_kind": fallback_kind or "",
                        "is_other": is_other,
                        "is_fallback": is_fallback,
                        "other_and_fallback": overlap,
                    }
                )

            for reason_index, reason in enumerate(reason_sidecar.reasons):
                sentence = render_toda_group_proof_narrative_reason_sentence(
                    reason
                )
                reason_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "stem": k,
                        "group": group,
                        "reason_index": reason_index,
                        "reason_kind": reason.kind.value,
                        "premise_count": len(reason.premise_steps),
                        "conclusion_type": type(
                            reason.conclusion_step.conclusion
                        ).__name__,
                        "sentence_rendered": sentence is not None,
                    }
                )

            group_rows.append(
                {
                    "n": n,
                    "k": k,
                    "stem": k,
                    "group": group,
                    "nodes": len(presentation.nodes),
                    "blocks": len(blocks),
                    "arguments": len(arguments),
                    "typed_reasons": len(reason_sidecar.reasons),
                    "other_blocks": len(other_blocks),
                    "other_steps": group_other_steps,
                    "fallback_steps": group_fallback_steps,
                    "other_fallback_overlap_steps": group_overlap_steps,
                }
            )

    statement_summary = defaultdict(
        lambda: Counter(
            total=0,
            other=0,
            fallback=0,
            overlap=0,
            rule_name=0,
            type_name=0,
            raw=0,
        )
    )
    statement_groups = defaultdict(set)
    rule_summary = Counter()
    role_fallback_summary = Counter()
    stem_summary = defaultdict(
        lambda: Counter(
            nodes=0,
            other=0,
            fallback=0,
            overlap=0,
            reasons=0,
        )
    )

    for row in step_rows:
        statement_type = row["statement_type"]
        bucket = statement_summary[statement_type]
        bucket["total"] += 1
        if row["is_other"]:
            bucket["other"] += 1
        if row["is_fallback"]:
            bucket["fallback"] += 1
            statement_groups[statement_type].add(row["group"])
            role_fallback_summary[
                (row["block_role"], row["fallback_kind"])
            ] += 1
            if row["fallback_kind"] == "rule_name":
                bucket["rule_name"] += 1
                rule_summary[
                    (
                        statement_type,
                        row["inference_rule_name"],
                    )
                ] += 1
            elif row["fallback_kind"] == "type_name":
                bucket["type_name"] += 1
            else:
                bucket["raw"] += 1
        if row["other_and_fallback"]:
            bucket["overlap"] += 1

        stem = int(row["stem"])
        stem_summary[stem]["nodes"] += 1
        if row["is_other"]:
            stem_summary[stem]["other"] += 1
        if row["is_fallback"]:
            stem_summary[stem]["fallback"] += 1
        if row["other_and_fallback"]:
            stem_summary[stem]["overlap"] += 1

    for row in reason_rows:
        stem_summary[int(row["stem"])]["reasons"] += 1

    statement_rows = []
    for statement_type, counts in sorted(
        statement_summary.items(),
        key=lambda item: (
            -item[1]["fallback"],
            -item[1]["other"],
            item[0],
        ),
    ):
        statement_rows.append(
            {
                "statement_type": statement_type,
                "total_steps": counts["total"],
                "other_steps": counts["other"],
                "fallback_steps": counts["fallback"],
                "overlap_steps": counts["overlap"],
                "rule_name_fallbacks": counts["rule_name"],
                "type_fallbacks": counts["type_name"],
                "raw_fallbacks": counts["raw"],
                "affected_groups": len(
                    statement_groups[statement_type]
                ),
            }
        )

    rule_rows = [
        {
            "statement_type": statement_type,
            "inference_rule_name": rule_name,
            "occurrences": count,
        }
        for (
            statement_type,
            rule_name,
        ), count in rule_summary.most_common()
    ]

    role_rows = [
        {
            "block_role": block_role,
            "fallback_kind": fallback_kind,
            "occurrences": count,
        }
        for (
            block_role,
            fallback_kind,
        ), count in sorted(
            role_fallback_summary.items(),
            key=lambda item: (
                -item[1],
                item[0][0],
                item[0][1],
            ),
        )
    ]

    stem_rows = [
        {
            "stem": stem,
            "nodes": counts["nodes"],
            "other_steps": counts["other"],
            "fallback_steps": counts["fallback"],
            "overlap_steps": counts["overlap"],
            "typed_reasons": counts["reasons"],
        }
        for stem, counts in sorted(stem_summary.items())
    ]

    reason_kind_counts = Counter(
        row["reason_kind"]
        for row in reason_rows
    )
    reason_conclusion_counts = Counter(
        (
            row["reason_kind"],
            row["conclusion_type"],
        )
        for row in reason_rows
    )
    reason_summary_rows = [
        {
            "reason_kind": kind,
            "conclusion_type": conclusion_type,
            "occurrences": count,
        }
        for (
            kind,
            conclusion_type,
        ), count in sorted(
            reason_conclusion_counts.items(),
            key=lambda item: (
                item[0][0],
                -item[1],
                item[0][1],
            ),
        )
    ]

    _write_csv(
        OUTPUT_DIR / "step_cross_cutting_inventory.csv",
        (
            "n",
            "k",
            "stem",
            "group",
            "node_index",
            "block_index",
            "block_role",
            "statement_type",
            "inference_rule_name",
            "fallback_kind",
            "is_other",
            "is_fallback",
            "other_and_fallback",
        ),
        step_rows,
    )
    _write_csv(
        OUTPUT_DIR / "statement_type_summary.csv",
        (
            "statement_type",
            "total_steps",
            "other_steps",
            "fallback_steps",
            "overlap_steps",
            "rule_name_fallbacks",
            "type_fallbacks",
            "raw_fallbacks",
            "affected_groups",
        ),
        statement_rows,
    )
    _write_csv(
        OUTPUT_DIR / "rule_name_summary.csv",
        (
            "statement_type",
            "inference_rule_name",
            "occurrences",
        ),
        rule_rows,
    )
    _write_csv(
        OUTPUT_DIR / "block_role_fallback_summary.csv",
        (
            "block_role",
            "fallback_kind",
            "occurrences",
        ),
        role_rows,
    )
    _write_csv(
        OUTPUT_DIR / "stem_summary.csv",
        (
            "stem",
            "nodes",
            "other_steps",
            "fallback_steps",
            "overlap_steps",
            "typed_reasons",
        ),
        stem_rows,
    )
    _write_csv(
        OUTPUT_DIR / "group_summary.csv",
        (
            "n",
            "k",
            "stem",
            "group",
            "nodes",
            "blocks",
            "arguments",
            "typed_reasons",
            "other_blocks",
            "other_steps",
            "fallback_steps",
            "other_fallback_overlap_steps",
        ),
        group_rows,
    )
    _write_csv(
        OUTPUT_DIR / "reason_cross_cutting_summary.csv",
        (
            "reason_kind",
            "conclusion_type",
            "occurrences",
        ),
        reason_summary_rows,
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

    fallback_rows = [
        row
        for row in step_rows
        if row["is_fallback"]
    ]
    other_rows = [
        row
        for row in step_rows
        if row["is_other"]
    ]
    overlap_rows = [
        row
        for row in step_rows
        if row["other_and_fallback"]
    ]
    rule_name_count = sum(
        row["fallback_kind"] == "rule_name"
        for row in fallback_rows
    )
    type_name_count = sum(
        row["fallback_kind"] == "type_name"
        for row in fallback_rows
    )
    raw_count = len(fallback_rows) - rule_name_count - type_name_count

    top_statement_lines = [
        (
            f"  {row['statement_type']}: "
            f"fallback={row['fallback_steps']}, "
            f"OTHER={row['other_steps']}, "
            f"overlap={row['overlap_steps']}, "
            f"groups={row['affected_groups']}"
        )
        for row in statement_rows
        if (
            int(row["fallback_steps"]) > 0
            or int(row["other_steps"]) > 0
        )
    ][:20]

    summary_lines = [
        "=" * 78,
        "Phase 151-3 — Cross-cutting Audit",
        "=" * 78,
        f"groups: {len(group_rows)}",
        f"exceptions: {len(exceptions)}",
        f"presentation nodes: {total_nodes}",
        f"blocks: {total_blocks}",
        f"arguments: {total_arguments}",
        f"OTHER blocks: {total_other_blocks}",
        f"OTHER steps: {len(other_rows)}",
        f"fallback steps: {len(fallback_rows)}",
        f"  rule-name: {rule_name_count}",
        f"  type-name: {type_name_count}",
        f"  raw: {raw_count}",
        f"OTHER ∩ fallback steps: {len(overlap_rows)}",
        (
            "fallback outside OTHER: "
            f"{len(fallback_rows) - len(overlap_rows)}"
        ),
        (
            "OTHER without fallback: "
            f"{len(other_rows) - len(overlap_rows)}"
        ),
        f"typed reasons: {len(reason_rows)}",
        "",
        "Typed reason kinds:",
    ]
    for kind, count in sorted(reason_kind_counts.items()):
        summary_lines.append(
            f"  {kind}: {count}"
        )

    summary_lines.extend(
        (
            "",
            "Top cross-cutting statement types:",
            *top_statement_lines,
            "",
            "Interpretation boundary:",
            "  This phase classifies concentration and overlap only.",
            "  It does not change semantic roles, renderers, reasons, or public routes.",
            "",
            "Output files:",
            "  step_cross_cutting_inventory.csv",
            "  statement_type_summary.csv",
            "  rule_name_summary.csv",
            "  block_role_fallback_summary.csv",
            "  stem_summary.csv",
            "  group_summary.csv",
            "  reason_cross_cutting_summary.csv",
            "  exception_inventory.csv",
            "  cross_cutting_summary.txt",
            "=" * 78,
        )
    )
    summary = "\n".join(summary_lines) + "\n"
    (
        OUTPUT_DIR / "cross_cutting_summary.txt"
    ).write_text(
        summary,
        encoding="utf-8",
    )
    print(summary)

    baseline_ok = (
        len(group_rows) == EXPECTED_GROUP_COUNT
        and not exceptions
        and total_nodes == EXPECTED_NODES
        and total_blocks == EXPECTED_BLOCKS
        and total_arguments == EXPECTED_ARGUMENTS
        and total_other_blocks == EXPECTED_OTHER_BLOCKS
        and rule_name_count == EXPECTED_RULE_NAME_FALLBACKS
        and type_name_count == EXPECTED_TYPE_FALLBACKS
        and raw_count == 0
    )

    if not baseline_ok:
        print(
            "FAIL: Phase 151-3 did not reproduce the Phase 151-2 baseline."
        )
        return 1

    print(
        "PASS: Phase 151-2 baseline reproduced and cross-cutting inventories generated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
