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


def _normalize(text: str) -> str:
    normalized = text
    normalized = normalized.replace("\\[", "$")
    normalized = normalized.replace("\\]", "$")
    normalized = normalized.replace("$$", "$")
    normalized = re.sub(r"\s+", "", normalized)
    normalized = normalized.replace("**", "")
    normalized = normalized.replace("`", "")
    return normalized


def _duplicates_body(
    statement: str,
    rendered_narrative: str,
) -> bool:
    needle = _normalize(statement)
    haystack = _normalize(rendered_narrative)

    if not needle:
        return False

    return needle in haystack


def _dependent_count(
    presentation,
    step,
) -> int:
    return sum(
        1
        for edge in presentation.edges
        if edge.premise_step is step
    )


def _selection_class(
    candidate_count: int,
    unresolved_count: int,
) -> str:
    if candidate_count == 0:
        return "unresolved_only"

    if candidate_count == 1 and unresolved_count == 0:
        return "single_candidate"

    if candidate_count == 1:
        return "single_candidate_with_unresolved"

    if unresolved_count == 0:
        return "multiple_candidates"

    return "multiple_candidates_with_unresolved"


def _ownership_class(
    duplicate_flags: tuple[bool, ...],
) -> str:
    if not duplicate_flags:
        return "no_renderable_candidate"

    duplicate_count = sum(
        1
        for flag in duplicate_flags
        if flag
    )

    if duplicate_count == 0:
        return "reference_only_display_candidate"

    if duplicate_count == len(duplicate_flags):
        return "all_candidates_already_in_body"

    return "mixed_reference_body_ownership"


