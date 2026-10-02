from __future__ import annotations

import argparse
import ast
import csv
import json
import subprocess
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


FUNCTION_SAFE = "safe_function_deletion"
FUNCTION_BLOCKED_EXTERNAL = "blocked_external_function_reference"
FUNCTION_MISSING = "missing_candidate_function"
FUNCTION_PARSE_ERROR = "candidate_file_parse_error"

FILE_SAFE = "safe_whole_file_deletion"
FILE_FUNCTION_ONLY = "function_only_retained_tests_or_symbols"
FILE_BLOCKED_EXTERNAL = "blocked_external_module_import"
FILE_UNRESOLVED = "unresolved_file_safety"


@dataclass(frozen=True)
class CandidateRecord:
    test_id: str
    file_path: str
    function_name: str
    function_status: str
    external_function_reference_count: int
    external_function_references: str
    file_test_function_count: int
    deletion_candidate_test_count: int
    retained_test_count: int
    retained_tests: str
    module_helper_count: int
    module_constant_count: int
    module_import_count: int
    externally_imported_symbol_count: int
    externally_imported_symbols: str
    whole_module_import_count: int
    whole_module_importers: str
    file_status: str
    recommended_action: str
    reason: str


@dataclass(frozen=True)
class FileRecord:
    file_path: str
    test_function_count: int
    deletion_candidate_test_count: int
    retained_test_count: int
    retained_tests: str
    helper_function_count: int
    helper_functions: str
    class_count: int
    classes: str
    constant_count: int
    constants: str
    import_count: int
    external_symbol_import_count: int
    external_symbol_imports: str
    whole_module_import_count: int
    whole_module_importers: str
    file_status: str
    recommended_action: str
    reason: str


def _git_head(
    repo_root: Path,
) -> str:
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


def _read_csv(
    path: Path,
) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _write_csv(
    path: Path,
    rows: Iterable[object],
) -> None:
    rows = list(rows)

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fieldnames = list(
        asdict(rows[0]).keys()
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
                asdict(row)
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


def _module_name_from_test_path(
    file_path: str,
) -> str:
    normalized = file_path.replace(
        "\\",
        "/",
    )

    if not normalized.endswith(
        ".py"
    ):
        raise ValueError(
            "test path must end with .py"
        )

    return normalized[
        :-3
    ].replace(
        "/",
        ".",
    )


def _top_level_test_functions(
    tree: ast.Module,
) -> list[ast.FunctionDef]:
    return [
        node
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name.startswith(
                "test_"
            )
        )
    ]


def _top_level_helpers(
    tree: ast.Module,
) -> list[str]:
    return [
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
            and not node.name.startswith(
                "test_"
            )
        )
    ]


def _top_level_classes(
    tree: ast.Module,
) -> list[str]:
    return [
        node.name
        for node in tree.body
        if isinstance(
            node,
            ast.ClassDef,
        )
    ]


def _top_level_constants(
    tree: ast.Module,
) -> list[str]:
    result = []

    for node in tree.body:
        if isinstance(
            node,
            ast.Assign,
        ):
            for target in node.targets:
                if (
                    isinstance(
                        target,
                        ast.Name,
                    )
                    and target.id.upper()
                    == target.id
                ):
                    result.append(
                        target.id
                    )

        elif (
            isinstance(
                node,
                ast.AnnAssign,
            )
            and isinstance(
                node.target,
                ast.Name,
            )
            and node.target.id.upper()
            == node.target.id
        ):
            result.append(
                node.target.id
            )

    return result


def _top_level_import_count(
    tree: ast.Module,
) -> int:
    return sum(
        isinstance(
            node,
            (
                ast.Import,
                ast.ImportFrom,
            ),
        )
        for node in tree.body
    )


def _iter_active_python_files(
    repo_root: Path,
) -> Iterable[Path]:
    ignored_top_levels = {
        ".git",
        ".pytest_cache",
        "__pycache__",
        ".venv",
        "venv",
    }

    for path in repo_root.rglob(
        "*.py"
    ):
        relative = path.relative_to(
            repo_root
        )

        if (
            relative.parts
            and relative.parts[0]
            in ignored_top_levels
        ):
            continue

        if "__pycache__" in relative.parts:
            continue

        yield path


