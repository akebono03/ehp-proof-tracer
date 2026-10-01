from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


CATEGORY_CURRENT = "current_contract"
CATEGORY_HISTORICAL = "historical_compatibility"
CATEGORY_AUDIT = "audit_only"
CATEGORY_SNAPSHOT = "superseded_snapshot"
CATEGORY_DUPLICATE = "duplicate_coverage"
CATEGORY_HEAVY = "performance_heavy_integration"

ALL_CATEGORIES = (
    CATEGORY_CURRENT,
    CATEGORY_HISTORICAL,
    CATEGORY_AUDIT,
    CATEGORY_SNAPSHOT,
    CATEGORY_DUPLICATE,
    CATEGORY_HEAVY,
)

AUDIT_TOKENS = (
    "audit",
    "probe",
    "diagnostic",
    "observability",
    "completion",
    "closure",
    "inventory",
)

HISTORICAL_TOKENS = (
    "compatibility",
    "regression",
    "legacy",
    "historical",
    "stale",
    "boundary_regression",
)

SNAPSHOT_TOKENS = (
    "snapshot",
    "fixed_count",
    "fixed_total",
    "exact_count",
    "golden",
)

HEAVY_TOKENS = (
    "repository_wide",
    "repositorywide",
    "all_group",
    "allgroup",
    "cross_group",
    "completion_audit",
    "closure_audit",
    "full_regression",
    "end_to_end",
)

INTEGRATION_TOKENS = (
    "integration",
    "end_to_end",
    "repository",
    "web",
    "cli",
)

PHASE_RE = re.compile(r"test_phase(?P<phase>\d+)")


@dataclass
class TestInventoryRow:
    test_id: str
    file: str
    function: str
    line: int
    phase: str
    primary_category: str
    confidence: str
    signals: str
    assert_count: int
    loop_count: int
    parametrized: bool
    integration_surface: bool
    normalized_ast_sha256: str


@dataclass
class FileInventoryRow:
    file: str
    phase: str
    bytes: int
    sha256: str
    test_functions: int
    current_contract: int
    historical_compatibility: int
    audit_only: int
    superseded_snapshot: int
    duplicate_coverage: int
    performance_heavy_integration: int


class FunctionFeatureVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.assert_count = 0
        self.loop_count = 0
        self.calls: list[str] = []
        self.constants: list[object] = []

    def visit_Assert(self, node: ast.Assert) -> None:
        self.assert_count += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.loop_count += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.loop_count += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.loop_count += 1
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.calls.append(_call_name(node.func))
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        self.constants.append(node.value)
        self.generic_visit(node)


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _phase_from_path(path: Path) -> str:
    match = PHASE_RE.search(path.name)
    return match.group("phase") if match else "core"


def _normalized_function_dump(node: ast.AST) -> str:
    clone = ast.parse(ast.unparse(node))
    func = clone.body[0]
    if isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
        func.name = "test_normalized"
        func.decorator_list = []
    return ast.dump(clone, annotate_fields=True, include_attributes=False)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    names: list[str] = []
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call):
            names.append(_call_name(decorator.func))
        else:
            names.append(_call_name(decorator))
    return names


def _contains_any(text: str, tokens: Iterable[str]) -> list[str]:
    lowered = text.lower()
    return [token for token in tokens if token in lowered]


def _has_numeric_equality_assert(node: ast.AST) -> bool:
    for item in ast.walk(node):
        if not isinstance(item, ast.Assert):
            continue
        test = item.test
        if not isinstance(test, ast.Compare):
            continue
        values = [test.left, *test.comparators]
        if any(
            isinstance(value, ast.Constant)
            and isinstance(value.value, int)
            for value in values
        ):
            return True
    return False


