from __future__ import annotations

import argparse
import ast
import csv
import json
import shutil
from collections import defaultdict
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


def _find_top_level_function(
    tree: ast.Module,
    function_name: str,
) -> ast.FunctionDef:
    matches = [
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

    if len(
        matches
    ) != 1:
        raise RuntimeError(
            "expected exactly one top-level function "
            + function_name
        )

    return matches[
        0
    ]


def _function_span(
    node: ast.FunctionDef,
) -> tuple[
    int,
    int,
]:
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


def _remove_functions(
    path: Path,
    function_names: set[str],
) -> None:
    source = path.read_text(
        encoding="utf-8-sig",
    )
    tree = ast.parse(
        source
    )
    lines = source.splitlines(
        keepends=True
    )

    spans = []

    for function_name in sorted(
        function_names
    ):
        function = (
            _find_top_level_function(
                tree,
                function_name,
            )
        )
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

    path.write_text(
        new_source,
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
            "phase155_r3_3c_removal_output"
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
        test_id = row[
            "test_id"
        ]
        target_file, function_name = (
            _split_test_id(
                test_id
            )
        )
        functions_by_file[
            target_file
        ].add(
            function_name
        )

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )
    backup_root = (
        repo_root.parent
        / (
            repo_root.name
            + "_phase155_r3_3c_backup_"
            + timestamp
        )
    )

    affected_files = sorted(
        functions_by_file
    )

    for relative in affected_files:
        source_path = (
            repo_root
            / relative
        )

        if not source_path.exists():
            raise RuntimeError(
                "affected source file not found before deletion: "
                + str(
                    source_path
                )
            )

        backup_path = (
            backup_root
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

    deleted_whole_files = []
    modified_function_files = []

    for relative in affected_files:
        source_path = (
            repo_root
            / relative
        )

        if relative in safe_whole_files:
            source_path.unlink()
            deleted_whole_files.append(
                relative
            )
            continue

        _remove_functions(
            source_path,
            functions_by_file[
                relative
            ],
        )
        modified_function_files.append(
            relative
        )

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = {
        "phase": "155-R3-3C",
        "backup_root": str(
            backup_root
        ),
        "safe_function_deletions": len(
            safe_candidates
        ),
        "affected_files": len(
            affected_files
        ),
        "whole_files_deleted": len(
            deleted_whole_files
        ),
        "function_only_files_modified": len(
            modified_function_files
        ),
        "deleted_whole_files": (
            deleted_whole_files
        ),
        "modified_function_files": (
            modified_function_files
        ),
        "production_code_modified": False,
    }

    (
        output_dir
        / "phase155_r3_3c_removal_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r3_3c_deleted_test_ids.txt"
    ).write_text(
        "\n".join(
            sorted(
                row[
                    "test_id"
                ]
                for row
                in safe_candidates
            )
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R3-3C verified duplicate removal applied."
    )
    print(
        "safe test functions removed:",
        len(
            safe_candidates
        ),
    )
    print(
        "affected files:",
        len(
            affected_files
        ),
    )
    print(
        "whole test files deleted:",
        len(
            deleted_whole_files
        ),
    )
    print(
        "function-only test files modified:",
        len(
            modified_function_files
        ),
    )
    print(
        "backup:",
        backup_root,
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
