"""Phase 168 R3-41P6: remove rule-name-dependent exactness prose selection.

Only the existing typed_sentence() function in the Typed Projection is edited.
Application verifies the observed R3-41P4/P5 SHA-256 and preserves newline style.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
OUTPUT = PACKAGE / "output"
TARGET = PROJECT / "phase168_r3_27_typed_statement_projection.py"
EXPECTED_SHA256 = "b23866ee3365ef0257a03670d85636abf2cc60cb244d0f702d9d0620345abf34"
BACKUP = OUTPUT / "backups" / TARGET.name

OLD_BLOCK = """                    if step.premises and any(
                        "exact" in str(getattr(p.inference_rule, "name", "")).lower()
                        or isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement))
                        for p in step.premises
                    ):
"""
NEW_BLOCK = """                    if any(
                        isinstance(p.conclusion, (TodaProp42ExactnessStatement, EHPImageEqualsKernelStatement))
                        for p in step.premises
                    ):
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def full_function(source: str) -> str:
    tree = ast.parse(source)
    matches = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "typed_sentence"]
    if len(matches) != 1:
        raise ValueError("Expected a unique typed_sentence() function")
    node = matches[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def transform(source: str) -> str:
    if source.count(OLD_BLOCK) != 1:
        raise ValueError("Expected exactness prose condition was not found exactly once")
    old_fn = full_function(source)
    if OLD_BLOCK not in old_fn:
        raise ValueError("Condition is not inside typed_sentence()")
    changed = source.replace(OLD_BLOCK, NEW_BLOCK, 1)
    changed_fn = full_function(changed)
    if changed.replace(changed_fn, old_fn, 1) != source:
        raise ValueError("Unexpected change outside typed_sentence()")
    if '"exact" in str(getattr(p.inference_rule, "name", "")).lower()' in changed_fn:
        raise ValueError("Name-based gate remains in typed_sentence()")
    return changed


def apply() -> None:
    if not TARGET.is_file():
        raise FileNotFoundError(TARGET)
    data = TARGET.read_bytes()
    found = sha256(data)
    if found != EXPECTED_SHA256:
        raise ValueError(
            f"Source checksum mismatch: {found}. Expected {EXPECTED_SHA256}. "
            "No changes made. Inspect your working tree before retrying."
        )
    source = data.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in source else "\n"
    normalized = source.replace("\r\n", "\n")
    changed = transform(normalized)
    result_bytes = changed.replace("\n", newline).encode("utf-8")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != data:
        raise ValueError("Backup already exists and differs; refusing overwrite")
    if not BACKUP.exists():
        BACKUP.write_bytes(data)
    full_files = OUTPUT / "full_files"
    full_files.mkdir(parents=True, exist_ok=True)
    (full_files / TARGET.name).write_text(changed, encoding="utf-8", newline="\n")
    (OUTPUT / "typed_sentence_FULL.py").write_text(
        full_function(changed), encoding="utf-8", newline="\n"
    )
    (OUTPUT / "post_patch.json").write_text(json.dumps({
        "file": TARGET.name,
        "function": "typed_sentence",
        "before_sha256": found,
        "after_sha256": sha256(result_bytes),
        "changed_files": [TARGET.name],
        "math_rules_changed": False,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    staging = TARGET.with_name(TARGET.name + ".r341p6.tmp")
    try:
        staging.write_bytes(result_bytes)
        staging.replace(TARGET)
    finally:
        if staging.exists():
            staging.unlink()
    print("PATCHED", TARGET)
    print("BACKUP", BACKUP)
    print("FULL_FUNCTION", OUTPUT / "typed_sentence_FULL.py")
    print("FULL_FILE", full_files / TARGET.name)
    print("ONLY_TYPED_SENTENCE_CHANGED")


if __name__ == "__main__":
    apply()
