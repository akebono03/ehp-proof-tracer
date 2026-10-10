"""Phase 163 R4-R5: conservative structural triage of unmapped Toda rules.

This is a read-only evidence audit, not an assertion registry migration.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from phase163_r4_r3_statement_mapping import analyze


RULE_FILES = (
    "toda_rules.py", "hopf_rules.py", "stable_rules.py",
    "ehp_rules.py", "scalar_rules.py", "relation_rules.py", "set_rules.py",
)
FIELDS = (
    "site_id", "line", "rule_name", "function", "statement_type",
    "reference_locator", "definition_evidence", "specialization_evidence",
    "classification", "confidence", "source_sha256", "review_action",
)


def _literal_text(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _function_for(tree: ast.AST, lineno: int) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    matches = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.lineno <= lineno <= node.end_lineno
    ]
    return min(matches, key=lambda n: n.end_lineno - n.lineno) if matches else None


def _rule_call_for(tree: ast.AST, lineno: int) -> ast.Call | None:
    calls = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        and node.func.id == "InferenceRule"
        and node.lineno <= lineno <= node.end_lineno
    ]
    return min(calls, key=lambda n: n.end_lineno - n.lineno) if calls else None


def _statement_type(function: ast.AST | None) -> str:
    if function is None:
        return ""
    found: set[str] = set()
    for node in ast.walk(function):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            name = node.func.id
            if name.endswith("Statement"):
                found.add(name)
    return ";".join(sorted(found))


def _keyword(call: ast.Call | None, key: str) -> ast.AST | None:
    if call is None:
        return None
    return next((k.value for k in call.keywords if k.arg == key), None)


def _source_reference(call: ast.Call | None) -> str:
    if call is None:
        return ""
    value = _keyword(call, "literature_reference")
    if not isinstance(value, ast.Call):
        return ""
    return _literal_text(_keyword(value, "locator")) or ""


def triage_site(site: dict[str, object], tree: ast.AST, source: str) -> dict[str, str | int]:
    lineno = int(site["line"])
    function = _function_for(tree, lineno)
    call = _rule_call_for(tree, lineno)
    function_name = "" if function is None else function.name
    statement_type = _statement_type(function)
    locator = _source_reference(call)
    name = str(site.get("name") or "")
    lower = (function_name + " " + name).lower()
    definition_hint = "definition" in lower or "define" in lower
    specialization_hint = "specializ" in lower or "finite-dimensional" in lower or " n=" in lower
    if locator:
        classification = "explicit_reference_candidate"
        action = "verify locator, exact conclusion and fixed/internal boundary"
    elif definition_hint:
        classification = "definition_candidate"
        action = "check whether this introduces a definition or proves a property"
    elif specialization_hint:
        classification = "specialization_candidate"
        action = "identify parent generic assertion; do not register as independent source"
    elif statement_type:
        classification = "structured_rule_unresolved"
        action = "inspect constructed Statement and its literature source"
    else:
        classification = "unresolved_rule"
        action = "inspect rule builder and conclusion or dynamic values"
    return {
        "site_id": f"toda_rules.py:{lineno}",
        "line": lineno,
        "rule_name": name,
        "function": function_name,
        "statement_type": statement_type,
        "reference_locator": locator,
        "definition_evidence": "name_hint_only" if definition_hint else "",
        "specialization_evidence": "name_hint_only" if specialization_hint else "",
        "classification": classification,
        "confidence": "candidate_only",
        "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        "review_action": action,
    }


def inspect_sources(root: Path) -> dict[str, object]:
    required = (*RULE_FILES, "toda_literature_statement_boundary.py")
    missing = [name for name in required if not (root / name).is_file()]
    if missing:
        raise FileNotFoundError("missing source files: " + ", ".join(missing))
    sources = {name: (root / name).read_text(encoding="utf-8-sig") for name in RULE_FILES}
    boundary = (root / "toda_literature_statement_boundary.py").read_text(encoding="utf-8-sig")
    mapping = analyze(boundary, sources)
    tree = ast.parse(sources["toda_rules.py"], filename="toda_rules.py")
    targets = [
        site for site in mapping["rule_sites"]
        if site["file"] == "toda_rules.py"
        and site["status"] == "not_listed_in_boundary_mapping"
    ]
    rows = [triage_site(site, tree, sources["toda_rules.py"]) for site in targets]
    if len({row["site_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate rule site ids; review scanner line identity")
    unlinked = [
        {
            "locator": str(c["locator"]),
            "component_key": str(c["key"]),
            "statement_role": str(c["role"]),
            "resolution": "not_verified",
        }
        for c in mapping["unlinked_components"]
    ]
    return {"rows": rows, "unlinked": unlinked,
            "counts": {
                "rule_constructor_sites": len(mapping["rule_sites"]),
                "toda_unmapped_sites": len(rows),
                "unlinked_boundary_components": len(unlinked),
                "triage": dict(sorted(Counter(r["classification"] for r in rows).items())),
            }}


def write_csv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(root: Path, output: Path) -> dict[str, object]:
    audit = inspect_sources(root)
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "toda_rule_triage.csv", audit["rows"], FIELDS)
    write_csv(output / "unlinked_boundary_review.csv", audit["unlinked"],
              ("locator", "component_key", "statement_role", "resolution"))
    summary = {
        "phase": "163 R4-R5",
        "counts": audit["counts"],
        "claims": ["candidate triage only", "no verified mathematical identity",
                   "no registry migration", "no inference permission granted"],
        "source": "live project sources at execution time",
        "full_pytest": "not_run",
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Phase 163 R4-R5 — 未対応 Toda 規則の構造的分類",
        "",
        "生成関数・Statement 型・明示された文献参照を併記した候補監査であり、命題数の確定ではない。",
        "",
        "## 件数",
        "",
    ]
    lines.extend(f"- {k}: {v}" for k, v in audit["counts"].items() if k != "triage")
    lines.extend(["", "## 分類候補", ""])
    lines.extend(f"- {k}: {v}" for k, v in audit["counts"]["triage"].items())
    lines.extend([
        "", "## 制限",
        "",
        "- 規則名の definition / specialization は弱いヒントであり、数学的分類の確定ではない。",
        "- `statement_type` は同一生成関数内で生成される型の候補であり、特定の規則との一致保証ではない。",
        "- 文献参照 locator は直接的な AST 構築のみ抽出し、別変数・関数経由は未解決のまま残す。",
        "- 旧 Registry・ProofStep・Renderer・Backward Search は変更しない。",
        "- 引用可能性・数学的同一性・Definition の網羅性は未確認。",
        "- 全体 pytest は未実施。",
        "",
    ])
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path.cwd() / "phase163_r4_r5_output")
    args = parser.parse_args()
    summary = write_report(args.root, args.output)
    print("Phase 163 R4-R5:", summary["counts"])
    print("Saved:", args.output / "report.md")
    print("No existing source changes; full pytest suite not run.")


if __name__ == "__main__":
    main()
