
from __future__ import annotations

import argparse
import ast
import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


REMOVABLE = "removable_duplicate"
RETAIN = "retain_independent"
HISTORICAL = "historical_keep"
REVIEW = "needs_review"
SAFE_FUNCTION = "safe_function_deletion"
SAFE_WHOLE_FILE = "safe_whole_file_deletion"


@dataclass(frozen=True)
class TestLocation:
    test_id: str
    file_path: str
    function_name: str
    file_exists: bool
    function_definition_count: int
    exists: bool


@dataclass(frozen=True)
class PairClosure:
    candidate_id: str
    decision: str
    older_test_id: str
    newer_test_id: str
    older_exists: bool
    newer_exists: bool
    both_exist: bool
    closure_status: str


@dataclass(frozen=True)
class DuplicateDefinition:
    file_path: str
    function_name: str
    definition_count: int


def _read_csv(
    path: Path,
) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _write_dataclass_csv(
    path: Path,
    rows: list[object],
) -> None:
    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    first = asdict(rows[0])

    with path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(first),
        )
        writer.writeheader()

        for row in rows:
            writer.writerow(
                asdict(row)
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
        return completed.stdout.strip()
    except (
        OSError,
        subprocess.CalledProcessError,
    ):
        return "unavailable"


def _split_test_id(
    test_id: str,
) -> tuple[str, str]:
    file_path, function_name = test_id.split(
        "::",
        1,
    )

    return (
        file_path.replace(
            "\\",
            "/",
        ),
        function_name,
    )


def _parse_test_file(
    path: Path,
) -> ast.Module:
    return ast.parse(
        path.read_text(
            encoding="utf-8-sig",
        )
    )


def _top_level_test_counts(
    tree: ast.Module,
) -> Counter[str]:
    return Counter(
        node.name
        for node in tree.body
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name.startswith(
                "test_"
            )
        )
    )


def _inventory(
    repo_root: Path,
) -> tuple[
    int,
    int,
    list[
        DuplicateDefinition
    ],
    dict[
        str,
        Counter[str]
    ],
]:
    test_files = sorted(
        (
            repo_root
            / "tests"
        ).glob(
            "test_*.py"
        )
    )

    total_functions = 0
    duplicates = []
    counts_by_file = {}

    for path in test_files:
        relative = path.relative_to(
            repo_root
        ).as_posix()
        tree = _parse_test_file(
            path
        )
        counts = _top_level_test_counts(
            tree
        )
        counts_by_file[
            relative
        ] = counts
        total_functions += sum(
            counts.values()
        )

        for name, count in sorted(
            counts.items()
        ):
            if count > 1:
                duplicates.append(
                    DuplicateDefinition(
                        file_path=relative,
                        function_name=name,
                        definition_count=count,
                    )
                )

    return (
        len(
            test_files
        ),
        total_functions,
        duplicates,
        counts_by_file,
    )


def _locate(
    repo_root: Path,
    test_id: str,
    counts_by_file: dict[
        str,
        Counter[str]
    ],
) -> TestLocation:
    file_path, function_name = (
        _split_test_id(
            test_id
        )
    )
    path = repo_root / file_path
    file_exists = path.exists()
    count = (
        counts_by_file.get(
            file_path,
            Counter(),
        ).get(
            function_name,
            0,
        )
        if file_exists
        else 0
    )

    return TestLocation(
        test_id=test_id,
        file_path=file_path,
        function_name=function_name,
        file_exists=file_exists,
        function_definition_count=count,
        exists=(
            file_exists
            and count > 0
        ),
    )


