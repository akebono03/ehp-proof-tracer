from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


CATEGORY_EXACT = "exact_duplicate_candidate"
CATEGORY_SEMANTIC = "semantic_duplicate_candidate"
CATEGORY_SUPERSEDED = "superseded_candidate"
CATEGORY_INDEPENDENT = "independently_valuable"
CATEGORY_HISTORICAL = "historical_compatibility"

CANDIDATE_CATEGORIES = (
    CATEGORY_EXACT,
    CATEGORY_SEMANTIC,
    CATEGORY_SUPERSEDED,
)

HISTORICAL_TOKENS = (
    "legacy",
    "historical",
    "compatibility",
    "backward",
)

NON_CONTRACT_CALLS = {
    "assert",
    "len",
    "tuple",
    "list",
    "set",
    "dict",
    "sorted",
    "enumerate",
    "range",
    "str",
    "int",
    "bool",
    "isinstance",
    "type",
    "id",
    "next",
    "any",
    "all",
    "sum",
    "min",
    "max",
    "print",
}


@dataclass(frozen=True)
class TestRecord:
    test_id: str
    file: str
    function: str
    phase: str
    line: int
    exact_hash: str
    semantic_hash: str
    call_surface: str
    assertion_atoms: str
    semantic_atoms: str
    assertion_count: int
    primary_category: str
    category_reason: str


@dataclass(frozen=True)
class PairCandidate:
    candidate_id: str
    category: str
    older_test_id: str
    newer_test_id: str
    older_phase: str
    newer_phase: str
    shared_call_surface: str
    older_semantic_atoms: str
    newer_semantic_atoms: str
    evidence: str
    deletion_authorized: bool


