"""Correct the existing citation test fixture without weakening validation."""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = Path("phase168_r3_12_body_binding/tests/test_phase168_r3_12_body_binding.py")
STATE = PACKAGE / "test_fix_state.json"
BEFORE = "wrong = replace(model, step_citation_numbers=((2,),))"
AFTER = "wrong = replace(model, citations=(), step_citation_numbers=((2,),))"


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def verify_test_source(source: str) -> None:
    tree = ast.parse(source)
    matches = [item for item in tree.body
               if isinstance(item, ast.FunctionDef)
               and item.name == "test_unknown_citation_number_is_rejected"]
    if len(matches) != 1:
        raise ValueError("Expected exactly one unknown-citation test")
    method = matches[0]
    lines = source.splitlines(keepends=True)
    body = "".join(lines[method.lineno - 1:method.end_lineno])
    if body.count(BEFORE) != 1 and body.count(AFTER) != 1:
        raise ValueError("The existing test fixture has an unexpected shape")
    if 'match="missing or unrelated"' not in body:
        raise ValueError("Unknown-citation rejection assertion changed")
    reverse = [item for item in tree.body
               if isinstance(item, ast.FunctionDef)
               and item.name == "test_reverse_citation_mapping_is_checked"]
    if len(reverse) != 1:
        raise ValueError("Expected reverse-citation regression test")


def patched_bytes(data: bytes) -> bytes:
    text = data.decode("utf-8")
    verify_test_source(text)
    if AFTER in text and BEFORE not in text:
        return data
    if text.count(BEFORE) != 1:
        raise ValueError("Original malformed fixture missing or duplicated")
    updated = text.replace(BEFORE, AFTER, 1)
    ast.parse(updated)
    return updated.encode("utf-8")


def apply_fixture_patch() -> None:
    path = ROOT / TARGET
    original = path.read_bytes()
    desired = patched_bytes(original)
    if STATE.exists():
        state = json.loads(STATE.read_text("utf-8"))
        if _digest(original) == state["installed_sha256"]:
            print("TEST_ALREADY_PATCHED", TARGET)
            return
        raise ValueError("Existing test fix state does not match current test")
    if original == desired:
        print("TEST_ALREADY_PATCHED", TARGET)
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = PACKAGE / "backup" / stamp
    backup.mkdir(parents=True, exist_ok=False)
    (backup / TARGET.name).write_bytes(original)
    try:
        path.write_bytes(desired)
        if path.read_bytes() != desired:
            raise RuntimeError("Test fixture patch was not preserved")
        state = {"backup_name": stamp, "installed_sha256": _digest(desired)}
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        dest = PACKAGE / "full_files" / TARGET
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(desired)
        print("PATCHED_TEST", TARGET)
        print("FULL_TEST_FILE", dest)
    except Exception:
        path.write_bytes(original)
        STATE.unlink(missing_ok=True)
        raise


def rollback_fixture_patch() -> None:
    if not STATE.exists():
        print("TEST_ROLLBACK_NOT_REQUIRED")
        return
    state = json.loads(STATE.read_text("utf-8"))
    path = ROOT / TARGET
    if _digest(path.read_bytes()) != state["installed_sha256"]:
        raise ValueError("Test changed since applying fix; refusing rollback")
    old = (PACKAGE / "backup" / state["backup_name"] / TARGET.name).read_bytes()
    path.write_bytes(old)
    STATE.unlink()
    print("ROLLED_BACK_TEST", TARGET)


def main() -> None:
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "--rollback"):
        raise SystemExit("Usage: python -m phase168_r3_41b1_citation_fixture_fix.fix_test [--rollback]")
    if len(sys.argv) == 2:
        rollback_fixture_patch()
    else:
        apply_fixture_patch()


if __name__ == "__main__":
    main()
