
from __future__ import annotations

import argparse
import ast
import json
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _function_nodes(
    source: str,
    function_name: str,
) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    tree = ast.parse(source)
    return [
        node
        for node in tree.body
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function_name
        )
    ]


def _node_span(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> tuple[int, int]:
    decorator_lines = [
        decorator.lineno
        for decorator in node.decorator_list
    ]
    start = min(
        [node.lineno, *decorator_lines]
    ) - 1
    end = node.end_lineno or node.lineno
    return start, end


def _replace_definition_name(
    source_lines: list[str],
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    old_name: str,
    new_name: str,
) -> None:
    definition_line_index = node.lineno - 1
    line = source_lines[definition_line_index]

    if isinstance(node, ast.AsyncFunctionDef):
        old_prefix = "async def " + old_name + "("
        new_prefix = "async def " + new_name + "("
    else:
        old_prefix = "def " + old_name + "("
        new_prefix = "def " + new_name + "("

    if old_prefix not in line:
        raise RuntimeError(
            "cannot find function definition prefix for "
            + old_name
        )

    source_lines[definition_line_index] = line.replace(
        old_prefix,
        new_prefix,
        1,
    )


def _unique_hidden_name(
    existing_names: set[str],
    original_name: str,
    ordinal: int,
) -> str:
    base = (
        original_name
        + "_phase155_hidden_coverage_"
        + str(ordinal)
    )
    candidate = base
    suffix = 2

    while candidate in existing_names:
        candidate = base + "_" + str(suffix)
        suffix += 1

    existing_names.add(candidate)
    return candidate


def _plan_duplicate_group(
    repo_root: Path,
    duplicate_semantics: dict,
    hidden_decision: dict,
) -> dict:
    file_path = duplicate_semantics["file_path"]
    function_name = duplicate_semantics["function_name"]
    path = repo_root / file_path
    source = path.read_text(encoding="utf-8-sig")
    nodes = _function_nodes(
        source,
        function_name,
    )

    expected_count = duplicate_semantics["definition_count"]
    if len(nodes) != expected_count:
        raise RuntimeError(
            f"{file_path}::{function_name} expected "
            f"{expected_count} definitions, found {len(nodes)}"
        )

    if len(nodes) < 2:
        raise RuntimeError(
            f"{file_path}::{function_name} is no longer duplicated"
        )

    recommendation = hidden_decision["recommendation"]
    if recommendation not in (
        "shadowed_definition_cleanup_ready",
        "preserve_hidden_coverage_before_cleanup",
    ):
        raise RuntimeError(
            "unsupported hidden-coverage recommendation: "
            + recommendation
        )

    return {
        "file_path": file_path,
        "function_name": function_name,
        "definition_count": len(nodes),
        "recommendation": recommendation,
    }


def _apply_file_operations(
    source: str,
    duplicate_plans: list[dict],
    older_function_names: set[str],
) -> tuple[str, list[dict], list[str]]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    existing_names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }

    removals = []
    renamed = []
    removed_pair_functions = []

    for plan in duplicate_plans:
        function_name = plan["function_name"]
        nodes = [
            node
            for node in tree.body
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == function_name
            )
        ]

        earlier_nodes = nodes[:-1]

        if plan["recommendation"] == "shadowed_definition_cleanup_ready":
            for node in earlier_nodes:
                start, end = _node_span(node)
                removals.append((start, end))
            continue

        for ordinal, node in enumerate(earlier_nodes, start=1):
            new_name = _unique_hidden_name(
                existing_names,
                function_name,
                ordinal,
            )
            _replace_definition_name(
                lines,
                node,
                function_name,
                new_name,
            )
            renamed.append(
                {
                    "original_name": function_name,
                    "new_name": new_name,
                    "line": node.lineno,
                }
            )

    for function_name in sorted(older_function_names):
        matches = [
            node
            for node in tree.body
            if (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == function_name
            )
        ]

        if len(matches) != 1:
            raise RuntimeError(
                f"expected exactly one unresolved-pair older "
                f"function {function_name}, found {len(matches)}"
            )

        start, end = _node_span(matches[0])
        removals.append((start, end))
        removed_pair_functions.append(function_name)

    for start, end in sorted(
        set(removals),
        reverse=True,
    ):
        del lines[start:end]

    new_source = "".join(lines)
    ast.parse(new_source)

    return (
        new_source,
        renamed,
        removed_pair_functions,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r2-output",
        type=Path,
        default=Path("phase155_r3_3d_r2_audit_output"),
    )
    parser.add_argument(
        "--r3-output",
        type=Path,
        default=Path("phase155_r3_3d_r3_audit_output"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase155_r3_3d_r4_cleanup_output"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return path if path.is_absolute() else repo_root / path

    r2_dir = resolve(args.r2_output)
    r3_dir = resolve(args.r3_output)

    duplicate_path = (
        r2_dir
        / "phase155_r3_3d_r2_duplicate_semantics.json"
    )
    hidden_path = (
        r3_dir
        / "phase155_r3_3d_r3_hidden_coverage.json"
    )
    pair_path = (
        r3_dir
        / "phase155_r3_3d_r3_pair_decisions.json"
    )

    for path in (
        duplicate_path,
        hidden_path,
        pair_path,
    ):
        if not path.exists():
            raise SystemExit(
                "required audit input not found: "
                + str(path)
            )

    duplicate_semantics = _load_json(
        duplicate_path
    )
    hidden_decisions = _load_json(
        hidden_path
    )
    pair_decisions = _load_json(
        pair_path
    )

    hidden_by_test_id = {
        item["test_id"]: item
        for item in hidden_decisions
    }

    duplicate_plans = []
    for duplicate in duplicate_semantics:
        test_id = (
            duplicate["file_path"]
            + "::"
            + duplicate["function_name"]
        )
        decision = hidden_by_test_id.get(
            test_id
        )
        if decision is None:
            raise RuntimeError(
                "missing hidden-coverage decision for "
                + test_id
            )

        duplicate_plans.append(
            _plan_duplicate_group(
                repo_root,
                duplicate,
                decision,
            )
        )

    older_test_ids = []
    newer_test_ids = []

    for pair in pair_decisions:
        if (
            pair["repaired_decision"]
            != "delete_older_keep_newer_candidate"
        ):
            raise RuntimeError(
                "R3-3D-r4 requires every unresolved pair "
                "to be delete-older/keep-newer ready"
            )
        older_test_ids.append(
            pair["older_test_id"]
        )
        newer_test_ids.append(
            pair["newer_test_id"]
        )

    operations_by_file = defaultdict(
        lambda: {
            "duplicate_plans": [],
            "older_function_names": set(),
        }
    )

    for plan in duplicate_plans:
        operations_by_file[
            plan["file_path"]
        ]["duplicate_plans"].append(
            plan
        )

    for test_id in older_test_ids:
        file_path, function_name = test_id.split(
            "::",
            1,
        )
        file_path = file_path.replace(
            "\\",
            "/",
        )
        operations_by_file[
            file_path
        ]["older_function_names"].add(
            function_name
        )

    changed_files = sorted(
        operations_by_file
    )

    print("Planned changed files / functions:")
    for file_path in changed_files:
        print("  " + file_path)
        for plan in operations_by_file[
            file_path
        ]["duplicate_plans"]:
            print(
                "    duplicate group:",
                plan["function_name"],
                "->",
                plan["recommendation"],
            )
        for function_name in sorted(
            operations_by_file[
                file_path
            ]["older_function_names"]
        ):
            print(
                "    remove unresolved-pair older:",
                function_name,
            )

    staged = {}
    manifest_entries = []
    renamed_test_ids = []

    for file_path in changed_files:
        path = repo_root / file_path
        source = path.read_text(
            encoding="utf-8-sig"
        )
        new_source, renamed, removed_pairs = (
            _apply_file_operations(
                source,
                operations_by_file[
                    file_path
                ]["duplicate_plans"],
                operations_by_file[
                    file_path
                ]["older_function_names"],
            )
        )
        staged[
            file_path
        ] = new_source

        for item in renamed:
            renamed_test_ids.append(
                file_path
                + "::"
                + item["new_name"]
            )

        manifest_entries.append(
            {
                "file_path": file_path,
                "renamed_hidden_tests": renamed,
                "removed_pair_functions": removed_pairs,
                "duplicate_groups": operations_by_file[
                    file_path
                ]["duplicate_plans"],
            }
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )
    backup_root = (
        repo_root.parent
        / (
            repo_root.name
            + "_phase155_r3_3d_r4_backup_"
            + timestamp
        )
    )

    for file_path in changed_files:
        source_path = repo_root / file_path
        backup_path = backup_root / file_path
        backup_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        shutil.copy2(
            source_path,
            backup_path,
        )

    for file_path, new_source in staged.items():
        (repo_root / file_path).write_text(
            new_source,
            encoding="utf-8",
        )

    output_dir = resolve(
        args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest = {
        "changed_files": changed_files,
        "changed_file_count": len(changed_files),
        "duplicate_group_count": len(
            duplicate_plans
        ),
        "hidden_tests_renamed_and_activated": len(
            renamed_test_ids
        ),
        "cleanup_ready_shadowed_definitions_removed": sum(
            plan["definition_count"] - 1
            for plan in duplicate_plans
            if plan["recommendation"]
            == "shadowed_definition_cleanup_ready"
        ),
        "unresolved_pair_older_tests_removed": len(
            set(older_test_ids)
        ),
        "older_test_ids": sorted(
            set(older_test_ids)
        ),
        "newer_test_ids": sorted(
            set(newer_test_ids)
        ),
        "renamed_test_ids": sorted(
            renamed_test_ids
        ),
        "backup_root": str(
            backup_root
        ),
        "entries": manifest_entries,
        "production_changes": False,
        "import_changes": False,
    }

    (
        output_dir
        / "phase155_r3_3d_r4_cleanup_manifest.json"
    ).write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Phase 155-R3-3D-r4 cleanup applied."
    )
    print(
        "changed test files:",
        len(changed_files),
    )
    print(
        "hidden tests renamed and activated:",
        len(renamed_test_ids),
    )
    print(
        "unresolved-pair older tests removed:",
        len(
            set(older_test_ids)
        ),
    )
    print(
        "production changes: none"
    )
    print(
        "import changes: none"
    )
    print(
        "backup:",
        backup_root,
    )
    print(
        "manifest:",
        output_dir
        / "phase155_r3_3d_r4_cleanup_manifest.json",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
