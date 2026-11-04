"""Read-only, public-route exhaustive audit of all registered n=4 stems.

The report records independently observed search and Web states. A database
record, abstract certificate, or unverified search conclusion cannot silently
be promoted to a verified named-generator completion.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import (
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    abstract_invariants_latex,
)
from web_group_proof import build_standard_web_group_proof_view

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "sphere.csv"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "all_n4_status_report.json"
DEFAULT_CSV_OUTPUT = Path(__file__).resolve().parent / "all_n4_status_report.csv"
DEFAULT_MARKDOWN_OUTPUT = Path(__file__).resolve().parent / "all_n4_status_report.md"
EXPECTED_K = tuple(range(1, 34))


def discover_registered_n4(path: Path = CSV_PATH) -> dict[int, tuple[str, ...]]:
    """Enumerate only explicit n=4 rows; never infer stable-range records."""
    if not path.is_file():
        raise FileNotFoundError(path)
    orders: dict[int, list[str]] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not {"k", "n", "id", "orders"}.issubset(reader.fieldnames):
            raise ValueError("sphere.csv schema missing required columns")
        for row in reader:
            raw_n = (row.get("n") or "").strip()
            raw_k = (row.get("k") or "").strip()
            if not raw_n or not raw_k:
                continue
            n = int(raw_n)
            k = int(raw_k)
            if n != 4 or k < 0:
                continue
            orders.setdefault(k, []).append((row.get("orders") or "").strip())
    if tuple(sorted(orders)) != EXPECTED_K:
        raise ValueError(
            f"reviewed HEAD expects n=4 k=1..33; found {tuple(sorted(orders))}"
        )
    return {k: tuple(orders[k]) for k in sorted(orders)}


def classify_observed_status(
    search_status: str | None,
    web_key: str | None,
    web_partial: bool | None,
    has_abstract: bool,
    conclusion_present: bool,
    open_goal_count: int | None,
) -> str:
    """Classify only matching observed states, never infer a named proof."""
    if search_status is None or web_key is None or web_partial is None:
        return "NOT_VERIFIED_ERROR"
    if search_status == ProofSearchStatus.COMPLETE.value:
        if (web_key == "generic-complete-proof" and web_partial is False
                and conclusion_present and open_goal_count == 0):
            return "NAMED_COMPLETE"
        return "INCONSISTENT_SEARCH_WEB"
    if web_key != "generic-partial-proof" or web_partial is not True:
        return "INCONSISTENT_SEARCH_WEB"
    if conclusion_present:
        return "INCONSISTENT_SEARCH_WEB"
    if has_abstract:
        return "ABSTRACT_ONLY_NAMED_PENDING"
    return "NAMED_PENDING_NO_ABSTRACT"


def compact_text(value: object, limit: int = 700) -> str:
    """Keep reports bounded without claiming missing text was proven."""
    text = str(value).replace("\r", " ").replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + " [truncated]"


def view_text(line: Any) -> str:
    """Extract already-rendered text for display diagnostics only."""
    segments = getattr(line, "segments", ())
    if segments:
        return "".join(getattr(segment, "value", "") for segment in segments)
    return str(getattr(line, "prefix", ""))


def inspect_registered_group(k: int, orders: tuple[str, ...]) -> dict[str, Any]:
    """Run the real search and the separately verified public Web route."""
    row: dict[str, Any] = {
        "n": 4,
        "k": k,
        "dimension": k + 4,
        "db_orders": list(orders),
        "db_row_count": len(orders),
        "db_goal_available": False,
        "db_goal_repr": None,
        "abstract_input_compatible": None,
        "named_generator_shape_compatible": None,
        "named_shape_gate_diagnosis": None,
        "search_status": None,
        "search_conclusion_present": False,
        "proven_steps": None,
        "open_goals": None,
        "open_goal_types": [],
        "all_open_goal_reprs": [],
        "open_goal_examples": [],
        "diagnostic_count": None,
        "diagnostic_examples": [],
        "all_diagnostics": [],
        "abstract_certified": False,
        "abstract_invariants_latex": None,
        "web_key": None,
        "web_partial": None,
        "web_rendered_lines": None,
        "web_conclusion_latex": None,
        "web_heading_texts": [],
        "web_problem_lines": [],
        "inner_proof_heading_count": None,
        "unsupported_math_line_count": None,
        "raw_relation_diagnostic_count": None,
        "web_abstract_heading_count": None,
        "web_open_goal_heading_count": None,
        "category": "NOT_VERIFIED_ERROR",
        "errors": [],
    }

    goal: object | None = None
    try:
        goal = exact_prior_database_result(4, k)
        row["db_goal_available"] = goal is not None
        row["db_goal_repr"] = repr(goal) if goal is not None else None
        if goal is not None and k >= 3:
            row["abstract_input_compatible"] = checked_abstract_inputs(goal) is not None
            row["named_generator_shape_compatible"] = checked_general_inputs(goal) is not None
            if not row["abstract_input_compatible"]:
                row["named_shape_gate_diagnosis"] = "ABSTRACT_PRIOR_SHAPE_OR_ORDER_INCOMPATIBLE"
            elif not row["named_generator_shape_compatible"]:
                row["named_shape_gate_diagnosis"] = "NAMED_GENERATOR_IMAGE_OR_ALIAS_NOT_MATCHED"
            else:
                row["named_shape_gate_diagnosis"] = "NAMED_PRECONDITIONS_MATCH_BUT_PROOF_STILL_REQUIRED"
    except Exception as exc:
        row["errors"].append(f"goal:{type(exc).__name__}: {compact_text(exc)}")

    try:
        result = search_group_from_registered_goal(n=4, k=k, goal=goal)
        row["search_status"] = result.status.value
        row["search_conclusion_present"] = result.conclusion is not None
        row["proven_steps"] = len(result.proven_steps)
        row["open_goals"] = len(result.open_goals)
        row["open_goal_types"] = [type(item).__name__ for item in result.open_goals]
        row["all_open_goal_reprs"] = [repr(item) for item in result.open_goals]
        row["open_goal_examples"] = [compact_text(repr(item)) for item in result.open_goals[:3]]
        row["diagnostic_count"] = len(result.diagnostics)
        row["all_diagnostics"] = list(result.diagnostics)
        row["diagnostic_examples"] = [compact_text(item) for item in result.diagnostics[:3]]
        row["abstract_certified"] = result.abstract_structure is not None
        if result.abstract_structure is not None:
            row["abstract_invariants_latex"] = abstract_invariants_latex(
                result.abstract_structure.invariant_summands
            )
    except Exception as exc:
        row["errors"].append(f"search:{type(exc).__name__}: {compact_text(exc)}")

    try:
        view = build_standard_web_group_proof_view(
            n=4, k=k, goal=goal, mode="narrative", citation_source="model",
        )
        row["web_key"] = view.key
        row["web_partial"] = view.partial_result
        row["web_rendered_lines"] = len(view.rendered_lines)
        row["web_conclusion_latex"] = view.conclusion_latex
        row["web_heading_texts"] = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
        lines = [view_text(line) for line in view.rendered_lines]
        row["inner_proof_heading_count"] = sum(
            (getattr(line, "prefix", "").strip() == "証明")
            for line in view.rendered_lines
        )
        row["unsupported_math_line_count"] = sum(
            "数式表示未対応" in text for text in lines
        )
        row["raw_relation_diagnostic_count"] = sum(
            "Relation(" in text for text in lines
        )
        row["web_problem_lines"] = [
            compact_text(text, 1400) for text in lines
            if "数式表示未対応" in text or "Relation(" in text
        ]
        row["web_abstract_heading_count"] = sum(
            line.kind == "heading" and line.prefix == "証明済みの抽象群構造"
            for line in view.rendered_lines
        )
        row["web_open_goal_heading_count"] = sum(
            line.kind == "heading" and line.prefix == "未解決 Goal"
            for line in view.rendered_lines
        )
    except Exception as exc:
        row["errors"].append(f"public_web:{type(exc).__name__}: {compact_text(exc)}")

    row["category"] = classify_observed_status(
        search_status=row["search_status"],
        web_key=row["web_key"],
        web_partial=row["web_partial"],
        has_abstract=row["abstract_certified"],
        conclusion_present=row["search_conclusion_present"],
        open_goal_count=row["open_goals"],
    )
    if row["errors"]:
        row["category"] = "NOT_VERIFIED_ERROR"
    return row


def make_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize complete and pending categories without changing them."""
    all_counts = Counter(row["category"] for row in rows)
    high_rows = [row for row in rows if row["k"] >= 8]
    high_counts = Counter(row["category"] for row in high_rows)
    return {
        "n": 4,
        "all_registered_groups": len(rows),
        "k_ge_8_registered_groups": len(high_rows),
        "all_status_counts": dict(sorted(all_counts.items())),
        "k_ge_8_status_counts": dict(sorted(high_counts.items())),
        "k_ge_8_named_complete": [row["k"] for row in high_rows if row["category"] == "NAMED_COMPLETE"],
        "k_ge_8_abstract_only": [row["k"] for row in high_rows if row["category"] == "ABSTRACT_ONLY_NAMED_PENDING"],
        "k_ge_8_pending_without_abstract": [row["k"] for row in high_rows if row["category"] == "NAMED_PENDING_NO_ABSTRACT"],
        "k_ge_8_unverified_or_inconsistent": [row["k"] for row in high_rows if row["category"] in ("NOT_VERIFIED_ERROR", "INCONSISTENT_SEARCH_WEB")],
        "k_ge_8_unrendered_math": [row["k"] for row in high_rows if (row["unsupported_math_line_count"] or 0) > 0],
        "k_ge_8_raw_relation_diagnostics": [row["k"] for row in high_rows if (row["raw_relation_diagnostic_count"] or 0) > 0],
        "k_ge_8_abstract_input_shape_eligible": [row["k"] for row in high_rows if row["abstract_input_compatible"] is True],
        "k_ge_8_named_input_shape_eligible": [row["k"] for row in high_rows if row["named_generator_shape_compatible"] is True],
        "full_pytest_run": False,
        "production_code_changed": False,
        "proof_search_rules_changed": False,
    }