def _parse_repository(
    repo_root: Path,
) -> tuple[
    dict[str, ast.Module],
    dict[str, str],
]:
    trees = {}
    errors = {}

    for path in _iter_active_python_files(
        repo_root
    ):
        relative = path.relative_to(
            repo_root
        ).as_posix()

        try:
            source = path.read_text(
                encoding="utf-8-sig",
            )
            trees[
                relative
            ] = ast.parse(
                source
            )
        except (
            OSError,
            SyntaxError,
            UnicodeError,
        ) as exc:
            errors[
                relative
            ] = (
                type(exc).__name__
                + ": "
                + str(exc)
            )

    return (
        trees,
        errors,
    )


def _external_imports_for_module(
    trees: dict[str, ast.Module],
    target_file: str,
) -> tuple[
    list[tuple[str, str]],
    list[str],
]:
    target_module = (
        _module_name_from_test_path(
            target_file
        )
    )
    symbol_imports = []
    module_importers = []

    for file_path, tree in trees.items():
        if file_path == target_file:
            continue

        for node in ast.walk(
            tree
        ):
            if isinstance(
                node,
                ast.ImportFrom,
            ):
                module = (
                    node.module
                    or ""
                )

                if module == target_module:
                    for alias in node.names:
                        symbol_imports.append(
                            (
                                file_path,
                                alias.name,
                            )
                        )

            elif isinstance(
                node,
                ast.Import,
            ):
                for alias in node.names:
                    if (
                        alias.name
                        == target_module
                    ):
                        module_importers.append(
                            file_path
                        )

    return (
        sorted(
            set(
                symbol_imports
            )
        ),
        sorted(
            set(
                module_importers
            )
        ),
    )


def _external_function_references(
    trees: dict[str, ast.Module],
    target_file: str,
    function_name: str,
) -> list[str]:
    target_module = (
        _module_name_from_test_path(
            target_file
        )
    )
    result = []

    for file_path, tree in trees.items():
        if file_path == target_file:
            continue

        imported_aliases = set()
        module_aliases = set()

        for node in ast.walk(
            tree
        ):
            if isinstance(
                node,
                ast.ImportFrom,
            ) and (
                node.module
                == target_module
            ):
                for alias in node.names:
                    if (
                        alias.name
                        == function_name
                    ):
                        imported_aliases.add(
                            alias.asname
                            or alias.name
                        )

            elif isinstance(
                node,
                ast.Import,
            ):
                for alias in node.names:
                    if (
                        alias.name
                        == target_module
                    ):
                        module_aliases.add(
                            alias.asname
                            or alias.name.split(
                                "."
                            )[
                                -1
                            ]
                        )

        if imported_aliases:
            result.append(
                file_path
                + ":direct-import"
            )

        if module_aliases:
            for node in ast.walk(
                tree
            ):
                if (
                    isinstance(
                        node,
                        ast.Attribute,
                    )
                    and node.attr
                    == function_name
                    and isinstance(
                        node.value,
                        ast.Name,
                    )
                    and node.value.id
                    in module_aliases
                ):
                    result.append(
                        file_path
                        + ":module-attribute"
                    )
                    break

    return sorted(
        set(
            result
        )
    )


