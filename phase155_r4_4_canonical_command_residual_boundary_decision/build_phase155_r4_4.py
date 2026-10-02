from __future__ import annotations

import argparse
import ast
import csv
import json
from collections import Counter
from pathlib import Path


CATEGORY_CANONICAL = "canonical_candidate"
CATEGORY_PUBLIC = "canonical_public_surface_candidate"
CATEGORY_INTERNAL = "canonical_internal_contract_candidate"
CATEGORY_LINEAGE_SUPPORT = "lineage_support_candidate"
CATEGORY_HISTORICAL = "historical_compatibility"
CATEGORY_AUDIT = "audit_only_candidate"
CATEGORY_HEAVY = "performance_heavy_integration_candidate"
CATEGORY_REVIEW = "review_required"
CATEGORY_GLOBAL_PROMOTION = "canonical_module_global_contract_candidate"
CATEGORY_RESIDUAL = "residual_validation_lane"


CANONICAL_CATEGORIES = {
    CATEGORY_CANONICAL,
    CATEGORY_PUBLIC,
    CATEGORY_INTERNAL,
    CATEGORY_GLOBAL_PROMOTION,
}


EXCLUDED_ROOT_PREFIXES = (
    "apply_",
    "audit_",
    "show_",
    "test_",
    "probe_",
)


RUNNER_SOURCE = 'from __future__ import annotations\n\nimport argparse\nfrom collections import defaultdict\nfrom pathlib import Path\n\nimport pytest\n\n\ndef _read_nodeids(path: Path) -> list[str]:\n    return [\n        line.strip()\n        for line in path.read_text(\n            encoding="utf-8-sig"\n        ).splitlines()\n        if line.strip()\n    ]\n\n\ndef _collect_only_batched(\n    nodeids: list[str],\n    batch_file_count: int,\n) -> int:\n    by_file: dict[str, list[str]] = defaultdict(list)\n\n    for nodeid in nodeids:\n        file_path = nodeid.split(\n            "::",\n            1,\n        )[0]\n        by_file[file_path].append(nodeid)\n\n    files = sorted(by_file)\n\n    batches = [\n        files[index:index + batch_file_count]\n        for index in range(\n            0,\n            len(files),\n            batch_file_count,\n        )\n    ]\n\n    for batch_number, batch_files in enumerate(\n        batches,\n        start=1,\n    ):\n        batch_nodeids = [\n            nodeid\n            for file_path in batch_files\n            for nodeid in by_file[file_path]\n        ]\n\n        print(\n            f"collect batch {batch_number}/{len(batches)} "\n            f"({len(batch_files)} files, "\n            f"{len(batch_nodeids)} source test IDs)",\n            flush=True,\n        )\n\n        exit_code = pytest.main(\n            [\n                "--collect-only",\n                "-q",\n                "-p",\n                "no:cacheprovider",\n                *batch_nodeids,\n            ]\n        )\n\n        if exit_code != 0:\n            return int(exit_code)\n\n    return 0\n\n\ndef main() -> int:\n    parser = argparse.ArgumentParser()\n    parser.add_argument(\n        "--manifest",\n        type=Path,\n        default=(\n            Path(__file__)\n            .with_name(\n                "phase155_r4_4_canonical_nodeids.txt"\n            )\n        ),\n    )\n    parser.add_argument(\n        "--collect-only",\n        action="store_true",\n    )\n    parser.add_argument(\n        "--batch-files",\n        type=int,\n        default=40,\n    )\n    args = parser.parse_args()\n\n    nodeids = _read_nodeids(args.manifest)\n\n    if not nodeids:\n        raise SystemExit("canonical manifest is empty")\n\n    print(\n        "canonical source test IDs:",\n        len(nodeids),\n        flush=True,\n    )\n\n    if args.collect_only:\n        return _collect_only_batched(\n            nodeids,\n            args.batch_files,\n        )\n\n    print(\n        "WARNING: canonical regression executes a large test set.",\n        flush=True,\n    )\n\n    return int(\n        pytest.main(\n            [\n                "-q",\n                "-p",\n                "no:cacheprovider",\n                *nodeids,\n            ]\n        )\n    )\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n'
RUNNER_PS1_SOURCE = '$ErrorActionPreference = "Stop"\n\n$OutputDir = Split-Path -Parent $MyInvocation.MyCommand.Path\n$RepoRoot = Split-Path -Parent $OutputDir\n\nSet-Location $RepoRoot\n\nWrite-Host "=============================================================="\nWrite-Host "Phase 155 canonical regression"\nWrite-Host "=============================================================="\nWrite-Host "This executes the canonical regression set."\nWrite-Host "This can be HEAVY."\nWrite-Host ""\n\npython `\n  "$OutputDir\\run_phase155_canonical_regression.py"\n\nif ($LASTEXITCODE -ne 0) {\n  throw "Phase 155 canonical regression failed."\n}\n'


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _production_modules(repo_root: Path) -> set[str]:
    modules = set()

    for path in sorted(repo_root.glob("*.py")):
        stem = path.stem

        if stem.startswith(EXCLUDED_ROOT_PREFIXES):
            continue

        if stem in {
            "conftest",
            "setup",
        }:
            continue

        modules.add(stem)

    return modules


