from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


ROOT_MISSING_EXECUTION = "missing_execution_record"

CAUSE_PARAMETERIZED_ALL_PASS = "parameterized_nodeid_all_pass"
CAUSE_PARAMETERIZED_HAS_FAILURE = "parameterized_nodeid_has_failure"
CAUSE_COLLECTED_BUT_NOT_RECORDED = "collected_but_not_recorded"
CAUSE_NOT_COLLECTED = "not_collected"
CAUSE_NONPARAMETERIZED_MATCH = "nonparameterized_execution_match"
CAUSE_UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class MissingTestRecord:
    candidate_id: str
    requested_test_id: str
    pair_side: str
    original_outcome: str


@dataclass(frozen=True)
class CollectionRecord:
    requested_test_id: str
    pytest_exit_code: int
    collected_nodeids: str
    collected_count: int
    stderr: str


@dataclass(frozen=True)
class MissingExecutionAudit:
    candidate_id: str
    requested_test_id: str
    pair_side: str
    original_outcome: str
    execution_matches: str
    execution_match_count: int
    execution_outcomes: str
    collection_matches: str
    collection_match_count: int
    collection_exit_code: int
    parameterized: bool
    root_cause: str
    recorder_fix_needed: bool
    test_fix_needed: bool
    reason: str


def _git_head(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except (
        OSError,
        subprocess.CalledProcessError,
    ):
        return "unavailable"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: Iterable[object]) -> None:
    rows = list(rows)

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fieldnames = list(asdict(rows[0]).keys())

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
                asdict(row)
            )


def normalize_nodeid(nodeid: str) -> str:
    normalized = nodeid.replace(
        "\\",
        "/",
    ).strip()

    parts = normalized.split(
        "::"
    )

    if len(parts) < 2:
        return normalized

    function_part = parts[-1]
    function_part = re.sub(
        r"\[.*\]$",
        "",
        function_part,
    )
    parts[-1] = function_part

    return "::".join(parts)


def is_parameterized_nodeid(
    nodeid: str,
) -> bool:
    parts = nodeid.replace(
        "\\",
        "/",
    ).split(
        "::"
    )

    if len(parts) < 2:
        return False

    return bool(
        re.search(
            r"\[.*\]$",
            parts[-1],
        )
    )


def load_missing_tests(
    root_cause_rows: list[dict[str, str]],
) -> list[MissingTestRecord]:
    seen: set[
        tuple[str, str, str]
    ] = set()
    result = []

    for row in root_cause_rows:
        if row.get(
            "root_cause"
        ) != ROOT_MISSING_EXECUTION:
            continue

        for side in (
            "older",
            "newer",
        ):
            outcome = row.get(
                side + "_outcome",
                "",
            )

            if outcome != "missing":
                continue

            test_id = row.get(
                side + "_test_id",
                "",
            )

            key = (
                row[
                    "candidate_id"
                ],
                side,
                test_id,
            )

            if (
                not test_id
                or key in seen
            ):
                continue

            seen.add(
                key
            )

            result.append(
                MissingTestRecord(
                    candidate_id=row[
                        "candidate_id"
                    ],
                    requested_test_id=(
                        test_id
                    ),
                    pair_side=side,
                    original_outcome=(
                        outcome
                    ),
                )
            )

    return result


def execution_matches(
    requested_test_id: str,
    execution_rows: list[
        dict[str, str]
    ],
) -> list[
    dict[str, str]
]:
    requested_base = (
        normalize_nodeid(
            requested_test_id
        )
    )

    return [
        row
        for row in execution_rows
        if normalize_nodeid(
            row.get(
                "test_id",
                "",
            )
        )
        == requested_base
    ]


def collect_nodeids(
    repo_root: Path,
    requested_test_id: str,
) -> CollectionRecord:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            requested_test_id,
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    requested_base = (
        normalize_nodeid(
            requested_test_id
        )
    )
    collected = []

    for raw_line in (
        completed.stdout.splitlines()
    ):
        line = raw_line.strip()

        if "::" not in line:
            continue

        candidate = line.replace(
            "\\",
            "/",
        )

        if normalize_nodeid(
            candidate
        ) != requested_base:
            continue

        collected.append(
            candidate
        )

    return CollectionRecord(
        requested_test_id=(
            requested_test_id
        ),
        pytest_exit_code=(
            completed.returncode
        ),
        collected_nodeids="\x1f".join(
            collected
        ),
        collected_count=len(
            collected
        ),
        stderr=(
            completed.stderr.strip()[
                :4000
            ]
        ),
    )


