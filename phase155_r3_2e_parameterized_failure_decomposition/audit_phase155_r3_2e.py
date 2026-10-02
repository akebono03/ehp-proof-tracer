from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pytest


CAUSE_ALL_INSTANCES_PASS = "all_parameterized_instances_pass"
CAUSE_INSTANCE_FAILURE = "parameterized_instance_failure"
CAUSE_SETUP_FAILURE = "setup_or_teardown_failure"
CAUSE_NOT_COLLECTED = "not_collected"
CAUSE_NO_CALL_REPORT = "collected_without_call_report"
CAUSE_UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class BaseTest:
    requested_test_id: str


@dataclass(frozen=True)
class InstanceReport:
    requested_test_id: str
    nodeid: str
    phase: str
    outcome: str
    duration_seconds: float
    longrepr: str


@dataclass(frozen=True)
class BaseDecomposition:
    requested_test_id: str
    collected_instances: str
    collected_count: int
    call_instances: str
    call_count: int
    passed_calls: int
    failed_calls: int
    skipped_calls: int
    setup_or_teardown_failures: int
    root_cause: str
    r3_2d_false_failure_classification: bool
    blocking: bool
    reason: str


class FreshRecorder:
    def __init__(self) -> None:
        self.collected: list[str] = []
        self.reports: list[tuple[str, str, str, float, str]] = []

    @pytest.hookimpl
    def pytest_collection_modifyitems(
        self,
        session,
        config,
        items,
    ) -> None:
        self.collected = [
            item.nodeid.replace(
                "\\",
                "/",
            )
            for item in items
        ]

    @pytest.hookimpl
    def pytest_runtest_logreport(
        self,
        report,
    ) -> None:
        longrepr = ""

        if report.failed:
            longrepr = str(
                report.longrepr
            )[:4000]

        self.reports.append(
            (
                report.nodeid.replace(
                    "\\",
                    "/",
                ),
                report.when,
                report.outcome,
                float(
                    report.duration
                ),
                longrepr,
            )
        )


def _git_head(
    repo_root: Path,
) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return (
            completed.stdout.strip()
        )
    except (
        OSError,
        subprocess.CalledProcessError,
    ):
        return "unavailable"


def _read_csv(
    path: Path,
) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(
            csv.DictReader(
                handle
            )
        )


def _write_csv(
    path: Path,
    rows: Iterable[object],
) -> None:
    rows = list(
        rows
    )

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fieldnames = list(
        asdict(
            rows[0]
        ).keys()
    )

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
                asdict(
                    row
                )
            )


def normalize_nodeid(
    nodeid: str,
) -> str:
    normalized = nodeid.replace(
        "\\",
        "/",
    ).strip()

    parts = normalized.split(
        "::"
    )

    if len(
        parts
    ) < 2:
        return normalized

    parts[-1] = re.sub(
        r"\[.*\]$",
        "",
        parts[-1],
    )

    return "::".join(
        parts
    )


def load_base_tests(
    r3_2d_rows: list[
        dict[str, str]
    ],
) -> tuple[
    BaseTest,
    ...,
]:
    ordered: dict[
        str,
        None,
    ] = {}

    for row in r3_2d_rows:
        requested = row.get(
            "requested_test_id",
            "",
        ).strip()

        if not requested:
            continue

        ordered[
            normalize_nodeid(
                requested
            )
        ] = None

    return tuple(
        BaseTest(
            requested_test_id=(
                test_id
            )
        )
        for test_id in ordered
    )


def fresh_execute(
    repo_root: Path,
    base_tests: tuple[
        BaseTest,
        ...,
    ],
) -> tuple[
    FreshRecorder,
    int,
]:
    recorder = FreshRecorder()

    previous = Path.cwd()

    try:
        os.chdir(
            repo_root
        )

        exit_code = pytest.main(
            [
                *[
                    base.requested_test_id
                    for base in base_tests
                ],
                "-q",
                "--tb=short",
                "-p",
                "no:cacheprovider",
            ],
            plugins=[
                recorder
            ],
        )
    finally:
        os.chdir(
            previous
        )

    return (
        recorder,
        int(
            exit_code
        ),
    )


def map_instance_reports(
    base_tests: tuple[
        BaseTest,
        ...,
    ],
    recorder: FreshRecorder,
) -> list[
    InstanceReport
]:
    requested_ids = {
        base.requested_test_id
        for base in base_tests
    }

    result = []

    for (
        nodeid,
        phase,
        outcome,
        duration,
        longrepr,
    ) in recorder.reports:
        base_id = normalize_nodeid(
            nodeid
        )

        if base_id not in requested_ids:
            continue

        result.append(
            InstanceReport(
                requested_test_id=(
                    base_id
                ),
                nodeid=nodeid,
                phase=phase,
                outcome=outcome,
                duration_seconds=(
                    duration
                ),
                longrepr=longrepr,
            )
        )

    return result