def _dependency_class(
    dependent_counts: tuple[int, ...],
) -> str:
    if not dependent_counts:
        return "no_renderable_candidate"

    used = tuple(
        count > 0
        for count in dependent_counts
    )

    if all(used):
        return "all_candidates_proof_used"

    if any(used):
        return "mixed_proof_usage"

    return "no_candidate_proof_dependents"


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
    selection_totals = Counter()
    ownership_totals = Counter()
    dependency_totals = Counter()
    selection_groups = defaultdict(set)
    ownership_groups = defaultdict(set)
    dependency_groups = defaultdict(set)
    unresolved_type_counts = Counter()
    unresolved_type_groups = defaultdict(set)

    entry_rows = []
    candidate_rows = []
    unresolved_rows = []
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
                seen_candidate_keys = set()

                for step in entry.proof_steps:
                    statement_type = type(
                        step.conclusion
                    ).__name__

                    (
                        candidate,
                        source,
                        unresolved_kind,
                    ) = _candidate_statement(
                        step
                    )

                    if candidate is None:
                        unresolved.append(
                            (
                                unresolved_kind,
                                statement_type,
                                step,
                            )
                        )
                        continue

                    key = _normalize(
                        candidate
                    )

                    if key in seen_candidate_keys:
                        continue

                    seen_candidate_keys.add(
                        key
                    )

                    candidates.append(
                        (
                            candidate,
                            source,
                            statement_type,
                            step,
                        )
                    )

                duplicate_flags = tuple(
                    _duplicates_body(
                        candidate,
                        rendered_narrative,
                    )
                    for (
                        candidate,
                        _,
                        _,
                        _,
                    ) in candidates
                )

                dependent_counts = tuple(
                    _dependent_count(
                        presentation,
                        step,
                    )
                    for (
                        _,
                        _,
                        _,
                        step,
                    ) in candidates
                )

                selection_class = (
                    _selection_class(
                        len(candidates),
                        len(unresolved),
                    )
                )
                ownership_class = (
                    _ownership_class(
                        duplicate_flags
                    )
                )
                dependency_class = (
                    _dependency_class(
                        dependent_counts
                    )
                )

                selection_totals[
                    selection_class
                ] += 1
                ownership_totals[
                    ownership_class
                ] += 1
                dependency_totals[
                    dependency_class
                ] += 1

                selection_groups[
                    selection_class
                ].add(group)
                ownership_groups[
                    ownership_class
                ].add(group)
                dependency_groups[
                    dependency_class
                ].add(group)

                totals[
                    "statement_candidates"
                ] += len(candidates)
                totals[
                    "unresolved_steps"
                ] += len(unresolved)

                entry_rows.append(
                    {
                        "n": n,
                        "k": k,
                        "group": group,
                        "reference_number": entry.number,
                        "reference_title": title,
                        "proof_step_count": len(
                            entry.proof_steps
                        ),
                        "candidate_count": len(
                            candidates
                        ),
                        "unresolved_count": len(
                            unresolved
                        ),
                        "selection_class": (
                            selection_class
                        ),
                        "ownership_class": (
                            ownership_class
                        ),
                        "dependency_class": (
                            dependency_class
                        ),
                        "duplicate_candidate_count": sum(
                            1
                            for flag in duplicate_flags
                            if flag
                        ),
                        "proof_used_candidate_count": sum(
                            1
                            for count in dependent_counts
                            if count > 0
                        ),
                    }
                )

                for candidate_index, (
                    candidate,
                    source,
                    statement_type,
                    step,
                ) in enumerate(
                    candidates,
                    start=1,
                ):
                    duplicate = (
                        duplicate_flags[
                            candidate_index - 1
                        ]
                    )
                    dependent_count = (
                        dependent_counts[
                            candidate_index - 1
                        ]
                    )

                    candidate_rows.append(
                        {
                            "n": n,
                            "k": k,
                            "group": group,
                            "reference_number": (
                                entry.number
                            ),
                            "reference_title": title,
                            "candidate_index": (
                                candidate_index
                            ),
                            "statement_type": (
                                statement_type
                            ),
                            "render_source": source,
                            "duplicates_body": (
                                duplicate
                            ),
                            "dependent_count": (
                                dependent_count
                            ),
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

                for (
                    unresolved_kind,
                    statement_type,
                    step,
                ) in unresolved:
                    unresolved_type_counts[
                        statement_type
                    ] += 1
                    unresolved_type_groups[
                        statement_type
                    ].add(group)

                    unresolved_rows.append(
                        {
                            "n": n,
                            "k": k,
                            "group": group,
                            "reference_number": (
                                entry.number
                            ),
                            "reference_title": title,
                            "statement_type": (
                                statement_type
                            ),
                            "fallback_kind": (
                                unresolved_kind
                            ),
                            "dependent_count": (
                                _dependent_count(
                                    presentation,
                                    step,
                                )
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

    selection_order = (
        "single_candidate",
        "single_candidate_with_unresolved",
        "multiple_candidates",
        "multiple_candidates_with_unresolved",
        "unresolved_only",
    )

    ownership_order = (
        "reference_only_display_candidate",
        "all_candidates_already_in_body",
        "mixed_reference_body_ownership",
        "no_renderable_candidate",
    )

    dependency_order = (
        "all_candidates_proof_used",
        "mixed_proof_usage",
        "no_candidate_proof_dependents",
        "no_renderable_candidate",
    )

    selection_rows = [
        {
            "selection_class": classification,
            "entries": selection_totals[
                classification
            ],
            "affected_groups": len(
                selection_groups[
                    classification
                ]
            ),
        }
        for classification in selection_order
    ]

    ownership_rows = [
        {
            "ownership_class": classification,
            "entries": ownership_totals[
                classification
            ],
            "affected_groups": len(
                ownership_groups[
                    classification
                ]
            ),
        }
        for classification in ownership_order
    ]

    dependency_rows = [
        {
            "dependency_class": classification,
            "entries": dependency_totals[
                classification
            ],
            "affected_groups": len(
                dependency_groups[
                    classification
                ]
            ),
        }
        for classification in dependency_order
    ]

    unresolved_type_rows = [
        {
            "statement_type": statement_type,
            "occurrences": count,
            "affected_groups": len(
                unresolved_type_groups[
                    statement_type
                ]
            ),
        }
        for statement_type, count in sorted(
            unresolved_type_counts.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )
    ]

    _write_csv(
        OUTPUT_DIR
        / "reference_entry_selection_ownership.csv",
        (
            "n",
            "k",
            "group",
            "reference_number",
            "reference_title",
            "proof_step_count",
            "candidate_count",
            "unresolved_count",
            "selection_class",
            "ownership_class",
            "dependency_class",
            "duplicate_candidate_count",
            "proof_used_candidate_count",
        ),
        entry_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "reference_candidate_inventory.csv",
        (
            "n",
            "k",
            "group",
            "reference_number",
            "reference_title",
            "candidate_index",
            "statement_type",
            "render_source",
            "duplicates_body",
            "dependent_count",
            "candidate_statement",
            "inference_rule_name",
        ),
        candidate_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "unresolved_reference_steps.csv",
        (
            "n",
            "k",
            "group",
            "reference_number",
            "reference_title",
            "statement_type",
            "fallback_kind",
            "dependent_count",
            "inference_rule_name",
        ),
        unresolved_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "selection_class_summary.csv",
        (
            "selection_class",
            "entries",
            "affected_groups",
        ),
        selection_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "ownership_class_summary.csv",
        (
            "ownership_class",
            "entries",
            "affected_groups",
        ),
        ownership_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "dependency_class_summary.csv",
        (
            "dependency_class",
            "entries",
            "affected_groups",
        ),
        dependency_rows,
    )

    _write_csv(
        OUTPUT_DIR
        / "unresolved_statement_type_summary.csv",
        (
            "statement_type",
            "occurrences",
            "affected_groups",
        ),
        unresolved_type_rows,
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
            "Phase 153-R3-2 — Reference Statement "
            "Selection / Ownership Audit"
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
        "statement candidates: "
        + str(totals["statement_candidates"]),
        "unresolved steps: "
        + str(totals["unresolved_steps"]),
        "",
        "Selection complexity:",
    ]

    for row in selection_rows:
        summary.append(
            "  "
            + row["selection_class"]
            + ": entries="
            + str(row["entries"])
            + ", affected_groups="
            + str(row["affected_groups"])
        )

    summary.append("")
    summary.append(
        "Current display ownership evidence:"
    )

    for row in ownership_rows:
        summary.append(
            "  "
            + row["ownership_class"]
            + ": entries="
            + str(row["entries"])
            + ", affected_groups="
            + str(row["affected_groups"])
        )

    summary.append("")
    summary.append(
        "Proof-graph usage evidence:"
    )

    for row in dependency_rows:
        summary.append(
            "  "
            + row["dependency_class"]
            + ": entries="
            + str(row["entries"])
            + ", affected_groups="
            + str(row["affected_groups"])
        )

    summary.append("")
    summary.append(
        "Unresolved statement types:"
    )

    if unresolved_type_rows:
        for row in unresolved_type_rows:
            summary.append(
                "  "
                + row["statement_type"]
                + ": occurrences="
                + str(row["occurrences"])
                + ", affected_groups="
                + str(row["affected_groups"])
            )
    else:
        summary.append(
            "  none"
        )

    summary.extend(
        [
            "",
            "Audit interpretation:",
            (
                "  selection_class measures whether one "
                "reference entry has one or several "
                "renderable statement candidates."
            ),
            (
                "  ownership_class records whether the same "
                "rendered statement is already present in "
                "the current narrative body."
            ),
            (
                "  dependency_class records whether candidate "
                "steps are actually consumed by later proof "
                "steps in the proof graph."
            ),
            (
                "  These are audit facts only; R3-2 does not "
                "yet choose or suppress any statement."
            ),
            "",
            "Output files:",
            "  reference_entry_selection_ownership.csv",
            "  reference_candidate_inventory.csv",
            "  unresolved_reference_steps.csv",
            "  selection_class_summary.csv",
            "  ownership_class_summary.csv",
            "  dependency_class_summary.csv",
            "  unresolved_statement_type_summary.csv",
            "  exception_inventory.csv",
            "  reference_selection_ownership_summary.txt",
            "=" * 78,
        ]
    )

    summary_text = "\n".join(
        summary
    ) + "\n"

    (
        OUTPUT_DIR
        / "reference_selection_ownership_summary.txt"
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

    selection_total = sum(
        selection_totals[
            classification
        ]
        for classification in selection_order
    )

    if (
        selection_total
        != totals["reference_entries"]
    ):
        print(
            "FAIL: selection classification "
            "does not partition reference entries."
        )
        return 1

    ownership_total = sum(
        ownership_totals[
            classification
        ]
        for classification in ownership_order
    )

    if (
        ownership_total
        != totals["reference_entries"]
    ):
        print(
            "FAIL: ownership classification "
            "does not partition reference entries."
        )
        return 1

    dependency_total = sum(
        dependency_totals[
            classification
        ]
        for classification in dependency_order
    )

    if (
        dependency_total
        != totals["reference_entries"]
    ):
        print(
            "FAIL: dependency classification "
            "does not partition reference entries."
        )
        return 1

    print(
        "PASS: all reference entries were classified "
        "for selection and ownership without changing "
        "production behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