def classify_missing(
    missing: MissingTestRecord,
    execution_rows: list[
        dict[str, str]
    ],
    collection: CollectionRecord,
) -> MissingExecutionAudit:
    matches = execution_matches(
        missing.requested_test_id,
        execution_rows,
    )

    match_ids = [
        row.get(
            "test_id",
            "",
        )
        for row in matches
    ]
    outcomes = [
        row.get(
            "outcome",
            "",
        )
        for row in matches
    ]

    collection_ids = list(
        filter(
            None,
            collection.collected_nodeids.split(
                "\x1f"
            ),
        )
    )

    parameterized = any(
        is_parameterized_nodeid(
            nodeid
        )
        for nodeid in (
            match_ids
            + collection_ids
        )
    )

    if matches:
        if parameterized:
            if all(
                outcome == "passed"
                for outcome in outcomes
            ):
                root_cause = (
                    CAUSE_PARAMETERIZED_ALL_PASS
                )
                recorder_fix_needed = True
                test_fix_needed = False
                reason = (
                    "The requested base node ID expanded to parameterized "
                    "pytest node IDs. All recorded parameter instances passed, "
                    "but R3-2 looked up the unparameterized base node ID by "
                    "exact key and therefore reported it as missing."
                )
            else:
                root_cause = (
                    CAUSE_PARAMETERIZED_HAS_FAILURE
                )
                recorder_fix_needed = True
                test_fix_needed = True
                reason = (
                    "The requested base node ID expanded to parameterized "
                    "instances and at least one recorded instance did not pass."
                )
        else:
            root_cause = (
                CAUSE_NONPARAMETERIZED_MATCH
            )
            recorder_fix_needed = True
            test_fix_needed = False
            reason = (
                "A normalized execution record exists for the requested "
                "non-parameterized test. R3-2 exact-key matching lost it."
            )

    elif collection.collected_count > 0:
        root_cause = (
            CAUSE_COLLECTED_BUT_NOT_RECORDED
        )
        recorder_fix_needed = True
        test_fix_needed = False
        reason = (
            "pytest currently collects one or more matching node IDs, but "
            "none appear in the saved R3-2 execution records."
        )

    elif (
        collection.pytest_exit_code
        != 0
    ):
        root_cause = (
            CAUSE_NOT_COLLECTED
        )
        recorder_fix_needed = False
        test_fix_needed = True
        reason = (
            "pytest could not collect the requested test node ID."
        )

    else:
        root_cause = (
            CAUSE_UNRESOLVED
        )
        recorder_fix_needed = False
        test_fix_needed = False
        reason = (
            "No execution or collection match explains the missing record."
        )

    return MissingExecutionAudit(
        candidate_id=(
            missing.candidate_id
        ),
        requested_test_id=(
            missing.requested_test_id
        ),
        pair_side=(
            missing.pair_side
        ),
        original_outcome=(
            missing.original_outcome
        ),
        execution_matches="\x1f".join(
            match_ids
        ),
        execution_match_count=len(
            matches
        ),
        execution_outcomes="\x1f".join(
            outcomes
        ),
        collection_matches=(
            collection.collected_nodeids
        ),
        collection_match_count=(
            collection.collected_count
        ),
        collection_exit_code=(
            collection.pytest_exit_code
        ),
        parameterized=(
            parameterized
        ),
        root_cause=(
            root_cause
        ),
        recorder_fix_needed=(
            recorder_fix_needed
        ),
        test_fix_needed=(
            test_fix_needed
        ),
        reason=reason,
    )


