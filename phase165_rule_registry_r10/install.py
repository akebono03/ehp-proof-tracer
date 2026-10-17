"""Idempotent narrow installer. Preserves existing custom-module R8 API."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase165_r8_rule_provider.py"
REGISTRY = ROOT / "phase165_r10_rule_registry.py"
LOCAL_REGISTRY = Path(__file__).resolve().parent / "phase165_r10_rule_registry.py"
BEGIN = "    from phase165_r10_rule_registry import build_rule_registry\n"


def install() -> None:
    src = TARGET.read_text(encoding="utf-8")
    if BEGIN in src:
        print("R10 installed already; preserving existing code")
        if not REGISTRY.exists():
            shutil.copy2(LOCAL_REGISTRY, REGISTRY)
        return
    parsed = ast.parse(src)
    matches = [n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == "discover_inference_rules"]
    if len(matches) != 1:
        raise RuntimeError("Expected precisely one discover_inference_rules function")
    fn = matches[0]
    lines = src.splitlines(keepends=True)
    old = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if "DEFAULT_RULE_MODULES" not in old or "RuleCatalogReport" not in old:
        raise RuntimeError("Unexpected R8 discovery signature/body; no changes made")
    replacement = '''def discover_inference_rules(
    module_names: tuple[str, ...] = DEFAULT_RULE_MODULES,
) -> tuple[tuple[InferenceRule, ...], RuleCatalogReport]:
    """Obtain rule factories through the single R10 Rule Registry.

    This preserves the existing public API and discovery priority. It does
    not grant ProofStep/reference authority or synthesize missing inputs.
    """
    from phase165_r10_rule_registry import build_rule_registry
    registry = build_rule_registry(module_names)
    return registry.rules(), RuleCatalogReport(
        modules=registry.modules,
        rule_names=tuple(entry.rule.name for entry in registry.entries),
        skipped_factories=registry.skipped_factories,
        skipped_rules=registry.skipped_rules,
    )
'''
    next_src = "".join(lines[:fn.lineno - 1]) + replacement + "".join(lines[fn.end_lineno:])
    ast.parse(next_src)
    if REGISTRY.exists() and REGISTRY.read_bytes() != LOCAL_REGISTRY.read_bytes():
        raise RuntimeError("Existing registry differs; refusing to overwrite")
    backup = TARGET.with_suffix(".phase165_r10_before.py")
    if not backup.exists():
        shutil.copy2(TARGET, backup)
    if not REGISTRY.exists():
        shutil.copy2(LOCAL_REGISTRY, REGISTRY)
    TARGET.write_text(next_src, encoding="utf-8")
    print("R10 installed: active rule discovery now uses one stable-ID registry")


if __name__ == "__main__":
    install()