def build_safety_audit(
    repo_root: Path,
    deletion_rows: list[
        dict[
            str,
            str,
        ]
    ],
) -> tuple[
    list[CandidateRecord],
    list[FileRecord],
]:
    candidate_ids = {
        row[
            "test_id"
        ]
        for row in deletion_rows
    }
    candidates_by_file: dict[
        str,
        set[str],
    ] = defaultdict(
        set
    )

    for test_id in candidate_ids:
        file_path, function_name = (
            _split_test_id(
                test_id
            )
        )
        candidates_by_file[
            file_path
        ].add(
            function_name
        )

    trees, parse_errors = (
        _parse_repository(
            repo_root
        )
    )

    file_records = []
    candidate_records = []

    for file_path in sorted(
        candidates_by_file
    ):
        candidate_functions = (
            candidates_by_file[
                file_path
            ]
        )
        tree = trees.get(
            file_path
        )

        if tree is None:
            reason = (
                parse_errors.get(
                    file_path,
                    "candidate file missing from repository scan",
                )
            )

            for function_name in sorted(
                candidate_functions
            ):
                candidate_records.append(
                    CandidateRecord(
                        test_id=(
                            file_path
                            + "::"
                            + function_name
                        ),
                        file_path=file_path,
                        function_name=(
                            function_name
                        ),
                        function_status=(
                            FUNCTION_PARSE_ERROR
                        ),
                        external_function_reference_count=0,
                        external_function_references="",
                        file_test_function_count=0,
                        deletion_candidate_test_count=len(
                            candidate_functions
                        ),
                        retained_test_count=0,
                        retained_tests="",
                        module_helper_count=0,
                        module_constant_count=0,
                        module_import_count=0,
                        externally_imported_symbol_count=0,
                        externally_imported_symbols="",
                        whole_module_import_count=0,
                        whole_module_importers="",
                        file_status=(
                            FILE_UNRESOLVED
                        ),
                        recommended_action="retain",
                        reason=reason,
                    )
                )

            file_records.append(
                FileRecord(
                    file_path=file_path,
                    test_function_count=0,
                    deletion_candidate_test_count=len(
                        candidate_functions
                    ),
                    retained_test_count=0,
                    retained_tests="",
                    helper_function_count=0,
                    helper_functions="",
                    class_count=0,
                    classes="",
                    constant_count=0,
                    constants="",
                    import_count=0,
                    external_symbol_import_count=0,
                    external_symbol_imports="",
                    whole_module_import_count=0,
                    whole_module_importers="",
                    file_status=(
                        FILE_UNRESOLVED
                    ),
                    recommended_action="retain",
                    reason=reason,
                )
            )
            continue

        test_functions = {
            node.name
            for node in (
                _top_level_test_functions(
                    tree
                )
            )
        }
        retained_tests = sorted(
            test_functions
            - candidate_functions
        )
        helpers = sorted(
            _top_level_helpers(
                tree
            )
        )
        classes = sorted(
            _top_level_classes(
                tree
            )
        )
        constants = sorted(
            _top_level_constants(
                tree
            )
        )
        import_count = (
            _top_level_import_count(
                tree
            )
        )

        (
            symbol_imports,
            module_importers,
        ) = _external_imports_for_module(
            trees,
            file_path,
        )

        externally_imported_symbols = [
            source_file
            + ":"
            + symbol
            for (
                source_file,
                symbol,
            )
            in symbol_imports
        ]

        all_tests_are_candidates = (
            bool(
                test_functions
            )
            and test_functions.issubset(
                candidate_functions
            )
        )

        if module_importers:
            file_status = (
                FILE_BLOCKED_EXTERNAL
            )
            recommended_action = (
                "function deletion only"
            )
            file_reason = (
                "Whole module is imported elsewhere."
            )

        elif symbol_imports:
            file_status = (
                FILE_BLOCKED_EXTERNAL
            )
            recommended_action = (
                "function deletion only; preserve imported helpers/symbols"
            )
            file_reason = (
                "Symbols from this test module are imported elsewhere."
            )

        elif retained_tests:
            file_status = (
                FILE_FUNCTION_ONLY
            )
            recommended_action = (
                "delete candidate functions only"
            )
            file_reason = (
                "The file contains retained tests."
            )

        elif not all_tests_are_candidates:
            file_status = (
                FILE_UNRESOLVED
            )
            recommended_action = (
                "retain file"
            )
            file_reason = (
                "Not every test function in the file is represented by a deletion candidate."
            )

        else:
            file_status = (
                FILE_SAFE
            )
            recommended_action = (
                "whole file deletion eligible"
            )
            file_reason = (
                "All test functions are deletion candidates and no external module/symbol import was found."
            )

        file_records.append(
            FileRecord(
                file_path=file_path,
                test_function_count=len(
                    test_functions
                ),
                deletion_candidate_test_count=len(
                    candidate_functions
                    & test_functions
                ),
                retained_test_count=len(
                    retained_tests
                ),
                retained_tests="\x1f".join(
                    retained_tests
                ),
                helper_function_count=len(
                    helpers
                ),
                helper_functions="\x1f".join(
                    helpers
                ),
                class_count=len(
                    classes
                ),
                classes="\x1f".join(
                    classes
                ),
                constant_count=len(
                    constants
                ),
                constants="\x1f".join(
                    constants
                ),
                import_count=import_count,
                external_symbol_import_count=len(
                    symbol_imports
                ),
                external_symbol_imports=(
                    "\x1f".join(
                        externally_imported_symbols
                    )
                ),
                whole_module_import_count=len(
                    module_importers
                ),
                whole_module_importers=(
                    "\x1f".join(
                        module_importers
                    )
                ),
                file_status=file_status,
                recommended_action=(
                    recommended_action
                ),
                reason=file_reason,
            )
        )

        file_record = (
            file_records[
                -1
            ]
        )

        for function_name in sorted(
            candidate_functions
        ):
            test_id = (
                file_path
                + "::"
                + function_name
            )

            if function_name not in (
                test_functions
            ):
                function_status = (
                    FUNCTION_MISSING
                )
                external_refs = []
                action = "retain"
                reason = (
                    "Candidate test function was not found as a top-level test."
                )
            else:
                external_refs = (
                    _external_function_references(
                        trees,
                        file_path,
                        function_name,
                    )
                )

                if external_refs:
                    function_status = (
                        FUNCTION_BLOCKED_EXTERNAL
                    )
                    action = "retain"
                    reason = (
                        "The candidate test function is referenced from another module."
                    )
                else:
                    function_status = (
                        FUNCTION_SAFE
                    )

                    if (
                        file_record.file_status
                        == FILE_SAFE
                    ):
                        action = (
                            "delete with whole file"
                        )
                    else:
                        action = (
                            "delete function only"
                        )

                    reason = (
                        "No external reference to the candidate test function was found."
                    )

            candidate_records.append(
                CandidateRecord(
                    test_id=test_id,
                    file_path=file_path,
                    function_name=(
                        function_name
                    ),
                    function_status=(
                        function_status
                    ),
                    external_function_reference_count=len(
                        external_refs
                    ),
                    external_function_references=(
                        "\x1f".join(
                            external_refs
                        )
                    ),
                    file_test_function_count=(
                        file_record.test_function_count
                    ),
                    deletion_candidate_test_count=(
                        file_record.deletion_candidate_test_count
                    ),
                    retained_test_count=(
                        file_record.retained_test_count
                    ),
                    retained_tests=(
                        file_record.retained_tests
                    ),
                    module_helper_count=(
                        file_record.helper_function_count
                    ),
                    module_constant_count=(
                        file_record.constant_count
                    ),
                    module_import_count=(
                        file_record.import_count
                    ),
                    externally_imported_symbol_count=(
                        file_record.external_symbol_import_count
                    ),
                    externally_imported_symbols=(
                        file_record.external_symbol_imports
                    ),
                    whole_module_import_count=(
                        file_record.whole_module_import_count
                    ),
                    whole_module_importers=(
                        file_record.whole_module_importers
                    ),
                    file_status=(
                        file_record.file_status
                    ),
                    recommended_action=(
                        action
                    ),
                    reason=reason,
                )
            )

    return (
        candidate_records,
        file_records,
    )


