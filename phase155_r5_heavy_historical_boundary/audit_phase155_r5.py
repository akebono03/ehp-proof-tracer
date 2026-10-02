from __future__ import annotations

import argparse
import ast
import csv
import json
import re
from collections import Counter
from pathlib import Path


CATEGORY_CANONICAL = "canonical_candidate"
CATEGORY_PUBLIC = "canonical_public_surface_candidate"
CATEGORY_INTERNAL = "canonical_internal_contract_candidate"
CATEGORY_GLOBAL = "canonical_module_global_contract_candidate"
CATEGORY_HISTORICAL = "historical_compatibility"
CATEGORY_AUDIT = "audit_only_candidate"
CATEGORY_HEAVY = "performance_heavy_integration_candidate"
CATEGORY_RESIDUAL = "residual_validation_lane"

R5_HISTORICAL = "historical_compatibility"
R5_AUDIT = "audit_only"
R5_HEAVY = "performance_heavy_integration"
R5_RESIDUAL = "residual_retained"
R5_CANONICAL = "canonical_routine"

HISTORICAL_STRONG_PATTERNS = (
    "historical only",
    "historical compatibility",
    "legacy compatibility",
    "backward compatibility",
    "backward-compatible",
    "backward compatible",
)

AUDIT_FILENAME_PATTERNS = (
    "audit",
    "inventory",
    "coverage_matrix",
    "parity",
)

HEAVY_FILENAME_PATTERNS = (
    "all_group",
    "all_groups",
    "cross_group",
    "population",
    "exhaustive",
    "full_depth",
    "repository_wide",
    "whole_suite",
)

