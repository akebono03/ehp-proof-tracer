from __future__ import annotations

import argparse
import ast
import csv
import json
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


STATUS_HIGH = "stale_candidate_high"
STATUS_MEDIUM = "stale_candidate_medium"
STATUS_REVIEW = "contract_sensitive_review"
STATUS_COMPATIBLE = "current_compatible"

ALL_STATUSES = (
    STATUS_HIGH,
    STATUS_MEDIUM,
    STATUS_REVIEW,
    STATUS_COMPATIBLE,
)

CONTRACT_ASCII_PUNCTUATION = "ascii_prose_punctuation"
CONTRACT_NO_INTERNAL_FALLBACK = "no_internal_fallback_leakage"
CONTRACT_REASON_DEDUP = "semantic_reason_deduplication"
CONTRACT_REFERENCE_RELEVANCE = "reference_relevance_and_root_exclusion"
CONTRACT_FIXED_SNAPSHOT = "fixed_snapshot_risk"

FINAL_RESULT_SENTENCE_FRAGMENT = (
    "以上で得た群構造、生成元、および写像に関する結果を合わせると"
)

INTERNAL_FALLBACK_PATTERNS = (
    re.compile(r"[A-Z][A-Za-z0-9_]+Statement"),
    re.compile(r"(?:Scalar|Relation|Group|Map|Toda)[A-Za-z0-9_]+Statement"),
)

REFERENCE_ROOT_LABELS = (
    "Proposition 5.6",
    "Proposition 5.8",
    "Proposition 5.9",
    "Proposition 5.11",
    "Proposition 5.15",
)

CURRENT_PHASE_FLOOR = 154
PHASE_RE = re.compile(r"test_phase(?P<phase>\d+)")


@dataclass(frozen=True)
class ExpectationFinding:
    finding_id: str
    test_id: str
    file: str
    function: str
    line: int
    phase: str
    r1_category: str
    status: str
    contract: str
    assertion_kind: str
    expected_literal: str
    reason: str


@dataclass(frozen=True)
class FileSummary:
    file: str
    test_functions: int
    findings: int
    stale_candidate_high: int
    stale_candidate_medium: int
    contract_sensitive_review: int
    current_compatible: int


@dataclass(frozen=True)
class R1Row:
    test_id: str
    file: str
    function: str
    phase: str
    primary_category: str


def _phase_from_path(path: Path) -> str:
    match = PHASE_RE.search(path.name)
    return match.group("phase") if match else "core"


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


def _iter_test_functions(
    tree: ast.Module,
) -> Iterable[ast.FunctionDef | ast.AsyncFunctionDef]:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            yield node
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name.startswith("test_"):
                    yield child


