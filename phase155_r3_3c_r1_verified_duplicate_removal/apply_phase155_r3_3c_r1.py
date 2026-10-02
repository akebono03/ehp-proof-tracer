from __future__ import annotations

import argparse
import ast
import csv
import json
import shutil
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


SAFE_FUNCTION = "safe_function_deletion"
SAFE_WHOLE_FILE = "safe_whole_file_deletion"


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


def _matching_top_level_functions(
    tree: ast.Module,
    function_name: str,
) -> list[ast.FunctionDef]:
    return [
        node
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == function_name
        )
    ]


def _function_span(
    node: ast.FunctionDef,
) -> tuple[int, int]:
    decorator_lines = [
        decorator.lineno
        for decorator in node.decorator_list
    ]

    start_line = min(
        [
            node.lineno,
            *decorator_lines,
        ]
    )
    end_line = (
        node.end_lineno
        if node.end_lineno
        is not None
        else node.lineno
    )

    return (
        start_line,
        end_line,
    )


def _render_without_functions(
    source: str,
    function_names: set[str],
) -> tuple[str, Counter[str]]:
    tree = ast.parse(
        source
    )
    lines = source.splitlines(
        keepends=True
    )
    spans = []
    counts: Counter[str] = Counter()

    for function_name in sorted(
        function_names
    ):
        matches = (
            _matching_top_level_functions(
                tree,
                function_name,
            )
        )

        if not matches:
            raise RuntimeError(
                "candidate top-level function not found: "
                + function_name
            )

        counts[
            function_name
        ] = len(
            matches
        )

        for function in matches:
            start_line, end_line = (
                _function_span(
                    function
                )
            )
            spans.append(
                (
                    start_line,
                    end_line,
                    function_name,
                )
            )

    spans.sort(
        reverse=True
    )

    for (
        start_line,
        end_line,
        _function_name,
    ) in spans:
        start_index = (
            start_line
            - 1
        )
        end_index = end_line

        while (
            end_index
            < len(
                lines
            )
            and lines[
                end_index
            ].strip()
            == ""
        ):
            end_index += 1

        del lines[
            start_index:
            end_index
        ]

    new_source = "".join(
        lines
    )

    ast.parse(
        new_source
    )

    return (
        new_source,
        counts,
    )


def _latest_failed_backup(
    repo_root: Path,
) -> Path:
    pattern = (
        repo_root.name
        + "_phase155_r3_3c_backup_*"
    )
    candidates = sorted(
        [
            path
            for path in repo_root.parent.glob(
                pattern
            )
            if path.is_dir()
        ],
        key=lambda path: (
            path.stat().st_mtime,
            path.name,
        ),
        reverse=True,
    )

    if not candidates:
        raise RuntimeError(
            "No Phase 155-R3-3C backup directory was found beside the repository."
        )

    return candidates[
        0
    ]


