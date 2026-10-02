from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pytest


CATEGORY_EXACT = "exact_duplicate_candidate"
CATEGORY_SEMANTIC = "semantic_duplicate_candidate"
CATEGORY_SUPERSEDED = "superseded_candidate"

DECISION_REMOVABLE = "removable_duplicate"
DECISION_RETAIN = "retain_independent"
DECISION_HISTORICAL = "historical_keep"
DECISION_REVIEW = "needs_review"

HISTORICAL_TOKENS = (
    "legacy",
    "historical",
    "compatibility",
    "backward",
)


@dataclass(frozen=True)
class CandidatePair:
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
    deletion_authorized: str


@dataclass(frozen=True)
class TestExecution:
    test_id: str
    outcome: str
    duration_seconds: float
    longrepr: str


@dataclass(frozen=True)
class SourceEvidence:
    test_id: str
    file: str
    function: str
    function_hash: str
    semantic_function_hash: str
    dependency_hash: str
    dependency_symbols: str
    source_available: bool
    source_error: str


@dataclass(frozen=True)
class VerifiedPair:
    candidate_id: str
    candidate_category: str
    older_test_id: str
    newer_test_id: str
    older_outcome: str
    newer_outcome: str
    function_hash_equal: bool
    semantic_function_hash_equal: bool
    dependency_hash_equal: bool
    older_dependency_symbols: str
    newer_dependency_symbols: str
    decision: str
    decision_reason: str
    deletion_authorized: bool


class ResultRecorder:
    def __init__(self) -> None:
        self.records: dict[str, TestExecution] = {}
        self.collection_errors: list[str] = []

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report) -> None:
        if report.when != "call":
            return
        longrepr = ""
        if report.failed:
            longrepr = str(report.longrepr)
        self.records[report.nodeid] = TestExecution(
            test_id=report.nodeid,
            outcome=report.outcome,
            duration_seconds=float(report.duration),
            longrepr=longrepr[:4000],
        )

    @pytest.hookimpl
    def pytest_collectreport(self, report) -> None:
        if report.failed:
            self.collection_errors.append(
                str(report.longrepr)[:4000]
            )


class _RenameFunction(ast.NodeTransformer):
    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ):
        node = self.generic_visit(node)
        node.name = "__test__"
        node.decorator_list = []
        return node

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ):
        node = self.generic_visit(node)
        node.name = "__test__"
        node.decorator_list = []
        return node


class _SemanticStrings(ast.NodeTransformer):
    def visit_Constant(
        self,
        node: ast.Constant,
    ):
        if isinstance(
            node.value,
            str,
        ):
            return ast.copy_location(
                ast.Constant(
                    value=(
                        node.value
                        .replace("、", ", ")
                        .replace("。", ".")
                    )
                ),
                node,
            )
        return node