HEAVY_FUNCTION_PATTERNS = (
    "all_group",
    "all_groups",
    "cross_group",
    "population",
    "exhaustive",
    "full_depth",
    "repository_wide",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        return list(csv.DictReader(handle))


def _safe_read(path: Path) -> str:
    return path.read_text(
        encoding="utf-8-sig"
    )


def _imports_audit_module(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(
                    "audit_"
                ):
                    return True

        elif isinstance(node, ast.ImportFrom):
            if (
                node.module is not None
                and (
                    node.module.startswith(
                        "audit_"
                    )
                    or ".audit_" in node.module
                )
            ):
                return True

    return False


def _function_node(
    tree: ast.Module,
    function_name: str,
):
    for node in tree.body:
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name == function_name
        ):
            return node

    return None


def _function_has_broad_iteration(
    node: ast.AST | None,
) -> bool:
    if node is None:
        return False

    for child in ast.walk(node):
        if isinstance(
            child,
            (
                ast.For,
                ast.AsyncFor,
            ),
        ):
            return True

        if (
            isinstance(child, ast.Call)
            and isinstance(
                child.func,
                ast.Attribute,
            )
            and child.func.attr
            == "parametrize"
        ):
            return True

    return False


def _contains_any(
    text: str,
    patterns: tuple[str, ...],
) -> bool:
    lowered = text.lower()

    return any(
        pattern in lowered
        for pattern in patterns
    )


def _classify_residual(
    file_path: str,
    function_name: str,
    source: str,
    tree: ast.Module,
) -> tuple[str, str, dict[str, bool]]:
    filename = Path(
        file_path
    ).name.lower()
    function_lower = (
        function_name.lower()
    )
    source_lower = source.lower()

    historical_strong = (
        _contains_any(
            source_lower,
            HISTORICAL_STRONG_PATTERNS,
        )
        or (
            "compatibility"
            in filename
            and (
                "legacy"
                in source_lower
                or "backward"
                in source_lower
            )
        )
    )

    audit_import = _imports_audit_module(
        tree
    )
    audit_name = _contains_any(
        filename,
        AUDIT_FILENAME_PATTERNS,
    )

    heavy_name = (
        _contains_any(
            filename,
            HEAVY_FILENAME_PATTERNS,
        )
        or _contains_any(
            function_lower,
            HEAVY_FUNCTION_PATTERNS,
        )
    )

    function_node = _function_node(
        tree,
        function_name,
    )
    broad_iteration = (
        _function_has_broad_iteration(
            function_node
        )
    )

    heavy_strong = (
        heavy_name
        and (
            broad_iteration
            or audit_import
            or "targets" in source_lower
            or "cases" in source_lower
        )
    )

    evidence = {
        "historical_strong": historical_strong,
        "audit_import": audit_import,
        "audit_name": audit_name,
        "heavy_name": heavy_name,
        "broad_iteration": broad_iteration,
        "heavy_strong": heavy_strong,
    }

    if historical_strong:
        return (
            R5_HISTORICAL,
            "strong historical/legacy compatibility evidence",
            evidence,
        )

    if heavy_strong:
        return (
            R5_HEAVY,
            "broad/cross-group population evidence; keep outside routine regression",
            evidence,
        )

    if audit_import or audit_name:
        return (
            R5_AUDIT,
            "audit/inventory evidence; run on demand",
            evidence,
        )

    return (
        R5_RESIDUAL,
        "no strong historical/audit/heavy evidence; retain without routine execution",
        evidence,
    )


def _lane_for_existing_category(
    category: str,
) -> str | None:
    if category in {
        CATEGORY_CANONICAL,
        CATEGORY_PUBLIC,
        CATEGORY_INTERNAL,
        CATEGORY_GLOBAL,
    }:
        return R5_CANONICAL

    if category == CATEGORY_HISTORICAL:
        return R5_HISTORICAL

    if category == CATEGORY_AUDIT:
        return R5_AUDIT

    if category == CATEGORY_HEAVY:
        return R5_HEAVY

    return None


def _checkpoint_path(
    checkpoint_dir: Path,
    file_path: str,
) -> Path:
    safe_name = re.sub(
        r"[^A-Za-z0-9_.-]+",
        "_",
        file_path,
    )

    return (
        checkpoint_dir
        / (
            safe_name
            + ".json"
        )
    )


def _write_manifest(
    path: Path,
    rows: list[dict[str, str]],
    lane: str,
) -> None:
    nodeids = [
        row["test_id"]
        for row in rows
        if row["r5_lane"] == lane
    ]

    path.write_text(
        "\n".join(nodeids)
        + (
            "\n"
            if nodeids
            else ""
        ),
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
        "--r4-4-classification",
        type=Path,
        default=Path(
            "phase155_r4_4_audit_output/"
            "phase155_r4_4_final_classification.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r5_audit_output"
        ),
    )
    parser.add_argument(
        "--reset-checkpoints",
        action="store_true",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()

    classification_path = (
        args.r4_4_classification
        if args.r4_4_classification.is_absolute()
        else repo_root
        / args.r4_4_classification
    )

    if not classification_path.exists():
        raise SystemExit(
            "required R4-4 classification not found: "
            + str(
                classification_path
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

    checkpoint_dir = (
        output_dir
        / "checkpoints"
    )

    if (
        args.reset_checkpoints
        and checkpoint_dir.exists()
    ):
        for path in checkpoint_dir.glob(
            "*.json"
        ):
            path.unlink()

    checkpoint_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = _read_csv(
        classification_path
    )

    file_to_rows: dict[
        str,
        list[dict[str, str]],
    ] = {}

    for row in rows:
        file_to_rows.setdefault(
            row["file_path"],
            [],
        ).append(row)

    files = sorted(
        file_to_rows
    )

    final_rows = []
    reused_files = 0
    analyzed_files = 0

    print("R5 static boundary audit")
    print("files:", len(files))
    print("test bodies: NOT executed")
    print("checkpoint/resume: enabled")
    print("")

    for index, file_path in enumerate(
        files,
        start=1,
    ):
        checkpoint = _checkpoint_path(
            checkpoint_dir,
            file_path,
        )

        source_path = (
            repo_root
            / file_path
        )

        if checkpoint.exists():
            payload = json.loads(
                checkpoint.read_text(
                    encoding="utf-8"
                )
            )

            final_rows.extend(
                payload["rows"]
            )
            reused_files += 1

            print(
                f"[{index}/{len(files)}] "
                f"skip checkpoint: "
                f"{file_path}",
                flush=True,
            )
            continue

        print(
            f"[{index}/{len(files)}] "
            f"analyze: "
            f"{file_path}",
            flush=True,
        )

        source = _safe_read(
            source_path
        )
        tree = ast.parse(
            source
        )

        file_results = []

        for row in file_to_rows[
            file_path
        ]:
            existing_lane = (
                _lane_for_existing_category(
                    row["r4_4_category"]
                )
            )

            if existing_lane is not None:
                lane = existing_lane
                reason = (
                    "R4-4 category preserved"
                )
                evidence = {
                    "historical_strong": False,
                    "audit_import": False,
                    "audit_name": False,
                    "heavy_name": False,
                    "broad_iteration": False,
                    "heavy_strong": False,
                }

            elif (
                row["r4_4_category"]
                == CATEGORY_RESIDUAL
            ):
                (
                    lane,
                    reason,
                    evidence,
                ) = _classify_residual(
                    file_path,
                    row["function_name"],
                    source,
                    tree,
                )

            else:
                lane = R5_RESIDUAL
                reason = (
                    "unknown R4-4 category retained conservatively"
                )
                evidence = {
                    "historical_strong": False,
                    "audit_import": False,
                    "audit_name": False,
                    "heavy_name": False,
                    "broad_iteration": False,
                    "heavy_strong": False,
                }

            result = {
                **row,
                "r5_lane": lane,
                "r5_reason": reason,
                **{
                    "r5_" + key: value
                    for key, value
                    in evidence.items()
                },
            }

            file_results.append(
                result
            )
            final_rows.append(
                result
            )

        checkpoint.write_text(
            json.dumps(
                {
                    "file_path": file_path,
                    "rows": file_results,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        analyzed_files += 1

    counts = Counter(
        row["r5_lane"]
        for row in final_rows
    )

    classification_out = (
        output_dir
        / "phase155_r5_boundary_classification.csv"
    )

    with classification_out.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as handle:
        fieldnames = list(
            final_rows[0].keys()
        )
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(
            final_rows
        )

    manifests = {
        R5_CANONICAL: (
            output_dir
            / "phase155_r5_canonical_routine_nodeids.txt"
        ),
        R5_HISTORICAL: (
            output_dir
            / "phase155_r5_historical_nodeids.txt"
        ),
        R5_AUDIT: (
            output_dir
            / "phase155_r5_audit_only_nodeids.txt"
        ),
        R5_HEAVY: (
            output_dir
            / "phase155_r5_heavy_nodeids.txt"
        ),
        R5_RESIDUAL: (
            output_dir
            / "phase155_r5_residual_retained_nodeids.txt"
        ),
    }

    for lane, path in manifests.items():
        _write_manifest(
            path,
            final_rows,
            lane,
        )

    nonroutine = [
        row["test_id"]
        for row in final_rows
        if row["r5_lane"] != R5_CANONICAL
    ]

    (
        output_dir
        / "phase155_r5_nonroutine_nodeids.txt"
    ).write_text(
        "\n".join(
            nonroutine
        )
        + (
            "\n"
            if nonroutine
            else ""
        ),
        encoding="utf-8",
    )

    completion = {
        "all_source_rows_classified": (
            len(final_rows)
            == len(rows)
        ),
        "canonical_preserved": (
            counts[
                R5_CANONICAL
            ]
            == sum(
                1
                for row in rows
                if row[
                    "r4_4_category"
                ]
                in {
                    CATEGORY_CANONICAL,
                    CATEGORY_PUBLIC,
                    CATEGORY_INTERNAL,
                    CATEGORY_GLOBAL,
                }
            )
        ),
        "no_test_execution": True,
        "checkpoint_resume_enabled": True,
    }

    validated = all(
        completion.values()
    )

    metadata = {
        "source_test_functions": len(rows),
        "files": len(files),
        "files_analyzed_this_run": analyzed_files,
        "files_reused_from_checkpoint": reused_files,
        "lane_counts": dict(counts),
        "nonroutine_tests": len(nonroutine),
        "completion": completion,
        "validated": validated,
        "test_bodies_executed": False,
        "canonical_regression_executed": False,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r5_metadata.json"
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
        "# Phase 155-R5 — heavy / historical boundary",
        "",
        "## Execution lanes",
        "",
        f"- canonical_routine: {counts[R5_CANONICAL]}",
        f"- historical_compatibility: {counts[R5_HISTORICAL]}",
        f"- audit_only: {counts[R5_AUDIT]}",
        f"- performance_heavy_integration: {counts[R5_HEAVY]}",
        f"- residual_retained: {counts[R5_RESIDUAL]}",
        f"- nonroutine total: {len(nonroutine)}",
        "",
        "## Policy",
        "",
        "- canonical_routine is the only routine regression lane.",
        "- historical_compatibility runs only for compatibility/release review.",
        "- audit_only runs only when its audit question is relevant.",
        "- performance_heavy_integration never runs in normal focused/canonical feedback loops.",
        "- residual_retained is preserved but not routine until R6 measurement/closure.",
        "- no test was deleted.",
        "- no test body was executed.",
        "- checkpoint/resume is enabled.",
        "",
        "## Future-test rule",
        "",
        "- New tests should be lightweight by default.",
        "- New all-group/cross-group/population scans must not enter routine canonical regression.",
        "- Heavy integration tests must be explicitly separated at creation time.",
        "- Long audit runners must show progress and support checkpoint/resume.",
        "",
        "## Completion",
        "",
    ]

    for key, value in completion.items():
        lines.append(
            "- "
            + key
            + ": "
            + (
                "PASS"
                if value
                else "FAIL"
            )
        )

    lines.extend(
        [
            "",
            (
                "**Phase 155-R5 boundary validated: True**"
                if validated
                else "**Phase 155-R5 boundary validated: False**"
            ),
            "",
            "Canonical regression: NOT run.",
            "Repository-wide pytest: NOT run.",
        ]
    )

    (
        output_dir
        / "phase155_r5_summary.md"
    ).write_text(
        "\n".join(lines)
        + "\n",
        encoding="utf-8",
    )

    print("")
    print(
        "Phase 155-R5 boundary audit completed."
    )
    print(
        "canonical_routine:",
        counts[R5_CANONICAL],
    )
    print(
        "historical_compatibility:",
        counts[R5_HISTORICAL],
    )
    print(
        "audit_only:",
        counts[R5_AUDIT],
    )
    print(
        "performance_heavy_integration:",
        counts[R5_HEAVY],
    )
    print(
        "residual_retained:",
        counts[R5_RESIDUAL],
    )
    print(
        "nonroutine total:",
        len(nonroutine),
    )
    print(
        "files analyzed this run:",
        analyzed_files,
    )
    print(
        "files reused from checkpoint:",
        reused_files,
    )
    print(
        "R5 boundary validated:",
        validated,
    )
    print("test bodies: NOT run")
    print("canonical regression: NOT run")
    print("repository-wide pytest: NOT run")
    print("output:", output_dir)

    return 0 if validated else 2


if __name__ == "__main__":
    raise SystemExit(main())
