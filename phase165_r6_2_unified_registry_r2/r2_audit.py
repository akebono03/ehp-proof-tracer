"""Read-only audit of argument-requiring inference-rule factories (Python 3.10).

Do not import production modules or call rule factories: only parse source files.
"""
from __future__ import annotations

import ast
from collections import Counter
import json
from pathlib import Path
from typing import Any

MODULES = (
    "ehp_rules", "stable_rules", "set_rules", "hopf_rules",
    "scalar_rules", "relation_rules", "map_property_rules",
    "homomorphism_rules", "indeterminacy_rules",
)


def _expr(node: ast.AST | None) -> str | None:
    if node is None:
        return None
    try:
        return ast.unparse(node)
    except (AttributeError, ValueError, TypeError):
        return None


def required_parameters(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    """Follow inspect.signature's positional / keyword required-arg semantics."""
    args = function.args
    positional = list(args.posonlyargs) + list(args.args)
    n_required = len(positional) - len(args.defaults)
    output: list[dict[str, Any]] = []
    for index, parameter in enumerate(positional):
        if index < n_required:
            output.append({
                "name": parameter.arg,
                "kind": "POSITIONAL_ONLY" if index < len(args.posonlyargs) else "POSITIONAL_OR_KEYWORD",
                "annotation": _expr(parameter.annotation),
            })
    for parameter, default in zip(args.kwonlyargs, args.kw_defaults):
        if default is None:
            output.append({"name": parameter.arg, "kind": "KEYWORD_ONLY", "annotation": _expr(parameter.annotation)})
    return output


def inspect_factory_sources(root: Path, modules: tuple[str, ...] = MODULES) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for module in modules:
        path = root / (module + ".py")
        if not path.is_file():
            raise FileNotFoundError(str(path))
        tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.name.endswith("_inference_rule"):
                continue
            required = required_parameters(node)
            if not required:
                continue
            symbols = {item["name"] for item in required}
            body = ast.walk(node)
            possible_rule = any(isinstance(x, ast.Call) and (
                isinstance(x.func, ast.Name) and x.func.id == "InferenceRule" or
                isinstance(x.func, ast.Attribute) and x.func.attr == "InferenceRule"
            ) for x in body)
            rows.append({
                "rule_id": module + "." + node.name,
                "module": module,
                "factory": node.name,
                "line": node.lineno,
                "parameters": required,
                "contains_inference_rule_constructor": possible_rule,
                "argument_names": sorted(symbols),
                "registration": "REQUIRES_EXPLICIT_TYPED_ARGUMENTS",
                "forward": "NOT_EVALUATED",
                "backward": "NOT_EVALUATED",
                "source_witness_required": "UNKNOWN_REQUIRES_REVIEW",
                "search_connection": "NOT_IN_R8_NO_ARG_DEFAULT",
                "certification": "NOT_CERTIFIED",
            })
    return sorted(rows, key=lambda x: x["rule_id"])


def analyze(root: Path, *, modules: tuple[str, ...] = MODULES) -> dict[str, Any]:
    rules = inspect_factory_sources(root, modules)
    return {
        "phase": "165 R6-2 unified registry R2",
        "status": "AUDITED_READ_ONLY",
        "source_root": str(root),
        "rule_count": len(rules),
        "modules": list(modules),
        "count_by_module": dict(sorted(Counter(row["module"] for row in rules).items())),
        "rules": rules,
        "registration_policy": {
            "default": "BLOCKED_UNTIL_EXPLICIT_ARGUMENT_BINDING",
            "existing_safe_registration": "build_unified_backward_rule_registry(extra_rules=...)",
            "no_automatic_witness_synthesis": True,
            "no_default_search_connection": True,
        },
        "limitations": [
            "AST signatures do not verify runtime types or mathematical soundness.",
            "This audit does not call factories or manufacture typed witness arguments.",
            "A parameter annotation alone cannot establish a trusted source for its value.",
            "Only the nine R8 default modules are inventoried in this stage.",
        ],
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Phase 165 R6-2 R2：引数必須規則の登録条件監査", "",
        "- 状態: `" + str(report["status"]) + "`",
        "- 検出数: " + str(report["rule_count"]),
        "- 本番コード変更: なし", "- 証人の自動生成: なし", "",
        "| Rule ID | 必須引数（型注釈） | 登録状態 |", "|---|---|---|",
    ]
    for entry in report["rules"]:
        args = ", ".join(p["name"] + ": " + (p["annotation"] or "型注釈なし") for p in entry["parameters"])
        lines.append("| `" + entry["rule_id"] + "` | " + args.replace("|", "/") + " | EXPLICIT_ONLY |")
    lines += ["", "## 判定上の制約", ""]
    lines.extend("- " + v for v in report["limitations"])
    lines += ["", "## 次 Phase との境界", "", "R3 では個別 Provider と R8 外の一般規則を収集・整理する。R2 では規則本体も共通探索も変更しない。", ""]
    return "\n".join(lines)


def write_reports(root: Path, output: Path) -> dict[str, Any]:
    report = analyze(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "required_argument_rules.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "required_argument_rules.md").write_text(markdown(report), encoding="utf-8")
    return report


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = write_reports(args.root, args.output)
    print(json.dumps({"status": result["status"], "required_argument_factories": result["rule_count"], "module_counts": result["count_by_module"], "registered_automatically": 0, "full_pytest_run": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