def _git_head(
    repo_root: Path,
) -> str:
    try:
        completed = subprocess.run(
            [
                "git",
                "rev-parse",
                "HEAD",
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return (
            completed.stdout.strip()
        )
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
        return list(
            csv.DictReader(
                handle
            )
        )


def load_candidate_pairs(
    path: Path,
) -> list[CandidatePair]:
    result = []

    for row in _read_csv(
        path
    ):
        result.append(
            CandidatePair(
                candidate_id=row[
                    "candidate_id"
                ],
                category=row[
                    "category"
                ],
                older_test_id=row[
                    "older_test_id"
                ],
                newer_test_id=row[
                    "newer_test_id"
                ],
                older_phase=row[
                    "older_phase"
                ],
                newer_phase=row[
                    "newer_phase"
                ],
                shared_call_surface=row[
                    "shared_call_surface"
                ],
                older_semantic_atoms=row[
                    "older_semantic_atoms"
                ],
                newer_semantic_atoms=row[
                    "newer_semantic_atoms"
                ],
                evidence=row[
                    "evidence"
                ],
                deletion_authorized=row[
                    "deletion_authorized"
                ],
            )
        )

    return result


def unique_test_ids(
    pairs: Iterable[
        CandidatePair
    ],
) -> tuple[str, ...]:
    ordered: dict[
        str,
        None,
    ] = {}

    for pair in pairs:
        ordered[
            pair.older_test_id
        ] = None
        ordered[
            pair.newer_test_id
        ] = None

    return tuple(
        ordered
    )


def _split_nodeid(
    test_id: str,
) -> tuple[str, str]:
    file_name, function_name = (
        test_id.split(
            "::",
            1,
        )
    )

    function_name = (
        function_name.split(
            "[",
            1,
        )[0]
    )

    return (
        file_name,
        function_name,
    )


def _find_function(
    tree: ast.Module,
    function_name: str,
) -> ast.AST | None:
    for node in tree.body:
        if (
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
            and node.name
            == function_name
        ):
            return node

        if isinstance(
            node,
            ast.ClassDef,
        ):
            for child in node.body:
                if (
                    isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    )
                    and child.name
                    == function_name
                ):
                    return child

    return None


def _normalized_hash(
    node: ast.AST,
    *,
    semantic: bool,
) -> str:
    parsed = ast.parse(
        ast.unparse(
            node
        )
    )
    copied = parsed.body[0]

    copied = _RenameFunction().visit(
        copied
    )

    if semantic:
        copied = _SemanticStrings().visit(
            copied
        )

    copied = ast.fix_missing_locations(
        copied
    )

    payload = ast.dump(
        copied,
        annotate_fields=True,
        include_attributes=False,
    )

    return hashlib.sha256(
        payload.encode(
            "utf-8"
        )
    ).hexdigest()


def _defined_symbols(
    tree: ast.Module,
) -> dict[str, ast.AST]:
    result: dict[
        str,
        ast.AST,
    ] = {}

    for node in tree.body:
        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef,
            ),
        ):
            result[
                node.name
            ] = node

        elif isinstance(
            node,
            ast.Assign,
        ):
            for target in (
                node.targets
            ):
                if isinstance(
                    target,
                    ast.Name,
                ):
                    result[
                        target.id
                    ] = node

        elif isinstance(
            node,
            ast.AnnAssign,
        ):
            if isinstance(
                node.target,
                ast.Name,
            ):
                result[
                    node.target.id
                ] = node

        elif isinstance(
            node,
            ast.Import,
        ):
            for alias in node.names:
                name = (
                    alias.asname
                    or alias.name.split(
                        ".",
                        1,
                    )[0]
                )
                result[
                    name
                ] = node

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            for alias in node.names:
                name = (
                    alias.asname
                    or alias.name
                )
                result[
                    name
                ] = node

    return result


def _loaded_names(
    node: ast.AST,
) -> set[str]:
    return {
        child.id
        for child in ast.walk(
            node
        )
        if (
            isinstance(
                child,
                ast.Name,
            )
            and isinstance(
                child.ctx,
                ast.Load,
            )
        )
    }


def _dependency_signature(
    tree: ast.Module,
    function: ast.AST,
) -> tuple[
    str,
    tuple[str, ...],
]:
    symbols = _defined_symbols(
        tree
    )
    directly_used = sorted(
        name
        for name in _loaded_names(
            function
        )
        if name in symbols
    )

    components = []

    for name in directly_used:
        definition = symbols[
            name
        ]
        components.append(
            name
            + ":"
            + ast.dump(
                definition,
                annotate_fields=True,
                include_attributes=False,
            )
        )

    payload = "\n".join(
        components
    )

    return (
        hashlib.sha256(
            payload.encode(
                "utf-8"
            )
        ).hexdigest(),
        tuple(
            directly_used
        ),
    )


def source_evidence(
    repo_root: Path,
    test_id: str,
) -> SourceEvidence:
    file_name, function_name = (
        _split_nodeid(
            test_id
        )
    )
    path = (
        repo_root
        / file_name
    )

    if not path.exists():
        return SourceEvidence(
            test_id=test_id,
            file=file_name,
            function=function_name,
            function_hash="",
            semantic_function_hash="",
            dependency_hash="",
            dependency_symbols="",
            source_available=False,
            source_error=(
                "test file not found"
            ),
        )

    try:
        source = path.read_text(
            encoding="utf-8-sig",
        )
        tree = ast.parse(
            source
        )
    except (
        OSError,
        SyntaxError,
    ) as exc:
        return SourceEvidence(
            test_id=test_id,
            file=file_name,
            function=function_name,
            function_hash="",
            semantic_function_hash="",
            dependency_hash="",
            dependency_symbols="",
            source_available=False,
            source_error=str(
                exc
            ),
        )

    function = _find_function(
        tree,
        function_name,
    )

    if function is None:
        return SourceEvidence(
            test_id=test_id,
            file=file_name,
            function=function_name,
            function_hash="",
            semantic_function_hash="",
            dependency_hash="",
            dependency_symbols="",
            source_available=False,
            source_error=(
                "test function not found"
            ),
        )

    dependency_hash, symbols = (
        _dependency_signature(
            tree,
            function,
        )
    )

    return SourceEvidence(
        test_id=test_id,
        file=file_name,
        function=function_name,
        function_hash=_normalized_hash(
            function,
            semantic=False,
        ),
        semantic_function_hash=(
            _normalized_hash(
                function,
                semantic=True,
            )
        ),
        dependency_hash=(
            dependency_hash
        ),
        dependency_symbols=(
            "\x1f".join(
                symbols
            )
        ),
        source_available=True,
        source_error="",
    )


