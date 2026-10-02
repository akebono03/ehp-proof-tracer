
from __future__ import annotations

import argparse
import ast
import csv
import importlib
import inspect
import json
import sys
from collections import defaultdict
from pathlib import Path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _split_test_id(test_id: str) -> tuple[str, str]:
    file_path, function_name = test_id.split("::", 1)
    return file_path.replace("\\", "/"), function_name


def _module_name_from_test_path(file_path: str) -> str:
    path = Path(file_path)
    return ".".join(path.with_suffix("").parts)


def _function_nodes(path: Path, function_name: str):
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    lines = source.splitlines()

    result = []
    for index, node in enumerate(tree.body):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == function_name
        ):
            start = min(
                [node.lineno, *[d.lineno for d in node.decorator_list]]
            )
            end = node.end_lineno or node.lineno
            function_source = "\n".join(lines[start - 1:end])
            asserts = [
                ast.dump(child.test, include_attributes=False)
                for child in ast.walk(node)
                if isinstance(child, ast.Assert)
            ]
            calls = sorted(
                {
                    ast.dump(child.func, include_attributes=False)
                    for child in ast.walk(node)
                    if isinstance(child, ast.Call)
                }
            )
            result.append(
                {
                    "ordinal": len(result) + 1,
                    "start_line": start,
                    "end_line": end,
                    "source": function_source,
                    "assertions": asserts,
                    "call_targets": calls,
                }
            )
    return result


