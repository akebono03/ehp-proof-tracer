from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pytest


DECISION_REMOVABLE = "removable_duplicate"
DECISION_RETAIN = "retain_independent"
DECISION_HISTORICAL = "historical_keep"
DECISION_REVIEW = "needs_review"

CATEGORY_EXACT = "exact_duplicate_candidate"
CATEGORY_SEMANTIC = "semantic_duplicate_candidate"
CATEGORY_SUPERSEDED = "superseded_candidate"


@dataclass(frozen=True)
class RuntimeAggregate:
    requested_test_id: str
    collected_count: int
    call_count: int
    passed_count: int
    failed_count: int
    skipped_count: int
    setup_teardown_failure_count: int
    runtime_status: str


@dataclass(frozen=True)
class ClosurePair:
    candidate_id: str
    category: str
    older_test_id: str
    newer_test_id: str
    older_runtime_status: str
    newer_runtime_status: str
    function_hash_equal: bool
    semantic_function_hash_equal: bool
    dependency_hash_equal: bool
    decision: str
    deletion_authorized: bool
    reason: str


class Recorder:
    def __init__(self) -> None:
        self.collected: list[str] = []
        self.reports: list[
            tuple[
                str,
                str,
                str,
            ]
        ] = []

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
        self.reports.append(
            (
                report.nodeid.replace(
                    "\\",
                    "/",
                ),
                report.when,
                report.outcome,
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
) -> list[
    dict[
        str,
        str,
    ]
]:
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
    rows: Iterable[
        object
    ],
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


def _unique_test_ids(
    candidate_rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> tuple[
    str,
    ...,
]:
    ordered: dict[
        str,
        None,
    ] = {}

    for row in candidate_rows:
        ordered[
            normalize_nodeid(
                row[
                    "older_test_id"
                ]
            )
        ] = None
        ordered[
            normalize_nodeid(
                row[
                    "newer_test_id"
                ]
            )
        ] = None

    return tuple(
        ordered
    )


def _fresh_execute(
    repo_root: Path,
    test_ids: tuple[
        str,
        ...,
    ],
) -> tuple[
    Recorder,
    int,
]:
    recorder = Recorder()
    previous = Path.cwd()

    try:
        os.chdir(
            repo_root
        )
        exit_code = pytest.main(
            [
                *test_ids,
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


def aggregate_runtime(
    requested_test_ids: tuple[
        str,
        ...,
    ],
    recorder: Recorder,
) -> list[
    RuntimeAggregate
]:
    collected_by_base: dict[
        str,
        list[str],
    ] = {}

    for nodeid in recorder.collected:
        collected_by_base.setdefault(
            normalize_nodeid(
                nodeid
            ),
            [],
        ).append(
            nodeid
        )

    reports_by_base: dict[
        str,
        list[
            tuple[
                str,
                str,
                str,
            ]
        ],
    ] = {}

    for nodeid, phase, outcome in recorder.reports:
        reports_by_base.setdefault(
            normalize_nodeid(
                nodeid
            ),
            [],
        ).append(
            (
                nodeid,
                phase,
                outcome,
            )
        )

    result = []

    for requested in requested_test_ids:
        collected = (
            collected_by_base.get(
                requested,
                [],
            )
        )
        reports = (
            reports_by_base.get(
                requested,
                [],
            )
        )
        calls = [
            report
            for report in reports
            if report[
                1
            ]
            == "call"
        ]

        passed = sum(
            report[
                2
            ]
            == "passed"
            for report in calls
        )
        failed = sum(
            report[
                2
            ]
            == "failed"
            for report in calls
        )
        skipped = sum(
            report[
                2
            ]
            == "skipped"
            for report in calls
        )
        setup_teardown_failed = sum(
            phase
            in (
                "setup",
                "teardown",
            )
            and outcome
            == "failed"
            for _nodeid, phase, outcome
            in reports
        )

        if not collected:
            status = (
                "not_collected"
            )
        elif setup_teardown_failed:
            status = (
                "setup_teardown_failed"
            )
        elif failed:
            status = "failed"
        elif (
            calls
            and passed
            == len(
                calls
            )
        ):
            status = "passed"
        elif not calls:
            status = (
                "no_call_report"
            )
        else:
            status = "non_pass"

        result.append(
            RuntimeAggregate(
                requested_test_id=(
                    requested
                ),
                collected_count=len(
                    collected
                ),
                call_count=len(
                    calls
                ),
                passed_count=passed,
                failed_count=failed,
                skipped_count=skipped,
                setup_teardown_failure_count=(
                    setup_teardown_failed
                ),
                runtime_status=status,
            )
        )

    return result


def _is_true(
    value: str,
) -> bool:
    return value.strip().lower() in {
        "true",
        "1",
        "yes",
    }


def _atoms(
    value: str,
) -> set[
    str
]:
    return set(
        filter(
            None,
            value.split(
                "\x1f"
            ),
        )
    )


def classify_pairs(
    candidate_rows: list[
        dict[
            str,
            str,
        ]
    ],
    prior_verified_rows: list[
        dict[
            str,
            str,
        ]
    ],
    source_rows: list[
        dict[
            str,
            str,
        ]
    ],
    runtime_rows: list[
        RuntimeAggregate
    ],
) -> list[
    ClosurePair
]:
    prior_by_id = {
        row[
            "candidate_id"
        ]: row
        for row
        in prior_verified_rows
    }
    source_by_test = {
        normalize_nodeid(
            row[
                "test_id"
            ]
        ): row
        for row
        in source_rows
    }
    runtime_by_test = {
        row.requested_test_id: row
        for row
        in runtime_rows
    }

    result = []

    for candidate in candidate_rows:
        candidate_id = (
            candidate[
                "candidate_id"
            ]
        )
        category = candidate[
            "category"
        ]
        older = normalize_nodeid(
            candidate[
                "older_test_id"
            ]
        )
        newer = normalize_nodeid(
            candidate[
                "newer_test_id"
            ]
        )
        older_runtime = (
            runtime_by_test.get(
                older
            )
        )
        newer_runtime = (
            runtime_by_test.get(
                newer
            )
        )
        older_status = (
            older_runtime.runtime_status
            if older_runtime
            else "missing_runtime"
        )
        newer_status = (
            newer_runtime.runtime_status
            if newer_runtime
            else "missing_runtime"
        )

        prior = prior_by_id.get(
            candidate_id,
            {},
        )

        function_equal = _is_true(
            prior.get(
                "function_hash_equal",
                "False",
            )
        )
        semantic_equal = _is_true(
            prior.get(
                "semantic_function_hash_equal",
                "False",
            )
        )
        dependency_equal = _is_true(
            prior.get(
                "dependency_hash_equal",
                "False",
            )
        )

        older_source = (
            source_by_test.get(
                older,
                {},
            )
        )
        newer_source = (
            source_by_test.get(
                newer,
                {},
            )
        )
        source_available = (
            _is_true(
                older_source.get(
                    "source_available",
                    "False",
                )
            )
            and _is_true(
                newer_source.get(
                    "source_available",
                    "False",
                )
            )
        )

        historical = (
            prior.get(
                "decision"
            )
            == DECISION_HISTORICAL
        )

        if historical:
            decision = (
                DECISION_HISTORICAL
            )
            authorized = False
            reason = (
                "Historical/compatibility intent remains explicitly retained."
            )

        elif (
            older_status
            != "passed"
            or newer_status
            != "passed"
        ):
            decision = (
                DECISION_REVIEW
            )
            authorized = False
            reason = (
                "Both candidate tests must pass after normalized "
                "parameterized aggregation."
            )

        elif not source_available:
            decision = (
                DECISION_REVIEW
            )
            authorized = False
            reason = (
                "Source evidence is incomplete."
            )

        elif category == CATEGORY_EXACT:
            if (
                function_equal
                and dependency_equal
            ):
                decision = (
                    DECISION_REMOVABLE
                )
                authorized = True
                reason = (
                    "Fresh runtime passes; exact body and dependency "
                    "fingerprints match."
                )
            else:
                decision = (
                    DECISION_RETAIN
                )
                authorized = False
                reason = (
                    "Fresh runtime passes, but exact replacement is not "
                    "proven under the dependency fingerprint."
                )

        elif category == CATEGORY_SEMANTIC:
            if (
                semantic_equal
                and dependency_equal
            ):
                decision = (
                    DECISION_REMOVABLE
                )
                authorized = True
                reason = (
                    "Fresh runtime passes; semantic body and dependency "
                    "fingerprints match."
                )
            else:
                decision = (
                    DECISION_RETAIN
                )
                authorized = False
                reason = (
                    "Fresh runtime passes, but semantic replacement is not "
                    "proven under the dependency fingerprint."
                )

        elif category == CATEGORY_SUPERSEDED:
            older_atoms = _atoms(
                candidate.get(
                    "older_semantic_atoms",
                    "",
                )
            )
            newer_atoms = _atoms(
                candidate.get(
                    "newer_semantic_atoms",
                    "",
                )
            )

            if (
                older_atoms
                and older_atoms.issubset(
                    newer_atoms
                )
                and dependency_equal
            ):
                decision = (
                    DECISION_REMOVABLE
                )
                authorized = True
                reason = (
                    "Fresh runtime passes; newer assertion contract contains "
                    "the older contract under the same dependency fingerprint."
                )
            else:
                decision = (
                    DECISION_RETAIN
                )
                authorized = False
                reason = (
                    "Fresh runtime passes, but full supersession is not proven."
                )

        else:
            decision = (
                DECISION_REVIEW
            )
            authorized = False
            reason = (
                "Unknown candidate category."
            )

        result.append(
            ClosurePair(
                candidate_id=(
                    candidate_id
                ),
                category=category,
                older_test_id=older,
                newer_test_id=newer,
                older_runtime_status=(
                    older_status
                ),
                newer_runtime_status=(
                    newer_status
                ),
                function_hash_equal=(
                    function_equal
                ),
                semantic_function_hash_equal=(
                    semantic_equal
                ),
                dependency_hash_equal=(
                    dependency_equal
                ),
                decision=decision,
                deletion_authorized=(
                    authorized
                ),
                reason=reason,
            )
        )

    return result


def write_summary(
    path: Path,
    repo_root: Path,
    runtime_rows: list[
        RuntimeAggregate
    ],
    closure_rows: list[
        ClosurePair
    ],
    pytest_exit_code: int,
) -> None:
    runtime_counts = Counter(
        row.runtime_status
        for row in runtime_rows
    )
    decisions = Counter(
        row.decision
        for row in closure_rows
    )

    lines = [
        "# Phase 155-R3-2F — verification repair and closure",
        "",
        "## Changes",
        "",
        "- Production code changes: none",
        "- Existing test files changed: 2",
        "- Existing test functions changed: 2",
        "- Stale whole-module `\"pi6\"` substring bans removed",
        "- Parameterized pytest node IDs are aggregated by normalized base node ID",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Fresh focused pytest exit code: {pytest_exit_code}",
        f"- Unique candidate base tests: {len(runtime_rows)}",
        f"- Candidate pairs: {len(closure_rows)}",
        "",
        "## Runtime status",
        "",
        "| status | base tests |",
        "| --- | ---: |",
    ]

    for status in sorted(
        runtime_counts
    ):
        lines.append(
            f"| `{status}` | {runtime_counts[status]} |"
        )

    lines.extend(
        [
            "",
            "## Final pair decisions",
            "",
            "| decision | pairs |",
            "| --- | ---: |",
        ]
    )

    for decision in (
        DECISION_REMOVABLE,
        DECISION_RETAIN,
        DECISION_HISTORICAL,
        DECISION_REVIEW,
    ):
        lines.append(
            f"| `{decision}` | {decisions[decision]} |"
        )

    closure_ok = (
        pytest_exit_code == 0
        and runtime_counts.get(
            "passed",
            0,
        )
        == len(
            runtime_rows
        )
        and decisions[
            DECISION_REVIEW
        ]
        == 0
    )

    lines.extend(
        [
            "",
            "## Closure",
            "",
            f"- R3-2 closure condition satisfied: `{str(closure_ok).lower()}`",
            "- No duplicate test is deleted in R3-2F.",
            "- `removable_duplicate` pairs become R3-3 consolidation candidates only.",
            "- Repository-wide pytest is still deferred until Phase 155 closure.",
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
        "--candidate-pairs",
        type=Path,
        default=Path(
            "phase155_r3_1_audit_output/"
            "phase155_r3_1_candidate_pairs.csv"
        ),
    )
    parser.add_argument(
        "--prior-verified",
        type=Path,
        default=Path(
            "phase155_r3_2_audit_output/"
            "phase155_r3_2_verified_pairs.csv"
        ),
    )
    parser.add_argument(
        "--source-evidence",
        type=Path,
        default=Path(
            "phase155_r3_2_audit_output/"
            "phase155_r3_2_source_evidence.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_2f_audit_output"
        ),
    )

    args = parser.parse_args()
    repo_root = (
        args.repo_root.resolve()
    )

    def resolve(
        path: Path,
    ) -> Path:
        return (
            path
            if path.is_absolute()
            else repo_root
            / path
        )

    candidate_path = resolve(
        args.candidate_pairs
    )
    prior_path = resolve(
        args.prior_verified
    )
    source_path = resolve(
        args.source_evidence
    )

    for required in (
        candidate_path,
        prior_path,
        source_path,
    ):
        if not required.exists():
            raise SystemExit(
                "required R3 audit input not found: "
                + str(
                    required
                )
            )

    candidate_rows = _read_csv(
        candidate_path
    )
    prior_rows = _read_csv(
        prior_path
    )
    source_rows = _read_csv(
        source_path
    )

    test_ids = _unique_test_ids(
        candidate_rows
    )
    recorder, pytest_exit_code = (
        _fresh_execute(
            repo_root,
            test_ids,
        )
    )
    runtime_rows = aggregate_runtime(
        test_ids,
        recorder,
    )
    closure_rows = classify_pairs(
        candidate_rows,
        prior_rows,
        source_rows,
        runtime_rows,
    )

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_csv(
        output_dir
        / "phase155_r3_2f_runtime_aggregate.csv",
        runtime_rows,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2f_verified_pairs.csv",
        closure_rows,
    )

    write_summary(
        output_dir
        / "phase155_r3_2f_summary.md",
        repo_root,
        runtime_rows,
        closure_rows,
        pytest_exit_code,
    )

    runtime_counts = Counter(
        row.runtime_status
        for row in runtime_rows
    )
    decision_counts = Counter(
        row.decision
        for row in closure_rows
    )

    closure_ok = (
        pytest_exit_code == 0
        and runtime_counts.get(
            "passed",
            0,
        )
        == len(
            runtime_rows
        )
        and decision_counts[
            DECISION_REVIEW
        ]
        == 0
    )

    metadata = {
        "phase": "155-R3-2F",
        "git_head": _git_head(
            repo_root
        ),
        "unique_candidate_base_tests": len(
            runtime_rows
        ),
        "candidate_pairs": len(
            closure_rows
        ),
        "focused_pytest_exit_code": (
            pytest_exit_code
        ),
        "runtime_status_counts": dict(
            runtime_counts
        ),
        "decision_counts": dict(
            decision_counts
        ),
        "closure_condition_satisfied": (
            closure_ok
        ),
        "production_code_modified": False,
        "existing_test_files_modified": 2,
        "existing_test_functions_modified": 2,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2f_metadata.json"
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
        "Phase 155-R3-2F verification completed."
    )
    print(
        "unique candidate base tests:",
        len(
            runtime_rows
        ),
    )
    print(
        "passed base tests:",
        runtime_counts[
            "passed"
        ],
    )
    print(
        "non-passing base tests:",
        len(
            runtime_rows
        )
        - runtime_counts[
            "passed"
        ],
    )
    print(
        "candidate pairs:",
        len(
            closure_rows
        ),
    )
    print(
        "removable duplicate pairs:",
        decision_counts[
            DECISION_REMOVABLE
        ],
    )
    print(
        "retain independent pairs:",
        decision_counts[
            DECISION_RETAIN
        ],
    )
    print(
        "historical keep pairs:",
        decision_counts[
            DECISION_HISTORICAL
        ],
    )
    print(
        "needs review pairs:",
        decision_counts[
            DECISION_REVIEW
        ],
    )
    print(
        "focused pytest exit code:",
        pytest_exit_code,
    )
    print(
        "R3-2 closure condition satisfied:",
        closure_ok,
    )
    print(
        "output:",
        output_dir,
    )

    if not closure_ok:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
