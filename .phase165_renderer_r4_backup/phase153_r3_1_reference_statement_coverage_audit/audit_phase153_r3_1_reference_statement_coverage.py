from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
    _render_group_proof_narrative_latex,
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_references import (
    build_toda_group_proof_narrative_reference_entries,
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

OUTPUT_DIR = Path(__file__).resolve().parent / "audit_output"


def _group_label(n: int, k: int) -> str:
    return "pi_" + str(n + k) + "^" + str(n)


def _context(n: int, k: int):
    report = build_standard_toda_report(
        n=n,
        k=k,
    )

    if not report.candidates:
        raise AssertionError(
            "no report candidate for n="
            + str(n)
            + ", k="
            + str(k)
        )

    group_result = (
        report.candidates[0]
        .source_candidate
        .group_result
    )

    replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=MAX_DEPTH,
    )

    presentation = build_toda_group_proof_presentation(
        replay
    )

    semantic_presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
            presentation
        )
    )

    rendered = render_toda_group_proof_narrative_markdown(
        presentation
    )

    return semantic_presentation, rendered


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


def _candidate_statement(step) -> tuple[str | None, str, str]:
    latex = _render_group_proof_narrative_latex(
        step
    )

    if latex is not None:
        return (
            "$" + latex + "$",
            "narrative_latex",
            "",
        )

    rendered = _render_generic_narrative_step(
        step
    )
    fallback_kind = _fallback_kind(
        step,
        rendered,
    )

    if fallback_kind is None:
        return (
            rendered,
            "generic_semantic",
            "",
        )

    return (
        None,
        "unresolved",
        fallback_kind,
    )


def _normalize_for_duplicate_check(text: str) -> str:
    normalized = text
    normalized = normalized.replace("\\[", "$")
    normalized = normalized.replace("\\]", "$")
    normalized = normalized.replace("$$", "$")
    normalized = re.sub(r"\s+", "", normalized)
    normalized = normalized.replace("**", "")
    normalized = normalized.replace("`", "")
    return normalized


def _statement_is_duplicated_in_body(
    statement: str,
    rendered_narrative: str,
) -> bool:
    needle = _normalize_for_duplicate_check(
        statement
    )
    haystack = _normalize_for_duplicate_check(
        rendered_narrative
    )

    if not needle:
        return False

    return needle in haystack


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
        writer.writerows(rows)


