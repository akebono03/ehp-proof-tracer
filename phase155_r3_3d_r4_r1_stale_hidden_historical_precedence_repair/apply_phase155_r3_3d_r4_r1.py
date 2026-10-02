
from __future__ import annotations

import argparse
import ast
import csv
import json
from datetime import datetime
from pathlib import Path
import shutil


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _split_test_id(test_id: str) -> tuple[str, str]:
    file_path, function_name = test_id.split("::", 1)
    return file_path.replace("\\", "/"), function_name


def _function_nodes(source: str, function_name: str):
    tree = ast.parse(source)
    return [
        node
        for node in tree.body
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function_name
        )
    ]


def _node_span(node) -> tuple[int, int]:
    decorator_lines = [d.lineno for d in node.decorator_list]
    start = min([node.lineno, *decorator_lines]) - 1
    end = node.end_lineno or node.lineno
    return start, end


def _extract_function_source(
    path: Path,
    function_name: str,
) -> str:
    source = path.read_text(encoding="utf-8-sig")
    lines = source.splitlines(keepends=True)
    nodes = _function_nodes(source, function_name)

    if len(nodes) != 1:
        raise RuntimeError(
            f"backup expected exactly one {function_name}, "
            f"found {len(nodes)} in {path}"
        )

    start, end = _node_span(nodes[0])
    return "".join(lines[start:end]).rstrip() + "\n"


def _remove_function(
    source: str,
    function_name: str,
) -> str:
    lines = source.splitlines(keepends=True)
    nodes = _function_nodes(source, function_name)

    if len(nodes) != 1:
        raise RuntimeError(
            f"expected exactly one {function_name}, found {len(nodes)}"
        )

    start, end = _node_span(nodes[0])
    del lines[start:end]
    result = "".join(lines)
    ast.parse(result)
    return result


def _append_function_if_missing(
    source: str,
    function_name: str,
    function_source: str,
) -> str:
    nodes = _function_nodes(source, function_name)
    if len(nodes) == 1:
        return source
    if len(nodes) > 1:
        raise RuntimeError(
            f"cannot restore {function_name}: already duplicated"
        )

    result = source.rstrip() + "\n\n\n" + function_source.rstrip() + "\n"
    ast.parse(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--r4-cleanup-output",
        type=Path,
        default=Path("phase155_r3_3d_r4_cleanup_output"),
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
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_3d_r4_r1_repair_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return path if path.is_absolute() else repo_root / path

    cleanup_dir = resolve(args.r4_cleanup_output)
    manifest_path = (
        cleanup_dir
        / "phase155_r3_3d_r4_cleanup_manifest.json"
    )
    verified_path = resolve(args.verified_pairs)

    if not manifest_path.exists():
        raise SystemExit("missing r4 manifest: " + str(manifest_path))
    if not verified_path.exists():
        raise SystemExit("missing verified pairs: " + str(verified_path))

    manifest = _load_json(manifest_path)
    verified = _read_csv(verified_path)

    historical_ids = {
        test_id
        for row in verified
        if row.get("decision") == "historical_keep"
        for test_id in (
            row["older_test_id"],
            row["newer_test_id"],
        )
    }

    removed_older_ids = set(manifest["older_test_ids"])
    historical_removed_ids = sorted(
        removed_older_ids & historical_ids
    )

    if len(historical_removed_ids) != 2:
        raise RuntimeError(
            "expected exactly 2 removed older IDs to require "
            "historical_keep restoration, found "
            + str(len(historical_removed_ids))
        )

    stale_hidden_ids = sorted(manifest["renamed_test_ids"])
    if len(stale_hidden_ids) != 6:
        raise RuntimeError(
            "expected exactly 6 activated hidden tests, found "
            + str(len(stale_hidden_ids))
        )

    backup_root = Path(manifest["backup_root"])
    if not backup_root.exists():
        raise RuntimeError(
            "R3-3D-r4 backup root not found: "
            + str(backup_root)
        )

    affected_files = sorted(
        {
            _split_test_id(test_id)[0]
            for test_id in (
                stale_hidden_ids
                + historical_removed_ids
            )
        }
    )

    staged = {
        file_path: (
            repo_root
            / file_path
        ).read_text(encoding="utf-8-sig")
        for file_path in affected_files
    }

    removed_hidden_functions = []
    for test_id in stale_hidden_ids:
        file_path, function_name = _split_test_id(test_id)
        staged[file_path] = _remove_function(
            staged[file_path],
            function_name,
        )
        removed_hidden_functions.append(test_id)

    restored_historical_functions = []
    for test_id in historical_removed_ids:
        file_path, function_name = _split_test_id(test_id)
        backup_path = backup_root / file_path
        function_source = _extract_function_source(
            backup_path,
            function_name,
        )
        staged[file_path] = _append_function_if_missing(
            staged[file_path],
            function_name,
            function_source,
        )
        restored_historical_functions.append(test_id)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    repair_backup = (
        repo_root.parent
        / (
            repo_root.name
            + "_phase155_r3_3d_r4_r1_backup_"
            + timestamp
        )
    )

    for file_path in affected_files:
        source_path = repo_root / file_path
        backup_path = repair_backup / file_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, backup_path)

    for file_path, source in staged.items():
        (repo_root / file_path).write_text(
            source,
            encoding="utf-8",
        )

    output_dir = resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "changed_files": affected_files,
        "removed_stale_hidden_tests": removed_hidden_functions,
        "restored_historical_keep_tests": restored_historical_functions,
        "historical_precedence_rule": (
            "historical_keep overrides removable_duplicate "
            "when the same test ID participates in both classifications"
        ),
        "r4_backup_root": str(backup_root),
        "r4_r1_backup_root": str(repair_backup),
        "production_changes": False,
        "import_changes": False,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_3d_r4_r1_repair_manifest.json"
    ).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Phase 155-R3-3D-r4-r1 repair applied.")
    print("changed test files:", len(affected_files))
    print("stale hidden tests removed:", len(removed_hidden_functions))
    print(
        "historical_keep tests restored:",
        len(restored_historical_functions),
    )
    print("production changes: none")
    print("import changes: none")
    print("backup:", repair_backup)
    print(
        "manifest:",
        output_dir
        / "phase155_r3_3d_r4_r1_repair_manifest.json",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
