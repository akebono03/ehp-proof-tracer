
from __future__ import annotations

import argparse
import ast
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _split_test_id(test_id: str) -> tuple[str, str]:
    file_path, function_name = test_id.split("::", 1)
    return file_path.replace("\\", "/"), function_name


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8-sig"))


def _top_level_test_functions(path: Path):
    tree = _parse(path)
    return [
        node
        for node in tree.body
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name.startswith("test_")
        )
    ]


def _assertion_dumps(node: ast.AST) -> list[str]:
    return [
        ast.dump(child.test, include_attributes=False)
        for child in ast.walk(node)
        if isinstance(child, ast.Assert)
    ]


def _call_dumps(node: ast.AST) -> set[str]:
    return {
        ast.dump(child.func, include_attributes=False)
        for child in ast.walk(node)
        if isinstance(child, ast.Call)
    }


def _all_assertion_coverage(
    repo_root: Path,
) -> dict[str, list[dict[str, object]]]:
    coverage: dict[str, list[dict[str, object]]] = defaultdict(list)

    for path in sorted((repo_root / "tests").glob("test_*.py")):
        relative = path.relative_to(repo_root).as_posix()
        functions = _top_level_test_functions(path)

        last_ordinal_by_name = {}
        ordinal_counter = Counter()
        for node in functions:
            ordinal_counter[node.name] += 1
            last_ordinal_by_name[node.name] = ordinal_counter[node.name]

        ordinal_counter.clear()
        for node in functions:
            ordinal_counter[node.name] += 1
            ordinal = ordinal_counter[node.name]
            is_runtime_definition = (
                ordinal == last_ordinal_by_name[node.name]
            )
            for assertion in _assertion_dumps(node):
                coverage[assertion].append(
                    {
                        "test_id": relative + "::" + node.name,
                        "file_path": relative,
                        "function_name": node.name,
                        "definition_ordinal": ordinal,
                        "is_runtime_definition": is_runtime_definition,
                        "line": node.lineno,
                    }
                )

    return coverage


def _source_refs_to_function_names(
    repo_root: Path,
    function_names: set[str],
) -> dict[str, list[str]]:
    result = {name: [] for name in function_names}

    for path in sorted(repo_root.rglob("*.py")):
        parts = set(path.parts)
        if "__pycache__" in parts:
            continue

        try:
            source = path.read_text(encoding="utf-8-sig")
            tree = ast.parse(source)
        except (
            UnicodeDecodeError,
            SyntaxError,
            OSError,
        ):
            continue

        relative = path.relative_to(repo_root).as_posix()

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in result:
                result[node.id].append(relative + ":" + str(node.lineno))
            elif isinstance(node, ast.Attribute) and node.attr in result:
                result[node.attr].append(relative + ":" + str(node.lineno))
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name in result:
                        result[alias.name].append(
                            relative + ":" + str(node.lineno)
                        )

    return {
        key: sorted(set(value))
        for key, value in result.items()
    }


def _current_function_semantics(
    repo_root: Path,
    test_id: str,
) -> dict[str, object]:
    file_path, function_name = _split_test_id(test_id)
    path = repo_root / file_path
    matches = [
        node
        for node in _top_level_test_functions(path)
        if node.name == function_name
    ]

    if not matches:
        raise RuntimeError("test function not found: " + test_id)

    node = matches[-1]
    return {
        "test_id": test_id,
        "file_path": file_path,
        "function_name": function_name,
        "assertions": _assertion_dumps(node),
        "calls": sorted(_call_dumps(node)),
        "line": node.lineno,
    }


