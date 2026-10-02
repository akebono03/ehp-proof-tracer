from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


DURATION_RE = re.compile(
    r"^(?P<seconds>\d+(?:\.\d+)?)s\s+"
    r"(?P<phase>call|setup|teardown)\s+"
    r"(?P<nodeid>tests/[^\s]+::[^\s]+)\s*$"
)

SUPERSESSION_HINTS = (
    (
        "test_phase144_6_r5_43_6.py",
        "test_phase144_6_r5_43_11d_final_completion_audit.py",
    ),
    (
        "test_phase144_6_r5_43_8.py",
        "test_phase144_6_r5_43_11d_final_completion_audit.py",
    ),
    (
        "test_phase144_6_r5_43_9.py",
        "test_phase144_6_r5_43_11d_final_completion_audit.py",
    ),
    (
        "test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py",
        "test_phase144_6_r5_43_11d_final_completion_audit.py",
    ),
    (
        "test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py",
        "test_phase144_6_r5_43_11d_final_completion_audit.py",
    ),
)

OVERLAP_STEMS = (
    "r5_43_10",
    "r5_43_11",
    "r5_43_11a",
    "r5_43_11c",
    "r5_43_11d",
)


@dataclass(frozen=True)
class ReviewRow:
    nodeid: str
    file: str
    function: str
    measured_seconds: float | None
    runtime_class: str
    execution_lane: str
    redundancy_class: str
    superseded_by: str | None
    explicit_audit_signal: bool
    cross_group_signal: bool
    fixed_count_signal: bool
    inventory_signal: bool
    production_renderer_signal: bool
    recommendation: str


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


def _function_source(
    path: Path,
    function_name: str,
) -> str:
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
            return "\n".join(
                lines[
                    node.lineno - 1:
                    node.end_lineno
                ]
            )

    raise RuntimeError(
        "Function not found: "
        + function_name
        + " in "
        + str(
            path
        )
    )


def _file_source(
    path: Path,
) -> str:
    return path.read_text(
        encoding="utf-8-sig"
    )


def _superseded_by(
    file_name: str,
) -> str | None:
    for old_name, new_name in SUPERSESSION_HINTS:
        if file_name == old_name:
            return new_name

    return None


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
    path = repo_root / relative_file

    function_source = _function_source(
        path,
        function_name,
    )
    file_source = _file_source(
        path
    )
    file_name = path.name

    measured_seconds = durations.get(
        nodeid
    )
    runtime_class = _runtime_class(
        measured_seconds
    )

    explicit_audit_signal = (
        "audit_" in file_source
        or "_audit" in file_name
        or "_audit" in function_name
        or "is_audit_only" in function_source
    )

    cross_group_signal = (
        "TARGETS" in function_source
        or "for n, k in" in function_source
        or "range(2, 16)" in function_source
        or "representative_groups" in function_name
        or "cross_group" in file_name
    )

    fixed_count_signal = bool(
        re.search(
            r"==\s*(?:6|13|16|33|45|48|55|157|177|190)\b",
            function_source,
        )
    )

    inventory_signal = (
        "build_" in function_source
        and "inventory" in function_source
    )

    production_renderer_signal = (
        "toda_group_proof_narrative_contribution_renderer"
        in file_source
        or "render_toda_group_proof_narrative"
        in function_source
    )

    superseded = _superseded_by(
        file_name
    )

    if superseded is not None:
        redundancy_class = (
            "SUPERSEDED_CANDIDATE"
        )
    elif any(
        stem in file_name
        for stem in OVERLAP_STEMS
    ) and (
        fixed_count_signal
        or inventory_signal
    ):
        redundancy_class = (
            "OVERLAP_CANDIDATE"
        )
    else:
        redundancy_class = "UNIQUE_OR_REVIEW"

    if explicit_audit_signal:
        execution_lane = "AUDIT_ONLY"
    elif (
        measured_seconds is not None
        and measured_seconds >= 10.0
    ) or (
        cross_group_signal
        and inventory_signal
    ):
        execution_lane = "SPLIT_OR_CACHE"
    else:
        execution_lane = "ROUTINE_CANDIDATE"

    if (
        redundancy_class
        == "SUPERSEDED_CANDIDATE"
    ):
        recommendation = (
            "Do not run routinely. Compare assertions with the later "
            "completion audit; delete or archive only after unique "
            "contract coverage is proven absent."
        )
    elif execution_lane == "AUDIT_ONLY":
        recommendation = (
            "Move out of routine regression. Keep as explicit audit "
            "unless a small current-contract test replaces its unique "
            "assertion."
        )
    elif execution_lane == "SPLIT_OR_CACHE":
        recommendation = (
            "Keep coverage but replace repeated repository/group inventory "
            "construction with module-scoped/shared cached context or a "
            "small representative contract test."
        )
    else:
        recommendation = (
            "Potential routine test. Preserve only if it protects a current "
            "contract not already covered by later completion invariants."
        )

    return ReviewRow(
        nodeid=nodeid,
        file=relative_file,
        function=function_name,
        measured_seconds=measured_seconds,
        runtime_class=runtime_class,
        execution_lane=execution_lane,
        redundancy_class=redundancy_class,
        superseded_by=superseded,
        explicit_audit_signal=explicit_audit_signal,
        cross_group_signal=cross_group_signal,
        fixed_count_signal=fixed_count_signal,
        inventory_signal=inventory_signal,
        production_renderer_signal=production_renderer_signal,
        recommendation=recommendation,
    )


