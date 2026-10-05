from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
import sys
import traceback


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(REPO_ROOT),
    )


N_RANGE = range(2, 16)
K_RANGE = range(0, 8)
MAX_DEPTH = 2
EXPECTED_GROUP_COUNT = 112
OUTPUT_DIR = PACKAGE_DIR / "output"

TITLE = "# Group proof narrative"
TARGET_HEADER = "## 証明対象"
REFERENCE_HEADER = "## 使用する結果"
PROOF_HEADER = "## 証明"
QED_MARKER = "□"


def _group_label(n: int, k: int) -> str:
    return f"pi_{n + k}^{n}"


def _route_hint(n: int, k: int) -> str:
    if n == 8 and k == 7:
        return "phase134_24_pi15_8_dedicated"
    if n == 5 and k == 3:
        return "phase134_9_pi8_5_dedicated"
    if n == 3 and k == 3:
        return "pi6_3_generic_semantic"
    if (n, k) in {
        (4, 6),
        (5, 7),
        (9, 7),
    }:
        return "phase150_rc4_generic_public_wrapper"
    return "default_public_renderer"


def _index_or_none(
    lines: list[str],
    marker: str,
) -> int | None:
    try:
        return lines.index(
            marker
        )
    except ValueError:
        return None


def _inspect_rendered(
    rendered: str,
) -> dict[str, object]:
    lines = rendered.splitlines()

    title_index = _index_or_none(
        lines,
        TITLE,
    )
    target_index = _index_or_none(
        lines,
        TARGET_HEADER,
    )
    reference_index = _index_or_none(
        lines,
        REFERENCE_HEADER,
    )
    proof_index = _index_or_none(
        lines,
        PROOF_HEADER,
    )

    nonempty_lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]
    ends_with_qed = bool(
        nonempty_lines
        and nonempty_lines[-1]
        == QED_MARKER
    )

    section_indices = [
        index
        for index in (
            target_index,
            reference_index,
            proof_index,
        )
        if index is not None
    ]
    section_order_is_monotone = (
        section_indices
        == sorted(
            section_indices
        )
    )

    target_before_reference = (
        target_index is not None
        and reference_index is not None
        and target_index < reference_index
    )
    reference_before_proof = (
        reference_index is not None
        and proof_index is not None
        and reference_index < proof_index
    )
    target_before_proof = (
        target_index is not None
        and proof_index is not None
        and target_index < proof_index
    )

    full_contract = (
        title_index is not None
        and target_before_reference
        and reference_before_proof
        and ends_with_qed
    )

    missing_sections = []

    if title_index is None:
        missing_sections.append(
            "title"
        )
    if target_index is None:
        missing_sections.append(
            "target"
        )
    if reference_index is None:
        missing_sections.append(
            "reference"
        )
    if proof_index is None:
        missing_sections.append(
            "proof"
        )
    if not ends_with_qed:
        missing_sections.append(
            "qed"
        )

    return {
        "has_title": title_index is not None,
        "has_target": target_index is not None,
        "has_reference": reference_index is not None,
        "has_proof": proof_index is not None,
        "ends_with_qed": ends_with_qed,
        "section_order_is_monotone": (
            section_order_is_monotone
        ),
        "target_before_reference": (
            target_before_reference
        ),
        "reference_before_proof": (
            reference_before_proof
        ),
        "target_before_proof": (
            target_before_proof
        ),
        "full_contract": full_contract,
        "missing_sections": ",".join(
            missing_sections
        ),
        "line_count": len(
            lines
        ),
        "char_count": len(
            rendered
        ),
    }


