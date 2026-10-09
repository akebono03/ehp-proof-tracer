"""Apply the smallest guarded R10 connection change to the current checkout."""
from __future__ import annotations
import ast
from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()
TARGET = ROOT / "phase162_web_narrative_integration.py"
NEW = Path(__file__).with_name("phase162_reference_boundary.py")
MODULE = ROOT / NEW.name


def _function_source(content: str, name: str) -> str:
    tree = ast.parse(content)
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if len(nodes) != 1:
        raise ValueError(f"Function not uniquely found: {name}")
    lines = content.splitlines(keepends=True)
    node = nodes[0]
    return "".join(lines[node.lineno - 1:node.end_lineno])


def apply():
    if not TARGET.is_file():
        raise SystemExit("Run from the EHP Proof Tracer repository root")
    current = TARGET.read_text(encoding="utf-8")
    ast.parse(current)
    target_names = ("_phase162_ehp_leaves", "_build_phase162_legacy_validated_isomorphism_markdown")
    parts = {name: _function_source(current, name) for name in target_names}
    anchor = 'hopf_eta5 = build_phase58_representative_result()["final_hopf_step"]'
    if sum(part.count(anchor) for part in parts.values()) != 2:
        raise SystemExit("R10 guard: expected two unchanged Hopf witness assignments; no file changed")
    addition = """hopf_eta5 = cite_verified_fixed_statement(
        build_phase58_representative_result()["final_hopf_step"],
        reference_locator="(5.3)",
        component_key="nu_prime_hopf_relation",
        expected_conclusion=build_phase58_representative_result()["expected_final_hopf"],
    )"""
    updated = current
    for name in target_names:
        old = parts[name]
        new = old.replace(anchor, addition, 1)
        if name == "_phase162_ehp_leaves":
            indentation = "    "
        else:
            indentation = "    "
        # The replaced first line already includes indentation from source.
        # Subsequent lines use four spaces, matching both existing functions.
        updated = updated.replace(old, new, 1)
    imp = "from phase162_reference_boundary import cite_verified_fixed_statement\n"
    if imp not in updated:
        updated = imp + updated
    ast.parse(updated)
    if MODULE.exists() and MODULE.read_bytes() != NEW.read_bytes():
        raise SystemExit("Existing boundary module differs; refusing overwrite")
    backup = TARGET.with_suffix(TARGET.suffix + ".phase162_r10.bak")
    if not backup.exists():
        shutil.copy2(TARGET, backup)
    MODULE.write_bytes(NEW.read_bytes())
    TARGET.write_text(updated, encoding="utf-8")
    print("Updated:", TARGET.name)
    print("Installed:", MODULE.name)
    print("Backup:", backup.name)
    report = Path(__file__).with_name("CHANGED_CODE.md")
    sections = ["# Phase 162 R10: complete changed functions", "", "## Import", "```python", imp.strip(), "```", ""]
    for name in target_names:
        sections += ["## " + name, "```python", _function_source(updated, name).rstrip(), "```", ""]
    sections += ["## New module", "```python", NEW.read_text(encoding="utf-8").rstrip(), "```", ""]
    report.write_text("\n".join(sections), encoding="utf-8")
    print("Full replacement functions:", report)

if __name__ == "__main__":
    apply()