def write_summary(
    path: Path,
    repo_root: Path,
    candidates: list[
        CandidateRecord
    ],
    files: list[
        FileRecord
    ],
) -> None:
    function_counts = Counter(
        row.function_status
        for row in candidates
    )
    file_counts = Counter(
        row.file_status
        for row in files
    )

    safe_functions = sum(
        row.function_status
        == FUNCTION_SAFE
        for row in candidates
    )
    blocked_functions = (
        len(
            candidates
        )
        - safe_functions
    )
    whole_file_eligible = sum(
        row.file_status
        == FILE_SAFE
        for row in files
    )
    function_only_files = sum(
        row.file_status
        in (
            FILE_FUNCTION_ONLY,
            FILE_BLOCKED_EXTERNAL,
        )
        for row in files
    )
    unresolved_files = sum(
        row.file_status
        == FILE_UNRESOLVED
        for row in files
    )

    lines = [
        "# Phase 155-R3-3B — deletion-candidate file/dependency safety audit",
        "",
        "## Input",
        "",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Deletion candidate functions: {len(candidates)}",
        f"- Candidate files: {len(files)}",
        "",
        "## Function safety",
        "",
        f"- Safe function deletions: {safe_functions}",
        f"- Blocked/unresolved function deletions: {blocked_functions}",
        "",
        "| function status | count |",
        "| --- | ---: |",
    ]

    for status in (
        FUNCTION_SAFE,
        FUNCTION_BLOCKED_EXTERNAL,
        FUNCTION_MISSING,
        FUNCTION_PARSE_ERROR,
    ):
        lines.append(
            f"| `{status}` | {function_counts[status]} |"
        )

    lines.extend(
        [
            "",
            "## File safety",
            "",
            f"- Whole-file deletion eligible: {whole_file_eligible}",
            f"- Function-only files: {function_only_files}",
            f"- Unresolved files: {unresolved_files}",
            "",
            "| file status | count |",
            "| --- | ---: |",
        ]
    )

    for status in (
        FILE_SAFE,
        FILE_FUNCTION_ONLY,
        FILE_BLOCKED_EXTERNAL,
        FILE_UNRESOLVED,
    ):
        lines.append(
            f"| `{status}` | {file_counts[status]} |"
        )

    lines.extend(
        [
            "",
            "## Safety interpretation",
            "",
            "A candidate function is not approved when another Python module imports/references that test function directly.",
            "",
            "A whole file is approved only when every top-level test function is a deletion candidate and no other Python module imports the module or any symbol from it.",
            "",
            "Files containing retained tests or externally imported helpers/constants remain function-only deletion targets.",
            "",
            "R3-3B performs no deletion. R3-3C may modify only the rows marked safe by this audit.",
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
        "--deletion-candidates",
        type=Path,
        default=Path(
            "phase155_r3_3a_audit_output/"
            "phase155_r3_3a_deletion_candidates.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_3b_audit_output"
        ),
    )

    args = parser.parse_args()
    repo_root = (
        args.repo_root.resolve()
    )

    candidate_path = (
        args.deletion_candidates
        if args.deletion_candidates.is_absolute()
        else repo_root
        / args.deletion_candidates
    )

    if not candidate_path.exists():
        raise SystemExit(
            "R3-3A deletion candidates CSV not found: "
            + str(
                candidate_path
            )
        )

    deletion_rows = _read_csv(
        candidate_path
    )

    candidates, files = (
        build_safety_audit(
            repo_root,
            deletion_rows,
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
        / "phase155_r3_3b_candidate_safety.csv",
        candidates,
    )
    _write_csv(
        output_dir
        / "phase155_r3_3b_file_safety.csv",
        files,
    )

    safe_candidates = [
        row
        for row in candidates
        if row.function_status
        == FUNCTION_SAFE
    ]
    _write_csv(
        output_dir
        / "phase155_r3_3b_safe_function_deletions.csv",
        safe_candidates,
    )

    safe_files = [
        row
        for row in files
        if row.file_status
        == FILE_SAFE
    ]
    _write_csv(
        output_dir
        / "phase155_r3_3b_safe_whole_file_deletions.csv",
        safe_files,
    )

    write_summary(
        output_dir
        / "phase155_r3_3b_summary.md",
        repo_root,
        candidates,
        files,
    )

    function_counts = Counter(
        row.function_status
        for row in candidates
    )
    file_counts = Counter(
        row.file_status
        for row in files
    )

    blocking_functions = (
        len(
            candidates
        )
        - function_counts[
            FUNCTION_SAFE
        ]
    )
    unresolved_files = (
        file_counts[
            FILE_UNRESOLVED
        ]
    )

    metadata = {
        "phase": "155-R3-3B",
        "git_head": _git_head(
            repo_root
        ),
        "deletion_candidate_functions": len(
            candidates
        ),
        "candidate_files": len(
            files
        ),
        "safe_function_deletions": (
            function_counts[
                FUNCTION_SAFE
            ]
        ),
        "blocked_or_unresolved_functions": (
            blocking_functions
        ),
        "safe_whole_file_deletions": (
            file_counts[
                FILE_SAFE
            ]
        ),
        "function_only_files": (
            file_counts[
                FILE_FUNCTION_ONLY
            ]
            + file_counts[
                FILE_BLOCKED_EXTERNAL
            ]
        ),
        "unresolved_files": (
            unresolved_files
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3b_metadata.json"
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
        "Phase 155-R3-3B deletion-candidate safety audit completed."
    )
    print(
        "deletion candidate functions:",
        len(
            candidates
        ),
    )
    print(
        "candidate files:",
        len(
            files
        ),
    )
    print(
        "safe function deletions:",
        function_counts[
            FUNCTION_SAFE
        ],
    )
    print(
        "blocked external function references:",
        function_counts[
            FUNCTION_BLOCKED_EXTERNAL
        ],
    )
    print(
        "missing candidate functions:",
        function_counts[
            FUNCTION_MISSING
        ],
    )
    print(
        "parse-error candidate functions:",
        function_counts[
            FUNCTION_PARSE_ERROR
        ],
    )
    print(
        "safe whole-file deletions:",
        file_counts[
            FILE_SAFE
        ],
    )
    print(
        "function-only retained-test files:",
        file_counts[
            FILE_FUNCTION_ONLY
        ],
    )
    print(
        "external-import blocked files:",
        file_counts[
            FILE_BLOCKED_EXTERNAL
        ],
    )
    print(
        "unresolved files:",
        file_counts[
            FILE_UNRESOLVED
        ],
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
