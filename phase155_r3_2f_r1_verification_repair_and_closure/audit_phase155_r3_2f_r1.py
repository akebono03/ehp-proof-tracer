from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import os
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pytest


DECISION_REMOVABLE = "removable_duplicate"
DECISION_RETAIN = "retain_independent"
DECISION_HISTORICAL = "historical_keep"
DECISION_REVIEW = "needs_review"

CATEGORY_EXACT = "exact_duplicate_candidate"
CATEGORY_SEMANTIC = "semantic_duplicate_candidate"
CATEGORY_SUPERSEDED = "superseded_candidate"

HISTORICAL_TOKENS = (
    "legacy",
    "historical",
    "compatibility",
    "backward",
)


@dataclass(frozen=True)
class RuntimeAggregate:
    requested_test_id: str
    collected_count: int
    call_count: int
    passed_count: int
    failed_count: int
    skipped_count: int
    setup_teardown_failure_count: int
    runtime_status: str


@dataclass(frozen=True)
class SourceEvidence:
    test_id: str
    function_hash: str
    semantic_function_hash: str
    dependency_hash: str
    source_available: bool


@dataclass(frozen=True)
class ClosurePair:
    candidate_id: str
    category: str
    older_test_id: str
    newer_test_id: str
    older_runtime_status: str
    newer_runtime_status: str
    function_hash_equal: bool
    semantic_function_hash_equal: bool
    dependency_hash_equal: bool
    decision: str
    deletion_authorized: bool
    reason: str


class Recorder:
    def __init__(
        self,
    ) -> None:
        self.collected: list[str] = []
        self.reports: list[tuple[str, str, str]] = []

    @pytest.hookimpl
    def pytest_collection_modifyitems(
        self,
        session,
        config,
        items,
    ) -> None:
        self.collected = [
            item.nodeid.replace(
                "\\",
                "/",
            )
            for item in items
        ]

    @pytest.hookimpl
    def pytest_runtest_logreport(
        self,
        report,
    ) -> None:
        self.reports.append(
            (
                report.nodeid.replace(
                    "\\",
                    "/",
                ),
                report.when,
                report.outcome,
            )
        )


class _RenameFunction(
    ast.NodeTransformer
):
    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ):
        node = self.generic_visit(
            node
        )
        node.name = "__test__"
        node.decorator_list = []
        return node

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ):
        node = self.generic_visit(
            node
        )
        node.name = "__test__"
        node.decorator_list = []
        return node


class _SemanticStrings(
    ast.NodeTransformer
):
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
                        .replace(
                            "、",
                            ", ",
                        )
                        .replace(
                            "。",
                            ".",
                        )
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
        return list(
            csv.DictReader(
                handle
            )
        )


def _write_csv(
    path: Path,
    rows: Iterable[object],
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


def normalize_nodeid(
    nodeid: str,
) -> str:
    normalized = (
        nodeid
        .replace(
            "\\",
            "/",
        )
        .strip()
    )
    parts = normalized.split(
        "::"
    )

    if len(
        parts
    ) < 2:
        return normalized

    parts[-1] = re.sub(
        r"\[.*\]$",
        "",
        parts[-1],
    )

    return "::".join(
        parts
    )


def _unique_test_ids(
    candidate_rows: list[dict[str, str]],
) -> tuple[str, ...]:
    ordered = {}

    for row in candidate_rows:
        ordered[
            normalize_nodeid(
                row[
                    "older_test_id"
                ]
            )
        ] = None
        ordered[
            normalize_nodeid(
                row[
                    "newer_test_id"
                ]
            )
        ] = None

    return tuple(
        ordered
    )


def _fresh_execute(
    repo_root: Path,
    test_ids: tuple[str, ...],
) -> tuple[Recorder, int]:
    recorder = Recorder()
    previous = Path.cwd()

    try:
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
        recorder,
        int(
            exit_code
        ),
    )