def _runtime_definition_line(
    repo_root: Path,
    file_path: str,
    function_name: str,
) -> int:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    module_name = _module_name_from_test_path(file_path)
    if module_name in sys.modules:
        del sys.modules[module_name]

    module = importlib.import_module(module_name)
    value = getattr(module, function_name)
    _, line = inspect.getsourcelines(value)
    return line


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def _row_index(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    result = defaultdict(list)
    for row in rows:
        result[row.get(key, "")].append(row)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--r3d-r1-output",
        type=Path,
        default=Path("phase155_r3_3d_r1_audit_output"),
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
        "--output-dir",
        type=Path,
        default=Path("phase155_r3_3d_r2_audit_output"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return path if path.is_absolute() else repo_root / path

    r1_dir = resolve(args.r3d_r1_output)
    duplicate_path = r1_dir / "phase155_r3_3d_r1_duplicate_definitions.json"
    unresolved_path = r1_dir / "phase155_r3_3d_r1_unresolved_pairs.json"
    graph_path = resolve(args.graph_nodes)
    safety_path = resolve(args.candidate_safety)

    for path in (duplicate_path, unresolved_path, graph_path, safety_path):
        if not path.exists():
            raise SystemExit("required audit input not found: " + str(path))

    duplicate_groups = json.loads(duplicate_path.read_text(encoding="utf-8"))
    unresolved_pairs = json.loads(unresolved_path.read_text(encoding="utf-8"))
    graph_rows = _read_csv(graph_path)
    safety_rows = _read_csv(safety_path)

    graph_by_id = _row_index(graph_rows, "test_id")
    safety_by_id = _row_index(safety_rows, "test_id")

    duplicate_results = []

    for item in duplicate_groups:
        file_path = item["file_path"]
        function_name = item["function_name"]
        path = repo_root / file_path
        definitions = _function_nodes(path, function_name)
        runtime_line = _runtime_definition_line(
            repo_root,
            file_path,
            function_name,
        )

        collected_ordinal = None
        for definition in definitions:
            if definition["start_line"] == runtime_line:
                collected_ordinal = definition["ordinal"]
                break

        if collected_ordinal is None:
            raise RuntimeError(
                "runtime definition line did not match AST definition for "
                + file_path
                + "::"
                + function_name
            )

        collected = definitions[collected_ordinal - 1]
        collected_assertions = set(collected["assertions"])

        rendered_definitions = []
        for definition in definitions:
            assertions = set(definition["assertions"])
            rendered_definitions.append(
                {
                    **definition,
                    "is_runtime_definition": (
                        definition["ordinal"] == collected_ordinal
                    ),
                    "assertion_count": len(definition["assertions"]),
                    "assertions_only_here_vs_runtime": sorted(
                        assertions - collected_assertions
                    ),
                    "runtime_assertions_missing_here": sorted(
                        collected_assertions - assertions
                    ),
                }
            )

        earlier_unique = sorted(
            {
                assertion
                for definition in definitions[: collected_ordinal - 1]
                for assertion in definition["assertions"]
                if assertion not in collected_assertions
            }
        )

        duplicate_results.append(
            {
                "file_path": file_path,
                "function_name": function_name,
                "definition_count": len(definitions),
                "runtime_definition_line": runtime_line,
                "runtime_definition_ordinal": collected_ordinal,
                "earlier_only_assertion_count": len(earlier_unique),
                "earlier_only_assertions": earlier_unique,
                "shadowed_definition_has_unique_assertions": bool(earlier_unique),
                "definitions": rendered_definitions,
            }
        )

    unresolved_results = []

    for pair in unresolved_pairs:
        endpoints = []
        for label in ("older_test_id", "newer_test_id"):
            test_id = pair[label]
            graph_matches = graph_by_id.get(test_id, [])
            safety_matches = safety_by_id.get(test_id, [])

            endpoints.append(
                {
                    "role": label.replace("_test_id", ""),
                    "test_id": test_id,
                    "graph_rows": graph_matches,
                    "graph_deletion_candidate_values": sorted(
                        {
                            row.get("deletion_candidate", "")
                            for row in graph_matches
                        }
                    ),
                    "graph_marks_deletion_candidate": any(
                        _truthy(row.get("deletion_candidate", ""))
                        for row in graph_matches
                    ),
                    "candidate_safety_rows": safety_matches,
                    "has_safe_function_deletion_row": any(
                        row.get("function_status")
                        == "safe_function_deletion"
                        for row in safety_matches
                    ),
                }
            )

        deletion_marked = [
            endpoint
            for endpoint in endpoints
            if endpoint["graph_marks_deletion_candidate"]
        ]
        safety_marked = [
            endpoint
            for endpoint in endpoints
            if endpoint["has_safe_function_deletion_row"]
        ]

        if not deletion_marked:
            classification = "graph_has_no_deletion_candidate_endpoint"
        elif deletion_marked and not safety_marked:
            classification = "graph_candidate_missing_from_safety_input"
        elif any(
            endpoint["graph_marks_deletion_candidate"]
            and not endpoint["has_safe_function_deletion_row"]
            for endpoint in endpoints
        ):
            classification = "graph_safety_mapping_mismatch"
        else:
            classification = "candidate_marked_safe_but_present_after_removal"

        unresolved_results.append(
            {
                **pair,
                "classification": classification,
                "endpoints": endpoints,
            }
        )

    shadowed_unique_count = sum(
        1
        for item in duplicate_results
        if item["shadowed_definition_has_unique_assertions"]
    )
    shadowed_no_unique_count = (
        len(duplicate_results) - shadowed_unique_count
    )

    unresolved_class_counts = defaultdict(int)
    for item in unresolved_results:
        unresolved_class_counts[item["classification"]] += 1

    output_dir = resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "phase155_r3_3d_r2_duplicate_semantics.json").write_text(
        json.dumps(duplicate_results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "phase155_r3_3d_r2_unresolved_pair_semantics.json").write_text(
        json.dumps(unresolved_results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "duplicate_name_groups": len(duplicate_results),
        "runtime_last_definition_confirmed": all(
            item["runtime_definition_ordinal"] == item["definition_count"]
            for item in duplicate_results
        ),
        "shadowed_groups_with_unique_assertions": shadowed_unique_count,
        "shadowed_groups_without_unique_assertions": shadowed_no_unique_count,
        "unresolved_pairs": len(unresolved_results),
        "unresolved_pair_classifications": dict(unresolved_class_counts),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (output_dir / "phase155_r3_3d_r2_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Phase 155-R3-3D-r2 — divergent duplicate / unresolved pair semantic audit",
        "",
        "## Divergent duplicate definitions",
        "",
        f"- groups: {len(duplicate_results)}",
        f"- runtime uses final definition in all groups: {summary['runtime_last_definition_confirmed']}",
        f"- shadowed groups with unique assertions: {shadowed_unique_count}",
        f"- shadowed groups without unique assertions: {shadowed_no_unique_count}",
        "",
    ]

    for item in duplicate_results:
        lines.extend(
            [
                f"### `{item['file_path']}::{item['function_name']}`",
                "",
                f"- definitions: {item['definition_count']}",
                f"- runtime definition ordinal: {item['runtime_definition_ordinal']}",
                f"- runtime definition line: {item['runtime_definition_line']}",
                f"- earlier-only assertions: {item['earlier_only_assertion_count']}",
                f"- shadowed definition has unique assertions: {item['shadowed_definition_has_unique_assertions']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Unresolved removable pairs",
            "",
            f"- pairs: {len(unresolved_results)}",
            "",
        ]
    )

    for item in unresolved_results:
        lines.extend(
            [
                f"### `{item.get('candidate_id', '')}`",
                "",
                f"- older: `{item['older_test_id']}`",
                f"- newer: `{item['newer_test_id']}`",
                f"- classification: `{item['classification']}`",
                "",
            ]
        )
        for endpoint in item["endpoints"]:
            lines.extend(
                [
                    f"  - {endpoint['role']} graph deletion candidate: {endpoint['graph_marks_deletion_candidate']}",
                    f"  - {endpoint['role']} safe function deletion row: {endpoint['has_safe_function_deletion_row']}",
                ]
            )
        lines.append("")

    lines.extend(
        [
            "No production code or existing test was changed.",
            "Repository-wide pytest was NOT run.",
        ]
    )

    (output_dir / "phase155_r3_3d_r2_summary.md").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("Phase 155-R3-3D-r2 semantic audit completed.")
    print("duplicate-name groups:", len(duplicate_results))
    print(
        "runtime uses final definition in all groups:",
        summary["runtime_last_definition_confirmed"],
    )
    print(
        "shadowed groups with unique assertions:",
        shadowed_unique_count,
    )
    print(
        "shadowed groups without unique assertions:",
        shadowed_no_unique_count,
    )
    print("unresolved removable pairs:", len(unresolved_results))
    for key, value in sorted(unresolved_class_counts.items()):
        print("  " + key + ":", value)
    print("production changes: none")
    print("existing-test changes: none")
    print("test deletion: none")
    print("repository-wide pytest: NOT run")
    print("output:", output_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