def execute_candidates(
    repo_root: Path,
    test_ids: tuple[
        str,
        ...,
    ],
) -> tuple[
    dict[
        str,
        TestExecution,
    ],
    list[str],
    int,
]:
    recorder = ResultRecorder()

    previous = Path.cwd()

    try:
        import os

        os.chdir(
            repo_root
        )

        exit_code = pytest.main(
            [
                *test_ids,
                "-q",
                "--tb=short",
                "-p",
                "no:cacheprovider",
            ],
            plugins=[
                recorder
            ],
        )
    finally:
        os.chdir(
            previous
        )

    return (
        recorder.records,
        recorder.collection_errors,
        int(
            exit_code
        ),
    )


def _historical(
    test_id: str,
) -> bool:
    lowered = (
        test_id.lower()
    )

    return any(
        token in lowered
        for token
        in HISTORICAL_TOKENS
    )


def classify_pair(
    pair: CandidatePair,
    older_execution: TestExecution | None,
    newer_execution: TestExecution | None,
    older_source: SourceEvidence,
    newer_source: SourceEvidence,
) -> tuple[
    str,
    str,
    bool,
]:
    if (
        _historical(
            pair.older_test_id
        )
        or _historical(
            pair.newer_test_id
        )
    ):
        return (
            DECISION_HISTORICAL,
            (
                "At least one test explicitly identifies "
                "legacy/historical/compatibility intent."
            ),
            False,
        )

    if (
        older_execution is None
        or newer_execution is None
    ):
        return (
            DECISION_REVIEW,
            (
                "One or both candidate tests produced no "
                "call-phase pytest result."
            ),
            False,
        )

    if (
        older_execution.outcome
        != "passed"
        or newer_execution.outcome
        != "passed"
    ):
        return (
            DECISION_REVIEW,
            (
                "Both tests must pass current behavior "
                "before redundancy can be established."
            ),
            False,
        )

    if (
        not older_source.source_available
        or not newer_source.source_available
    ):
        return (
            DECISION_REVIEW,
            (
                "Source evidence is incomplete."
            ),
            False,
        )

    exact_equal = (
        older_source.function_hash
        == newer_source.function_hash
    )
    semantic_equal = (
        older_source.semantic_function_hash
        == newer_source.semantic_function_hash
    )
    dependencies_equal = (
        older_source.dependency_hash
        == newer_source.dependency_hash
    )

    if (
        pair.category
        == CATEGORY_EXACT
    ):
        if (
            exact_equal
            and dependencies_equal
        ):
            return (
                DECISION_REMOVABLE,
                (
                    "Both tests pass; normalized test bodies "
                    "and their directly referenced module-level "
                    "dependencies are identical."
                ),
                True,
            )

        return (
            DECISION_RETAIN,
            (
                "The R3-1 exact-body candidate has different "
                "direct dependency context, so independent "
                "coverage is retained."
            ),
            False,
        )

    if (
        pair.category
        == CATEGORY_SEMANTIC
    ):
        if (
            semantic_equal
            and dependencies_equal
        ):
            return (
                DECISION_REMOVABLE,
                (
                    "Both tests pass; semantic test bodies and "
                    "direct dependency context are identical "
                    "after punctuation normalization."
                ),
                True,
            )

        return (
            DECISION_RETAIN,
            (
                "Semantic similarity is not accompanied by "
                "identical direct dependency context."
            ),
            False,
        )

    if (
        pair.category
        == CATEGORY_SUPERSEDED
    ):
        older_atoms = set(
            filter(
                None,
                pair.older_semantic_atoms.split(
                    "\x1f"
                ),
            )
        )
        newer_atoms = set(
            filter(
                None,
                pair.newer_semantic_atoms.split(
                    "\x1f"
                ),
            )
        )

        if (
            older_atoms
            and older_atoms.issubset(
                newer_atoms
            )
            and dependencies_equal
        ):
            return (
                DECISION_REMOVABLE,
                (
                    "Both tests pass; the later test contains "
                    "the older semantic assertion contract and "
                    "uses identical direct dependency context."
                ),
                True,
            )

        return (
            DECISION_RETAIN,
            (
                "The later test does not prove full replacement "
                "under identical dependency context."
            ),
            False,
        )

    return (
        DECISION_REVIEW,
        (
            "Unknown candidate category."
        ),
        False,
    )