def aggregate_runtime(
    requested_test_ids: tuple[str, ...],
    recorder: Recorder,
) -> list[RuntimeAggregate]:
    collected_by_base = {}
    reports_by_base = {}

    for nodeid in recorder.collected:
        collected_by_base.setdefault(
            normalize_nodeid(
                nodeid
            ),
            [],
        ).append(
            nodeid
        )

    for (
        nodeid,
        phase,
        outcome,
    ) in recorder.reports:
        reports_by_base.setdefault(
            normalize_nodeid(
                nodeid
            ),
            [],
        ).append(
            (
                nodeid,
                phase,
                outcome,
            )
        )

    result = []

    for requested in requested_test_ids:
        collected = (
            collected_by_base.get(
                requested,
                [],
            )
        )
        reports = (
            reports_by_base.get(
                requested,
                [],
            )
        )
        calls = [
            report
            for report in reports
            if report[
                1
            ]
            == "call"
        ]
        passed = sum(
            report[
                2
            ]
            == "passed"
            for report in calls
        )
        failed = sum(
            report[
                2
            ]
            == "failed"
            for report in calls
        )
        skipped = sum(
            report[
                2
            ]
            == "skipped"
            for report in calls
        )
        setup_teardown_failed = sum(
            phase
            in (
                "setup",
                "teardown",
            )
            and outcome
            == "failed"
            for (
                _nodeid,
                phase,
                outcome,
            )
            in reports
        )

        if not collected:
            status = (
                "not_collected"
            )
        elif setup_teardown_failed:
            status = (
                "setup_teardown_failed"
            )
        elif failed:
            status = "failed"
        elif (
            calls
            and passed
            == len(
                calls
            )
        ):
            status = "passed"
        elif not calls:
            status = (
                "no_call_report"
            )
        else:
            status = "non_pass"

        result.append(
            RuntimeAggregate(
                requested_test_id=(
                    requested
                ),
                collected_count=len(
                    collected
                ),
                call_count=len(
                    calls
                ),
                passed_count=passed,
                failed_count=failed,
                skipped_count=skipped,
                setup_teardown_failure_count=(
                    setup_teardown_failed
                ),
                runtime_status=status,
            )
        )

    return result


def _split_test_id(
    test_id: str,
) -> tuple[str, str]:
    file_name, function_name = (
        normalize_nodeid(
            test_id
        ).split(
            "::",
            1,
        )
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
    copied = parsed.body[
        0
    ]
    copied = (
        _RenameFunction()
        .visit(
            copied
        )
    )

    if semantic:
        copied = (
            _SemanticStrings()
            .visit(
                copied
            )
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
    result = {}

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
            ast.Import,
        ):
            for alias in node.names:
                result[
                    alias.asname
                    or alias.name.split(
                        ".",
                        1,
                    )[
                        0
                    ]
                ] = node

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            for alias in node.names:
                result[
                    alias.asname
                    or alias.name
                ] = node

        elif isinstance(
            node,
            ast.Assign,
        ):
            for target in node.targets:
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
        ) and isinstance(
            node.target,
            ast.Name,
        ):
            result[
                node.target.id
            ] = node

    return result


def _dependency_hash(
    tree: ast.Module,
    function: ast.AST,
) -> str:
    symbols = _defined_symbols(
        tree
    )
    loaded_names = sorted(
        {
            node.id
            for node in ast.walk(
                function
            )
            if (
                isinstance(
                    node,
                    ast.Name,
                )
                and isinstance(
                    node.ctx,
                    ast.Load,
                )
                and node.id
                in symbols
            )
        }
    )

    payload = "\n".join(
        name
        + ":"
        + ast.dump(
            symbols[
                name
            ],
            annotate_fields=True,
            include_attributes=False,
        )
        for name in loaded_names
    )

    return hashlib.sha256(
        payload.encode(
            "utf-8"
        )
    ).hexdigest()