def main() -> int:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    totals = Counter()
    classification_groups = defaultdict(set)
    statement_type_counts = Counter()
    statement_type_groups = defaultdict(set)

    entry_rows = []
    statement_rows = []
    exceptions = []

    for n in N_RANGE:
        for k in K_RANGE:
            group = _group_label(
                n,
                k,
            )

            try:
                presentation, rendered_narrative = _context(
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

            totals["groups"] += 1
            totals["presentation_nodes"] += len(
                presentation.nodes
            )

            entries = (
                build_toda_group_proof_narrative_reference_entries(
                    presentation
                )
            )

            totals["reference_entries"] += len(
                entries
            )

            for entry in entries:
                title = (
                    entry.reference.locator
                    or entry.reference.label
                )

                candidates = []
                unresolved = []
                statement_types = []

                for step in entry.proof_steps:
                    statement_type = type(
                        step.conclusion
                    ).__name__
                    statement_types.append(
                        statement_type
                    )

                    (
                        candidate,
                        source,
                        unresolved_kind,
                    ) = _candidate_statement(
                        step
                    )

                    if candidate is not None:
                        candidates.append(
                            (
                                candidate,
                                source,
                                statement_type,
                                step,
                            )
                        )
                    else:
                        unresolved.append(
                            (
                                unresolved_kind,
                                statement_type,
                                step,
                            )
                        )

                distinct_candidates = []
                seen_candidates = set()

                for item in candidates:
                    candidate = item[0]
                    normalized = (
                        _normalize_for_duplicate_check(
                            candidate
                        )
                    )
                    if normalized in seen_candidates:
                        continue
                    seen_candidates.add(
                        normalized
                    )
                    distinct_candidates.append(
                        item
                    )

                duplicated_candidates = [
                    item
                    for item in distinct_candidates
                    if _statement_is_duplicated_in_body(
                        item[0],
                        rendered_narrative,
                    )
                ]

                if distinct_candidates:
                    classification = (
                        "reference_plus_statement"
                    )
                elif unresolved:
                    classification = (
                        "unresolved_rendering"
                    )
                else:
                    classification = (
                        "reference_only"
                    )

                if duplicated_candidates:
                    duplicate_case = (
                        "statement_duplicates_body"
                    )
                else:
                    duplicate_case = (
                        "no_exact_body_duplicate"
                    )

                totals[classification] += 1
                totals[duplicate_case] += 1
                classification_groups[
                    classification
                ].add(group)

                entry_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "group": group,
                        "reference_number": entry.number,
                        "reference_label": (
                            entry.reference.label
                        ),
                        "reference_locator": (
                            entry.reference.locator
                            or ""
                        ),
                        "reference_title": title,
                        "proof_step_count": len(
                            entry.proof_steps
                        ),
                        "statement_candidate_count": len(
                            distinct_candidates
                        ),
                        "unresolved_step_count": len(
                            unresolved
                        ),
                        "classification": classification,
                        "body_duplicate_classification": (
                            duplicate_case
                        ),
                        "statement_types": " | ".join(
                            statement_types
                        ),
                    }
                )

                for (
                    candidate,
                    source,
                    statement_type,
                    step,
                ) in distinct_candidates:
                    duplicate = (
                        _statement_is_duplicated_in_body(
                            candidate,
                            rendered_narrative,
                        )
                    )

                    totals[
                        "statement_candidates"
                    ] += 1
                    totals[
                        "duplicated_statement_candidates"
                        if duplicate
                        else "nonduplicated_statement_candidates"
                    ] += 1

                    statement_type_counts[
                        statement_type
                    ] += 1
                    statement_type_groups[
                        statement_type
                    ].add(group)

                    statement_rows.append(
                        {
                            "n": n,
                            "k": k,
                            "group": group,
                            "reference_number": entry.number,
                            "reference_title": title,
                            "statement_type": (
                                statement_type
                            ),
                            "render_source": source,
                            "duplicates_body": duplicate,
                            "candidate_statement": (
                                candidate
                            ),
                            "inference_rule_name": (
                                step.inference_rule.name
                                if (
                                    step.inference_rule
                                    is not None
                                )
                                else ""
                            ),
                        }
                    )

    category_rows = []
    for classification in (
        "reference_only",
        "reference_plus_statement",
        "unresolved_rendering",
    ):
        category_rows.append(
            {
                "classification": classification,
                "entries": totals[
                    classification
                ],
                "affected_groups": len(
                    classification_groups[
                        classification
                    ]
                ),
            }
        )

    type_rows = []
    for statement_type, count in sorted(
        statement_type_counts.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    ):
        type_rows.append(
            {
                "statement_type": statement_type,
                "candidate_occurrences": count,
                "affected_groups": len(
                    statement_type_groups[
                        statement_type
                    ]
                ),
            }
        )

    _write_csv(
        OUTPUT_DIR
        / "reference_entry_coverage.csv",
        (
            "n",
            "k",
            "group",
            "reference_number",
            "reference_label",
            "reference_locator",
            "reference_title",
            "proof_step_count",
            "statement_candidate_count",
            "unresolved_step_count",
            "classification",
            "body_duplicate_classification",
            "statement_types",
        ),
        entry_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "reference_statement_candidates.csv",
        (
            "n",
            "k",
            "group",
            "reference_number",
            "reference_title",
            "statement_type",
            "render_source",
            "duplicates_body",
            "candidate_statement",
            "inference_rule_name",
        ),
        statement_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "reference_entry_category_summary.csv",
        (
            "classification",
            "entries",
            "affected_groups",
        ),
        category_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "reference_statement_type_summary.csv",
        (
            "statement_type",
            "candidate_occurrences",
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
            "Phase 153-R3-1 — "
            "112 Groups Reference Statement Coverage Audit"
        ),
        "=" * 78,
        (
            "scope: n=2..15, k=0..7, "
            "depth=2, semantic closure"
        ),
        "production changes: none",
        "",
        "groups: "
        + str(totals["groups"]),
        "exceptions: "
        + str(len(exceptions)),
        "presentation nodes: "
        + str(totals["presentation_nodes"]),
        "reference entries: "
        + str(totals["reference_entries"]),
        "",
        "Reference entry classification:",
    ]

    for row in category_rows:
        summary.append(
            "  "
            + row["classification"]
            + ": entries="
            + str(row["entries"])
            + ", affected_groups="
            + str(row["affected_groups"])
        )

    summary.extend(
        [
            "",
            "Statement candidates:",
            "  total: "
            + str(
                totals["statement_candidates"]
            ),
            "  duplicates_body: "
            + str(
                totals[
                    "duplicated_statement_candidates"
                ]
            ),
            "  no_exact_body_duplicate: "
            + str(
                totals[
                    "nonduplicated_statement_candidates"
                ]
            ),
            "",
            "Reference entries with body duplication:",
            "  statement_duplicates_body: "
            + str(
                totals[
                    "statement_duplicates_body"
                ]
            ),
            "  no_exact_body_duplicate: "
            + str(
                totals[
                    "no_exact_body_duplicate"
                ]
            ),
            "",
            "Decision rule:",
            (
                "  at least one renderable mathematical "
                "candidate -> reference_plus_statement"
            ),
            (
                "  no candidate + unresolved renderer "
                "fallback -> unresolved_rendering"
            ),
            (
                "  no candidate and no unresolved fallback "
                "-> reference_only"
            ),
            (
                "  candidate normalized as an exact substring "
                "of current narrative -> statement_duplicates_body"
            ),
            "",
            "Output files:",
            "  reference_entry_coverage.csv",
            "  reference_statement_candidates.csv",
            "  reference_entry_category_summary.csv",
            "  reference_statement_type_summary.csv",
            "  exception_inventory.csv",
            "  reference_statement_coverage_summary.txt",
            "=" * 78,
        ]
    )

    summary_text = "\n".join(
        summary
    ) + "\n"

    (
        OUTPUT_DIR
        / "reference_statement_coverage_summary.txt"
    ).write_text(
        summary_text,
        encoding="utf-8",
    )

    print(summary_text)

    if (
        totals["groups"] != EXPECTED_GROUPS
        or exceptions
    ):
        print(
            "FAIL: 112-group audit population "
            "was not reproduced."
        )
        return 1

    classified = (
        totals["reference_only"]
        + totals["reference_plus_statement"]
        + totals["unresolved_rendering"]
    )

    if classified != totals["reference_entries"]:
        print(
            "FAIL: reference-entry classification "
            "does not partition the population."
        )
        return 1

    candidate_partition = (
        totals["duplicated_statement_candidates"]
        + totals["nonduplicated_statement_candidates"]
    )

    if (
        candidate_partition
        != totals["statement_candidates"]
    ):
        print(
            "FAIL: statement duplicate classification "
            "does not partition the candidates."
        )
        return 1

    print(
        "PASS: all reference entries were audited "
        "without changing production behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