def write_summary(
    path: Path,
    repo_root: Path,
    audits: list[
        MissingExecutionAudit
    ],
) -> None:
    counts = Counter(
        row.root_cause
        for row in audits
    )

    recorder_only = sum(
        row.recorder_fix_needed
        and not row.test_fix_needed
        for row in audits
    )
    test_related = sum(
        row.test_fix_needed
        for row in audits
    )

    lines = [
        "# Phase 155-R3-2D — missing execution record audit",
        "",
        "## Boundary",
        "",
        "This audit investigates only missing execution records identified by R3-2C-r1.",
        "It modifies no production code and no existing test.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Missing test references audited: {len(audits)}",
        "",
        "## Root causes",
        "",
        "| root cause | records |",
        "| --- | ---: |",
    ]

    for category in (
        CAUSE_PARAMETERIZED_ALL_PASS,
        CAUSE_PARAMETERIZED_HAS_FAILURE,
        CAUSE_COLLECTED_BUT_NOT_RECORDED,
        CAUSE_NONPARAMETERIZED_MATCH,
        CAUSE_NOT_COLLECTED,
        CAUSE_UNRESOLVED,
    ):
        lines.append(
            f"| `{category}` | {counts[category]} |"
        )

    lines.extend(
        [
            "",
            f"- Recorder-only records: {recorder_only}",
            f"- Test-related records: {test_related}",
            "",
            "## Interpretation",
            "",
            "`parameterized_nodeid_all_pass` means the original candidate test was specified as `file.py::test_name`, while pytest executed `file.py::test_name[param]` instances. R3-2 used exact-key lookup and therefore created a false missing record even though every parameter instance passed.",
            "",
            "`collected_but_not_recorded` means pytest currently collects the test but the previous execution recorder did not save a matching result.",
            "",
            "`not_collected` or `parameterized_nodeid_has_failure` requires test-side investigation before R3-2 closure.",
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
        "--root-causes",
        type=Path,
        default=Path(
            "phase155_r3_2c_r1_audit_output/"
            "phase155_r3_2c_r1_root_causes.csv"
        ),
    )
    parser.add_argument(
        "--executions",
        type=Path,
        default=Path(
            "phase155_r3_2_audit_output/"
            "phase155_r3_2_test_executions.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_2d_audit_output"
        ),
    )

    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return (
            path
            if path.is_absolute()
            else repo_root / path
        )

    root_causes_path = resolve(
        args.root_causes
    )
    executions_path = resolve(
        args.executions
    )

    for required in (
        root_causes_path,
        executions_path,
    ):
        if not required.exists():
            raise SystemExit(
                "required audit input not found: "
                + str(required)
            )

    root_rows = _read_csv(
        root_causes_path
    )
    execution_rows = _read_csv(
        executions_path
    )

    missing_tests = load_missing_tests(
        root_rows
    )

    collection_by_test = {
        test.requested_test_id: (
            collect_nodeids(
                repo_root,
                test.requested_test_id,
            )
        )
        for test in missing_tests
    }

    audits = [
        classify_missing(
            test,
            execution_rows,
            collection_by_test[
                test.requested_test_id
            ],
        )
        for test in missing_tests
    ]

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_csv(
        output_dir
        / "phase155_r3_2d_missing_execution_audit.csv",
        audits,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2d_collection_records.csv",
        collection_by_test.values(),
    )

    write_summary(
        output_dir
        / "phase155_r3_2d_summary.md",
        repo_root,
        audits,
    )

    counts = Counter(
        row.root_cause
        for row in audits
    )

    blocking = sum(
        row.test_fix_needed
        or (
            not row.recorder_fix_needed
            and row.root_cause
            == CAUSE_UNRESOLVED
        )
        for row in audits
    )

    metadata = {
        "phase": "155-R3-2D",
        "git_head": _git_head(
            repo_root
        ),
        "missing_test_references": len(
            audits
        ),
        "root_cause_counts": dict(
            counts
        ),
        "recorder_fix_needed_count": sum(
            row.recorder_fix_needed
            for row in audits
        ),
        "test_fix_needed_count": sum(
            row.test_fix_needed
            for row in audits
        ),
        "blocking_record_count": blocking,
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2d_metadata.json"
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
        "Phase 155-R3-2D missing execution record audit completed."
    )
    print(
        "missing test references:",
        len(audits),
    )
    print(
        "parameterized all-pass:",
        counts[
            CAUSE_PARAMETERIZED_ALL_PASS
        ],
    )
    print(
        "parameterized with failure:",
        counts[
            CAUSE_PARAMETERIZED_HAS_FAILURE
        ],
    )
    print(
        "collected but not recorded:",
        counts[
            CAUSE_COLLECTED_BUT_NOT_RECORDED
        ],
    )
    print(
        "nonparameterized normalized match:",
        counts[
            CAUSE_NONPARAMETERIZED_MATCH
        ],
    )
    print(
        "not collected:",
        counts[
            CAUSE_NOT_COLLECTED
        ],
    )
    print(
        "unresolved:",
        counts[
            CAUSE_UNRESOLVED
        ],
    )
    print(
        "recorder fix needed:",
        sum(
            row.recorder_fix_needed
            for row in audits
        ),
    )
    print(
        "test fix needed:",
        sum(
            row.test_fix_needed
            for row in audits
        ),
    )
    print(
        "blocking records:",
        blocking,
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