def _module_analysis(
    path: Path,
    production_modules: set[str],
) -> dict[str, object]:
    source = path.read_text(
        encoding="utf-8-sig"
    )
    tree = ast.parse(source)

    imported_production_names: dict[str, str] = {}
    functions = {}
    used_names: dict[str, set[str]] = {}
    local_calls: dict[str, set[str]] = {}
    global_dependencies: dict[str, set[str]] = {}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in production_modules:
                    local_name = (
                        alias.asname
                        if alias.asname
                        else root
                    )
                    imported_production_names[
                        local_name
                    ] = root

        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                continue
            root = node.module.split(".", 1)[0]
            if root in production_modules:
                for alias in node.names:
                    local_name = (
                        alias.asname
                        if alias.asname
                        else alias.name
                    )
                    imported_production_names[
                        local_name
                    ] = root

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        ):
            functions[node.name] = node

    for name, node in functions.items():
        used_names[name] = {
            child.id
            for child in ast.walk(node)
            if isinstance(child, ast.Name)
        }

        local_calls[name] = {
            child.func.id
            for child in ast.walk(node)
            if (
                isinstance(child, ast.Call)
                and isinstance(child.func, ast.Name)
                and child.func.id in functions
            )
        }

    def assigned_names(node: ast.AST) -> set[str]:
        result = set()

        if isinstance(
            node,
            (
                ast.Assign,
                ast.AnnAssign,
                ast.AugAssign,
            ),
        ):
            if isinstance(node, ast.Assign):
                targets = list(node.targets)
            else:
                targets = [node.target]

            for target in targets:
                for child in ast.walk(target):
                    if isinstance(child, ast.Name):
                        result.add(child.id)

        return result

    for node in tree.body:
        names = assigned_names(node)

        if not names:
            continue

        referenced = {
            child.id
            for child in ast.walk(node)
            if isinstance(child, ast.Name)
        } - names

        for name in names:
            global_dependencies[name] = set(referenced)

    return {
        "imported_production_names": imported_production_names,
        "functions": functions,
        "used_names": used_names,
        "local_calls": local_calls,
        "global_dependencies": global_dependencies,
    }


def _reachable_functions(
    start: str,
    local_calls: dict[str, set[str]],
) -> set[str]:
    seen = set()
    stack = [start]

    while stack:
        name = stack.pop()

        if name in seen:
            continue

        seen.add(name)

        stack.extend(
            sorted(
                local_calls.get(
                    name,
                    set(),
                )
                - seen
            )
        )

    return seen


def _expand_global_names(
    initial_names: set[str],
    global_dependencies: dict[str, set[str]],
) -> set[str]:
    expanded = set(initial_names)
    stack = list(initial_names)

    while stack:
        name = stack.pop()

        for dependency in global_dependencies.get(
            name,
            set(),
        ):
            if dependency in expanded:
                continue

            expanded.add(dependency)
            stack.append(dependency)

    return expanded


def _global_production_modules_used_by_test(
    analysis: dict[str, object],
    test_name: str,
) -> set[str]:
    reachable = _reachable_functions(
        test_name,
        analysis["local_calls"],
    )

    names = set()

    for function_name in reachable:
        names.update(
            analysis["used_names"].get(
                function_name,
                set(),
            )
        )

    names = _expand_global_names(
        names,
        analysis["global_dependencies"],
    )

    return {
        module
        for local_name, module in (
            analysis[
                "imported_production_names"
            ].items()
        )
        if local_name in names
    }


def _production_import_graph(
    repo_root: Path,
    production_modules: set[str],
) -> dict[str, set[str]]:
    graph = {
        module: set()
        for module in production_modules
    }

    for module in sorted(production_modules):
        path = repo_root / (module + ".py")

        try:
            tree = ast.parse(
                path.read_text(
                    encoding="utf-8-sig"
                )
            )
        except (
            OSError,
            SyntaxError,
            UnicodeDecodeError,
        ):
            continue

        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    candidate = alias.name.split(".", 1)[0]
                    if candidate in production_modules:
                        graph[module].add(candidate)

            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue

                root = node.module.split(".", 1)[0]

                if root in production_modules:
                    graph[module].add(root)

    return graph