def _semantic_relation(
    older: dict[str, object],
    newer: dict[str, object],
) -> dict[str, object]:
    older_assertions = set(older["assertions"])
    newer_assertions = set(newer["assertions"])
    older_calls = set(older["calls"])
    newer_calls = set(newer["calls"])

    return {
        "assertions_equal": older_assertions == newer_assertions,
        "older_assertions_subset_newer": older_assertions <= newer_assertions,
        "newer_assertions_subset_older": newer_assertions <= older_assertions,
        "older_only_assertions": sorted(older_assertions - newer_assertions),
        "newer_only_assertions": sorted(newer_assertions - older_assertions),
        "calls_equal": older_calls == newer_calls,
        "older_calls_subset_newer": older_calls <= newer_calls,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--r3d-r2-output",
        type=Path,
        default=Path("phase155_r3_3d_r2_audit_output"),
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
        default=Path("phase155_r3_3d_r3_audit_output"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    def resolve(path: Path) -> Path:
        return path if path.is_absolute() else repo_root / path

    r2_dir = resolve(args.r3d_r2_output)
    duplicate_path = r2_dir / "phase155_r3_3d_r2_duplicate_semantics.json"
    unresolved_path = (
        r2_dir
        / "phase155_r3_3d_r2_unresolved_pair_semantics.json"
    )
    verified_pairs_path = resolve(args.verified_pairs)

    for path in (
        duplicate_path,
        unresolved_path,
        verified_pairs_path,
    ):
        if not path.exists():
            raise SystemExit("required audit input not found: " + str(path))

    duplicate_groups = json.loads(
        duplicate_path.read_text(encoding="utf-8")
    )
    unresolved_pairs = json.loads(
        unresolved_path.read_text(encoding="utf-8")
    )
    verified_pairs = _read_csv(verified_pairs_path)
    verified_by_candidate = {
        row.get("candidate_id", ""): row
        for row in verified_pairs
    }

    coverage = _all_assertion_coverage(repo_root)

    hidden_results = []
    ready_shadow_cleanup = 0
    preservation_required = 0

    for group in duplicate_groups:
        test_id = group["file_path"] + "::" + group["function_name"]
        hidden_assertions = group["earlier_only_assertions"]
        assertion_results = []

        for assertion in hidden_assertions:
            locations = coverage.get(assertion, [])
            runtime_other_locations = [
                location
                for location in locations
                if (
                    location["is_runtime_definition"]
                    and location["test_id"] != test_id
                )
            ]

            assertion_results.append(
                {
                    "assertion": assertion,
                    "all_locations": locations,
                    "runtime_other_locations": runtime_other_locations,
                    "covered_by_other_runtime_test": bool(
                        runtime_other_locations
                    ),
                }
            )

        all_hidden_covered_elsewhere = all(
            item["covered_by_other_runtime_test"]
            for item in assertion_results
        )

        if not hidden_assertions or all_hidden_covered_elsewhere:
            recommendation = "shadowed_definition_cleanup_ready"
            ready_shadow_cleanup += 1
        else:
            recommendation = "preserve_hidden_coverage_before_cleanup"
            preservation_required += 1

        hidden_results.append(
            {
                "test_id": test_id,
                "runtime_definition_ordinal": (
                    group["runtime_definition_ordinal"]
                ),
                "hidden_assertion_count": len(hidden_assertions),
                "all_hidden_assertions_covered_elsewhere": (
                    all_hidden_covered_elsewhere
                ),
                "recommendation": recommendation,
                "assertions": assertion_results,
            }
        )

    unresolved_function_names = set()
    for pair in unresolved_pairs:
        for key in ("older_test_id", "newer_test_id"):
            _, function_name = _split_test_id(pair[key])
            unresolved_function_names.add(function_name)

    refs = _source_refs_to_function_names(
        repo_root,
        unresolved_function_names,
    )

    pair_results = []
    pair_delete_ready = 0
    pair_manual = 0

    for pair in unresolved_pairs:
        candidate_id = pair.get("candidate_id", "")
        verified = verified_by_candidate.get(candidate_id, {})
        older = _current_function_semantics(
            repo_root,
            pair["older_test_id"],
        )
        newer = _current_function_semantics(
            repo_root,
            pair["newer_test_id"],
        )
        relation = _semantic_relation(older, newer)

        older_refs = [
            ref
            for ref in refs.get(older["function_name"], [])
            if not ref.startswith(older["file_path"] + ":")
        ]
        newer_refs = [
            ref
            for ref in refs.get(newer["function_name"], [])
            if not ref.startswith(newer["file_path"] + ":")
        ]

        verified_decision = verified.get("decision", "")
        safe_semantic_containment = (
            relation["older_assertions_subset_newer"]
            and relation["older_calls_subset_newer"]
        )
        no_external_older_refs = not older_refs

        if (
            verified_decision == "removable_duplicate"
            and safe_semantic_containment
            and no_external_older_refs
        ):
            repaired_decision = "delete_older_keep_newer_candidate"
            pair_delete_ready += 1
        else:
            repaired_decision = "manual_semantic_review_required"
            pair_manual += 1

        pair_results.append(
            {
                "candidate_id": candidate_id,
                "verified_decision": verified_decision,
                "older_test_id": pair["older_test_id"],
                "newer_test_id": pair["newer_test_id"],
                "relation": relation,
                "older_external_references": older_refs,
                "newer_external_references": newer_refs,
                "safe_semantic_containment": safe_semantic_containment,
                "no_external_older_references": no_external_older_refs,
                "repaired_decision": repaired_decision,
            }
        )

    output_dir = resolve(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "phase155_r3_3d_r3_hidden_coverage.json").write_text(
        json.dumps(hidden_results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "phase155_r3_3d_r3_pair_decisions.json").write_text(
        json.dumps(pair_results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    repair_plan = {
        "shadowed_duplicate_groups": len(hidden_results),
        "shadowed_cleanup_ready": ready_shadow_cleanup,
        "hidden_coverage_preservation_required": preservation_required,
        "unresolved_pairs": len(pair_results),
        "pair_delete_older_keep_newer_candidates": pair_delete_ready,
        "pair_manual_semantic_review_required": pair_manual,
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (output_dir / "phase155_r3_3d_r3_repair_plan.json").write_text(
        json.dumps(repair_plan, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    md = [
        "# Phase 155-R3-3D-r3 — hidden coverage preservation / pair decision repair",
        "",
        "## Hidden coverage",
        "",
        f"- duplicate-name groups: {len(hidden_results)}",
        f"- shadowed cleanup ready: {ready_shadow_cleanup}",
        f"- hidden coverage preservation required: {preservation_required}",
        "",
    ]

    for item in hidden_results:
        md.extend(
            [
                f"### `{item['test_id']}`",
                "",
                f"- hidden assertions: {item['hidden_assertion_count']}",
                f"- all hidden assertions covered by other runtime tests: {item['all_hidden_assertions_covered_elsewhere']}",
                f"- recommendation: `{item['recommendation']}`",
                "",
            ]
        )

    md.extend(
        [
            "## Unresolved pair decision repair",
            "",
            f"- pairs: {len(pair_results)}",
            f"- delete-older / keep-newer candidates: {pair_delete_ready}",
            f"- manual semantic review required: {pair_manual}",
            "",
        ]
    )

    for item in pair_results:
        md.extend(
            [
                f"### `{item['candidate_id']}`",
                "",
                f"- older: `{item['older_test_id']}`",
                f"- newer: `{item['newer_test_id']}`",
                f"- verified decision: `{item['verified_decision']}`",
                f"- older assertions subset newer: {item['relation']['older_assertions_subset_newer']}",
                f"- older calls subset newer: {item['relation']['older_calls_subset_newer']}",
                f"- external references to older test function: {len(item['older_external_references'])}",
                f"- repaired decision: `{item['repaired_decision']}`",
                "",
            ]
        )

    md.extend(
        [
            "No production code or existing tests were changed.",
            "Repository-wide pytest was NOT run.",
        ]
    )

    (output_dir / "phase155_r3_3d_r3_summary.md").write_text(
        "\n".join(md) + "\n",
        encoding="utf-8",
    )

    print("Phase 155-R3-3D-r3 audit completed.")
    print("duplicate-name groups:", len(hidden_results))
    print("shadowed cleanup ready:", ready_shadow_cleanup)
    print(
        "hidden coverage preservation required:",
        preservation_required,
    )
    print("unresolved pairs:", len(pair_results))
    print(
        "delete-older / keep-newer candidates:",
        pair_delete_ready,
    )
    print(
        "manual semantic review required:",
        pair_manual,
    )
    print("production changes: none")
    print("existing-test changes: none")
    print("test deletion: none")
    print("repository-wide pytest: NOT run")
    print("output:", output_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