def _classify_pre_duplicate(
    path: Path,
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    features: FunctionFeatureVisitor,
) -> tuple[str, str, list[str], bool, bool]:
    combined = f"{path.name} {node.name}"
    signals: list[str] = []

    audit_hits = _contains_any(combined, AUDIT_TOKENS)
    historical_hits = _contains_any(combined, HISTORICAL_TOKENS)
    snapshot_hits = _contains_any(combined, SNAPSHOT_TOKENS)
    heavy_hits = _contains_any(combined, HEAVY_TOKENS)
    integration_hits = _contains_any(combined, INTEGRATION_TOKENS)

    decorators = _decorator_names(node)
    parametrized = any("parametrize" in name for name in decorators)
    integration_surface = bool(integration_hits)

    if parametrized:
        signals.append("parametrized")
    if integration_surface:
        signals.append("integration_surface")
    if features.loop_count:
        signals.append(f"loops={features.loop_count}")

    numeric_count_assert = _has_numeric_equality_assert(node)
    if numeric_count_assert:
        signals.append("numeric_equality_assert")

    for hit in audit_hits:
        signals.append(f"token:{hit}")
    for hit in historical_hits:
        signals.append(f"token:{hit}")
    for hit in snapshot_hits:
        signals.append(f"token:{hit}")
    for hit in heavy_hits:
        signals.append(f"token:{hit}")

    # Conservative ordering. A category stronger than current_contract is selected
    # only from an explicit structural/name signal. Old Phase number alone is never
    # enough to downgrade a test.
    if snapshot_hits and numeric_count_assert:
        return CATEGORY_SNAPSHOT, "high", signals, parametrized, integration_surface

    if heavy_hits and (features.loop_count > 0 or integration_surface):
        return CATEGORY_HEAVY, "high", signals, parametrized, integration_surface

    if audit_hits:
        return CATEGORY_AUDIT, "high", signals, parametrized, integration_surface

    if historical_hits:
        return CATEGORY_HISTORICAL, "medium", signals, parametrized, integration_surface

    return CATEGORY_CURRENT, "medium", signals, parametrized, integration_surface


def _iter_test_functions(tree: ast.Module) -> Iterable[ast.FunctionDef | ast.AsyncFunctionDef]:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            yield node
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name.startswith("test_"):
                    yield child


def collect_inventory(repo_root: Path) -> tuple[list[TestInventoryRow], list[FileInventoryRow], dict[str, list[str]]]:
    tests_dir = repo_root / "tests"
    if not tests_dir.is_dir():
        raise SystemExit(f"tests directory not found: {tests_dir}")

    source_files = sorted(tests_dir.glob("test_*.py"))
    provisional: list[dict[str, object]] = []
    file_meta: dict[str, dict[str, object]] = {}

    for path in source_files:
        relative = path.relative_to(repo_root).as_posix()
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
        phase = _phase_from_path(path)
        file_meta[relative] = {
            "phase": phase,
            "bytes": path.stat().st_size,
            "sha256": _sha256_file(path),
        }

        for node in _iter_test_functions(tree):
            features = FunctionFeatureVisitor()
            features.visit(node)
            category, confidence, signals, parametrized, integration_surface = _classify_pre_duplicate(
                path,
                node,
                features,
            )
            fingerprint = _sha256_text(_normalized_function_dump(node))
            provisional.append(
                {
                    "test_id": f"{relative}::{node.name}",
                    "file": relative,
                    "function": node.name,
                    "line": node.lineno,
                    "phase": phase,
                    "primary_category": category,
                    "confidence": confidence,
                    "signals": signals,
                    "assert_count": features.assert_count,
                    "loop_count": features.loop_count,
                    "parametrized": parametrized,
                    "integration_surface": integration_surface,
                    "normalized_ast_sha256": fingerprint,
                }
            )

    fingerprints: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in provisional:
        fingerprints[str(item["normalized_ast_sha256"])].append(item)

    duplicate_groups: dict[str, list[str]] = {}
    for fingerprint, items in fingerprints.items():
        if len(items) < 2:
            continue
        ids = sorted(str(item["test_id"]) for item in items)
        duplicate_groups[fingerprint] = ids
        for item in items:
            # Exact normalized AST duplicates are stronger evidence than naming.
            # Preserve heavy/snapshot categories because they are operationally
            # important for later R2/R5 work; otherwise classify as duplicate.
            if item["primary_category"] not in {CATEGORY_HEAVY, CATEGORY_SNAPSHOT}:
                item["primary_category"] = CATEGORY_DUPLICATE
                item["confidence"] = "high"
                signals = list(item["signals"])
                signals.append(f"exact_ast_duplicate_group={len(items)}")
                item["signals"] = signals

    rows = [
        TestInventoryRow(
            test_id=str(item["test_id"]),
            file=str(item["file"]),
            function=str(item["function"]),
            line=int(item["line"]),
            phase=str(item["phase"]),
            primary_category=str(item["primary_category"]),
            confidence=str(item["confidence"]),
            signals=";".join(str(x) for x in item["signals"]),
            assert_count=int(item["assert_count"]),
            loop_count=int(item["loop_count"]),
            parametrized=bool(item["parametrized"]),
            integration_surface=bool(item["integration_surface"]),
            normalized_ast_sha256=str(item["normalized_ast_sha256"]),
        )
        for item in provisional
    ]

    by_file: dict[str, list[TestInventoryRow]] = defaultdict(list)
    for row in rows:
        by_file[row.file].append(row)

    file_rows: list[FileInventoryRow] = []
    for relative in sorted(file_meta):
        tests = by_file.get(relative, [])
        counts = Counter(row.primary_category for row in tests)
        meta = file_meta[relative]
        file_rows.append(
            FileInventoryRow(
                file=relative,
                phase=str(meta["phase"]),
                bytes=int(meta["bytes"]),
                sha256=str(meta["sha256"]),
                test_functions=len(tests),
                current_contract=counts[CATEGORY_CURRENT],
                historical_compatibility=counts[CATEGORY_HISTORICAL],
                audit_only=counts[CATEGORY_AUDIT],
                superseded_snapshot=counts[CATEGORY_SNAPSHOT],
                duplicate_coverage=counts[CATEGORY_DUPLICATE],
                performance_heavy_integration=counts[CATEGORY_HEAVY],
            )
        )

    return rows, file_rows, duplicate_groups


