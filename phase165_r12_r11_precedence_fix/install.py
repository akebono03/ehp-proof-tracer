"""Focused R12-R11 fix: prefer universal inference only after reference screening."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def insert_once(text: str, anchor: str, replacement: str, marker: str) -> str:
    if marker in text:
        return text
    if text.count(anchor) != 1:
        raise RuntimeError("Expected exactly one anchor: " + anchor)
    return text.replace(anchor, replacement, 1)


def main() -> None:
    project = Path.cwd()
    package = Path(__file__).resolve().parent
    module_target = project / "phase165_r12_r11_prop42_unified.py"
    test_target = project / "phase165_r12_r11_prop42_unified" / "tests" / "test_phase165_r12_r11_prop42_unified.py"
    shared_target = project / "phase165_r52_r9_shared_math.py"
    expected_module = package / "payload" / module_target.name
    expected_test = package / "tests" / test_target.name
    for target in (module_target, test_target, shared_target):
        if not target.is_file():
            raise FileNotFoundError("Run the original R12-R11 package first: " + str(target))
    existing_module = module_target.read_text(encoding="utf8")
    new_module = expected_module.read_text(encoding="utf8")
    prefix = new_module.split("\n\ndef prefer_universal_prop42_derivation(", 1)[0]
    if existing_module != prefix and existing_module != new_module:
        raise RuntimeError("Installed R11 source differs; refusing overwrite")
    existing_test = test_target.read_text(encoding="utf8")
    new_test = expected_test.read_text(encoding="utf8")
    old_test = new_test.replace(
        "    prefer_universal_prop42_derivation,\n", ""
    ).replace(
        "    screened = prefer_universal_prop42_derivation(screened)\n    provider =",
        "    provider =",
    ).split("\n\ndef test_r11_precedence_preserves_old_leaves_without_screened_general_source():", 1)[0]
    if existing_test != old_test and existing_test != new_test:
        raise RuntimeError("Installed R11 tests differ; refusing overwrite")
    shared = shared_target.read_text(encoding="utf8")
    anchor = "    if expansion_provider is None:\n        expansion_provider = shared_expansion_provider("
    replacement = (
        "    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation\n"
        "    proof_context = prefer_universal_prop42_derivation(proof_context)\n"
        "    if expansion_provider is None:\n"
        "        expansion_provider = shared_expansion_provider("
    )
    updated_shared = insert_once(
        shared, anchor, replacement,
        "    proof_context = prefer_universal_prop42_derivation(proof_context)"
    )
    for target, data in ((module_target, new_module), (test_target, new_test),
                         (shared_target, updated_shared)):
        ast.parse(data, filename=str(target))
    for target, data in ((module_target, new_module), (test_target, new_test),
                         (shared_target, updated_shared)):
        if target.read_text(encoding="utf8") == data:
            print("Already installed:", target)
            continue
        backup = target.with_name(target.name + ".r12_r11_precedence.bak")
        if not backup.exists():
            shutil.copy2(target, backup)
        target.write_text(data, encoding="utf8")
        print("Updated:", target)
    print("R12-R11 source priority fix installed; full pytest NOT run")


if __name__ == "__main__":
    main()