def render_markdown(rows: list[dict[str, Any]], summary: dict[str, Any], head: str) -> str:
    """Render a plain report without rewriting the Web's own narrative."""
    lines = [
        "# Phase 173 / n=4 全件・読み取り専用監査",
        "",
        f"- GitHub develop HEAD: `{head}`",
        "- 対象: `sphere.csv` の n=4, k=1..33 の全33群",
        "- 方法: 実際の Proof Search と公開 Web model 経路を個別照合",
        "- 全体 pytest: 未実施。本番コード変更: なし。",
        "- `NAMED_COMPLETE`: 検索結果と検証済み公開 Web の双方が完成",
        "- `ABSTRACT_ONLY_NAMED_PENDING`: 抽象群証明あり、記名生成元は未完成",
        "- `NAMED_PENDING_NO_ABSTRACT`: 記名証明未完成、抽象群の証明も確認できない",
        "- `NOT_VERIFIED_ERROR`: 実行例外等により確定できない（未完成と断定しない）",
        "",
        "## k>=8 の集計",
        "",
    ]
    for key, value in summary["k_ge_8_status_counts"].items():
        lines.append(f"- `{key}`: {value}群")
    lines.extend(("", "## 全33群", "", "| k | 群 | DB位数 | 判定 | 未解決 Goal | 抽象群 | 出典/表示エラー |", "|---:|---|---|---|---:|---|---|"))
    for row in rows:
        orders = " + ".join("Z" if value == "inf" else "0" if value == "0" else "Z/" + value for value in row["db_orders"])
        errors = "; ".join(row["errors"]) if row["errors"] else "-"
        errors = errors.replace("|", "/")[:150]
        abstract = str(row["abstract_invariants_latex"] or "-").replace("|", "/")
        goals = str(row["open_goals"]) if row["open_goals"] is not None else "-"
        lines.append(f"| {row['k']} | pi_{row['dimension']}^4 | {orders} | {row['category']} | {goals} | `{abstract}` | {errors} |")
    lines.extend(("", "## 未解決 Goal と表示診断", ""))
    for row in rows:
        if row["category"] == "NAMED_COMPLETE":
            continue
        lines.extend((
            f"### k={row['k']} / pi_{row['dimension']}^4",
            f"- 抽象群必要条件: `{row['abstract_input_compatible']}`、記名生成元の形状必要条件: `{row['named_generator_shape_compatible']}`、前提診断: `{row['named_shape_gate_diagnosis']}`",
            f"- 探索状態: `{row['search_status']}`、ProofStep: `{row['proven_steps']}`",
            f"- 未解決 Goal 型: `{', '.join(row['open_goal_types'])}`",
            f"- 表示不対応数式行: `{row['unsupported_math_line_count']}`、生の Relation 診断行: `{row['raw_relation_diagnostic_count']}`",
        ))
        for message in row["diagnostic_examples"]:
            lines.append(f"- 診断: `{message.replace('`', chr(39))}`")
        for message in row["errors"]:
            lines.append(f"- 実行エラー: `{message.replace('`', chr(39))}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--csv-output", type=Path, default=DEFAULT_CSV_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--head", required=True)
    args = parser.parse_args()

    registered = discover_registered_n4()
    rows: list[dict[str, Any]] = []
    for k, orders in registered.items():
        print(f"AUDIT_N4_K={k}_START", flush=True)
        row = inspect_registered_group(k, orders)
        rows.append(row)
        print(
            f"AUDIT_N4_K={k} CATEGORY={row['category']} "
            f"STATUS={row['search_status']} ABSTRACT={row['abstract_certified']} "
            f"OPEN_GOALS={row['open_goals']} WEB={row['web_key']} "
            f"ABSTRACT_SHAPE={row['abstract_input_compatible']} "
            f"NAMED_SHAPE={row['named_generator_shape_compatible']} "
            f"UNRENDERED_MATH={row['unsupported_math_line_count']} "
            f"ERRORS={len(row['errors'])}",
            flush=True,
        )
    summary = make_summary(rows)
    report = {
        "phase": "173-R4-R15R12R3",
        "audit_type": "READ_ONLY_ALL_REGISTERED_N4",
        "head_reviewed": args.head,
        "summary": summary,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.csv_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = [
        "k", "dimension", "db_goal_available", "abstract_input_compatible", "named_generator_shape_compatible", "named_shape_gate_diagnosis", "search_status", "category",
        "proven_steps", "open_goals", "abstract_certified", "abstract_invariants_latex",
        "web_key", "web_partial", "web_rendered_lines", "inner_proof_heading_count",
        "unsupported_math_line_count", "raw_relation_diagnostic_count",
        "web_abstract_heading_count", "web_open_goal_heading_count",
        "open_goal_types", "diagnostic_examples", "errors",
    ]
    with args.csv_output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            flat = dict(row)
            for key in ("open_goal_types", "diagnostic_examples", "errors"):
                flat[key] = "; ".join(flat[key])
            writer.writerow(flat)
    args.markdown_output.write_text(
        render_markdown(rows, summary, args.head), encoding="utf-8",
    )
    print("AUDIT_N4_ALL_REGISTERED=" + str(len(rows)), flush=True)
    print("AUDIT_N4_K_GE_8=" + str(summary["k_ge_8_registered_groups"]), flush=True)
    print("AUDIT_N4_K_GE_8_STATUS_COUNTS=" + json.dumps(summary["k_ge_8_status_counts"], ensure_ascii=False), flush=True)
    print("AUDIT_N4_K_GE_8_NAMED_COMPLETE=" + str(summary["k_ge_8_named_complete"]), flush=True)
    print("AUDIT_N4_K_GE_8_ABSTRACT_ONLY=" + str(summary["k_ge_8_abstract_only"]), flush=True)
    print("AUDIT_N4_K_GE_8_ERRORS=" + str(summary["k_ge_8_unverified_or_inconsistent"]), flush=True)
    print("AUDIT_N4_K_GE_8_ABSTRACT_SHAPE_ELIGIBLE=" + str(summary["k_ge_8_abstract_input_shape_eligible"]), flush=True)
    print("AUDIT_N4_K_GE_8_NAMED_SHAPE_ELIGIBLE=" + str(summary["k_ge_8_named_input_shape_eligible"]), flush=True)
    print("AUDIT_N4_ALL_JSON=" + str(args.output), flush=True)
    print("AUDIT_N4_ALL_CSV=" + str(args.csv_output), flush=True)
    print("AUDIT_N4_ALL_MARKDOWN=" + str(args.markdown_output), flush=True)
    bad = summary["k_ge_8_unverified_or_inconsistent"]
    print("AUDIT_N4_ALL_STATUS=" + ("REVIEW_REQUIRED" if bad else "PASS"), flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
