"""Apply exactly one name-independent, typed structural display-suppression correction.

Application changes only the existing render_model_backed_narrative_markdown function,
retaining every other byte. It checks the observed R3-41P4 SHA-256 before editing.
"""
from __future__ import annotations

import ast
import hashlib
import json
import shutil
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
TARGET = PROJECT / "phase168_r3_5_model_renderer.py"
EXPECTED_SHA256 = "d3daacf4b29a675aa2a9b72ce14d27bf25fb3f72557a10693707a441afdccabe"
BACKUP = OUTPUT / "backups" / TARGET.name

OLD_RULE_IMPORT = "    from proof import ProofRule, Relation\n"
NEW_RULE_IMPORT = "    from proof import ProofRule, Relation, RelationType\n"
OLD_IMPORT = "        from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaSuspensionMap\n"
NEW_IMPORT = (
    "        from expression import IteratedSuspension\n"
    "        from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaSuspensionMap\n"
)
OLD_CONDITION = '''                        and getattr(consumer.inference_rule, "name", None)
                        == "proved generator suspension normalizes transported cyclic group"
                        and transported.lhs == conclusion.lhs
'''
NEW_CONDITION = '''                        and transported.relation_type is RelationType.EQUALITY
                        and conclusion.relation_type is RelationType.EQUALITY
                        and isinstance(witness_step.conclusion.map, TodaSuspensionMap)
                        and isinstance(transported.rhs.generator, IteratedSuspension)
                        and type(transported.rhs.generator.exponent) is int
                        and transported.rhs.generator.exponent == 1
                        and element_tex(transported.rhs.generator.expression) is not None
                        and element_tex(transported.rhs.generator.expression)
                            == element_tex(witness_step.conclusion.source_generator)
                        and element_tex(conclusion.rhs.generator) is not None
                        and element_tex(conclusion.rhs.generator)
                            == element_tex(witness_step.conclusion.target_generator)
                        and transported.lhs == conclusion.lhs
'''


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(source: str) -> str:
    if source.count(OLD_RULE_IMPORT) != 1:
        raise ValueError("Expected Renderer rule import not found exactly once")
    if source.count(OLD_IMPORT) != 1:
        raise ValueError("Expected local import not found exactly once")
    if source.count(OLD_CONDITION) != 1:
        raise ValueError("Expected name-dependent condition not found exactly once")
    changed = source.replace(OLD_RULE_IMPORT, NEW_RULE_IMPORT, 1)
    changed = changed.replace(OLD_IMPORT, NEW_IMPORT, 1)
    changed = changed.replace(OLD_CONDITION, NEW_CONDITION, 1)
    tree = ast.parse(changed, filename=str(TARGET))
    matching = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "render_model_backed_narrative_markdown"]
    if len(matching) != 1:
        raise ValueError("Expected one complete renderer function")
    return changed


def extract_full_function(source: str) -> str:
    tree = ast.parse(source, filename=str(TARGET))
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name == "render_model_backed_narrative_markdown"]
    if len(matches) != 1:
        raise ValueError("Function definition not unique")
    node = matches[0]
    return "\n".join(source.splitlines()[node.lineno-1:node.end_lineno]) + "\n"


def apply() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(str(TARGET))
    original_bytes = TARGET.read_bytes()
    found_hash = digest(original_bytes)
    if found_hash != EXPECTED_SHA256:
        raise ValueError(
            f"Refusing patch: actual SHA-256 {found_hash}; "
            f"expected R3-41P4 {EXPECTED_SHA256}. "
            "Check whether GitHub/local source has moved."
        )
    original = original_bytes.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in original else "\n"
    # Git for Windows may check out CRLF; preserve the current local style.
    normalized = original.replace("\r\n", "\n")
    changed = transform(normalized)
    changed_bytes = changed.replace("\n", newline).encode("utf-8")
    full_function = extract_full_function(changed)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists():
        if BACKUP.read_bytes() != original_bytes:
            raise ValueError("Existing backup does not match input; refusing overwrite")
    else:
        BACKUP.write_bytes(original_bytes)
    full_file = OUTPUT / "full_files" / TARGET.name
    full_file.parent.mkdir(parents=True, exist_ok=True)
    full_file.write_text(changed, encoding="utf-8", newline="\n")
    (OUTPUT / "render_model_backed_narrative_markdown_FULL.py").write_text(
        full_function, encoding="utf-8", newline="\n"
    )
    (OUTPUT / "post_patch.json").write_text(json.dumps({
        "file": TARGET.name,
        "sha256_before": found_hash,
        "sha256_after": digest(changed_bytes),
        "function": "render_model_backed_narrative_markdown",
        "changed_files": [TARGET.name],
        "full_function_path": "render_model_backed_narrative_markdown_FULL.py",
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Atomic replace after verification and backup creation. All generated
    # application source stays within one existing file.
    staging = TARGET.with_name(TARGET.name + ".r341p5.tmp")
    try:
        staging.write_bytes(changed_bytes)
        staging.replace(TARGET)
    finally:
        if staging.exists():
            staging.unlink()
    print("PATCHED", TARGET)
    print("BACKUP", BACKUP)
    print("FULL_FUNCTION", OUTPUT / "render_model_backed_narrative_markdown_FULL.py")
    print("FULL_FILE", full_file)
    print("APPLICATION_PATCH_ONLY_RENDERER_FUNCTION")


if __name__ == "__main__":
    apply()