def _render_group(
    n: int,
    k: int,
) -> str:
    from toda_calculation_facade import (
        build_standard_toda_report,
    )
    from toda_group_proof_narrative_renderer import (
        render_toda_group_proof_narrative_markdown,
    )
    from toda_group_proof_presentation import (
        build_toda_group_proof_presentation,
    )
    from toda_group_result_proof_replay import (
        build_toda_group_result_proof_replay,
    )

    report = build_standard_toda_report(
        n=n,
        k=k,
    )

    if not report.candidates:
        raise RuntimeError(
            "standard report has no candidates "
            f"for n={n}, k={k}"
        )

    group_result = (
        report.candidates[0]
        .source_candidate
        .group_result
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
        render_toda_group_proof_narrative_markdown(
            presentation
        )
    )


def _write_csv(
    path: Path,
    rows: list[dict[str, object]],
    fieldnames: tuple[str, ...],
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

        for row in rows:
            writer.writerow(
                {
                    field: row.get(
                        field,
                        "",
                    )
                    for field in fieldnames
                }
            )


def main() -> int:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows: list[
        dict[str, object]
    ] = []
    exceptions: list[
        dict[str, object]
    ] = []
    totals = Counter()
    route_totals: dict[
        str,
        Counter,
    ] = {}

    for n in N_RANGE:
        for k in K_RANGE:
            totals[
                "groups"
            ] += 1

            label = _group_label(
                n,
                k,
            )
            route_hint = _route_hint(
                n,
                k,
            )

            try:
                rendered = _render_group(
                    n,
                    k,
                )
                inspection = (
                    _inspect_rendered(
                        rendered
                    )
                )

                row = {
                    "n": n,
                    "k": k,
                    "group": label,
                    "route_hint": route_hint,
                    **inspection,
                }
                rows.append(
                    row
                )

                for key in (
                    "has_title",
                    "has_target",
                    "has_reference",
                    "has_proof",
                    "ends_with_qed",
                    "full_contract",
                ):
                    if inspection[
                        key
                    ]:
                        totals[
                            key
                        ] += 1

                if not inspection[
                    "section_order_is_monotone"
                ]:
                    totals[
                        "non_monotone_section_order"
                    ] += 1

                route_counter = (
                    route_totals.setdefault(
                        route_hint,
                        Counter(),
                    )
                )
                route_counter[
                    "groups"
                ] += 1

                for key in (
                    "has_target",
                    "has_reference",
                    "has_proof",
                    "ends_with_qed",
                    "full_contract",
                ):
                    if inspection[
                        key
                    ]:
                        route_counter[
                            key
                        ] += 1

            except Exception as exc:
                totals[
                    "exceptions"
                ] += 1

                exceptions.append(
                    {
                        "n": n,
                        "k": k,
                        "group": label,
                        "route_hint": route_hint,
                        "exception_type": (
                            type(
                                exc
                            ).__name__
                        ),
                        "message": str(
                            exc
                        ),
                        "traceback": (
                            traceback.format_exc()
                        ),
                    }
                )

    fieldnames = (
        "n",
        "k",
        "group",
        "route_hint",
        "has_title",
        "has_target",
        "has_reference",
        "has_proof",
        "ends_with_qed",
        "section_order_is_monotone",
        "target_before_reference",
        "reference_before_proof",
        "target_before_proof",
        "full_contract",
        "missing_sections",
        "line_count",
        "char_count",
    )

    _write_csv(
        OUTPUT_DIR
        / "narrative_public_contract_inventory.csv",
        rows,
        fieldnames,
    )

    _write_csv(
        OUTPUT_DIR
        / "exception_inventory.csv",
        exceptions,
        (
            "n",
            "k",
            "group",
            "route_hint",
            "exception_type",
            "message",
            "traceback",
        ),
    )

    defect_rows = [
        row
        for row in rows
        if not bool(
            row[
                "full_contract"
            ]
        )
    ]

    _write_csv(
        OUTPUT_DIR
        / "narrative_public_contract_defects.csv",
        defect_rows,
        fieldnames,
    )

    summary_lines = [
        "=" * 78,
        (
            "Phase 158-R1 repair1 - "
            "Narrative Public Contract Inventory"
        ),
        "=" * 78,
        "scope: n=2..15, k=0..7, depth=2",
        "production changes: none",
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
            "rendered without exception: "
            + str(
                len(
                    rows
                )
            )
        ),
        (
            "exceptions: "
            + str(
                totals[
                    "exceptions"
                ]
            )
        ),
        (
            "has # Group proof narrative: "
            + str(
                totals[
                    "has_title"
                ]
            )
        ),
        (
            "has ## 証明対象: "
            + str(
                totals[
                    "has_target"
                ]
            )
        ),
        (
            "has ## 使用する結果: "
            + str(
                totals[
                    "has_reference"
                ]
            )
        ),
        (
            "has ## 証明: "
            + str(
                totals[
                    "has_proof"
                ]
            )
        ),
        (
            "ends with □: "
            + str(
                totals[
                    "ends_with_qed"
                ]
            )
        ),
        (
            "full public contract: "
            + str(
                totals[
                    "full_contract"
                ]
            )
        ),
        (
            "non-monotone section order: "
            + str(
                totals[
                    "non_monotone_section_order"
                ]
            )
        ),
        "",
        "Route hints:",
    ]

    for route_hint in sorted(
        route_totals
    ):
        counter = route_totals[
            route_hint
        ]
        summary_lines.extend(
            (
                f"  {route_hint}:",
                (
                    "    groups: "
                    + str(
                        counter[
                            "groups"
                        ]
                    )
                ),
                (
                    "    has target: "
                    + str(
                        counter[
                            "has_target"
                        ]
                    )
                ),
                (
                    "    has reference: "
                    + str(
                        counter[
                            "has_reference"
                        ]
                    )
                ),
                (
                    "    has proof: "
                    + str(
                        counter[
                            "has_proof"
                        ]
                    )
                ),
                (
                    "    ends with QED: "
                    + str(
                        counter[
                            "ends_with_qed"
                        ]
                    )
                ),
                (
                    "    full contract: "
                    + str(
                        counter[
                            "full_contract"
                        ]
                    )
                ),
            )
        )

    summary_lines.extend(
        (
            "",
            (
                "Expected Phase 158 "
                "public contract:"
            ),
            "  # Group proof narrative",
            "  ## 証明対象",
            "  ## 使用する結果",
            "  ---",
            "  ## 証明",
            "  ...",
            "  □",
            "",
            "R1 interpretation:",
            (
                "  This inventory records the "
                "current public structure only. "
                "It does not modify renderer behavior."
            ),
            (
                "  Missing ## 証明対象 is a "
                "Phase 158 defect even when the "
                "mathematical proof body itself is correct."
            ),
            (
                "  Reference attribution, "
                "proof-internal/fixed-statement "
                "classification, and mathematical "
                "derivations are out of scope."
            ),
            "",
            "Output files:",
            (
                "  "
                "narrative_public_contract_inventory.csv"
            ),
            (
                "  "
                "narrative_public_contract_defects.csv"
            ),
            "  exception_inventory.csv",
            (
                "  "
                "narrative_public_contract_summary.txt"
            ),
            "=" * 78,
        )
    )

    summary = "\n".join(
        summary_lines
    ) + "\n"

    print(
        summary
    )

    (
        OUTPUT_DIR
        / "narrative_public_contract_summary.txt"
    ).write_text(
        summary,
        encoding="utf-8-sig",
    )

    if totals[
        "groups"
    ] != EXPECTED_GROUP_COUNT:
        print(
            "FAIL: group count differs "
            "from the 112-group audit scope."
        )
        return 1

    if totals[
        "exceptions"
    ]:
        print(
            "AUDIT COMPLETE WITH EXCEPTIONS: "
            "inspect exception_inventory.csv."
        )
        return 1

    print(
        "AUDIT COMPLETE: current public-contract "
        "differences were recorded. "
        "Production behavior was not changed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