def _reachable_modules(
    roots: set[str],
    graph: dict[str, set[str]],
) -> set[str]:
    seen = set()
    stack = sorted(roots)

    while stack:
        module = stack.pop()

        if module in seen:
            continue

        seen.add(module)

        stack.extend(
            sorted(
                graph.get(
                    module,
                    set(),
                )
                - seen
            )
        )

    return seen


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--r4-3-classification",
        type=Path,
        default=Path(
            "phase155_r4_3_audit_output/"
            "phase155_r4_3_consolidated_classification.csv"
        ),
    )
    parser.add_argument(
        "--r4-3-ownership",
        type=Path,
        default=Path(
            "phase155_r4_3_audit_output/"
            "phase155_r4_3_production_ownership_matrix.json"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r4_4_audit_output"
        ),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    classification_path = (
        args.r4_3_classification
        if args.r4_3_classification.is_absolute()
        else repo_root / args.r4_3_classification
    )

    ownership_path = (
        args.r4_3_ownership
        if args.r4_3_ownership.is_absolute()
        else repo_root / args.r4_3_ownership
    )

    for path in (
        classification_path,
        ownership_path,
    ):
        if not path.exists():
            raise SystemExit(
                "required R4-3 input not found: "
                + str(path)
            )

    rows = _read_csv(classification_path)
    ownership_matrix = json.loads(
        ownership_path.read_text(
            encoding="utf-8"
        )
    )

    production_modules = _production_modules(
        repo_root
    )

    original_direct_owned_modules = {
        item["production_module"]
        for item in ownership_matrix
        if item["owning_test_count"] > 0
    }

    analyses = {}
    result_rows = []
    global_promotions = 0
    residual_count = 0

    for row in rows:
        category = row["r4_3_category"]
        file_path = row["file_path"]
        function_name = row["function_name"]

        global_modules = set()

        if category in (
            CATEGORY_REVIEW,
            CATEGORY_LINEAGE_SUPPORT,
        ):
            if file_path not in analyses:
                analyses[file_path] = _module_analysis(
                    repo_root / file_path,
                    production_modules,
                )

            global_modules = (
                _global_production_modules_used_by_test(
                    analyses[file_path],
                    function_name,
                )
            )

        if (
            category
            in (
                CATEGORY_REVIEW,
                CATEGORY_LINEAGE_SUPPORT,
            )
            and global_modules
        ):
            final_category = CATEGORY_GLOBAL_PROMOTION
            decision_reason = (
                "module-level dependency resolves to current production: "
                + ", ".join(
                    sorted(global_modules)
                )
            )
            global_promotions += 1

        elif category in (
            CATEGORY_REVIEW,
            CATEGORY_LINEAGE_SUPPORT,
        ):
            final_category = CATEGORY_RESIDUAL
            decision_reason = (
                "no direct/helper/module-global current production ownership; "
                "retain outside routine canonical pending R5/R6"
            )
            residual_count += 1

        else:
            final_category = category
            decision_reason = (
                "R4-3 classification retained"
            )

        result_rows.append(
            {
                **row,
                "module_global_production_modules": ";".join(
                    sorted(global_modules)
                ),
                "r4_4_category": final_category,
                "r4_4_reason": decision_reason,
            }
        )

    canonical_ids = [
        row["test_id"]
        for row in result_rows
        if row["r4_4_category"] in CANONICAL_CATEGORIES
    ]

    canonical_files = sorted(
        {
            row["file_path"]
            for row in result_rows
            if row["r4_4_category"]
            in CANONICAL_CATEGORIES
        }
    )

    category_counts = Counter(
        row["r4_4_category"]
        for row in result_rows
    )

    direct_and_global_owned_modules = set(
        original_direct_owned_modules
    )

    for row in result_rows:
        for module in filter(
            None,
            row[
                "module_global_production_modules"
            ].split(";"),
        ):
            direct_and_global_owned_modules.add(module)

    graph = _production_import_graph(
        repo_root,
        production_modules,
    )

    transitively_covered_modules = _reachable_modules(
        direct_and_global_owned_modules,
        graph,
    )

    unowned_after_transitive = sorted(
        production_modules
        - transitively_covered_modules
    )

    indirect_only_modules = sorted(
        transitively_covered_modules
        - direct_and_global_owned_modules
    )

    module_boundary = {
        "root_production_modules": len(production_modules),
        "direct_or_global_owned_modules": len(
            direct_and_global_owned_modules
        ),
        "indirect_only_modules": len(
            indirect_only_modules
        ),
        "unowned_after_transitive": len(
            unowned_after_transitive
        ),
        "indirect_only_module_names": indirect_only_modules,
        "unowned_after_transitive_names": unowned_after_transitive,
    }

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root / args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    csv_path = (
        output_dir
        / "phase155_r4_4_final_classification.csv"
    )

    with csv_path.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        fieldnames = list(
            result_rows[0].keys()
        )
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(result_rows)

    manifest_path = (
        output_dir
        / "phase155_r4_4_canonical_nodeids.txt"
    )
    manifest_path.write_text(
        "\n".join(canonical_ids) + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_4_canonical_files.txt"
    ).write_text(
        "\n".join(canonical_files) + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "phase155_r4_4_module_boundary.json"
    ).write_text(
        json.dumps(
            module_boundary,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (
        output_dir
        / "run_phase155_canonical_regression.py"
    ).write_text(
        RUNNER_SOURCE,
        encoding="utf-8",
    )

    (
        output_dir
        / "run_phase155_canonical_regression.ps1"
    ).write_text(
        RUNNER_PS1_SOURCE,
        encoding="utf-8-sig",
    )

    metadata = {
        "source_test_functions": len(rows),
        "module_global_promotions": global_promotions,
        "residual_validation_lane": residual_count,
        "canonical_source_test_ids": len(canonical_ids),
        "canonical_files": len(canonical_files),
        "category_counts": dict(category_counts),
        "module_boundary": module_boundary,
        "canonical_command": (
            "powershell -ExecutionPolicy Bypass "
            "-File .\\phase155_r4_4_audit_output\\"
            "run_phase155_canonical_regression.ps1"
        ),
        "canonical_collect_only_command": (
            "python .\\phase155_r4_4_audit_output\\"
            "run_phase155_canonical_regression.py --collect-only"
        ),
        "production_changes": False,
        "existing_test_changes": False,
        "repository_wide_pytest_executed": False,
        "canonical_regression_executed": False,
    }

    (
        output_dir
        / "phase155_r4_4_metadata.json"
    ).write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Phase 155-R4-4 — canonical command / residual boundary decision",
        "",
        "## Residual decision",
        "",
        f"- module-global promotions: {global_promotions}",
        f"- residual validation lane: {residual_count}",
        "",
        "Residual tests are retained. They are not marked removable.",
        "R5/R6 will decide historical/heavy/runtime treatment.",
        "",
        "## Canonical set",
        "",
        f"- canonical source test IDs: {len(canonical_ids)}",
        f"- canonical files: {len(canonical_files)}",
        "",
        "Canonical execution command:",
        "",
        "```powershell",
        "powershell -ExecutionPolicy Bypass -File .\\phase155_r4_4_audit_output\\run_phase155_canonical_regression.ps1",
        "```",
        "",
        "Canonical collect-only command:",
        "",
        "```powershell",
        "python .\\phase155_r4_4_audit_output\\run_phase155_canonical_regression.py --collect-only",
        "```",
        "",
        "## Production-module boundary",
        "",
        f"- root production modules: {module_boundary['root_production_modules']}",
        f"- direct/global owned modules: {module_boundary['direct_or_global_owned_modules']}",
        f"- indirect-only modules: {module_boundary['indirect_only_modules']}",
        f"- unowned after transitive imports: {module_boundary['unowned_after_transitive']}",
        "",
        "## Boundary",
        "",
        "No production code or existing test was changed.",
        "The canonical regression itself was NOT executed.",
        "Repository-wide pytest was NOT run.",
    ]

    (
        output_dir
        / "phase155_r4_4_summary.md"
    ).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(
        "Phase 155-R4-4 canonical boundary artifacts built."
    )
    print(
        "module-global promotions:",
        global_promotions,
    )
    print(
        "residual validation lane:",
        residual_count,
    )
    print(
        "canonical source test IDs:",
        len(canonical_ids),
    )
    print(
        "canonical files:",
        len(canonical_files),
    )
    print(
        "root production modules:",
        module_boundary[
            "root_production_modules"
        ],
    )
    print(
        "direct/global owned modules:",
        module_boundary[
            "direct_or_global_owned_modules"
        ],
    )
    print(
        "indirect-only modules:",
        module_boundary[
            "indirect_only_modules"
        ],
    )
    print(
        "unowned after transitive imports:",
        module_boundary[
            "unowned_after_transitive"
        ],
    )
    print("production changes: none")
    print("existing-test changes: none")
    print("canonical regression: NOT run")
    print("repository-wide pytest: NOT run")
    print("output:", output_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
