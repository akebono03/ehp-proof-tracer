"""Guarded, reversible adjustment of Phase R3H tests for the R3I1 proof frontier."""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
TARGET = ROOT / "phase169_r3h_toda53_hopf_source" / "tests" / "test_phase169_r3h_toda53_hopf_source.py"
REVIEWED = PACKAGE / "reviewed_r3h" / "test_phase169_r3h_toda53_hopf_source.py"
AFTER = PACKAGE / "full_tests" / "test_phase169_r3h_toda53_hopf_source.py"
BACKUP = PACKAGE / "output" / "test_phase169_r3h_toda53_hopf_source.py.before"
COMMITTED_BLOB = "0d6b2a4ca34534425fae125ce29f0523d0cdd71e"


def to_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def install() -> int:
    if not all(path.is_file() for path in (TARGET, REVIEWED, AFTER)):
        print("REFUSED: legacy Phase R3H test missing")
        return 2
    if to_blob(REVIEWED.read_bytes()) != COMMITTED_BLOB:
        print("REFUSED: reviewed test changed")
        return 3
    before = TARGET.read_bytes()
    if before != REVIEWED.read_bytes():
        print("REFUSED: local legacy test is not the reviewed R3H version")
        return 4
    if BACKUP.exists():
        print("REFUSED: previous legacy-test backup exists")
        return 5
    import ast
    ast.parse(AFTER.read_text(encoding="utf-8"))
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(before)
    # Preserve source file CRLF if any.
    edited = AFTER.read_bytes()
    if b"\r\n" in before and b"\r\n" not in edited:
        edited = edited.replace(b"\n", b"\r\n")
    TARGET.write_bytes(edited)
    print("UPDATED_R3H_TEST:", TARGET)
    print("R3H_TEST_BACKUP:", BACKUP)
    return 0


def restore() -> int:
    if not BACKUP.is_file():
        print("REFUSED: legacy test backup absent")
        return 6
    if not TARGET.is_file():
        print("REFUSED: legacy test target absent")
        return 7
    if TARGET.read_bytes() == BACKUP.read_bytes():
        BACKUP.unlink()
        print("R3H_TEST_ALREADY_RESTORED")
        return 0
    expected = AFTER.read_bytes()
    if b"\r\n" in BACKUP.read_bytes() and b"\r\n" not in expected:
        expected = expected.replace(b"\n", b"\r\n")
    if TARGET.read_bytes() != expected:
        print("REFUSED: legacy test changed since R3I1 install")
        return 8
    TARGET.write_bytes(BACKUP.read_bytes())
    BACKUP.unlink()
    print("RESTORED_R3H_TEST:", TARGET)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("install", "restore"):
        raise SystemExit("Usage: patch_r3h_tests.py install|restore")
    raise SystemExit(install() if sys.argv[1] == "install" else restore())
