"""Apply the R3-41P2 focused legacy-test expectation change, with backup.

Only one outdated sentence expectation in one existing test is changed.
Application code, search rules, renderers and citations are never edited.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
PROJECT = PACKAGE.parent
BACKUP_DIR = PACKAGE / "output" / "backups"
TARGET = Path("phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py")
FUNCTION = "test_pi32_all_steps_preserved_without_suppression"
OLD = '    assert "零写像である" in rendered'
NEW = r'    assert r"\operatorname{Im}\Delta=\ker E=0" in rendered'


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def apply_legacy_test_fix(
    project: Path = PROJECT, backup_dir: Path = BACKUP_DIR,
) -> dict[str, str]:
    """Replace exactly one outdated assertion inside the named test function.

    On mismatch, fail closed. Preserve the original bytes and record the
    patched hash so manual rollback never overwrites later user changes.
    """
    project = Path(project)
    backup_dir = Path(backup_dir)
    path = project / TARGET
    raw = path.read_bytes()
    source = raw.decode("utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    matches = [node for node in tree.body
               if isinstance(node, ast.FunctionDef) and node.name == FUNCTION]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {FUNCTION} in {path}")
    lines = source.splitlines(keepends=True)
    fn = matches[0]
    function_text = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if NEW in function_text and OLD not in function_text:
        return {"status": "already_patched", "file": str(path), "sha256": sha256(raw)}
    if function_text.count(OLD) != 1 or source.count(OLD) != 1 or NEW in function_text:
        raise ValueError("R3-29 original assertion differs; refusing to patch")

    old_raw = OLD.encode("utf-8")
    new_raw = NEW.encode("utf-8")
    if raw.count(old_raw) != 1:
        raise ValueError("R3-29 assertion bytes are ambiguous")
    patched = raw.replace(old_raw, new_raw, 1)
    ast.parse(patched.decode("utf-8-sig"), filename=str(path))
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / "r3_29_test_original.bin"
    state = backup_dir / "r3_29_test_state.json"
    if backup.exists() or state.exists():
        if not backup.exists() or not state.exists():
            raise ValueError("Incomplete previous backup; refusing to patch")
        prior = json.loads(state.read_text(encoding="utf-8"))
        if (prior.get("original_sha256") != sha256(raw)
                or sha256(backup.read_bytes()) != sha256(raw)
                or prior.get("patched_sha256") != sha256(patched)):
            raise ValueError("Existing backup has different content; refusing to patch")
    else:
        backup.write_bytes(raw)
        state.write_text(json.dumps({
            "target": TARGET.as_posix(),
            "original_sha256": sha256(raw),
            "patched_sha256": sha256(patched),
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temp = path.with_name(path.name + ".r341p2.tmp")
    try:
        temp.write_bytes(patched)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)
    return {"status": "patched", "file": str(path), "sha256": sha256(patched)}


def main() -> int:
    try:
        outcome = apply_legacy_test_fix()
    except Exception as exc:
        print("R3-41P2 TEST_PATCH_ERROR", f"{type(exc).__name__}: {exc}")
        return 1
    print("R3-41P2 TEST_PATCH", outcome["status"], outcome["file"])
    print("TEST_BACKUP_DIR", BACKUP_DIR)
    print("APPLICATION_FILES_NOT_CHANGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
