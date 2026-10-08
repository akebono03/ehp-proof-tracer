"""Read-only Phase 161 R1 rule instance audit (no proof search, no repository edits)."""
from __future__ import annotations

import dataclasses
import importlib
import inspect
import json
import pathlib
import sys
import traceback

RULE_NAMES = (
    "toda_53_n3_prop51_delta_injective_inference_rule",
    "toda_53_n3_delta_injective_hopf_zero_inference_rule",
    "toda_53_n3_hopf_zero_suspension_surjective_inference_rule",
    "toda_53_n3_hopf_eta5_surjective_inference_rule",
    "toda_53_n3_hopf_surjective_delta_zero_inference_rule",
    "toda_53_n3_delta_zero_suspension_injective_inference_rule",
    "toda_53_n3_suspension_isomorphism_inference_rule",
)


def safe_value(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, type):
        return f"{value.__module__}.{value.__qualname__}"
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {
            "type": f"{type(value).__module__}.{type(value).__qualname__}",
            "fields": {f.name: safe_value(getattr(value, f.name)) for f in dataclasses.fields(value)},
        }
    if isinstance(value, (tuple, list)):
        return [safe_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): safe_value(item) for key, item in value.items()}
    return repr(value)


def callable_info(func):
    if func is None:
        return None
    info = {
        "module": getattr(func, "__module__", None),
        "qualname": getattr(func, "__qualname__", None),
        "signature": str(inspect.signature(func)) if callable(func) else None,
    }
    try:
        info["source_file"] = inspect.getsourcefile(func)
        info["source_line"] = inspect.getsourcelines(func)[1]
        info["source"] = inspect.getsource(func)
    except (OSError, TypeError):
        info["source"] = None
    closure = getattr(func, "__closure__", None)
    names = getattr(getattr(func, "__code__", None), "co_freevars", ())
    if closure:
        info["closure"] = {name: safe_value(cell.cell_contents) for name, cell in zip(names, closure)}
    return info


def audit_rule(module, name):
    factory = getattr(module, name)
    rule = factory()
    return {
        "factory": name,
        "factory_source": callable_info(factory),
        "name": rule.name,
        "description": rule.description,
        "premise_count": len(rule.premise_patterns),
        "premise_patterns": [safe_value(p) for p in rule.premise_patterns],
        "conclusion_pattern": safe_value(rule.conclusion_pattern),
        "conclusion_builder": callable_info(rule.conclusion_builder),
        "match_guard": callable_info(rule.match_guard),
        "literature_reference": safe_value(rule.literature_reference),
    }


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    output = pathlib.Path(__file__).resolve().parent / "audit_output"
    output.mkdir(exist_ok=True)
    report = {"purpose": "read-only rule contract audit", "rules": [], "errors": []}
    try:
        module = importlib.import_module("toda_rules")
        report["toda_rules_location"] = getattr(module, "__file__", None)
    except Exception as exc:
        report["errors"].append({"import": "toda_rules", "error": str(exc), "traceback": traceback.format_exc()})
        module = None
    if module is not None:
        for name in RULE_NAMES:
            try:
                report["rules"].append(audit_rule(module, name))
            except Exception as exc:
                report["errors"].append({"factory": name, "error": str(exc), "traceback": traceback.format_exc()})
    (output / "phase161_r1_rule_contracts.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Phase 161 R1 — 7規則の実体監査", "", "実際の Production 規則を読み取った記録。逆向き探索の実行は行っていません。", ""]
    for rule in report["rules"]:
        lines += [f"## {rule['factory']}", "", f"- Production name: `{rule['name']}`", f"- Premise count: {rule['premise_count']}", f"- conclusion_pattern: `{repr(rule['conclusion_pattern'])}`", f"- conclusion_builder: `{bool(rule['conclusion_builder'])}`", f"- match_guard: `{bool(rule['match_guard'])}`", "", "### premise_patterns", "", "```json", json.dumps(rule["premise_patterns"], ensure_ascii=False, indent=2), "```", ""]
        for label in ("factory_source", "conclusion_builder", "match_guard"):
            entry = rule[label]
            if entry:
                lines += [f"### {label}", "", f"Source: `{entry.get('source_file')}:{entry.get('source_line')}`", "", "```python", entry.get("source") or "# Source not available", "```", ""]
                if entry.get("closure"):
                    lines += ["Closure:", "", "```json", json.dumps(entry["closure"], ensure_ascii=False, indent=2), "```", ""]
    if report["errors"]:
        lines += ["## 取得エラー", "", "```json", json.dumps(report["errors"], ensure_ascii=False, indent=2), "```", ""]
    (output / "phase161_r1_rule_contracts.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"rule_count": len(report["rules"]), "error_count": len(report["errors"]), "source_module": report.get("toda_rules_location"), "output": str(output)}, ensure_ascii=False, indent=2))
    return 0 if len(report["rules"]) == len(RULE_NAMES) and not report["errors"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
