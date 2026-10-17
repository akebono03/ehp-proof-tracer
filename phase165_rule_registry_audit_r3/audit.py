"""Read-only audit of rule implementation, generic discovery, and invertibility."""
from __future__ import annotations

import ast
import importlib
import inspect
import json
from pathlib import Path

from phase165_r8_rule_provider import DEFAULT_RULE_MODULES, discover_inference_rules

KEYWORDS = (
    "exact", "kernel", "image", "surject", "epimorph", "cyclic",
    "quotient", "generator", "suspension", "delta", "ehp",
)
ADDITIONAL_MODULES = (
    "toda_rules", "toda_delta_image_rules", "group_rules",
    "group_structure_rules", "set_rules", "ehp_rules", "stable_rules",
)


def classify_rule(*, implemented: bool, discovered: bool, pattern: bool | None) -> str:
    if not implemented:
        return "NOT_FOUND_IN_SCANNED_MODULES"
    if not discovered:
        return "IMPLEMENTED_NOT_DISCOVERED_BY_R8"
    if pattern is False:
        return "DISCOVERED_WITHOUT_CONCLUSION_PATTERN"
    return "DISCOVERED_WITH_CONCLUSION_PATTERN"


def _runtime_factories(module_name: str) -> list[dict]:
    try:
        module = importlib.import_module(module_name)
    except ImportError as exc:
        return [{"module": module_name, "import_error": str(exc)}]
    result = []
    for name, value in vars(module).items():
        if not (name.endswith("_inference_rule") and callable(value)
                and getattr(value, "__module__", None) == module.__name__):
            continue
        if not any(word in name.lower() for word in KEYWORDS):
            continue
        try:
            signature = inspect.signature(value)
            mandatory = tuple(str(p.name) for p in signature.parameters.values()
                              if p.default is inspect.Parameter.empty
                              and p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                                             inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                             inspect.Parameter.KEYWORD_ONLY))
        except (TypeError, ValueError):
            mandatory = ("SIGNATURE_UNKNOWN",)
        rule = None
        instantiate_error = None
        if not mandatory:
            try:
                rule = value()
            except Exception as exc:
                instantiate_error = f"{type(exc).__name__}: {exc}"[:350]
        result.append({
            "module": module_name,
            "factory": name,
            "mandatory_args": list(mandatory),
            "runtime_rule_name": getattr(rule, "name", None),
            "conclusion_pattern_present": (getattr(rule, "conclusion_pattern", None) is not None)
              if rule is not None else None,
            "premise_pattern_count": len(rule.premise_patterns) if rule is not None else None,
            "instantiate_error": instantiate_error,
        })
    return result


def _source_registry_mentions(root: Path, name: str) -> list[str]:
    paths = ("standard_production_applicability_catalog.py", "rule_catalog.py")
    found = []
    for rel in paths:
        file = root / rel
        if file.is_file() and name in file.read_text(encoding="utf-8-sig"):
            found.append(rel)
    return found


def main() -> dict:
    root = Path.cwd()
    if (root / "phase165_r52_r23_existing_rule_adapter.py").exists():
        raise RuntimeError("Dedicated pi43 adapter still exists; audit assumption invalid")
    discovered, report = discover_inference_rules()
    discovered_names = {rule.name for rule in discovered}
    module_names = tuple(dict.fromkeys(DEFAULT_RULE_MODULES + ADDITIONAL_MODULES))
    rows = [row for module in module_names for row in _runtime_factories(module)]
    for row in rows:
        if "factory" not in row:
            continue
        row["r8_default_module"] = row["module"] in DEFAULT_RULE_MODULES
        row["r8_discovered"] = row["runtime_rule_name"] in discovered_names and not row["mandatory_args"]
        row["registration_source_mentions"] = _source_registry_mentions(root, row["factory"])
        row["classification"] = classify_rule(
            implemented=True, discovered=row["r8_discovered"],
            pattern=row["conclusion_pattern_present"],
        )
    coverage = {}
    for word in KEYWORDS:
        relevant = [r for r in rows if "factory" in r and word in r["factory"].lower()]
        coverage[word] = {
            "implemented_factory_count": len(relevant),
            "r8_discovered_factory_count": sum(bool(r["r8_discovered"]) for r in relevant),
            "discovered_with_pattern": sum(r["r8_discovered"] and r["conclusion_pattern_present"] is True for r in relevant),
        }
    payload = {
        "phase": "165 rule registry audit R3", "mode": "READ_ONLY_DYNAMIC",
        "group_adapter_absent": True,
        "r8_default_modules": list(DEFAULT_RULE_MODULES),
        "r8_rules_discovered": len(discovered),
        "candidate_rule_factories": rows,
        "topic_coverage": coverage,
        "interpretation_note": "R8 discovery is not equivalent to registration in every rule catalog; source mentions are indicators, not proof of catalog activation.",
        "full_pytest_run": False,
    }
    output = Path(__file__).with_name("audit_result.json")
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("phase", "group_adapter_absent", "r8_rules_discovered", "topic_coverage", "full_pytest_run")}, ensure_ascii=False, indent=2))
    print("Audit saved:", output)
    return payload


if __name__ == "__main__":
    main()