def _markdown(
    rows: tuple[ReviewRow, ...],
) -> str:
    runtime_counts = Counter(
        row.runtime_class
        for row in rows
    )
    lane_counts = Counter(
        row.execution_lane
        for row in rows
    )
    redundancy_counts = Counter(
        row.redundancy_class
        for row in rows
    )

    measured = tuple(
        row
        for row in rows
        if row.measured_seconds
        is not None
    )

    total_measured = sum(
        row.measured_seconds
        or 0.0
        for row in measured
    )

    lines = [
        "# Phase 155 Closure-R2B Historical-heavy review",
        "",
        "## Boundary",
        "",
        "- Reviewed nodeids: 36",
        "- Repository tests executed: 0",
        "- Production changes: none",
        "- Existing test changes: none",
        "",
        "This report separates runtime-lane advice from redundancy advice.",
        "No test is deleted in R2B.",
        "",
        "## Runtime summary",
        "",
        "```text",
    ]

    for key, count in sorted(
        runtime_counts.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            f"MEASURED_TOTAL_SECONDS: {total_measured:.2f}",
            "```",
            "",
            "## Execution-lane recommendation",
            "",
            "```text",
        ]
    )

    for key, count in sorted(
        lane_counts.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Redundancy recommendation",
            "",
            "```text",
        ]
    )

    for key, count in sorted(
        redundancy_counts.items()
    ):
        lines.append(
            f"{key}: {count}"
        )

    lines.extend(
        [
            "```",
            "",
            "## Measured slow tests",
            "",
            "| seconds | lane | redundancy | nodeid |",
            "| ---: | --- | --- | --- |",
        ]
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
            + row.execution_lane
            + " | "
            + row.redundancy_class
            + " | `"
            + row.nodeid
            + "` |"
        )

    lines.extend(
        [
            "",
            "## Superseded candidates",
            "",
        ]
    )

    superseded_rows = tuple(
        row
        for row in rows
        if row.superseded_by
        is not None
    )

    if not superseded_rows:
        lines.append(
            "None."
        )
    else:
        for row in superseded_rows:
            lines.append(
                "- `"
                + row.nodeid
                + "` → compare against `"
                + str(
                    row.superseded_by
                )
                + "`."
            )

    lines.extend(
        [
            "",
            "## Recommended R2B follow-up",
            "",
            "1. Keep `43_11d final completion` as the closure-level audit source.",
            "2. For earlier 43_6/8/9/11/11a stages, prove whether each unique "
            "assertion is already implied by 43_11d/current contract tests.",
            "3. Move genuine historical population scans to audit-only execution.",
            "4. Replace repeated six-group inventory construction with shared "
            "module-scoped context or lightweight representative contracts.",
            "5. Do not re-run the 10,421-test suite during this cleanup.",
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
            "historical_heavy_nodeids.txt"
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
            "phase155_closure_r2b_output"
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
            "Historical-heavy manifest not found: "
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
    ) != 36:
        raise SystemExit(
            "Expected 36 HISTORICAL_HEAVY nodeids; "
            f"found {len(nodeids)}"
        )

    if len(
        set(
            nodeids
        )
    ) != 36:
        raise SystemExit(
            "Historical-heavy manifest contains duplicates."
        )

    if not all(
        nodeid.startswith(
            "tests/test_phase144_"
        )
        for nodeid in nodeids
    ):
        raise SystemExit(
            "Historical-heavy manifest contains a non-Phase144 nodeid."
        )

    log_text = log_path.read_text(
        encoding="utf-8",
        errors="replace",
    )
    durations = _duration_map(
        log_text
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
        "runtime_counts": dict(
            Counter(
                row.runtime_class
                for row in rows
            )
        ),
        "execution_lane_counts": dict(
            Counter(
                row.execution_lane
                for row in rows
            )
        ),
        "redundancy_counts": dict(
            Counter(
                row.redundancy_class
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
        / "phase155_closure_r2b_review.json"
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
        / "phase155_closure_r2b_review.md"
    ).write_text(
        _markdown(
            rows
        ),
        encoding="utf-8",
    )

    lane_groups = defaultdict(
        list
    )
    redundancy_groups = defaultdict(
        list
    )

    for row in rows:
        lane_groups[
            row.execution_lane
        ].append(
            row.nodeid
        )
        redundancy_groups[
            row.redundancy_class
        ].append(
            row.nodeid
        )

    for lane, members in lane_groups.items():
        (
            output_dir
            / (
                "lane_"
                + lane.lower()
                + ".txt"
            )
        ).write_text(
            "".join(
                member
                + "\n"
                for member in members
            ),
            encoding="utf-8",
        )

    for category, members in redundancy_groups.items():
        (
            output_dir
            / (
                "redundancy_"
                + category.lower()
                + ".txt"
            )
        ).write_text(
            "".join(
                member
                + "\n"
                for member in members
            ),
            encoding="utf-8",
        )

    print(
        "Phase 155 Closure-R2B static review"
    )
    print(
        "Reviewed HISTORICAL_HEAVY nodeids:",
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
        "Execution lanes:"
    )
    for key, count in sorted(
        Counter(
            row.execution_lane
            for row in rows
        ).items()
    ):
        print(
            f"  {key}: {count}"
        )

    print("")
    print(
        "Redundancy classes:"
    )
    for key, count in sorted(
        Counter(
            row.redundancy_class
            for row in rows
        ).items()
    ):
        print(
            f"  {key}: {count}"
        )

    measured = tuple(
        row
        for row in rows
        if row.measured_seconds
        is not None
    )

    print("")
    print(
        "Measured slow rows:",
        len(
            measured
        ),
    )

    if measured:
        slowest = max(
            measured,
            key=lambda row: (
                row.measured_seconds
                or 0.0
            ),
        )
        print(
            "Slowest measured:",
            f"{slowest.measured_seconds:.2f}s",
            slowest.nodeid,
        )

    print("")
    print(
        "R2B review validated: True"
    )
    print(
        "No deletion performed."
    )
    print(
        "No heavy test executed."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
