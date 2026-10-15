from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_provenance_catalog import (
    is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_references import (
    extract_toda_group_proof_step_literature_reference,
)
from toda_group_proof_narrative_semantics import (
    build_toda_group_proof_narrative_semantic_closure_presentation,
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

OUTPUT_DIR = (
    Path(__file__).resolve().parent
    / "audit_output"
)


def _group_label(
    n: int,
    k: int,
) -> str:
    return (
        "pi_"
        + str(n + k)
        + "^"
        + str(n)
    )


def _fallback_kind(
    step,
    rendered: str,
) -> str | None:
    rule = step.inference_rule

    if (
        rule is not None
        and rendered == rule.name
    ):
        return "rule_name"

    if rendered == (
        "`"
        + type(step.conclusion).__name__
        + "`"
    ):
        return "type_name"

    if rendered == repr(
        step.conclusion
    ):
        return "raw_repr"

    if rendered == str(
        step.conclusion
    ):
        return "raw_str"

    return None


def _context(
    n: int,
    k: int,
):
    report = build_standard_toda_report(
        n=n,
        k=k,
    )

    if not report.candidates:
        raise AssertionError(
            "no report candidate for "
            + "n="
            + str(n)
            + ", k="
            + str(k)
        )

    group_result = (
        report.candidates[
            0
        ].source_candidate.group_result
    )

    replay = (
        build_toda_group_result_proof_replay(
            group_result,
            max_depth=MAX_DEPTH,
        )
    )

    presentation = (
        build_toda_group_proof_presentation(
            replay
        )
    )

    return (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            presentation
        )
    )


def _premise_edge_count_by_step_id(
    presentation,
) -> Counter:
    counts = Counter()

    for edge in presentation.edges:
        counts[
            id(
                edge.parent_step
            )
        ] += 1

    return counts


def _classify_reference_leaf(
    step,
) -> tuple[
    str,
    str,
]:
    statement = step.conclusion

    if (
        is_toda_group_proof_narrative_provenance_only_statement(
            statement
        )
    ):
        return (
            "reference_only",
            "provenance_only_statement",
        )

    rendered = (
        _render_generic_narrative_step(
            step
        )
    )
    fallback_kind = (
        _fallback_kind(
            step,
            rendered,
        )
    )

    if fallback_kind is None:
        return (
            "reference_plus_semantic_fact",
            "meaningful_generic_rendering_available",
        )

    return (
        "unresolved_rendering",
        fallback_kind,
    )


def _write_csv(
    path: Path,
    fieldnames,
    rows,
) -> None:
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
        writer.writerows(
            rows
        )


def main() -> int:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    totals = Counter()
    category_groups = defaultdict(
        set
    )
    type_counts = Counter()
    type_groups = defaultdict(
        set
    )

    occurrence_rows = []
    exceptions = []

    for n in N_RANGE:
        for k in K_RANGE:
            group = _group_label(
                n,
                k,
            )

            try:
                presentation = _context(
                    n,
                    k,
                )
            except Exception as exc:
                exceptions.append(
                    {
                        "n": n,
                        "k": k,
                        "group": group,
                        "exception_type": (
                            type(exc).__name__
                        ),
                        "exception_message": (
                            str(exc)
                        ),
                    }
                )
                continue

            totals[
                "groups"
            ] += 1
            totals[
                "nodes"
            ] += len(
                presentation.nodes
            )

            premise_edge_counts = (
                _premise_edge_count_by_step_id(
                    presentation
                )
            )

            for node_index, node in enumerate(
                presentation.nodes
            ):
                step = node.proof_step

                if (
                    premise_edge_counts[
                        id(step)
                    ]
                    != 0
                ):
                    continue

                reference = (
                    extract_toda_group_proof_step_literature_reference(
                        step
                    )
                )

                if reference is None:
                    continue

                totals[
                    "reference_leaf_occurrences"
                ] += 1

                category, reason = (
                    _classify_reference_leaf(
                        step
                    )
                )

                totals[
                    category
                ] += 1
                category_groups[
                    category
                ].add(
                    group
                )

                statement_type = (
                    type(
                        step.conclusion
                    ).__name__
                )

                type_counts[
                    (
                        category,
                        statement_type,
                    )
                ] += 1
                type_groups[
                    (
                        category,
                        statement_type,
                    )
                ].add(
                    group
                )

                rendered = (
                    _render_generic_narrative_step(
                        step
                    )
                )
                fallback_kind = (
                    _fallback_kind(
                        step,
                        rendered,
                    )
                )

                occurrence_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "group": group,
                        "node_index": node_index,
                        "statement_type": (
                            statement_type
                        ),
                        "reference_label": (
                            reference.label
                        ),
                        "reference_locator": (
                            reference.locator
                            or ""
                        ),
                        "classification": (
                            category
                        ),
                        "classification_reason": (
                            reason
                        ),
                        "provenance_only": (
                            is_toda_group_proof_narrative_provenance_only_statement(
                                step.conclusion
                            )
                        ),
                        "fallback_kind": (
                            fallback_kind
                            or ""
                        ),
                        "inference_rule_name": (
                            step.inference_rule.name
                            if (
                                step.inference_rule
                                is not None
                            )
                            else ""
                        ),
                        "generic_rendering": (
                            rendered
                        ),
                    }
                )

    category_rows = []

    for category in (
        "reference_only",
        "reference_plus_semantic_fact",
        "unresolved_rendering",
    ):
        category_rows.append(
            {
                "classification": category,
                "occurrences": (
                    totals[
                        category
                    ]
                ),
                "statement_types": (
                    len(
                        {
                            statement_type
                            for (
                                row_category,
                                statement_type,
                            ), count
                            in type_counts.items()
                            if (
                                row_category
                                == category
                                and count > 0
                            )
                        }
                    )
                ),
                "affected_groups": (
                    len(
                        category_groups[
                            category
                        ]
                    )
                ),
            }
        )

    type_rows = []

    for (
        category,
        statement_type,
    ), count in sorted(
        type_counts.items(),
        key=lambda item: (
            (
                "reference_only",
                "reference_plus_semantic_fact",
                "unresolved_rendering",
            ).index(
                item[0][0]
            ),
            -item[1],
            item[0][1],
        ),
    ):
        type_rows.append(
            {
                "classification": (
                    category
                ),
                "statement_type": (
                    statement_type
                ),
                "occurrences": (
                    count
                ),
                "affected_groups": (
                    len(
                        type_groups[
                            (
                                category,
                                statement_type,
                            )
                        ]
                    )
                ),
            }
        )

    _write_csv(
        OUTPUT_DIR
        / "reference_leaf_occurrences.csv",
        (
            "n",
            "k",
            "group",
            "node_index",
            "statement_type",
            "reference_label",
            "reference_locator",
            "classification",
            "classification_reason",
            "provenance_only",
            "fallback_kind",
            "inference_rule_name",
            "generic_rendering",
        ),
        occurrence_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "reference_leaf_category_summary.csv",
        (
            "classification",
            "occurrences",
            "statement_types",
            "affected_groups",
        ),
        category_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "reference_leaf_by_statement_type.csv",
        (
            "classification",
            "statement_type",
            "occurrences",
            "affected_groups",
        ),
        type_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "exception_inventory.csv",
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
        (
            "Phase 153-R2 follow-up — "
            "Reference / Semantic Fact All-Group Audit"
        ),
        "=" * 78,
        (
            "scope: n=2..15, k=0..7, "
            "depth=2, semantic closure"
        ),
        (
            "production changes: none"
        ),
        "",
        (
            "groups: "
            + str(
                totals[
                    "groups"
                ]
            )
        ),
        (
            "exceptions: "
            + str(
                len(
                    exceptions
                )
            )
        ),
        (
            "presentation nodes: "
            + str(
                totals[
                    "nodes"
                ]
            )
        ),
        (
            "reference-bearing leaf premises: "
            + str(
                totals[
                    "reference_leaf_occurrences"
                ]
            )
        ),
        "",
        "Classification:",
    ]

    for row in category_rows:
        summary.append(
            "  "
            + row[
                "classification"
            ]
            + ": occurrences="
            + str(
                row[
                    "occurrences"
                ]
            )
            + ", statement_types="
            + str(
                row[
                    "statement_types"
                ]
            )
            + ", affected_groups="
            + str(
                row[
                    "affected_groups"
                ]
            )
        )

    summary.extend(
        [
            "",
            "Decision rule:",
            (
                "  provenance-only statement "
                "-> reference_only"
            ),
            (
                "  non-provenance-only + "
                "meaningful generic rendering "
                "-> reference_plus_semantic_fact"
            ),
            (
                "  non-provenance-only + "
                "generic fallback "
                "-> unresolved_rendering"
            ),
            "",
            "By statement type:",
        ]
    )

    for row in type_rows:
        summary.append(
            "  "
            + row[
                "classification"
            ]
            + " | "
            + row[
                "statement_type"
            ]
            + ": occurrences="
            + str(
                row[
                    "occurrences"
                ]
            )
            + ", affected_groups="
            + str(
                row[
                    "affected_groups"
                ]
            )
        )

    summary.extend(
        [
            "",
            "Output files:",
            "  reference_leaf_occurrences.csv",
            "  reference_leaf_category_summary.csv",
            "  reference_leaf_by_statement_type.csv",
            "  exception_inventory.csv",
            "  reference_leaf_summary.txt",
            "=" * 78,
        ]
    )

    summary_text = (
        "\n".join(
            summary
        )
        + "\n"
    )

    (
        OUTPUT_DIR
        / "reference_leaf_summary.txt"
    ).write_text(
        summary_text,
        encoding="utf-8",
    )

    print(
        summary_text
    )

    if (
        totals[
            "groups"
        ]
        != EXPECTED_GROUPS
        or exceptions
    ):
        print(
            "FAIL: 112-group audit population "
            "was not reproduced."
        )
        return 1

    partition_total = (
        totals[
            "reference_only"
        ]
        + totals[
            "reference_plus_semantic_fact"
        ]
        + totals[
            "unresolved_rendering"
        ]
    )

    if (
        partition_total
        != totals[
            "reference_leaf_occurrences"
        ]
    ):
        print(
            "FAIL: reference-leaf classification "
            "does not partition the population."
        )
        return 1

    print(
        "PASS: all reference-bearing leaf premises "
        "were classified without changing "
        "production behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