def verify_pairs(
    repo_root: Path,
    pairs: list[
        CandidatePair
    ],
) -> tuple[
    list[VerifiedPair],
    list[SourceEvidence],
    list[TestExecution],
    list[str],
    int,
]:
    test_ids = unique_test_ids(
        pairs
    )

    executions_by_id, collection_errors, exit_code = (
        execute_candidates(
            repo_root,
            test_ids,
        )
    )

    source_by_id = {
        test_id: source_evidence(
            repo_root,
            test_id,
        )
        for test_id in test_ids
    }

    executions = []

    for test_id in test_ids:
        execution = (
            executions_by_id.get(
                test_id
            )
        )

        if execution is None:
            execution = (
                TestExecution(
                    test_id=test_id,
                    outcome="missing",
                    duration_seconds=0.0,
                    longrepr=(
                        "No call-phase result recorded."
                    ),
                )
            )

        executions.append(
            execution
        )

    verified = []

    for pair in pairs:
        older_execution = (
            executions_by_id.get(
                pair.older_test_id
            )
        )
        newer_execution = (
            executions_by_id.get(
                pair.newer_test_id
            )
        )
        older_source = (
            source_by_id[
                pair.older_test_id
            ]
        )
        newer_source = (
            source_by_id[
                pair.newer_test_id
            ]
        )

        (
            decision,
            reason,
            deletion_authorized,
        ) = classify_pair(
            pair,
            older_execution,
            newer_execution,
            older_source,
            newer_source,
        )

        verified.append(
            VerifiedPair(
                candidate_id=(
                    pair.candidate_id
                ),
                candidate_category=(
                    pair.category
                ),
                older_test_id=(
                    pair.older_test_id
                ),
                newer_test_id=(
                    pair.newer_test_id
                ),
                older_outcome=(
                    older_execution.outcome
                    if older_execution
                    else "missing"
                ),
                newer_outcome=(
                    newer_execution.outcome
                    if newer_execution
                    else "missing"
                ),
                function_hash_equal=(
                    older_source.function_hash
                    == newer_source.function_hash
                ),
                semantic_function_hash_equal=(
                    older_source.semantic_function_hash
                    == newer_source.semantic_function_hash
                ),
                dependency_hash_equal=(
                    older_source.dependency_hash
                    == newer_source.dependency_hash
                ),
                older_dependency_symbols=(
                    older_source.dependency_symbols
                ),
                newer_dependency_symbols=(
                    newer_source.dependency_symbols
                ),
                decision=decision,
                decision_reason=reason,
                deletion_authorized=(
                    deletion_authorized
                ),
            )
        )

    return (
        verified,
        list(
            source_by_id.values()
        ),
        executions,
        collection_errors,
        exit_code,
    )


def _write_csv(
    path: Path,
    rows: Iterable[
        object
    ],
) -> None:
    rows = list(
        rows
    )

    if not rows:
        path.write_text(
            "",
            encoding="utf-8",
        )
        return

    fieldnames = list(
        asdict(
            rows[0]
        ).keys()
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
                asdict(
                    row
                )
            )