def _restore_partial_attempt(
    repo_root: Path,
    backup_root: Path,
    affected_files: set[str],
) -> None:
    missing_backup_files = [
        relative
        for relative in sorted(
            affected_files
        )
        if not (
            backup_root
            / relative
        ).exists()
    ]

    if missing_backup_files:
        raise RuntimeError(
            "The failed-run backup is incomplete. Missing: "
            + ", ".join(
                missing_backup_files
            )
        )

    for relative in sorted(
        affected_files
    ):
        backup_path = (
            backup_root
            / relative
        )
        destination = (
            repo_root
            / relative
        )
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copy2(
            backup_path,
            destination,
        )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
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
            "phase155_r3_3c_r1_removal_output"
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
        args.candidate_safety
    )
    file_path = resolve(
        args.file_safety
    )

    for required in (
        candidate_path,
        file_path,
    ):
        if not required.exists():
            raise SystemExit(
                "required R3-3B input not found: "
                + str(
                    required
                )
            )

    candidate_rows = _read_csv(
        candidate_path
    )
    file_rows = _read_csv(
        file_path
    )

    safe_candidates = [
        row
        for row in candidate_rows
        if row.get(
            "function_status"
        )
        == SAFE_FUNCTION
    ]
    safe_whole_files = {
        row[
            "file_path"
        ]
        for row in file_rows
        if row.get(
            "file_status"
        )
        == SAFE_WHOLE_FILE
    }

    if len(
        safe_candidates
    ) != 161:
        raise RuntimeError(
            "expected exactly 161 safe function deletions, got "
            + str(
                len(
                    safe_candidates
                )
            )
        )

    if len(
        safe_whole_files
    ) != 5:
        raise RuntimeError(
            "expected exactly 5 safe whole-file deletions, got "
            + str(
                len(
                    safe_whole_files
                )
            )
        )

    functions_by_file: dict[
        str,
        set[str],
    ] = defaultdict(
        set
    )

    for row in safe_candidates:
        target_file, function_name = (
            _split_test_id(
                row[
                    "test_id"
                ]
            )
        )
        functions_by_file[
            target_file
        ].add(
            function_name
        )

    affected_files = set(
        functions_by_file
    )

    failed_backup = (
        _latest_failed_backup(
            repo_root
        )
    )

    print(
        "Restoring failed R3-3C partial application from:"
    )
    print(
        failed_backup
    )

    _restore_partial_attempt(
        repo_root,
        failed_backup,
        affected_files,
    )

    staged_sources: dict[
        str,
        str
    ] = {}
    definition_counts: Counter[
        int
    ] = Counter()
    duplicate_definition_targets = []

    for relative in sorted(
        affected_files
    ):
        source_path = (
            repo_root
            / relative
        )

        if not source_path.exists():
            raise RuntimeError(
                "restored affected file is missing: "
                + relative
            )

        source = source_path.read_text(
            encoding="utf-8-sig",
        )

        if relative in safe_whole_files:
            ast.parse(
                source
            )
            continue

        new_source, counts = (
            _render_without_functions(
                source,
                functions_by_file[
                    relative
                ],
            )
        )

        for function_name, count in counts.items():
            definition_counts[
                count
            ] += 1

            if count > 1:
                duplicate_definition_targets.append(
                    {
                        "test_id": (
                            relative
                            + "::"
                            + function_name
                        ),
                        "source_definition_count": (
                            count
                        ),
                    }
                )

        staged_sources[
            relative
        ] = new_source

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )
    new_backup_root = (
        repo_root.parent
        / (
            repo_root.name
            + "_phase155_r3_3c_r1_backup_"
            + timestamp
        )
    )

    for relative in sorted(
        affected_files
    ):
        source_path = (
            repo_root
            / relative
        )
        backup_path = (
            new_backup_root
            / relative
        )
        backup_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copy2(
            source_path,
            backup_path,
        )

    for relative, new_source in (
        staged_sources.items()
    ):
        (
            repo_root
            / relative
        ).write_text(
            new_source,
            encoding="utf-8",
        )

    for relative in sorted(
        safe_whole_files
    ):
        (
            repo_root
            / relative
        ).unlink()

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = {
        "phase": "155-R3-3C-r1",
        "restored_failed_backup": str(
            failed_backup
        ),
        "new_backup_root": str(
            new_backup_root
        ),
        "safe_test_ids_removed": len(
            safe_candidates
        ),
        "affected_files": len(
            affected_files
        ),
        "whole_files_deleted": len(
            safe_whole_files
        ),
        "function_only_files_modified": len(
            staged_sources
        ),
        "duplicate_definition_targets": (
            duplicate_definition_targets
        ),
        "duplicate_definition_target_count": len(
            duplicate_definition_targets
        ),
        "definition_count_distribution": {
            str(
                key
            ): value
            for key, value
            in sorted(
                definition_counts.items()
            )
        },
        "production_code_modified": False,
    }

    (
        output_dir
        / "phase155_r3_3c_r1_removal_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R3-3C-r1 verified duplicate removal applied."
    )
    print(
        "safe test IDs removed:",
        len(
            safe_candidates
        ),
    )
    print(
        "whole test files deleted:",
        len(
            safe_whole_files
        ),
    )
    print(
        "function-only files modified:",
        len(
            staged_sources
        ),
    )
    print(
        "targets with duplicate source definitions:",
        len(
            duplicate_definition_targets
        ),
    )
    print(
        "new backup:",
        new_backup_root,
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