def _git_head(repo_root: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _phase_from_file(path: Path) -> str:
    match = re.search(
        r"test_phase(\d+)",
        path.name,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else ""


def _call_name(node: ast.Call) -> str:
    target = node.func
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        parts = [target.attr]
        value = target.value
        while isinstance(value, ast.Attribute):
            parts.append(value.attr)
            value = value.value
        if isinstance(value, ast.Name):
            parts.append(value.id)
        return ".".join(reversed(parts))
    return ""


def _normalize_string(value: str) -> str:
    value = value.replace("、", ", ")
    value = value.replace("。", ".")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def _assertion_nodes(function: ast.AST) -> list[ast.Assert]:
    return [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Assert)
    ]


def _assertion_atoms(function: ast.AST, semantic: bool) -> tuple[str, ...]:
    atoms: set[str] = set()
    for assertion in _assertion_nodes(function):
        for node in ast.walk(assertion.test):
            if isinstance(node, ast.Constant):
                value = node.value
                if isinstance(value, str):
                    text = _normalize_string(value) if semantic else value
                    if text:
                        atoms.add("str:" + text)
                elif isinstance(value, (int, float, bool)):
                    atoms.add(f"const:{value!r}")
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    atoms.add("cmp:" + type(op).__name__)
            elif isinstance(node, ast.Call):
                name = _call_name(node)
                if name:
                    atoms.add("call:" + name)
            elif isinstance(node, ast.Attribute):
                atoms.add("attr:" + node.attr)
    return tuple(sorted(atoms))


def _call_surface(function: ast.AST) -> tuple[str, ...]:
    result: set[str] = set()
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if not name:
            continue
        leaf = name.rsplit(".", 1)[-1]
        if leaf in NON_CONTRACT_CALLS:
            continue
        if leaf.startswith("test_"):
            continue
        result.add(name)
    return tuple(sorted(result))


class _RenameFunction(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        node = self.generic_visit(node)
        node.name = "__test__"
        node.decorator_list = []
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        node = self.generic_visit(node)
        node.name = "__test__"
        node.decorator_list = []
        return node


class _SemanticStrings(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            return ast.copy_location(
                ast.Constant(
                    value=_normalize_string(node.value),
                ),
                node,
            )
        return node


def _hash_function(function: ast.AST, semantic: bool) -> str:
    copied = ast.fix_missing_locations(
        ast.parse(
            ast.unparse(function)
        ).body[0]
    )
    copied = _RenameFunction().visit(copied)
    if semantic:
        copied = _SemanticStrings().visit(copied)
    copied = ast.fix_missing_locations(copied)
    payload = ast.dump(
        copied,
        annotate_fields=True,
        include_attributes=False,
    )
    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


def _is_test_function(node: ast.AST) -> bool:
    return (
        isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
        and node.name.startswith("test_")
    )


def _iter_test_functions(tree: ast.Module):
    for node in tree.body:
        if _is_test_function(node):
            yield node
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for child in node.body:
                if _is_test_function(child):
                    yield child


def _historical_by_name(test_id: str) -> bool:
    lowered = test_id.lower()
    return any(token in lowered for token in HISTORICAL_TOKENS)


def _split_field(value: str) -> set[str]:
    if not value:
        return set()
    return set(value.split("\x1f"))


def scan_tests(repo_root: Path) -> list[TestRecord]:
    raw: list[dict[str, object]] = []

    for path in sorted(
        (repo_root / "tests").glob("test_*.py")
    ):
        source = path.read_text(
            encoding="utf-8-sig",
        )
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue

        relative = path.relative_to(repo_root).as_posix()
        phase = _phase_from_file(path)

        for function in _iter_test_functions(tree):
            exact_atoms = _assertion_atoms(function, semantic=False)
            semantic_atoms = _assertion_atoms(function, semantic=True)
            calls = _call_surface(function)

            raw.append(
                {
                    "test_id": f"{relative}::{function.name}",
                    "file": relative,
                    "function": function.name,
                    "phase": phase,
                    "line": function.lineno,
                    "exact_hash": _hash_function(function, semantic=False),
                    "semantic_hash": _hash_function(function, semantic=True),
                    "call_surface": "\x1f".join(calls),
                    "assertion_atoms": "\x1f".join(exact_atoms),
                    "semantic_atoms": "\x1f".join(semantic_atoms),
                    "assertion_count": len(_assertion_nodes(function)),
                }
            )

    exact_groups: dict[str, list[str]] = defaultdict(list)
    semantic_groups: dict[str, list[str]] = defaultdict(list)
    for row in raw:
        exact_groups[str(row["exact_hash"])].append(str(row["test_id"]))
        semantic_groups[str(row["semantic_hash"])].append(str(row["test_id"]))

    records: list[TestRecord] = []
    for row in raw:
        test_id = str(row["test_id"])
        if _historical_by_name(test_id):
            category = CATEGORY_HISTORICAL
            reason = "Test name explicitly identifies legacy/historical/compatibility coverage."
        elif len(exact_groups[str(row["exact_hash"])]) > 1:
            category = CATEGORY_EXACT
            reason = "Another test has the same normalized function AST after removing the test function name/decorators."
        elif len(semantic_groups[str(row["semantic_hash"])]) > 1:
            category = CATEGORY_SEMANTIC
            reason = "Another test has the same normalized AST after punctuation normalization."
        else:
            category = CATEGORY_INDEPENDENT
            reason = "No exact or semantic duplicate was proven by the conservative static fingerprints."

        records.append(
            TestRecord(
                test_id=test_id,
                file=str(row["file"]),
                function=str(row["function"]),
                phase=str(row["phase"]),
                line=int(row["line"]),
                exact_hash=str(row["exact_hash"]),
                semantic_hash=str(row["semantic_hash"]),
                call_surface=str(row["call_surface"]),
                assertion_atoms=str(row["assertion_atoms"]),
                semantic_atoms=str(row["semantic_atoms"]),
                assertion_count=int(row["assertion_count"]),
                primary_category=category,
                category_reason=reason,
            )
        )

    return records


def _phase_number(value: str) -> int | None:
    return int(value) if value.isdigit() else None


def build_pair_candidates(
    records: list[TestRecord],
) -> list[PairCandidate]:
    result: list[PairCandidate] = []
    counter = 1

    exact_groups: dict[str, list[TestRecord]] = defaultdict(list)
    semantic_groups: dict[str, list[TestRecord]] = defaultdict(list)

    for record in records:
        exact_groups[record.exact_hash].append(record)
        semantic_groups[record.semantic_hash].append(record)

    seen_pairs: set[tuple[str, str, str]] = set()

    def add_pair(
        category: str,
        older: TestRecord,
        newer: TestRecord,
        evidence: str,
    ) -> None:
        nonlocal counter
        key = (
            category,
            older.test_id,
            newer.test_id,
        )
        if key in seen_pairs:
            return
        seen_pairs.add(key)
        result.append(
            PairCandidate(
                candidate_id=f"R3-{counter:05d}",
                category=category,
                older_test_id=older.test_id,
                newer_test_id=newer.test_id,
                older_phase=older.phase,
                newer_phase=newer.phase,
                shared_call_surface="\x1f".join(
                    sorted(
                        _split_field(older.call_surface)
                        & _split_field(newer.call_surface)
                    )
                ),
                older_semantic_atoms=older.semantic_atoms,
                newer_semantic_atoms=newer.semantic_atoms,
                evidence=evidence,
                deletion_authorized=False,
            )
        )
        counter += 1

    for group in exact_groups.values():
        if len(group) < 2:
            continue
        ordered = sorted(
            group,
            key=lambda item: (
                _phase_number(item.phase)
                if _phase_number(item.phase) is not None
                else -1,
                item.test_id,
            ),
        )
        anchor = ordered[-1]
        for item in ordered[:-1]:
            add_pair(
                CATEGORY_EXACT,
                item,
                anchor,
                "Exact normalized test-function AST matches the later/anchor test.",
            )

    for group in semantic_groups.values():
        if len(group) < 2:
            continue
        exact_hashes = {item.exact_hash for item in group}
        if len(exact_hashes) == 1:
            continue
        ordered = sorted(
            group,
            key=lambda item: (
                _phase_number(item.phase)
                if _phase_number(item.phase) is not None
                else -1,
                item.test_id,
            ),
        )
        anchor = ordered[-1]
        for item in ordered[:-1]:
            add_pair(
                CATEGORY_SEMANTIC,
                item,
                anchor,
                "Semantic AST matches after normalizing Japanese/ASCII punctuation.",
            )

    # Conservative superseded candidates:
    # - both have explicit phases and newer phase is greater;
    # - both exercise at least one common nontrivial call;
    # - older has at least two semantic assertion atoms;
    # - every older semantic assertion atom occurs in newer;
    # - exact/semantic duplicate pairs are handled above instead.
    by_surface: dict[str, list[TestRecord]] = defaultdict(list)
    for record in records:
        calls = tuple(sorted(_split_field(record.call_surface)))
        if calls:
            by_surface["\x1f".join(calls)].append(record)

    for group in by_surface.values():
        ordered = sorted(
            group,
            key=lambda item: (
                _phase_number(item.phase)
                if _phase_number(item.phase) is not None
                else -1,
                item.test_id,
            ),
        )
        for i, older in enumerate(ordered):
            older_phase = _phase_number(older.phase)
            if older_phase is None:
                continue
            old_atoms = _split_field(older.semantic_atoms)
            if len(old_atoms) < 2:
                continue

            for newer in ordered[i + 1:]:
                newer_phase = _phase_number(newer.phase)
                if newer_phase is None or newer_phase <= older_phase:
                    continue
                if older.exact_hash == newer.exact_hash:
                    continue
                if older.semantic_hash == newer.semantic_hash:
                    continue

                new_atoms = _split_field(newer.semantic_atoms)
                if not old_atoms.issubset(new_atoms):
                    continue

                add_pair(
                    CATEGORY_SUPERSEDED,
                    older,
                    newer,
                    (
                        "Later-phase test exercises the same call surface and its "
                        "semantic assertion atoms are a superset of the older test. "
                        "This is a candidate only; source review is required before deletion."
                    ),
                )
                break

    return result


def write_csv(path: Path, rows: Iterable[object]) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_summary(
    path: Path,
    repo_root: Path,
    records: list[TestRecord],
    pairs: list[PairCandidate],
) -> None:
    test_counts = Counter(
        record.primary_category
        for record in records
    )
    pair_counts = Counter(
        pair.category
        for pair in pairs
    )
    candidate_files = {
        pair.older_test_id.split("::", 1)[0]
        for pair in pairs
    } | {
        pair.newer_test_id.split("::", 1)[0]
        for pair in pairs
    }

    lines = [
        "# Phase 155-R3-1 — duplicate / superseded candidate audit",
        "",
        "## Boundary",
        "",
        "This is a conservative static candidate audit. It does not delete, rename, move, or rewrite any existing test.",
        "A candidate pair is not proof that the older test should be removed.",
        "Phase number alone is never used as evidence of redundancy.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Source-level test functions scanned: {len(records)}",
        f"- Candidate pairs: {len(pairs)}",
        f"- Files touched by candidate pairs: {len(candidate_files)}",
        "",
        "## Test-level primary categories",
        "",
        "| category | tests |",
        "| --- | ---: |",
    ]
    for category in (
        CATEGORY_EXACT,
        CATEGORY_SEMANTIC,
        CATEGORY_HISTORICAL,
        CATEGORY_INDEPENDENT,
    ):
        lines.append(
            f"| `{category}` | {test_counts[category]} |"
        )

    lines.extend(
        [
            "",
            "## Candidate-pair categories",
            "",
            "| category | pairs |",
            "| --- | ---: |",
        ]
    )
    for category in (
        CATEGORY_EXACT,
        CATEGORY_SEMANTIC,
        CATEGORY_SUPERSEDED,
    ):
        lines.append(
            f"| `{category}` | {pair_counts[category]} |"
        )

    lines.extend(
        [
            "",
            "## Decision rule",
            "",
            "- `exact_duplicate_candidate`: normalized function AST is identical after ignoring test function name/decorators.",
            "- `semantic_duplicate_candidate`: normalized AST becomes identical after Japanese/ASCII punctuation normalization.",
            "- `superseded_candidate`: a later-phase test uses the same nontrivial call surface and contains every semantic assertion atom of the older test.",
            "- `independently_valuable`: no conservative duplicate proof was found.",
            "- `historical_compatibility`: the test explicitly identifies legacy/historical/compatibility intent in its name.",
            "",
            "## Important limitation",
            "",
            "Helper functions, fixtures, parametrization semantics, negative assertions, fixture scope, setup cost, and human-readable intent can make two similar tests independently valuable.",
            "Therefore every candidate has `deletion_authorized=false`.",
            "R3-2 must read candidate source and execute the candidate pair before any removal decision.",
            "",
            "## R3-1 completion gate",
            "",
            "R3-1 is complete when the inventory and pair CSVs are generated and all candidate pairs remain non-destructive.",
            "No repository-wide pytest is run in R3-1.",
        ]
    )
    path.write_text(
        "\n".join(lines) + "\n",
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
        "--output-dir",
        type=Path,
        default=Path("phase155_r3_1_audit_output"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root / args.output_dir
    )
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = scan_tests(
        repo_root
    )
    pairs = build_pair_candidates(
        records
    )

    write_csv(
        output_dir / "phase155_r3_1_test_inventory.csv",
        records,
    )
    write_csv(
        output_dir / "phase155_r3_1_candidate_pairs.csv",
        pairs,
    )
    write_summary(
        output_dir / "phase155_r3_1_summary.md",
        repo_root,
        records,
        pairs,
    )

    metadata = {
        "phase": "155-R3-1",
        "git_head": _git_head(repo_root),
        "source_level_test_functions": len(records),
        "candidate_pairs": len(pairs),
        "pair_category_counts": dict(
            Counter(pair.category for pair in pairs)
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }
    (
        output_dir
        / "phase155_r3_1_metadata.json"
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
        "Phase 155-R3-1 duplicate / superseded candidate audit completed."
    )
    print(
        "source-level test functions:",
        len(records),
    )
    counts = Counter(
        pair.category
        for pair in pairs
    )
    print(
        "exact duplicate candidate pairs:",
        counts[CATEGORY_EXACT],
    )
    print(
        "semantic duplicate candidate pairs:",
        counts[CATEGORY_SEMANTIC],
    )
    print(
        "superseded candidate pairs:",
        counts[CATEGORY_SUPERSEDED],
    )
    print(
        "candidate pairs total:",
        len(pairs),
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