def write_summary(
    path: Path,
    repo_root: Path,
    pairs: list[
        CandidatePair
    ],
    verified: list[
        VerifiedPair
    ],
    executions: list[
        TestExecution
    ],
    collection_errors: list[
        str
    ],
    exit_code: int,
) -> None:
    decision_counts = Counter(
        row.decision
        for row
        in verified
    )

    category_decisions: dict[
        str,
        Counter[str],
    ] = {}

    for row in verified:
        category_decisions.setdefault(
            row.candidate_category,
            Counter(),
        )[
            row.decision
        ] += 1

    outcome_counts = Counter(
        row.outcome
        for row
        in executions
    )

    lines = [
        "# Phase 155-R3-2 — candidate coverage verification",
        "",
        "## Boundary",
        "",
        "R3-2 verifies the R3-1 candidate pairs by focused pytest execution and source/dependency comparison.",
        "It does not delete, move, rename, or rewrite existing tests.",
        "It does not modify production code.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Candidate pairs: {len(pairs)}",
        f"- Unique candidate tests executed: {len(executions)}",
        f"- Focused pytest exit code: {exit_code}",
        f"- Collection errors: {len(collection_errors)}",
        "",
        "## Decisions",
        "",
        "| decision | pairs |",
        "| --- | ---: |",
    ]

    for decision in (
        DECISION_REMOVABLE,
        DECISION_RETAIN,
        DECISION_HISTORICAL,
        DECISION_REVIEW,
    ):
        lines.append(
            f"| `{decision}` | {decision_counts[decision]} |"
        )

    lines.extend(
        [
            "",
            "## Candidate category × decision",
            "",
            "| candidate category | removable | retain | historical | review |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )

    for category in (
        CATEGORY_EXACT,
        CATEGORY_SEMANTIC,
        CATEGORY_SUPERSEDED,
    ):
        counts = (
            category_decisions.get(
                category,
                Counter(),
            )
        )
        lines.append(
            f"| `{category}` | "
            f"{counts[DECISION_REMOVABLE]} | "
            f"{counts[DECISION_RETAIN]} | "
            f"{counts[DECISION_HISTORICAL]} | "
            f"{counts[DECISION_REVIEW]} |"
        )

    lines.extend(
        [
            "",
            "## Focused pytest outcomes",
            "",
            "| outcome | tests |",
            "| --- | ---: |",
        ]
    )

    for outcome, count in sorted(
        outcome_counts.items()
    ):
        lines.append(
            f"| `{outcome}` | {count} |"
        )

    lines.extend(
        [
            "",
            "## Verification rule",
            "",
            "- `removable_duplicate`: both tests pass current behavior and source-backed dependency context proves full duplication/replacement.",
            "- `retain_independent`: candidate similarity exists, but helper/import/constant dependency context or coverage does not prove replacement.",
            "- `historical_keep`: the test explicitly identifies legacy/historical/compatibility intent.",
            "- `needs_review`: execution or source evidence is incomplete.",
            "",
            "For exact duplicates, normalized test bodies and direct module-level dependency fingerprints must match.",
            "For superseded candidates, the newer semantic assertion contract must contain the older contract and direct dependency fingerprints must also match.",
            "",
            "## Important boundary",
            "",
            "A `removable_duplicate` decision authorizes the pair as a removal candidate for R3-3 only.",
            "R3-2 itself deletes zero tests.",
            "Repository-wide pytest remains deferred until the end of Phase 155.",
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
        "--candidate-pairs",
        type=Path,
        default=Path(
            "phase155_r3_1_audit_output/"
            "phase155_r3_1_candidate_pairs.csv"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "phase155_r3_2_audit_output"
        ),
    )

    args = parser.parse_args()

    repo_root = (
        args.repo_root.resolve()
    )

    candidate_path = (
        args.candidate_pairs
        if args.candidate_pairs.is_absolute()
        else repo_root
        / args.candidate_pairs
    )

    if not candidate_path.exists():
        raise SystemExit(
            "R3-1 candidate-pairs CSV not found: "
            + str(
                candidate_path
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

    pairs = load_candidate_pairs(
        candidate_path
    )

    (
        verified,
        sources,
        executions,
        collection_errors,
        exit_code,
    ) = verify_pairs(
        repo_root,
        pairs,
    )

    _write_csv(
        output_dir
        / "phase155_r3_2_verified_pairs.csv",
        verified,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2_source_evidence.csv",
        sources,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2_test_executions.csv",
        executions,
    )

    (
        output_dir
        / "phase155_r3_2_collection_errors.txt"
    ).write_text(
        "\n\n".join(
            collection_errors
        )
        + (
            "\n"
            if collection_errors
            else ""
        ),
        encoding="utf-8",
    )

    write_summary(
        output_dir
        / "phase155_r3_2_summary.md",
        repo_root,
        pairs,
        verified,
        executions,
        collection_errors,
        exit_code,
    )

    decision_counts = Counter(
        row.decision
        for row
        in verified
    )

    metadata = {
        "phase": "155-R3-2",
        "git_head": _git_head(
            repo_root
        ),
        "candidate_pairs": len(
            pairs
        ),
        "unique_candidate_tests": len(
            executions
        ),
        "focused_pytest_exit_code": (
            exit_code
        ),
        "collection_errors": len(
            collection_errors
        ),
        "decision_counts": dict(
            decision_counts
        ),
        "production_code_modified": False,
        "existing_tests_modified": False,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2_metadata.json"
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
        "Phase 155-R3-2 candidate coverage verification completed."
    )
    print(
        "candidate pairs:",
        len(
            pairs
        ),
    )
    print(
        "unique candidate tests executed:",
        len(
            executions
        ),
    )
    print(
        "removable duplicate pairs:",
        decision_counts[
            DECISION_REMOVABLE
        ],
    )
    print(
        "retain independent pairs:",
        decision_counts[
            DECISION_RETAIN
        ],
    )
    print(
        "historical keep pairs:",
        decision_counts[
            DECISION_HISTORICAL
        ],
    )
    print(
        "needs review pairs:",
        decision_counts[
            DECISION_REVIEW
        ],
    )
    print(
        "focused pytest exit code:",
        exit_code,
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
