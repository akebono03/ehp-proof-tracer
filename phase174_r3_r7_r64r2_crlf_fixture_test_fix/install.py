"""R64R2: correct only the CRLF fixture in one existing R64R1 pytest function.

No production code, proof, source, reference, or mathematical rule changes.
The existing R64R1 installer and R64 audit are separately pinned.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess

PACKAGE = "phase174_r3_r7_r64r2_crlf_fixture_test_fix"
TARGET = "phase174_r3_r7_r64r1_pytest_tmp_path_fix/tests/test_install.py"
PINNED_UNCHANGED = {
    "phase174_r3_r7_r64r1_pytest_tmp_path_fix/install.py": "a7990fd025580d0c7de7cb5e917865aeef48545e",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py": "639b2290aeb09ead23367d0ed8a02e8f64ad6d6f",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/tests/test_audit.py": "3122053b18dd87c57e78c2d4385f01852b51c708",
}
EXPECTED_OLD_BLOB = "ae6d1f0e8266fad222e607fc9548ab60061e14d5"
EXPECTED_FIXED_BLOB = "bde087fa884eccab7138eb67b8015690558b6a27"
ORIGINAL_FUNCTION = 'def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:\n    create_review_fixture(tmp_path)\n    target = tmp_path / TARGET\n    target.write_bytes(target.read_bytes().replace(b"\\n", b"\\r\\n"))\n    status, _original, after = review(tmp_path)\n    assert status == "PATCH_REQUIRED"\n    assert b"\\r\\n" in after\n    target.write_bytes(after)\n    assert review(tmp_path)[0] == "ALREADY_APPLIED"\n'
REPLACEMENT_FUNCTION = 'def test_review_accepts_crlf_line_endings(tmp_path: Path) -> None:\n    create_review_fixture(tmp_path)\n    target = tmp_path / TARGET\n    normalized = target.read_bytes().replace(b"\\r\\n", b"\\n")\n    target.write_bytes(normalized.replace(b"\\n", b"\\r\\n"))\n    status, _original, after = review(tmp_path)\n    assert status == "PATCH_REQUIRED"\n    assert b"\\r\\n" in after\n    assert b"\\r\\r\\n" not in after\n    target.write_bytes(after)\n    assert review(tmp_path)[0] == "ALREADY_APPLIED"\n'


def git_blob_sha(data: bytes) -> str:
    """Return the Git blob hash for exact file bytes."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def normalized_contents(data: bytes) -> tuple[str, bytes, str]:
    """Accept LF/CRLF, reject stray CR, and retain the file's BOM and EOL."""
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    remainder = data[len(bom):]
    if b"\r" in remainder.replace(b"\r\n", b""):
        raise RuntimeError("R64R2_UNEXPECTED_CR_ONLY_OR_DOUBLE_CR")
    eol = "\r\n" if b"\r\n" in remainder else "\n"
    return remainder.decode("utf-8").replace("\r\n", "\n"), bom, eol


def patch_test(source: str) -> str:
    """Replace precisely the reviewed test function, leaving every other byte alone."""
    tree = ast.parse(source)
    matches = tuple(node for node in tree.body
                    if isinstance(node, ast.FunctionDef)
                    and node.name == "test_review_accepts_crlf_line_endings")
    if len(matches) != 1 or source.count(ORIGINAL_FUNCTION) != 1:
        raise RuntimeError("R64R2_UNREVIEWED_OR_AMBIGUOUS_FUNCTION")
    result = source.replace(ORIGINAL_FUNCTION, REPLACEMENT_FUNCTION, 1)
    ast.parse(result)
    if result.replace(REPLACEMENT_FUNCTION, ORIGINAL_FUNCTION, 1) != source:
        raise RuntimeError("R64R2_NONMINIMAL_PATCH")
    return result


def review(root: Path) -> tuple[str, bytes, bytes]:
    """Verify existing installer/audit, then plan exactly one pytest-only edit."""
    if not root.is_dir():
        raise RuntimeError("R64R2_REPOSITORY_MISSING")
    for relative, expected in PINNED_UNCHANGED.items():
        path = root / relative
        if not path.is_file():
            raise RuntimeError("R64R2_REQUIRED_FILE_MISSING: " + relative)
        contents, _bom, _eol = normalized_contents(path.read_bytes())
        if git_blob_sha(contents.encode("utf-8")) != expected:
            raise RuntimeError("R64R2_REVIEWED_SOURCE_MISMATCH: " + relative)
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R64R2_TARGET_MISSING")
    original = path.read_bytes()
    content, bom, eol = normalized_contents(original)
    current_hash = git_blob_sha(content.encode("utf-8"))
    if current_hash == EXPECTED_OLD_BLOB:
        revised = patch_test(content)
        if git_blob_sha(revised.encode("utf-8")) != EXPECTED_FIXED_BLOB:
            raise RuntimeError("R64R2_UNEXPECTED_REPLACEMENT_BLOB")
        status = "PATCH_REQUIRED"
    elif current_hash == EXPECTED_FIXED_BLOB:
        if content.count(REPLACEMENT_FUNCTION) != 1:
            raise RuntimeError("R64R2_FIXED_FUNCTION_MISSING")
        revised = content
        status = "ALREADY_APPLIED"
    else:
        raise RuntimeError("R64R2_UNREVIEWED_TARGET_BLOB: " + current_hash)
    after = bom + revised.replace("\n", eol).encode("utf-8")
    return status, original, after


def local_git_head(root: Path) -> str:
    """Report HEAD without requiring an obsolete fixed SHA."""
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                            capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError("R64R2_GIT_HEAD_UNAVAILABLE")
    return result.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    status, original, after = review(root)
    print("PHASE174_R64R2_SOURCE_GUARD=PASS")
    print("PHASE174_R64R2_SOURCE_PINS=4")
    print("PHASE174_R64R2_LOCAL_HEAD=" + local_git_head(root))
    print("PHASE174_R64R2_PATCH_STATUS=" + status)
    print("PHASE174_R64R2_PRODUCTION_CHANGES=0")
    print("PHASE174_R64R2_NEW_GIVEN=0")
    print("PHASE174_R64R2_NEW_MATHEMATICAL_RULES=0")
    if opts.dry_run:
        print("PHASE174_R64R2_GATE=PASS_R64R2_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if original != after:
        (root / TARGET).write_bytes(after)
        if (root / TARGET).read_bytes() != after:
            raise RuntimeError("R64R2_WRITE_VERIFY_FAILED")
    print("PHASE174_R64R2_GATE=PASS_R64R2_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
