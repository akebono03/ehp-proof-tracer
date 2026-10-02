from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


DURATION_RE = re.compile(
    r"^(?P<seconds>\d+(?:\.\d+)?)s\s+"
    r"(?P<phase>call|setup|teardown)\s+"
    r"(?P<nodeid>tests/[^\s]+::[^\s]+)\s*$"
)


@dataclass(frozen=True)
class ReviewRow:
    nodeid: str
    file: str
    function: str
    phase_family: str
    measured_seconds: float | None
    runtime_class: str
    source_assert_count: int
    all_group_scan: bool
    representative_builder: bool
    aggregate_builder: bool
    provenance_signal: bool
    order_signal: bool
    reference_signal: bool
    recommendation: str
    rationale: str


def _duration_map(
    log_text: str,
) -> dict[str, float]:
    result: dict[str, float] = {}

    for line in log_text.splitlines():
        match = DURATION_RE.match(
            line.strip()
        )
        if not match:
            continue

        nodeid = match.group(
            "nodeid"
        )
        seconds = float(
            match.group(
                "seconds"
            )
        )
        previous = result.get(
            nodeid
        )

        if (
            previous is None
            or seconds > previous
        ):
            result[
                nodeid
            ] = seconds

    return result


def _runtime_class(
    seconds: float | None,
) -> str:
    if seconds is None:
        return "UNMEASURED_TOP50"

    if seconds >= 120.0:
        return "EXTREME_120S_PLUS"

    if seconds >= 30.0:
        return "VERY_HEAVY_30S_PLUS"

    if seconds >= 10.0:
        return "HEAVY_10S_PLUS"

    if seconds >= 5.0:
        return "MODERATE_5S_PLUS"

    return "LIGHT_UNDER_5S"


def _phase_family(
    relative_file: str,
) -> str:
    name = Path(
        relative_file
    ).name

    for prefix in (
        "test_phase153_",
        "test_phase98_",
        "test_phase97_",
        "test_phase96_",
        "test_phase95_",
    ):
        if name.startswith(
            prefix
        ):
            return prefix[
                len(
                    "test_"
                ):
                -1
            ].upper()

    return "OTHER"


def _function_source(
    path: Path,
    function_name: str,
) -> tuple[str, int]:
    source = path.read_text(
        encoding="utf-8-sig"
    )
    tree = ast.parse(
        source
    )

    for node in tree.body:
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == function_name
        ):
            if node.end_lineno is None:
                raise RuntimeError(
                    "AST end_lineno unavailable: "
                    + function_name
                )

            lines = source.splitlines()
            function_source = "\n".join(
                lines[
                    node.lineno - 1:
                    node.end_lineno
                ]
            )
            assert_count = sum(
                isinstance(
                    child,
                    ast.Assert,
                )
                for child in ast.walk(
                    node
                )
            )
            return (
                function_source,
                assert_count,
            )

    raise RuntimeError(
        "Function not found: "
        + function_name
        + " in "
        + str(
            path
        )
    )