def decompose(
    base_tests: tuple[
        BaseTest,
        ...,
    ],
    recorder: FreshRecorder,
    instance_reports: list[
        InstanceReport
    ],
) -> list[
    BaseDecomposition
]:
    collected_by_base: dict[
        str,
        list[str],
    ] = defaultdict(
        list
    )

    for nodeid in recorder.collected:
        base_id = normalize_nodeid(
            nodeid
        )

        collected_by_base[
            base_id
        ].append(
            nodeid
        )

    reports_by_base: dict[
        str,
        list[InstanceReport],
    ] = defaultdict(
        list
    )

    for report in instance_reports:
        reports_by_base[
            report.requested_test_id
        ].append(
            report
        )

    result = []

    for base in base_tests:
        base_id = (
            base.requested_test_id
        )
        collected = (
            collected_by_base.get(
                base_id,
                [],
            )
        )
        reports = (
            reports_by_base.get(
                base_id,
                [],
            )
        )

        call_reports = [
            report
            for report in reports
            if report.phase
            == "call"
        ]
        setup_teardown_failures = [
            report
            for report in reports
            if (
                report.phase
                in (
                    "setup",
                    "teardown",
                )
                and report.outcome
                == "failed"
            )
        ]

        passed_calls = sum(
            report.outcome
            == "passed"
            for report in call_reports
        )
        failed_calls = sum(
            report.outcome
            == "failed"
            for report in call_reports
        )
        skipped_calls = sum(
            report.outcome
            == "skipped"
            for report in call_reports
        )

        if not collected:
            root_cause = (
                CAUSE_NOT_COLLECTED
            )
            false_failure = False
            blocking = True
            reason = (
                "The requested base test did not collect in the fresh "
                "focused run."
            )

        elif setup_teardown_failures:
            root_cause = (
                CAUSE_SETUP_FAILURE
            )
            false_failure = False
            blocking = True
            reason = (
                "At least one collected instance failed during setup "
                "or teardown."
            )

        elif failed_calls > 0:
            root_cause = (
                CAUSE_INSTANCE_FAILURE
            )
            false_failure = False
            blocking = True
            reason = (
                "At least one freshly executed parameterized call instance "
                "failed."
            )

        elif (
            call_reports
            and passed_calls
            == len(
                call_reports
            )
        ):
            root_cause = (
                CAUSE_ALL_INSTANCES_PASS
            )
            false_failure = True
            blocking = False
            reason = (
                "Every freshly executed call instance passed. "
                "The prior R3-2D 'parameterized with failure' result was "
                "caused by treating the synthetic base-level `missing` "
                "record from R3-2 as an execution outcome."
            )

        elif not call_reports:
            root_cause = (
                CAUSE_NO_CALL_REPORT
            )
            false_failure = False
            blocking = True
            reason = (
                "The base test collected but produced no call-phase report."
            )

        else:
            root_cause = (
                CAUSE_UNRESOLVED
            )
            false_failure = False
            blocking = True
            reason = (
                "Fresh execution produced an outcome combination not covered "
                "by the R3-2E classifier."
            )

        result.append(
            BaseDecomposition(
                requested_test_id=(
                    base_id
                ),
                collected_instances=(
                    "\x1f".join(
                        collected
                    )
                ),
                collected_count=len(
                    collected
                ),
                call_instances=(
                    "\x1f".join(
                        report.nodeid
                        for report
                        in call_reports
                    )
                ),
                call_count=len(
                    call_reports
                ),
                passed_calls=(
                    passed_calls
                ),
                failed_calls=(
                    failed_calls
                ),
                skipped_calls=(
                    skipped_calls
                ),
                setup_or_teardown_failures=len(
                    setup_teardown_failures
                ),
                root_cause=(
                    root_cause
                ),
                r3_2d_false_failure_classification=(
                    false_failure
                ),
                blocking=(
                    blocking
                ),
                reason=reason,
            )
        )

    return result