def _pair_closure_rows(
    repo_root: Path,
    verified_pairs: list[
        dict[
            str,
            str,
        ]
    ],
    counts_by_file: dict[
        str,
        Counter[str]
    ],
) -> list[
    PairClosure
]:
    result = []

    for row in verified_pairs:
        older = _locate(
            repo_root,
            row[
                "older_test_id"
            ],
            counts_by_file,
        )
        newer = _locate(
            repo_root,
            row[
                "newer_test_id"
            ],
            counts_by_file,
        )
        decision = row.get(
            "decision",
            "",
        )
        both_exist = (
            older.exists
            and newer.exists
        )

        if decision == REMOVABLE:
            closure_status = (
                "unresolved_removable_pair"
                if both_exist
                else "resolved_removable_pair"
            )
        elif decision == HISTORICAL:
            closure_status = (
                "historical_preserved"
                if (
                    older.exists
                    and newer.exists
                )
                else "historical_missing"
            )
        elif decision == REVIEW:
            closure_status = (
                "unexpected_needs_review"
            )
        else:
            closure_status = (
                "retain_pair_observed"
            )

        result.append(
            PairClosure(
                candidate_id=row.get(
                    "candidate_id",
                    "",
                ),
                decision=decision,
                older_test_id=(
                    row[
                        "older_test_id"
                    ]
                ),
                newer_test_id=(
                    row[
                        "newer_test_id"
                    ]
                ),
                older_exists=(
                    older.exists
                ),
                newer_exists=(
                    newer.exists
                ),
                both_exist=(
                    both_exist
                ),
                closure_status=(
                    closure_status
                ),
            )
        )

    return result


