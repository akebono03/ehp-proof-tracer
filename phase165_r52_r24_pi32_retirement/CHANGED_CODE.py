"""Phase 165 R52-R24: read-only π3² legacy-rule retirement gate."""
from __future__ import annotations

import ast
import json
from pathlib import Path

LEGACY = "toda_pi3_2_free_cyclic_generator_inference_rule"
GENERAL = "reverse_free_cyclic_transport_rule"


def _references(path: Path, identifier: str) -> list[dict[str, object]]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == identifier:
            found.append({"line": node.lineno, "kind": type(node.ctx).__name__})
    return found


def audit(root: Path) -> dict[str, object]:
    root = root.resolve()
    paths = {
        "legacy_definition": root / "toda_rules.py",
        "legacy_bootstrap": root / "toda_upstream_bootstrap.py",
        "generic_rule": root / "phase165_r14_r33_final_group.py",
        "shared_search": root / "phase165_r52_r9_shared_math.py",
        "generic_test": root / "test_phase165_r52_r9_shared_math.py",
        "legacy_probe": root / "probes" / "probe_phase49_capabilities.py",
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing repository inputs: " + ", ".join(missing))
    references = {
        name: _references(path, LEGACY)
        for name, path in paths.items()
    }
    generic_definitions = _references(paths["generic_rule"], GENERAL)
    shared_references = _references(paths["shared_search"], GENERAL)
    test_body = paths["generic_test"].read_text(encoding="utf-8-sig")
    generic_goal_test_exists = "test_r9_pi32_regenerated_by_shared_mathematical_expansion" in test_body
    remaining_live_calls = sum(
        1 for name in ("legacy_bootstrap", "legacy_probe")
        for r in references[name] if r["kind"] == "Load"
    )
    result = {
        "phase": "165 R52-R24",
        "mode": "READ_ONLY_PI32_LEGACY_RULE_RETIREMENT_GATE",
        "paths": {name: str(path.relative_to(root)) for name, path in paths.items()},
        "legacy_reference_occurrences": references,
        "generic_rule_references": generic_definitions,
        "shared_provider_references": shared_references,
        "generic_pi32_test_present": generic_goal_test_exists,
        "active_legacy_bootstrap_reference": bool(references["legacy_bootstrap"]),
        "legacy_probe_reference": bool(references["legacy_probe"]),
        "status": "DELETION_BLOCKED_BY_LEGACY_CONSUMERS" if remaining_live_calls else "REVIEW_BEFORE_DELETION",
        "missing_obligations": [
            "replace legacy bootstrap consumer and validate old public APIs",
            "replace legacy probe consumer or explicitly retire it",
            "compare old typed premises/conclusion with generic rule: not certified by static AST",
            "pass targeted legacy and shared proof tests before deleting definition",
        ] if remaining_live_calls else ["verify all dynamic imports and affected tests"],
        "production_modified": False,
        "full_pytest_run": False,
    }
    return result


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    report = audit(root)
    output = Path(__file__).resolve().parent / "audit_output"
    output.mkdir(exist_ok=True)
    (output / "retirement.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# R52-R24 π3² 専用規則削除可否監査", "", f"判定: **{report['status']}**", "", "## 現行依存", ""]
    for name in ("legacy_bootstrap", "legacy_probe", "shared_search"):
        lines.append(f"- {name}: {len(report['legacy_reference_occurrences'][name])} occurrences")
    lines += ["", "共通探索での一般規則による証明と、旧経路の API 互換性は別の確認事項です。", "旧経路の呼び出しが残る限り定義を削除しません。", ""]
    (output / "review.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("phase", "mode", "status", "active_legacy_bootstrap_reference", "legacy_probe_reference", "production_modified", "full_pytest_run")}, ensure_ascii=False, indent=2))
    print("Review:", output / "review.md")


if __name__ == "__main__":
    main()