def write_summary(
    path: Path,
    repo_root: Path,
    decompositions: list[
        BaseDecomposition
    ],
    pytest_exit_code: int,
) -> None:
    counts = Counter(
        row.root_cause
        for row in decompositions
    )

    total_instances = sum(
        row.call_count
        for row in decompositions
    )
    total_passed = sum(
        row.passed_calls
        for row in decompositions
    )
    total_failed = sum(
        row.failed_calls
        for row in decompositions
    )
    blocking = sum(
        row.blocking
        for row in decompositions
    )

    lines = [
        "# Phase 155-R3-2E — parameterized failure decomposition",
        "",
        "## Boundary",
        "",
        "This step freshly executes only the unique base tests referenced by R3-2D.",
        "It records pytest collection and all setup/call/teardown reports directly.",
        "It changes no production code and no existing test.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Unique base tests: {len(decompositions)}",
        f"- Fresh focused pytest exit code: {pytest_exit_code}",
        f"- Fresh call instances: {total_instances}",
        f"- Passed call instances: {total_passed}",
        f"- Failed call instances: {total_failed}",
        f"- Blocking base tests: {blocking}",
        "",
        "## Root causes",
        "",
        "| root cause | base tests |",
        "| --- | ---: |",
    ]

    for category in (
        CAUSE_ALL_INSTANCES_PASS,
        CAUSE_INSTANCE_FAILURE,
        CAUSE_SETUP_FAILURE,
        CAUSE_NOT_COLLECTED,
        CAUSE_NO_CALL_REPORT,
        CAUSE_UNRESOLVED,
    ):
        lines.append(
            f"| `{category}` | {counts[category]} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "`all_parameterized_instances_pass` proves that R3-2D's earlier `parameterized with failure` classification was false for that base test.",
            "The reason is structural: R3-2 wrote a synthetic base-level `missing` row when exact lookup failed, while actual pytest parameter instances were not written to that CSV.",
            "",
            "Only a fresh call-phase `failed`, setup/teardown failure, collection failure, or unresolved record blocks R3-2 closure.",
            "",
            "Repository-wide pytest remains deferred until Phase 155 closure.",
        ]
    )

    path.write_text(
        "\n".join(
            lines
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r3-2d-audit",
        type=Path,
        default=Path(
            "phase155_r3_2d_audit_output/"
            "phase155_r3_2d_missing_execution_audit.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_2e_audit_output"
        ),
    )

    args = parser.parse_args()
    repo_root = (
        args.repo_root.resolve()
    )

    audit_path = (
        args.r3_2d_audit
        if args.r3_2d_audit.is_absolute()
        else repo_root
        / args.r3_2d_audit
    )

    if not audit_path.exists():
        raise SystemExit(
            "R3-2D audit CSV not found: "
            + str(
                audit_path
            )
        )

    r3_2d_rows = _read_csv(
        audit_path
    )
    base_tests = load_base_tests(
        r3_2d_rows
    )

    if not base_tests:
        raise SystemExit(
            "No base tests found in R3-2D audit output."
        )

    recorder, pytest_exit_code = (
        fresh_execute(
            repo_root,
            base_tests,
        )
    )

    instance_reports = (
        map_instance_reports(
            base_tests,
            recorder,
        )
    )
    decompositions = (
        decompose(
            base_tests,
            recorder,
            instance_reports,
        )
    )

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root
        / args.output_dir
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_csv(
        output_dir
        / "phase155_r3_2e_instance_reports.csv",
        instance_reports,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2e_base_decomposition.csv",
        decompositions,
    )

    write_summary(
        output_dir
        / "phase155_r3_2e_summary.md",
        repo_root,
        decompositions,
        pytest_exit_code,
    )

    counts = Counter(
        row.root_cause
        for row in decompositions
    )
    blocking = sum(
        row.blocking
        for row in decompositions
    )

    metadata = {
        "phase": "155-R3-2E",
        "git_head": _git_head(
            repo_root
        ),
        "unique_base_tests": len(
            decompositions
        ),
        "fresh_pytest_exit_code": (
            pytest_exit_code
        ),
        "fresh_call_instances": sum(
            row.call_count
            for row in decompositions
        ),
        "fresh_passed_calls": sum(
            row.passed_calls
            for row in decompositions
        ),
        "fresh_failed_calls": sum(
            row.failed_calls
            for row in decompositions
        ),
        "root_cause_counts": dict(
            counts
        ),
        "false_r3_2d_failure_count": sum(
            row.r3_2d_false_failure_classification
            for row in decompositions
        ),
        "blocking_base_test_count": (
            blocking
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2e_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R3-2E parameterized failure decomposition completed."
    )
    print(
        "unique base tests:",
        len(
            decompositions
        ),
    )
    print(
        "fresh call instances:",
        sum(
            row.call_count
            for row in decompositions
        ),
    )
    print(
        "fresh passed calls:",
        sum(
            row.passed_calls
            for row in decompositions
        ),
    )
    print(
        "fresh failed calls:",
        sum(
            row.failed_calls
            for row in decompositions
        ),
    )
    print(
        "all-instances-pass base tests:",
        counts[
            CAUSE_ALL_INSTANCES_PASS
        ],
    )
    print(
        "instance-failure base tests:",
        counts[
            CAUSE_INSTANCE_FAILURE
        ],
    )
    print(
        "setup/teardown failure base tests:",
        counts[
            CAUSE_SETUP_FAILURE
        ],
    )
    print(
        "not-collected base tests:",
        counts[
            CAUSE_NOT_COLLECTED
        ],
    )
    print(
        "no-call-report base tests:",
        counts[
            CAUSE_NO_CALL_REPORT
        ],
    )
    print(
        "unresolved base tests:",
        counts[
            CAUSE_UNRESOLVED
        ],
    )
    print(
        "R3-2D false failure classifications:",
        sum(
            row.r3_2d_false_failure_classification
            for row in decompositions
        ),
    )
    print(
        "blocking base tests:",
        blocking,
    )
    print(
        "focused pytest exit code:",
        pytest_exit_code,
    )
    print(
        "output:",
        output_dir,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