def _collect_only(
    repo_root: Path,
    targets: list[
        str
    ],
) -> tuple[
    int,
    str,
]:
    if not targets:
        return (
            0,
            "",
        )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
            *targets,
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )

    output = (
        completed.stdout
        + completed.stderr
    )

    return (
        completed.returncode,
        output,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--verified-pairs",
        type=Path,
        default=Path(
            "phase155_r3_2f_r1_audit_output/"
            "phase155_r3_2f_r1_verified_pairs.csv"
        ),
    )
    parser.add_argument(
        "--graph-nodes",
        type=Path,
        default=Path(
            "phase155_r3_3a_audit_output/"
            "phase155_r3_3a_nodes.csv"
        ),
    )
    parser.add_argument(
        "--candidate-safety",
        type=Path,
        default=Path(
            "phase155_r3_3b_audit_output/"
            "phase155_r3_3b_candidate_safety.csv"
        ),
    )
    parser.add_argument(
        "--file-safety",
        type=Path,
        default=Path(
            "phase155_r3_3b_audit_output/"
            "phase155_r3_3b_file_safety.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_3d_audit_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(
        path: Path,
    ) -> Path:
        return (
            path
            if path.is_absolute()
            else repo_root
            / path
        )

    required_paths = {
        "verified_pairs": resolve(
            args.verified_pairs
        ),
        "graph_nodes": resolve(
            args.graph_nodes
        ),
        "candidate_safety": resolve(
            args.candidate_safety
        ),
        "file_safety": resolve(
            args.file_safety
        ),
    }

    for label, path in (
        required_paths.items()
    ):
        if not path.exists():
            raise SystemExit(
                label
                + " input not found: "
                + str(
                    path
                )
            )

    verified_pairs = _read_csv(
        required_paths[
            "verified_pairs"
        ]
    )
    graph_nodes = _read_csv(
        required_paths[
            "graph_nodes"
        ]
    )
    candidate_safety = _read_csv(
        required_paths[
            "candidate_safety"
        ]
    )
    file_safety = _read_csv(
        required_paths[
            "file_safety"
        ]
    )

    (
        test_file_count,
        test_function_definition_count,
        duplicate_definitions,
        counts_by_file,
    ) = _inventory(
        repo_root
    )

    safe_deletion_ids = sorted(
        {
            row[
                "test_id"
            ]
            for row in candidate_safety
            if row.get(
                "function_status"
            )
            == SAFE_FUNCTION
        }
    )
    deleted_locations = [
        _locate(
            repo_root,
            test_id,
            counts_by_file,
        )
        for test_id in (
            safe_deletion_ids
        )
    ]
    deletion_ids_still_present = [
        row
        for row in (
            deleted_locations
        )
        if row.exists
    ]

    whole_file_targets = sorted(
        {
            row[
                "file_path"
            ]
            for row in file_safety
            if row.get(
                "file_status"
            )
            == SAFE_WHOLE_FILE
        }
    )
    whole_files_still_present = [
        relative
        for relative in (
            whole_file_targets
        )
        if (
            repo_root
            / relative
        ).exists()
    ]

    survivor_ids = sorted(
        {
            row[
                "test_id"
            ]
            for row in graph_nodes
            if row.get(
                "deletion_candidate",
                "",
            ).lower()
            not in (
                "true",
                "1",
                "yes",
            )
        }
    )
    survivor_locations = [
        _locate(
            repo_root,
            test_id,
            counts_by_file,
        )
        for test_id in survivor_ids
    ]
    missing_survivors = [
        row
        for row in (
            survivor_locations
        )
        if not row.exists
    ]

    pair_rows = _pair_closure_rows(
        repo_root,
        verified_pairs,
        counts_by_file,
    )
    pair_status_counts = Counter(
        row.closure_status
        for row in pair_rows
    )

    historical_ids = sorted(
        {
            test_id
            for row in verified_pairs
            if row.get(
                "decision"
            )
            == HISTORICAL
            for test_id in (
                row[
                    "older_test_id"
                ],
                row[
                    "newer_test_id"
                ],
            )
        }
    )
    historical_locations = [
        _locate(
            repo_root,
            test_id,
            counts_by_file,
        )
        for test_id in historical_ids
    ]
    missing_historical = [
        row
        for row in (
            historical_locations
        )
        if not row.exists
    ]

    affected_remaining_files = sorted(
        {
            row[
                "file_path"
            ]
            for row in candidate_safety
            if (
                row.get(
                    "function_status"
                )
                == SAFE_FUNCTION
                and (
                    repo_root
                    / row[
                        "file_path"
                    ]
                ).exists()
            )
        }
    )

    collect_exit, collect_output = (
        _collect_only(
            repo_root,
            affected_remaining_files,
        )
    )

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    _write_dataclass_csv(
        output_dir
        / "phase155_r3_3d_pair_closure.csv",
        pair_rows,
    )
    _write_dataclass_csv(
        output_dir
        / "phase155_r3_3d_deleted_id_locations.csv",
        deleted_locations,
    )
    _write_dataclass_csv(
        output_dir
        / "phase155_r3_3d_survivor_locations.csv",
        survivor_locations,
    )
    _write_dataclass_csv(
        output_dir
        / "phase155_r3_3d_historical_locations.csv",
        historical_locations,
    )
    _write_dataclass_csv(
        output_dir
        / "phase155_r3_3d_duplicate_definitions.csv",
        duplicate_definitions,
    )

    (
        output_dir
        / "phase155_r3_3d_collect_only.txt"
    ).write_text(
        collect_output,
        encoding="utf-8",
    )

    completion_conditions = {
        "safe_deletion_ids_expected_161": (
            len(
                safe_deletion_ids
            )
            == 161
        ),
        "all_safe_deletion_ids_absent": (
            not deletion_ids_still_present
        ),
        "whole_file_targets_expected_5": (
            len(
                whole_file_targets
            )
            == 5
        ),
        "all_whole_file_targets_absent": (
            not whole_files_still_present
        ),
        "all_graph_survivors_present": (
            not missing_survivors
        ),
        "all_historical_keep_ids_present": (
            not missing_historical
        ),
        "no_unresolved_removable_pairs": (
            pair_status_counts[
                "unresolved_removable_pair"
            ]
            == 0
        ),
        "no_needs_review_pairs": (
            pair_status_counts[
                "unexpected_needs_review"
            ]
            == 0
        ),
        "no_source_level_duplicate_test_names": (
            not duplicate_definitions
        ),
        "affected_collection_exit_zero": (
            collect_exit
            == 0
        ),
    }
    closure_satisfied = all(
        completion_conditions.values()
    )

    summary_lines = [
        "# Phase 155-R3-3D — post-removal closure audit",
        "",
        "## Current inventory",
        "",
        f"- `tests/test_*.py`: {test_file_count}",
        f"- source-level top-level `test_*` definitions: {test_function_definition_count}",
        "",
        "R1 の historical inventory 数は固定 completion 条件には使用しない。R3-3D は current tree の実体を監査する。",
        "",
        "## Removal closure",
        "",
        f"- R3-3B safe deletion test IDs: {len(safe_deletion_ids)}",
        f"- safe deletion IDs still present: {len(deletion_ids_still_present)}",
        f"- whole-file deletion targets: {len(whole_file_targets)}",
        f"- whole-file targets still present: {len(whole_files_still_present)}",
        "",
        "## Survivor / historical protection",
        "",
        f"- graph survivor base test IDs: {len(survivor_ids)}",
        f"- missing graph survivors: {len(missing_survivors)}",
        f"- unique historical_keep test IDs: {len(historical_ids)}",
        f"- missing historical_keep IDs: {len(missing_historical)}",
        "",
        "## Candidate-pair closure",
        "",
        f"- verified candidate pairs: {len(verified_pairs)}",
        f"- resolved removable pairs: {pair_status_counts['resolved_removable_pair']}",
        f"- unresolved removable pairs: {pair_status_counts['unresolved_removable_pair']}",
        f"- historical pairs preserved: {pair_status_counts['historical_preserved']}",
        f"- historical pairs missing: {pair_status_counts['historical_missing']}",
        f"- retain-independent pairs observed: {pair_status_counts['retain_pair_observed']}",
        f"- needs-review pairs: {pair_status_counts['unexpected_needs_review']}",
        "",
        "## Source / collection integrity",
        "",
        f"- source-level duplicate test names: {len(duplicate_definitions)}",
        f"- remaining affected test files collected: {len(affected_remaining_files)}",
        f"- focused collect-only exit code: {collect_exit}",
        "",
        "## Completion conditions",
        "",
    ]

    for key, value in (
        completion_conditions.items()
    ):
        summary_lines.append(
            "- "
            + key
            + ": "
            + (
                "PASS"
                if value
                else "FAIL"
            )
        )

    summary_lines.extend(
        [
            "",
            "## R3-3D conclusion",
            "",
            (
                "**R3 duplicate/superseded cleanup closure satisfied: True**"
                if closure_satisfied
                else "**R3 duplicate/superseded cleanup closure satisfied: False**"
            ),
            "",
            "Repository-wide pytest is NOT run here. It remains deferred to Phase 155 closure.",
        ]
    )

    (
        output_dir
        / "phase155_r3_3d_summary.md"
    ).write_text(
        "\n".join(
            summary_lines
        )
        + "\n",
        encoding="utf-8",
    )

    metadata = {
        "phase": "155-R3-3D",
        "git_head": _git_head(
            repo_root
        ),
        "test_files": test_file_count,
        "test_function_definitions": (
            test_function_definition_count
        ),
        "safe_deletion_ids": len(
            safe_deletion_ids
        ),
        "safe_deletion_ids_still_present": len(
            deletion_ids_still_present
        ),
        "whole_file_targets": len(
            whole_file_targets
        ),
        "whole_file_targets_still_present": len(
            whole_files_still_present
        ),
        "graph_survivors": len(
            survivor_ids
        ),
        "missing_graph_survivors": len(
            missing_survivors
        ),
        "historical_keep_ids": len(
            historical_ids
        ),
        "missing_historical_keep_ids": len(
            missing_historical
        ),
        "unresolved_removable_pairs": (
            pair_status_counts[
                "unresolved_removable_pair"
            ]
        ),
        "source_level_duplicate_test_names": len(
            duplicate_definitions
        ),
        "affected_collect_only_exit_code": (
            collect_exit
        ),
        "closure_satisfied": (
            closure_satisfied
        ),
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3d_metadata.json"
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
        "Phase 155-R3-3D post-removal closure audit completed."
    )
    print(
        "current test files:",
        test_file_count,
    )
    print(
        "current source test definitions:",
        test_function_definition_count,
    )
    print(
        "safe deletion IDs:",
        len(
            safe_deletion_ids
        ),
    )
    print(
        "safe deletion IDs still present:",
        len(
            deletion_ids_still_present
        ),
    )
    print(
        "whole-file targets still present:",
        len(
            whole_files_still_present
        ),
    )
    print(
        "missing graph survivors:",
        len(
            missing_survivors
        ),
    )
    print(
        "missing historical_keep IDs:",
        len(
            missing_historical
        ),
    )
    print(
        "unresolved removable pairs:",
        pair_status_counts[
            "unresolved_removable_pair"
        ],
    )
    print(
        "source-level duplicate test names:",
        len(
            duplicate_definitions
        ),
    )
    print(
        "focused collect-only exit code:",
        collect_exit,
    )
    print(
        "R3 closure condition satisfied:",
        closure_satisfied,
    )
    print(
        "output:",
        output_dir,
    )

    return (
        0
        if closure_satisfied
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
