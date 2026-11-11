"""Fix only R64's tmp_path mkdir precondition; all audited sources remain pinned."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

PACKAGE = "phase174_r3_r7_r64r1_pytest_tmp_path_fix"
TARGET = "phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py"
PINNED_UNCHANGED = {
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py": "639b2290aeb09ead23367d0ed8a02e8f64ad6d6f",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/run.ps1": "3b3f31425f06213136fe88492fe8402ba90fb4c8",
}
EXPECTED_OLD_BLOB = "cd415c6f60f2a20ac2a49c9ccea8619afdae0e28"
EXPECTED_FIXED_BLOB = "3122053b18dd87c57e78c2d4385f01852b51c708"
ORIGINAL_FUNCTION = 'def test_source_guard_rejects_tamper(tmp_path: Path) -> None:\n    relative = next(iter(PINS))\n    target = tmp_path / relative\n    target.parent.mkdir(parents=True)\n    target.write_bytes(b"unreviewed")\n    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):\n        source_guard(tmp_path)\n'
REPLACEMENT_FUNCTION = 'def test_source_guard_rejects_tamper(tmp_path: Path) -> None:\n    relative = next(iter(PINS))\n    target = tmp_path / relative\n    target.parent.mkdir(parents=True, exist_ok=True)\n    target.write_bytes(b"unreviewed")\n    with pytest.raises(RuntimeError, match="R64_SOURCE_BLOB_MISMATCH"):\n        source_guard(tmp_path)\n'


def git_blob_sha(data: bytes) -> str:
    """Hash the exact bytes as a Git blob."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalized_contents(data: bytes) -> tuple[str, bytes, str]:
    """Allow whole-file LF or CRLF, preserve a UTF-8 BOM, reject CR-only."""
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    remainder = data[len(bom):]
    if b"\r" in remainder.replace(b"\r\n", b""):
        raise RuntimeError("R64R1_UNEXPECTED_CR_ONLY")
    eol = "\r\n" if b"\r\n" in remainder else "\n"
    return remainder.decode("utf-8").replace("\r\n", "\n"), bom, eol


def patch_test(source: str) -> str:
    """Replace one fully verified function, not an arbitrary mkdir occurrence."""
    parsed = ast.parse(source)
    matches = [item for item in parsed.body
               if isinstance(item, ast.FunctionDef)
               and item.name == "test_source_guard_rejects_tamper"]
    if len(matches) != 1 or source.count(ORIGINAL_FUNCTION) != 1:
        raise RuntimeError("R64R1_UNREVIEWED_OR_AMBIGUOUS_FUNCTION")
    patched = source.replace(ORIGINAL_FUNCTION, REPLACEMENT_FUNCTION, 1)
    ast.parse(patched)
    if patched.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION, 1) != source:
        raise RuntimeError("R64R1_PATCH_NOT_MINIMAL")
    return patched


def review(root: Path) -> tuple[str, bytes, bytes]:
    """Pin the original audit, test and runner independently of repository HEAD."""
    if not root.is_dir():
        raise RuntimeError("R64R1_REPOSITORY_DIRECTORY_MISSING")
    for relative, expected in PINNED_UNCHANGED.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError("R64R1_REQUIRED_FILE_MISSING: " + relative)
        content, _bom, _eol = normalized_contents(path.read_bytes())
        if git_blob_sha(content.encode("utf-8")) != expected:
            raise RuntimeError("R64R1_UNREVIEWED_SOURCE: " + relative)
    target = root / TARGET
    if not target.is_file():
        raise RuntimeError("R64R1_TEST_FILE_MISSING")
    original = target.read_bytes()
    content, bom, eol = normalized_contents(original)
    current_hash = git_blob_sha(content.encode("utf-8"))
    if current_hash == EXPECTED_OLD_BLOB:
        revised = patch_test(content)
        if git_blob_sha(revised.encode("utf-8")) != EXPECTED_FIXED_BLOB:
            raise RuntimeError("R64R1_UNEXPECTED_REPLACEMENT_BLOB")
        status = "PATCH_REQUIRED"
    elif current_hash == EXPECTED_FIXED_BLOB:
        if content.count(REPLACEMENT_FUNCTION) != 1:
            raise RuntimeError("R64R1_FIXED_FUNCTION_MISSING")
        revised = content
        status = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R64R1_UNREVIEWED_TEST_BLOB: " + current_hash)
    after = bom + revised.replace("\n", eol).encode("utf-8")
    return status, original, after


def git_local_head(root: Path) -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                            text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("R64R1_GIT_HEAD_UNAVAILABLE")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    status, original, after = review(root)
    head = git_local_head(root)
    print("PHASE174_R64R1_SOURCE_GUARD=PASS")
    print("PHASE174_R64R1_SOURCE_PINS=3")
    print("PHASE174_R64R1_LOCAL_HEAD=" + head)
    print("PHASE174_R64R1_PATCH_STATUS=" + status)
    print("PHASE174_R64R1_PRODUCTION_CHANGES=0")
    print("PHASE174_R64R1_NEW_GIVEN=0")
    print("PHASE174_R64R1_NEW_MATHEMATICAL_RULES=0")
    if options.dry_run:
        print("PHASE174_R64R1_GATE=PASS_R64R1_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if original != after:
        (root / TARGET).write_bytes(after)
        actual = (root / TARGET).read_bytes()
        if actual != after:
            raise RuntimeError("R64R1_INSTALL_VERIFY_FAILED")
    print("PHASE174_R64R1_GATE=PASS_R64R1_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