def source_evidence(
    repo_root: Path,
    test_id: str,
) -> SourceEvidence:
    file_name, function_name = (
        _split_test_id(
            test_id
        )
    )
    path = (
        repo_root
        / file_name
    )

    if not path.exists():
        return SourceEvidence(
            test_id=(
                normalize_nodeid(
                    test_id
                )
            ),
            function_hash="",
            semantic_function_hash="",
            dependency_hash="",
            source_available=False,
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
    ):
        return SourceEvidence(
            test_id=(
                normalize_nodeid(
                    test_id
                )
            ),
            function_hash="",
            semantic_function_hash="",
            dependency_hash="",
            source_available=False,
        )

    function = _find_function(
        tree,
        function_name,
    )

    if function is None:
        return SourceEvidence(
            test_id=(
                normalize_nodeid(
                    test_id
                )
            ),
            function_hash="",
            semantic_function_hash="",
            dependency_hash="",
            source_available=False,
        )

    return SourceEvidence(
        test_id=(
            normalize_nodeid(
                test_id
            )
        ),
        function_hash=(
            _normalized_hash(
                function,
                semantic=False,
            )
        ),
        semantic_function_hash=(
            _normalized_hash(
                function,
                semantic=True,
            )
        ),
        dependency_hash=(
            _dependency_hash(
                tree,
                function,
            )
        ),
        source_available=True,
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


def _atoms(
    value: str,
) -> set[str]:
    return set(
        filter(
            None,
            value.split(
                "\x1f"
            ),
        )
    )


def classify_pairs(
    candidate_rows: list[
        dict[
            str,
            str,
        ]
    ],
    runtime_rows: list[
        RuntimeAggregate
    ],
    source_rows: list[
        SourceEvidence
    ],
) -> list[
    ClosurePair
]:
    runtime_by_test = {
        row.requested_test_id: row
        for row in runtime_rows
    }
    source_by_test = {
        row.test_id: row
        for row in source_rows
    }

    result = []

    for candidate in candidate_rows:
        candidate_id = (
            candidate[
                "candidate_id"
            ]
        )
        category = candidate[
            "category"
        ]
        older = normalize_nodeid(
            candidate[
                "older_test_id"
            ]
        )
        newer = normalize_nodeid(
            candidate[
                "newer_test_id"
            ]
        )

        older_runtime = (
            runtime_by_test.get(
                older
            )
        )
        newer_runtime = (
            runtime_by_test.get(
                newer
            )
        )
        older_status = (
            older_runtime.runtime_status
            if older_runtime
            else "missing_runtime"
        )
        newer_status = (
            newer_runtime.runtime_status
            if newer_runtime
            else "missing_runtime"
        )

        older_source = (
            source_by_test.get(
                older
            )
        )
        newer_source = (
            source_by_test.get(
                newer
            )
        )

        source_available = (
            older_source
            is not None
            and newer_source
            is not None
            and older_source.source_available
            and newer_source.source_available
        )

        function_equal = (
            source_available
            and older_source.function_hash
            == newer_source.function_hash
        )
        semantic_equal = (
            source_available
            and older_source.semantic_function_hash
            == newer_source.semantic_function_hash
        )
        dependency_equal = (
            source_available
            and older_source.dependency_hash
            == newer_source.dependency_hash
        )

        historical = (
            _historical(
                older
            )
            or _historical(
                newer
            )
        )

        if historical:
            decision = (
                DECISION_HISTORICAL
            )
            authorized = False
            reason = (
                "Historical/compatibility intent is retained."
            )

        elif (
            older_status
            != "passed"
            or newer_status
            != "passed"
        ):
            decision = (
                DECISION_REVIEW
            )
            authorized = False
            reason = (
                "Both candidate tests must pass after parameterized aggregation."
            )

        elif not source_available:
            decision = (
                DECISION_REVIEW
            )
            authorized = False
            reason = (
                "Current source evidence is incomplete."
            )

        elif (
            category
            == CATEGORY_EXACT
        ):
            if (
                function_equal
                and dependency_equal
            ):
                decision = (
                    DECISION_REMOVABLE
                )
                authorized = True
                reason = (
                    "Current exact body and dependency fingerprints match."
                )
            else:
                decision = (
                    DECISION_RETAIN
                )
                authorized = False
                reason = (
                    "Current exact replacement is not proven."
                )

        elif (
            category
            == CATEGORY_SEMANTIC
        ):
            if (
                semantic_equal
                and dependency_equal
            ):
                decision = (
                    DECISION_REMOVABLE
                )
                authorized = True
                reason = (
                    "Current semantic body and dependency fingerprints match."
                )
            else:
                decision = (
                    DECISION_RETAIN
                )
                authorized = False
                reason = (
                    "Current semantic replacement is not proven."
                )

        elif (
            category
            == CATEGORY_SUPERSEDED
        ):
            older_atoms = _atoms(
                candidate.get(
                    "older_semantic_atoms",
                    "",
                )
            )
            newer_atoms = _atoms(
                candidate.get(
                    "newer_semantic_atoms",
                    "",
                )
            )

            if (
                older_atoms
                and older_atoms.issubset(
                    newer_atoms
                )
                and dependency_equal
            ):
                decision = (
                    DECISION_REMOVABLE
                )
                authorized = True
                reason = (
                    "Current runtime passes and newer assertion contract contains the older contract under the same dependency fingerprint."
                )
            else:
                decision = (
                    DECISION_RETAIN
                )
                authorized = False
                reason = (
                    "Current full supersession is not proven."
                )

        else:
            decision = (
                DECISION_REVIEW
            )
            authorized = False
            reason = (
                "Unknown candidate category."
            )

        result.append(
            ClosurePair(
                candidate_id=candidate_id,
                category=category,
                older_test_id=older,
                newer_test_id=newer,
                older_runtime_status=(
                    older_status
                ),
                newer_runtime_status=(
                    newer_status
                ),
                function_hash_equal=(
                    bool(
                        function_equal
                    )
                ),
                semantic_function_hash_equal=(
                    bool(
                        semantic_equal
                    )
                ),
                dependency_hash_equal=(
                    bool(
                        dependency_equal
                    )
                ),
                decision=decision,
                deletion_authorized=(
                    authorized
                ),
                reason=reason,
            )
        )

    return result


def write_summary(
    path: Path,
    repo_root: Path,
    runtime_rows: list[
        RuntimeAggregate
    ],
    closure_rows: list[
        ClosurePair
    ],
    pytest_exit_code: int,
) -> None:
    runtime_counts = Counter(
        row.runtime_status
        for row in runtime_rows
    )
    decisions = Counter(
        row.decision
        for row in closure_rows
    )

    closure_ok = (
        pytest_exit_code
        == 0
        and runtime_counts.get(
            "passed",
            0,
        )
        == len(
            runtime_rows
        )
        and decisions[
            DECISION_REVIEW
        ]
        == 0
    )

    lines = [
        "# Phase 155-R3-2F-r1 — verification repair and closure",
        "",
        "## Changes",
        "",
        "- Production code changes: none",
        "- Existing test files changed: 2",
        "- Existing test functions changed: 2",
        "- `ast` import added to those two test files",
        "- Hardcoding guard now inspects control-flow conditions instead of banning legitimate statement-field names across the whole module",
        "- Parameterized pytest node IDs are aggregated by normalized base node ID",
        "- Source fingerprints are recomputed from the current post-repair test files",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Fresh focused pytest exit code: {pytest_exit_code}",
        f"- Unique candidate base tests: {len(runtime_rows)}",
        f"- Candidate pairs: {len(closure_rows)}",
        "",
        "## Runtime status",
        "",
        "| status | base tests |",
        "| --- | ---: |",
    ]

    for status in sorted(
        runtime_counts
    ):
        lines.append(
            f"| `{status}` | {runtime_counts[status]} |"
        )

    lines.extend(
        [
            "",
            "## Final pair decisions",
            "",
            "| decision | pairs |",
            "| --- | ---: |",
        ]
    )

    for decision in (
        DECISION_REMOVABLE,
        DECISION_RETAIN,
        DECISION_HISTORICAL,
        DECISION_REVIEW,
    ):
        lines.append(
            f"| `{decision}` | {decisions[decision]} |"
        )

    lines.extend(
        [
            "",
            "## Closure",
            "",
            f"- R3-2 closure condition satisfied: `{str(closure_ok).lower()}`",
            "- Duplicate tests deleted in R3-2F-r1: 0",
            "- Repository-wide pytest remains deferred until Phase 155 closure.",
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
            "phase155_r3_2f_r1_audit_output"
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
            "R3-1 candidate pairs not found: "
            + str(
                candidate_path
            )
        )

    candidate_rows = _read_csv(
        candidate_path
    )
    test_ids = _unique_test_ids(
        candidate_rows
    )

    recorder, pytest_exit_code = (
        _fresh_execute(
            repo_root,
            test_ids,
        )
    )
    runtime_rows = aggregate_runtime(
        test_ids,
        recorder,
    )
    source_rows = [
        source_evidence(
            repo_root,
            test_id,
        )
        for test_id in test_ids
    ]
    closure_rows = classify_pairs(
        candidate_rows,
        runtime_rows,
        source_rows,
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
        / "phase155_r3_2f_r1_runtime_aggregate.csv",
        runtime_rows,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2f_r1_source_evidence.csv",
        source_rows,
    )
    _write_csv(
        output_dir
        / "phase155_r3_2f_r1_verified_pairs.csv",
        closure_rows,
    )

    write_summary(
        output_dir
        / "phase155_r3_2f_r1_summary.md",
        repo_root,
        runtime_rows,
        closure_rows,
        pytest_exit_code,
    )

    runtime_counts = Counter(
        row.runtime_status
        for row in runtime_rows
    )
    decision_counts = Counter(
        row.decision
        for row in closure_rows
    )

    closure_ok = (
        pytest_exit_code
        == 0
        and runtime_counts.get(
            "passed",
            0,
        )
        == len(
            runtime_rows
        )
        and decision_counts[
            DECISION_REVIEW
        ]
        == 0
    )

    metadata = {
        "phase": "155-R3-2F-r1",
        "git_head": _git_head(
            repo_root
        ),
        "unique_candidate_base_tests": len(
            runtime_rows
        ),
        "candidate_pairs": len(
            closure_rows
        ),
        "focused_pytest_exit_code": (
            pytest_exit_code
        ),
        "runtime_status_counts": dict(
            runtime_counts
        ),
        "decision_counts": dict(
            decision_counts
        ),
        "closure_condition_satisfied": (
            closure_ok
        ),
        "production_code_modified": False,
        "existing_test_files_modified": 2,
        "existing_test_functions_modified": 2,
        "tests_deleted": 0,
        "repository_wide_pytest_executed": False,
    }

    (
        output_dir
        / "phase155_r3_2f_r1_metadata.json"
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
        "Phase 155-R3-2F-r1 verification completed."
    )
    print(
        "unique candidate base tests:",
        len(
            runtime_rows
        ),
    )
    print(
        "passed base tests:",
        runtime_counts[
            "passed"
        ],
    )
    print(
        "non-passing base tests:",
        len(
            runtime_rows
        )
        - runtime_counts[
            "passed"
        ],
    )
    print(
        "candidate pairs:",
        len(
            closure_rows
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
        pytest_exit_code,
    )
    print(
        "R3-2 closure condition satisfied:",
        closure_ok,
    )
    print(
        "output:",
        output_dir,
    )

    if not closure_ok:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