def _git_head(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def write_csv(path: Path, rows: Iterable[object]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    first = asdict(rows[0])
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(first.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_duplicate_csv(path: Path, groups: dict[str, list[str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["normalized_ast_sha256", "group_size", "test_id"])
        for fingerprint, ids in sorted(groups.items()):
            for test_id in ids:
                writer.writerow([fingerprint, len(ids), test_id])


def write_summary(
    path: Path,
    repo_root: Path,
    rows: list[TestInventoryRow],
    file_rows: list[FileInventoryRow],
    duplicate_groups: dict[str, list[str]],
) -> None:
    category_counts = Counter(row.primary_category for row in rows)
    phase_counts = Counter(row.phase for row in rows)
    candidate_review = sum(
        category_counts[c]
        for c in (
            CATEGORY_HISTORICAL,
            CATEGORY_AUDIT,
            CATEGORY_SNAPSHOT,
            CATEGORY_DUPLICATE,
            CATEGORY_HEAVY,
        )
    )

    lines = [
        "# Phase 155-R1 — Test inventory / classification audit",
        "",
        "## Boundary",
        "",
        "This audit performs static inventory only. It does not execute pytest, delete tests, change production code, or decide removals.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Test files: {len(file_rows)}",
        f"- Test functions: {len(rows)}",
        f"- Exact normalized-AST duplicate groups: {len(duplicate_groups)}",
        f"- Non-current candidates requiring later review: {candidate_review}",
        "",
        "## Primary classification",
        "",
        "| category | test functions |",
        "| --- | ---: |",
    ]
    for category in ALL_CATEGORIES:
        lines.append(f"| `{category}` | {category_counts[category]} |")

    lines.extend(
        [
            "",
            "## Phase distribution",
            "",
            "| phase | test functions |",
            "| --- | ---: |",
        ]
    )
    def phase_sort_key(item: tuple[str, int]) -> tuple[int, int | str]:
        phase = item[0]
        return (0, int(phase)) if phase.isdigit() else (1, phase)

    for phase, count in sorted(phase_counts.items(), key=phase_sort_key):
        lines.append(f"| `{phase}` | {count} |")

    lines.extend(
        [
            "",
            "## Classification policy",
            "",
            "- A Phase number alone never makes a test historical.",
            "- `superseded_snapshot` requires an explicit snapshot/fixed-count signal plus a numeric equality assertion.",
            "- `duplicate_coverage` requires an exact normalized AST duplicate across test functions.",
            "- `performance_heavy_integration` requires a heavy-suite name signal plus loop/integration evidence.",
            "- `audit_only` and `historical_compatibility` are selected only from explicit naming signals.",
            "- Everything else remains conservatively in `current_contract` until R2/R3 review.",
            "",
            "## R1 conclusion",
            "",
            "R1 identifies candidates; it does not authorize deletion or expectation changes. R2 should inspect stale expectations, and R3 should review exact duplicates/superseded snapshots against the current contract.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 155-R1 static test inventory and classification audit."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="EHP Proof Tracer repository root (default: current directory)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase155_r1_audit_output"),
        help="Output directory (default: phase155_r1_audit_output)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = (repo_root / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    rows, file_rows, duplicate_groups = collect_inventory(repo_root)

    write_csv(output_dir / "phase155_r1_test_inventory.csv", rows)
    write_csv(output_dir / "phase155_r1_file_inventory.csv", file_rows)
    write_duplicate_csv(
        output_dir / "phase155_r1_duplicate_groups.csv",
        duplicate_groups,
    )
    write_summary(
        output_dir / "phase155_r1_summary.md",
        repo_root,
        rows,
        file_rows,
        duplicate_groups,
    )
    (output_dir / "phase155_r1_metadata.json").write_text(
        json.dumps(
            {
                "git_head": _git_head(repo_root),
                "test_files": len(file_rows),
                "test_functions": len(rows),
                "duplicate_groups": len(duplicate_groups),
                "categories": dict(Counter(row.primary_category for row in rows)),
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("Phase 155-R1 static inventory completed.")
    print(f"test files: {len(file_rows)}")
    print(f"test functions: {len(rows)}")
    print(f"output: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