def _literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _literal_string(node.left)
        right = _literal_string(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def _literal_int(node: ast.AST) -> int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    return None


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _positive_literal_membership(assertion: ast.Assert) -> list[tuple[str, int]]:
    test = assertion.test
    if isinstance(test, ast.Compare) and len(test.ops) == 1 and isinstance(test.ops[0], ast.In):
        literal = _literal_string(test.left)
        if literal is not None:
            return [(literal, assertion.lineno)]
    return []


def _negative_literal_membership(assertion: ast.Assert) -> list[tuple[str, int]]:
    test = assertion.test
    if isinstance(test, ast.Compare) and len(test.ops) == 1 and isinstance(test.ops[0], ast.NotIn):
        literal = _literal_string(test.left)
        if literal is not None:
            return [(literal, assertion.lineno)]
    return []


def _literal_equality(assertion: ast.Assert) -> list[tuple[str, int]]:
    test = assertion.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return []
    values = (test.left, test.comparators[0])
    result: list[tuple[str, int]] = []
    for value in values:
        literal = _literal_string(value)
        if literal is not None:
            result.append((literal, assertion.lineno))
    return result


def _count_expectation(assertion: ast.Assert) -> tuple[str, int, int] | None:
    test = assertion.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1:
        return None
    if not isinstance(test.ops[0], (ast.Eq, ast.LtE, ast.Lt, ast.GtE, ast.Gt)):
        return None

    left = test.left
    right = test.comparators[0]
    expected = _literal_int(right)
    if expected is None:
        expected = _literal_int(left)
        count_node = right
    else:
        count_node = left

    if expected is None or not isinstance(count_node, ast.Call):
        return None
    if _call_name(count_node.func).split(".")[-1] != "count":
        return None
    if not count_node.args:
        return None
    literal = _literal_string(count_node.args[0])
    if literal is None:
        return None
    return literal, expected, assertion.lineno


def _numeric_fixed_assertion(assertion: ast.Assert) -> tuple[int, int] | None:
    test = assertion.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return None
    left = _literal_int(test.left)
    right = _literal_int(test.comparators[0])
    if left is not None:
        return left, assertion.lineno
    if right is not None:
        return right, assertion.lineno
    return None


def _contains_japanese_prose_punctuation(text: str) -> bool:
    prose = re.sub(r"\$[^$]*\$", "MATH", text)
    if not re.search(r"[ぁ-んァ-ヶ一-龠々]", prose):
        return False
    return "、" in prose or prose.rstrip().endswith("。")


def _contains_internal_fallback(text: str) -> bool:
    return any(pattern.search(text) for pattern in INTERNAL_FALLBACK_PATTERNS)


def _looks_like_reference_positive_expectation(text: str) -> bool:
    return any(label in text for label in REFERENCE_ROOT_LABELS) and (
        "**[R" in text or "使用する結果" in text or "reference" in text.lower()
    )


def _load_r1_rows(path: Path) -> dict[str, R1Row]:
    result: dict[str, R1Row] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            item = R1Row(
                test_id=row["test_id"],
                file=row["file"],
                function=row["function"],
                phase=row["phase"],
                primary_category=row["primary_category"],
            )
            result[item.test_id] = item
    return result


def _make_finding(
    *,
    index: int,
    test_id: str,
    file: str,
    function: str,
    line: int,
    phase: str,
    r1_category: str,
    status: str,
    contract: str,
    assertion_kind: str,
    expected_literal: str,
    reason: str,
) -> ExpectationFinding:
    return ExpectationFinding(
        finding_id=f"R2-{index:05d}",
        test_id=test_id,
        file=file,
        function=function,
        line=line,
        phase=phase,
        r1_category=r1_category,
        status=status,
        contract=contract,
        assertion_kind=assertion_kind,
        expected_literal=expected_literal.replace("\r", "\\r").replace("\n", "\\n")[:500],
        reason=reason,
    )


def collect_findings(
    repo_root: Path,
    r1_rows: dict[str, R1Row],
) -> tuple[list[ExpectationFinding], list[FileSummary]]:
    tests_dir = repo_root / "tests"
    if not tests_dir.is_dir():
        raise SystemExit(f"tests directory not found: {tests_dir}")

    findings: list[ExpectationFinding] = []
    test_count_by_file: Counter[str] = Counter()
    finding_count_by_file: Counter[str] = Counter()
    status_by_file: dict[str, Counter[str]] = {}
    next_index = 1

    for path in sorted(tests_dir.glob("test_*.py")):
        relative = path.relative_to(repo_root).as_posix()
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
        phase = _phase_from_path(path)
        status_by_file.setdefault(relative, Counter())

        for function in _iter_test_functions(tree):
            test_count_by_file[relative] += 1
            test_id = f"{relative}::{function.name}"
            r1 = r1_rows.get(test_id)
            r1_category = r1.primary_category if r1 else "unclassified"
            function_had_finding = False

            for node in ast.walk(function):
                if not isinstance(node, ast.Assert):
                    continue

                for literal, line in _positive_literal_membership(node) + _literal_equality(node):
                    if _contains_japanese_prose_punctuation(literal):
                        findings.append(
                            _make_finding(
                                index=next_index,
                                test_id=test_id,
                                file=relative,
                                function=function.name,
                                line=line,
                                phase=phase,
                                r1_category=r1_category,
                                status=STATUS_HIGH,
                                contract=CONTRACT_ASCII_PUNCTUATION,
                                assertion_kind="positive_literal",
                                expected_literal=literal,
                                reason=(
                                    "Positive expected prose contains Japanese comma/full stop, "
                                    "while the Phase 154 public Narrative contract uses ASCII ', ' and '.'."
                                ),
                            )
                        )
                        next_index += 1
                        function_had_finding = True

                    if _contains_internal_fallback(literal):
                        findings.append(
                            _make_finding(
                                index=next_index,
                                test_id=test_id,
                                file=relative,
                                function=function.name,
                                line=line,
                                phase=phase,
                                r1_category=r1_category,
                                status=STATUS_HIGH,
                                contract=CONTRACT_NO_INTERNAL_FALLBACK,
                                assertion_kind="positive_literal",
                                expected_literal=literal,
                                reason=(
                                    "Positive expected public text contains an internal Statement/type token, "
                                    "which conflicts with the Phase 154 no-fallback-leakage contract."
                                ),
                            )
                        )
                        next_index += 1
                        function_had_finding = True

                    if _looks_like_reference_positive_expectation(literal) and phase.isdigit() and int(phase) < 153:
                        findings.append(
                            _make_finding(
                                index=next_index,
                                test_id=test_id,
                                file=relative,
                                function=function.name,
                                line=line,
                                phase=phase,
                                r1_category=r1_category,
                                status=STATUS_MEDIUM,
                                contract=CONTRACT_REFERENCE_RELEVANCE,
                                assertion_kind="positive_reference_literal",
                                expected_literal=literal,
                                reason=(
                                    "Pre-Phase-153 positive Reference expectation may predate used-reference filtering, "
                                    "root-reference exclusion, and Reference granularity rules. Manual confirmation required."
                                ),
                            )
                        )
                        next_index += 1
                        function_had_finding = True

                count_expectation = _count_expectation(node)
                if count_expectation is not None:
                    literal, expected, line = count_expectation
                    if FINAL_RESULT_SENTENCE_FRAGMENT in literal and expected > 1:
                        findings.append(
                            _make_finding(
                                index=next_index,
                                test_id=test_id,
                                file=relative,
                                function=function.name,
                                line=line,
                                phase=phase,
                                r1_category=r1_category,
                                status=STATUS_HIGH,
                                contract=CONTRACT_REASON_DEDUP,
                                assertion_kind="count_expectation",
                                expected_literal=f"count({literal!r}) {expected}",
                                reason=(
                                    "Expected repeated final-result reason count is greater than one, "
                                    "but Phase 154 deduplicates this public Narrative reason."
                                ),
                            )
                        )
                        next_index += 1
                        function_had_finding = True

                numeric_fixed = _numeric_fixed_assertion(node)
                if numeric_fixed is not None:
                    value, line = numeric_fixed
                    combined_name = f"{relative} {function.name}".lower()
                    if any(token in combined_name for token in ("count", "total", "snapshot", "completion", "closure", "audit")):
                        findings.append(
                            _make_finding(
                                index=next_index,
                                test_id=test_id,
                                file=relative,
                                function=function.name,
                                line=line,
                                phase=phase,
                                r1_category=r1_category,
                                status=STATUS_REVIEW,
                                contract=CONTRACT_FIXED_SNAPSHOT,
                                assertion_kind="numeric_fixed_expectation",
                                expected_literal=str(value),
                                reason=(
                                    "Fixed numeric expectation appears in an audit/count/snapshot-style test. "
                                    "It is not automatically stale, but it is contract-sensitive and should be reviewed before R3 consolidation."
                                ),
                            )
                        )
                        next_index += 1
                        function_had_finding = True

                # Negative expectations that enforce the current Phase 154 contract are recorded as compatible evidence.
                for literal, line in _negative_literal_membership(node):
                    compatible_reason: str | None = None
                    contract: str | None = None
                    if _contains_internal_fallback(literal):
                        contract = CONTRACT_NO_INTERNAL_FALLBACK
                        compatible_reason = "Negative expectation is aligned with the current no-internal-fallback contract."
                    elif _contains_japanese_prose_punctuation(literal):
                        contract = CONTRACT_ASCII_PUNCTUATION
                        compatible_reason = "Negative expectation is aligned with the current ASCII prose-punctuation contract."
                    if compatible_reason is not None and contract is not None:
                        findings.append(
                            _make_finding(
                                index=next_index,
                                test_id=test_id,
                                file=relative,
                                function=function.name,
                                line=line,
                                phase=phase,
                                r1_category=r1_category,
                                status=STATUS_COMPATIBLE,
                                contract=contract,
                                assertion_kind="negative_literal",
                                expected_literal=literal,
                                reason=compatible_reason,
                            )
                        )
                        next_index += 1
                        function_had_finding = True

            if function_had_finding:
                finding_count_by_file[relative] += 1

    for finding in findings:
        status_by_file[finding.file][finding.status] += 1

    file_summaries: list[FileSummary] = []
    for relative in sorted(test_count_by_file):
        counts = status_by_file[relative]
        file_summaries.append(
            FileSummary(
                file=relative,
                test_functions=test_count_by_file[relative],
                findings=sum(counts.values()),
                stale_candidate_high=counts[STATUS_HIGH],
                stale_candidate_medium=counts[STATUS_MEDIUM],
                contract_sensitive_review=counts[STATUS_REVIEW],
                current_compatible=counts[STATUS_COMPATIBLE],
            )
        )

    return findings, file_summaries


def _write_dataclass_csv(path: Path, rows: Iterable[object]) -> None:
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


def write_summary(
    path: Path,
    repo_root: Path,
    findings: list[ExpectationFinding],
    file_summaries: list[FileSummary],
) -> None:
    statuses = Counter(f.status for f in findings)
    contracts = Counter(f.contract for f in findings)
    high_files = sorted({f.file for f in findings if f.status == STATUS_HIGH})
    medium_files = sorted({f.file for f in findings if f.status == STATUS_MEDIUM})

    lines = [
        "# Phase 155-R2 — stale expectation audit",
        "",
        "## Boundary",
        "",
        "This is a static expectation audit. It does not execute the repository-wide pytest suite, rewrite tests, delete tests, or change production code.",
        "",
        f"- Repository root: `{repo_root}`",
        f"- Git HEAD: `{_git_head(repo_root)}`",
        f"- Test files scanned: {len(file_summaries)}",
        f"- Expectation findings: {len(findings)}",
        f"- High stale candidates: {statuses[STATUS_HIGH]}",
        f"- Medium stale candidates: {statuses[STATUS_MEDIUM]}",
        f"- Contract-sensitive review findings: {statuses[STATUS_REVIEW]}",
        f"- Current-compatible evidence: {statuses[STATUS_COMPATIBLE]}",
        "",
        "## Status counts",
        "",
        "| status | findings |",
        "| --- | ---: |",
    ]
    for status in ALL_STATUSES:
        lines.append(f"| `{status}` | {statuses[status]} |")

    lines.extend(
        [
            "",
            "## Contract counts",
            "",
            "| contract | findings |",
            "| --- | ---: |",
        ]
    )
    for contract, count in sorted(contracts.items()):
        lines.append(f"| `{contract}` | {count} |")

    lines.extend(
        [
            "",
            "## High-candidate files",
            "",
        ]
    )
    if high_files:
        lines.extend(f"- `{file}`" for file in high_files)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Medium-candidate files",
            "",
        ]
    )
    if medium_files:
        lines.extend(f"- `{file}`" for file in medium_files)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `stale_candidate_high` means the expected literal directly conflicts with a Phase 154 public presentation contract and should be inspected first.",
            "- `stale_candidate_medium` means an older positive Reference expectation may predate Phase 153 Reference relevance/root-exclusion rules; it is not automatically stale.",
            "- `contract_sensitive_review` marks fixed numeric snapshot/count expectations that are fragile under later structural generalization.",
            "- `current_compatible` records negative expectations that explicitly enforce the current contract; these are evidence to preserve, not removal candidates.",
            "",
            "## R2 boundary",
            "",
            "R2 only identifies expectation-level candidates. Do not delete or rewrite tests from this report alone. The next step is to inspect high/medium candidates against current production behavior with focused tests, then carry only confirmed stale expectations into R2 repair or R3 consolidation.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 155-R2 static stale expectation audit."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="EHP Proof Tracer repository root (default: current directory)",
    )
    parser.add_argument(
        "--r1-inventory",
        type=Path,
        default=Path("phase155_r1_audit_output/phase155_r1_test_inventory.csv"),
        help="Phase 155-R1 test inventory CSV",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("phase155_r2_audit_output"),
        help="Output directory (default: phase155_r2_audit_output)",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    r1_inventory = args.r1_inventory
    if not r1_inventory.is_absolute():
        r1_inventory = (repo_root / r1_inventory).resolve()
    if not r1_inventory.is_file():
        raise SystemExit(
            "Phase 155-R1 inventory not found: "
            f"{r1_inventory}\nRun Phase 155-R1 first."
        )

    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = (repo_root / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    r1_rows = _load_r1_rows(r1_inventory)
    findings, file_summaries = collect_findings(repo_root, r1_rows)

    _write_dataclass_csv(
        output_dir / "phase155_r2_expectation_findings.csv",
        findings,
    )
    _write_dataclass_csv(
        output_dir / "phase155_r2_file_summary.csv",
        file_summaries,
    )
    write_summary(
        output_dir / "phase155_r2_summary.md",
        repo_root,
        findings,
        file_summaries,
    )

    status_counts = Counter(f.status for f in findings)
    contract_counts = Counter(f.contract for f in findings)
    metadata = {
        "git_head": _git_head(repo_root),
        "r1_inventory": str(r1_inventory),
        "test_files": len(file_summaries),
        "expectation_findings": len(findings),
        "status_counts": dict(status_counts),
        "contract_counts": dict(contract_counts),
    }
    (output_dir / "phase155_r2_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    high = [f for f in findings if f.status == STATUS_HIGH]
    medium = [f for f in findings if f.status == STATUS_MEDIUM]
    review = [f for f in findings if f.status == STATUS_REVIEW]
    compatible = [f for f in findings if f.status == STATUS_COMPATIBLE]

    print("Phase 155-R2 stale expectation audit completed.")
    print(f"test files: {len(file_summaries)}")
    print(f"expectation findings: {len(findings)}")
    print(f"high stale candidates: {len(high)}")
    print(f"medium stale candidates: {len(medium)}")
    print(f"contract-sensitive review: {len(review)}")
    print(f"current-compatible evidence: {len(compatible)}")
    print(f"output: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