def _review_row(
    *,
    repo_root: Path,
    nodeid: str,
    durations: dict[str, float],
) -> ReviewRow:
    relative_file, function_name = nodeid.split(
        "::",
        1,
    )
    path = (
        repo_root
        / relative_file
    )

    function_source, assert_count = (
        _function_source(
            path,
            function_name,
        )
    )

    file_source = path.read_text(
        encoding="utf-8-sig"
    )
    family = _phase_family(
        relative_file
    )
    measured_seconds = durations.get(
        nodeid
    )
    runtime_class = _runtime_class(
        measured_seconds
    )

    all_group_scan = (
        "range(" in function_source
        and "build_standard_toda_report" in file_source
    ) or (
        "all_112" in function_name
    ) or (
        "112" in function_name
    )

    representative_builder = any(
        token in function_source
        for token in (
            "build_phase95_20_data",
            "build_phase98_3_data",
        )
    )

    aggregate_builder = any(
        token in function_source
        for token in (
            "build_phase73_8e_data",
            "build_phase75_9_data",
            "build_phase65_9_data",
        )
    )

    lower = (
        function_name
        + "\n"
        + function_source
    ).lower()

    provenance_signal = any(
        token in lower
        for token in (
            "goal_source",
            "source_entry",
            "repository_source",
            "provenance",
        )
    )

    order_signal = any(
        token in lower
        for token in (
            "registration_order",
            "preserve_goal_source_order",
            "candidate_identity_and_order",
            "candidates[",
        )
    )

    reference_signal = any(
        token in lower
        for token in (
            "reference",
            "[r",
            "selected_statement",
        )
    )

    if runtime_class == "EXTREME_120S_PLUS":
        recommendation = (
            "LIGHTWEIGHT_REPLACE"
        )
        rationale = (
            "The test protects a small contract but takes at least two minutes. "
            "Replace heavy integration builders with minimal synthetic repository/"
            "candidate objects that preserve the same provenance or order contract."
        )
    elif (
        family == "PHASE153"
        and all_group_scan
    ):
        recommendation = "AUDIT_ONLY"
        rationale = (
            "This is a cross-group Reference/Narrative population audit. "
            "Keep the population check out of routine regression and retain "
            "small focused renderer/selection contracts routinely."
        )
    elif (
        family in {
            "PHASE95",
            "PHASE96",
            "PHASE97",
            "PHASE98",
        }
        and (
            representative_builder
            or aggregate_builder
        )
        and (
            provenance_signal
            or order_signal
        )
    ):
        recommendation = (
            "LIGHTWEIGHT_REPLACE"
        )
        rationale = (
            "The asserted contract is identity/order/provenance, while the test "
            "constructs a large historical integration fixture. Replace the "
            "fixture with the minimal object graph needed by the current API."
        )
    elif family == "PHASE153":
        recommendation = (
            "KEEP_ROUTINE_CANDIDATE"
        )
        rationale = (
            "This appears to be a focused current Reference contract rather than "
            "a full population scan. Keep unless later redundancy review proves "
            "the same assertion is covered elsewhere."
        )
    else:
        recommendation = (
            "KEEP_ROUTINE_CANDIDATE"
        )
        rationale = (
            "No evidence from runtime/source shape alone justifies deletion or "
            "audit-only treatment. Preserve until an assertion-level replacement "
            "or overlap is proven."
        )

    return ReviewRow(
        nodeid=nodeid,
        file=relative_file,
        function=function_name,
        phase_family=family,
        measured_seconds=measured_seconds,
        runtime_class=runtime_class,
        source_assert_count=assert_count,
        all_group_scan=all_group_scan,
        representative_builder=representative_builder,
        aggregate_builder=aggregate_builder,
        provenance_signal=provenance_signal,
        order_signal=order_signal,
        reference_signal=reference_signal,
        recommendation=recommendation,
        rationale=rationale,
    )


def _markdown(
    rows: tuple[ReviewRow, ...],
) -> str:
    by_family = Counter(
        row.phase_family
        for row in rows
    )
    by_recommendation = Counter(
        row.recommendation
        for row in rows
    )
    by_runtime = Counter(
        row.runtime_class
        for row in rows
    )

    lines = [
        "# Phase 155 Closure-R2C-R1 CONTRACT_SENSITIVE review",
        "",
        "## Boundary",
        "",
        "- Reviewed nodeids: 24",
        "- Repository tests executed: 0",
        "- Production changes: none",
        "- Existing test changes: none",
        "",
        "## Phase-family counts",
        "",
        "```text",
    ]

    for key, count in sorted(
        by_family.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Recommendation counts",
            "",
            "```text",
        ]
    )

    for key, count in sorted(
        by_recommendation.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Runtime counts",
            "",
            "```text",
        ]
    )

    for key, count in sorted(
        by_runtime.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Priority",
            "",
            "The first repair target is every `EXTREME_120S_PLUS` test. "
            "These tests must not be rerun before replacement.",
            "",
            "| seconds | family | recommendation | nodeid |",
            "| ---: | --- | --- | --- |",
        ]
    )

    measured = tuple(
        row
        for row in rows
        if row.measured_seconds
        is not None
    )

    for row in sorted(
        measured,
        key=lambda item: (
            -(
                item.measured_seconds
                or 0.0
            ),
            item.nodeid,
        ),
    ):
        lines.append(
            "| "
            + f"{row.measured_seconds:.2f}"
            + " | "
            + row.phase_family
            + " | "
            + row.recommendation
            + " | `"
            + row.nodeid
            + "` |"
        )

    lines.extend(
        [
            "",
            "## Per-test review",
            "",
        ]
    )

    for row in rows:
        lines.append(
            "### `"
            + row.nodeid
            + "`"
        )
        lines.append("")
        lines.append(
            "- family: `"
            + row.phase_family
            + "`"
        )
        lines.append(
            "- runtime: `"
            + row.runtime_class
            + "`"
        )
        lines.append(
            "- recommendation: `"
            + row.recommendation
            + "`"
        )
        lines.append(
            "- source assert count: "
            + str(
                row.source_assert_count
            )
        )
        lines.append(
            "- signals: "
            + ", ".join(
                key
                for key, active in (
                    (
                        "all_group_scan",
                        row.all_group_scan,
                    ),
                    (
                        "representative_builder",
                        row.representative_builder,
                    ),
                    (
                        "aggregate_builder",
                        row.aggregate_builder,
                    ),
                    (
                        "provenance",
                        row.provenance_signal,
                    ),
                    (
                        "order",
                        row.order_signal,
                    ),
                    (
                        "reference",
                        row.reference_signal,
                    ),
                )
                if active
            )
        )
        lines.append(
            "- rationale: "
            + row.rationale
        )
        lines.append("")

    lines.extend(
        [
            "## Next repair boundary",
            "",
            "1. Replace the three extreme Phase95/97 tests first with minimal "
            "synthetic contracts.",
            "2. Separate Phase153 all-group population scans into audit-only.",
            "3. Review the remaining focused contract tests for overlap only "
            "after the extreme tests are removed.",
            "4. Do not run the repository-wide suite during R2C.",
            "",
        ]
    )

    return "\n".join(
        lines
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "phase155_closure_r2_output/"
            "contract_sensitive_nodeids.txt"
        ),
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path(
            "phase155_closure_output/"
            "phase155_full_pytest.log"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_closure_r2c_r1_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    manifest_path = (
        args.manifest
        if args.manifest.is_absolute()
        else repo_root
        / args.manifest
    )
    log_path = (
        args.log
        if args.log.is_absolute()
        else repo_root
        / args.log
    )
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )

    if not manifest_path.exists():
        raise SystemExit(
            "CONTRACT_SENSITIVE manifest not found: "
            + str(
                manifest_path
            )
        )

    if not log_path.exists():
        raise SystemExit(
            "Full-suite log not found: "
            + str(
                log_path
            )
        )

    nodeids = tuple(
        line.strip()
        for line in manifest_path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )

    if len(
        nodeids
    ) != 24:
        raise SystemExit(
            "Expected 24 CONTRACT_SENSITIVE nodeids; "
            f"found {len(nodeids)}"
        )

    if len(
        set(
            nodeids
        )
    ) != 24:
        raise SystemExit(
            "CONTRACT_SENSITIVE manifest contains duplicates."
        )

    durations = _duration_map(
        log_path.read_text(
            encoding="utf-8",
            errors="replace",
        )
    )

    rows = tuple(
        _review_row(
            repo_root=repo_root,
            nodeid=nodeid,
            durations=durations,
        )
        for nodeid in nodeids
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = {
        "reviewed_nodeids": len(
            rows
        ),
        "repository_tests_executed": 0,
        "production_changes": False,
        "existing_test_changes": False,
        "phase_family_counts": dict(
            Counter(
                row.phase_family
                for row in rows
            )
        ),
        "runtime_counts": dict(
            Counter(
                row.runtime_class
                for row in rows
            )
        ),
        "recommendation_counts": dict(
            Counter(
                row.recommendation
                for row in rows
            )
        ),
        "rows": [
            asdict(
                row
            )
            for row in rows
        ],
    }

    (
        output_dir
        / "phase155_closure_r2c_r1_review.json"
    ).write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_closure_r2c_r1_review.md"
    ).write_text(
        _markdown(
            rows
        ),
        encoding="utf-8",
    )

    for recommendation in (
        "LIGHTWEIGHT_REPLACE",
        "AUDIT_ONLY",
        "KEEP_ROUTINE_CANDIDATE",
    ):
        (
            output_dir
            / (
                recommendation.lower()
                + ".txt"
            )
        ).write_text(
            "".join(
                row.nodeid
                + "\n"
                for row in rows
                if row.recommendation
                == recommendation
            ),
            encoding="utf-8",
        )

    extreme = tuple(
        row
        for row in rows
        if row.runtime_class
        == "EXTREME_120S_PLUS"
    )

    (
        output_dir
        / "extreme_runtime_nodeids.txt"
    ).write_text(
        "".join(
            row.nodeid
            + "\n"
            for row in extreme
        ),
        encoding="utf-8",
    )

    print(
        "Phase 155 Closure-R2C-R1 CONTRACT_SENSITIVE static review"
    )
    print(
        "Reviewed nodeids:",
        len(
            rows
        ),
    )
    print(
        "Repository tests executed: 0"
    )
    print(
        "Production changes: none"
    )
    print(
        "Existing test changes: none"
    )
    print("")

    print(
        "Phase families:"
    )
    for key, count in sorted(
        Counter(
            row.phase_family
            for row in rows
        ).items()
    ):
        print(
            f"  {key}: {count}"
        )

    print("")
    print(
        "Recommendations:"
    )
    for key, count in sorted(
        Counter(
            row.recommendation
            for row in rows
        ).items()
    ):
        print(
            f"  {key}: {count}"
        )

    print("")
    print(
        "Extreme 120s+ tests:",
        len(
            extreme
        ),
    )
    for row in sorted(
        extreme,
        key=lambda item: -(
            item.measured_seconds
            or 0.0
        ),
    ):
        print(
            " ",
            f"{row.measured_seconds:.2f}s",
            row.nodeid,
        )

    if len(
        extreme
    ) != 3:
        raise SystemExit(
            "Expected exactly the three known extreme tests; "
            f"found {len(extreme)}"
        )

    print("")
    print(
        "R2C-R1 validated: True"
    )
    print(
        "No CONTRACT_SENSITIVE test body was executed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
