"""Safe installation of a source-cited Reference-body fallback (Phase 174 R3-R6-R4R1).

Two existing full modules are replaced ONLY after comparing their normalized
contents to pinned approved originals, then preserving their newline styles.
Neither backward-search logic nor any registered GIVEN is modified.
"""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path("phase174_r3_r6_r4r1_cited_reference_link_fix")
PUBLIC_REF = Path("phase168_r3_37c_reference_projection.py")
SOURCE_REF = Path("phase174_r3_r6_r4_common_reference/projection.py")
REVIEWED_HEAD = "f2e148afefb11eb0b0ca31da67c65ec1ffe9e1e9"
REVIEWED_REMOTE_BLOB = "754e63cf4beee3c882c601dbe4b97cb8ecbdc4d2"
REVIEWED_R4_SHA256 = "f8268429ba7c0751d20feea533fd5bad5d6a94912ec776f788be3c3e006b81ec"
REVIEWED_SOURCE_SHA256 = "fd848af37cd0debd8bc0f8b26d59c4415670f043bfa416d40d2df8218e10a188"
REVIEWED_OUTPUT_SHA256 = {
    PUBLIC_REF.as_posix(): "a58da77164fbc344b5a5c8fafb4a22081122d003abc62f905b5652e32fb29b9a",
    SOURCE_REF.as_posix(): "bde402ac49186f63645a559558c9e1bbaa465447d65c999e25d3ac29a749aba9",
}


def _git(*args: str) -> bytes:
    result = subprocess.run(("git",) + args, cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise ValueError("Git preflight rejected " + str(args) + ": "
                         + result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def _git_blob(raw: bytes) -> str:
    return sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()


def _normalized(raw: bytes) -> bytes:
    data = raw[3:] if raw.startswith(b"\xef\xbb\xbf") else raw
    return data.replace(b"\r\n", b"\n")


def _normalized_sha256(raw: bytes) -> str:
    return sha256(_normalized(raw)).hexdigest()


def _reapply_eol(source: bytes, new_lf_bytes: bytes) -> bytes:
    """Preserve a reviewed file's BOM and uniform line-ending convention."""
    bom = b"\xef\xbb\xbf" if source.startswith(b"\xef\xbb\xbf") else b""
    data = source[len(bom):]
    without_crlf = data.replace(b"\r\n", b"")
    if b"\n" in without_crlf or b"\r" in without_crlf:
        if b"\r\n" in data:
            raise ValueError("Mixed or unsupported EOL; refuse to rewrite")
        if b"\r" in without_crlf:
            raise ValueError("CR-only EOL is unsupported")
        return bom + new_lf_bytes
    if b"\r\n" in data:
        return bom + new_lf_bytes.replace(b"\n", b"\r\n")
    return bom + new_lf_bytes


def _reviewed_source(path: Path, expected_sha: str, generated: Path) -> bytes:
    original = (ROOT / path).read_bytes()
    current_sha = _normalized_sha256(original)
    new_lf = (ROOT / PACKAGE / generated).read_bytes()
    expected_output_sha = sha256(new_lf).hexdigest()
    if expected_output_sha != REVIEWED_OUTPUT_SHA256[path.as_posix()]:
        raise ValueError("Unreviewed generated replacement: " + path.as_posix())
    if current_sha == expected_output_sha:
        return original
    if current_sha != expected_sha:
        raise ValueError("Unreviewed local changes: " + path.as_posix()
                         + "; expected " + expected_sha + " found " + current_sha)
    return _reapply_eol(original, new_lf)


def reviewed_changes() -> tuple[tuple[Path, bytes, bool], ...]:
    """Check GitHub HEAD and both exact reviewed source modules before writing."""
    branch = _git("branch", "--show-current").decode("ascii").strip()
    local_head = _git("rev-parse", "HEAD").decode("ascii").strip()
    remote_head = _git("rev-parse", "origin/develop").decode("ascii").strip()
    print("PHASE174_R3R6R4R1_BRANCH=" + branch)
    print("PHASE174_R3R6R4R1_LOCAL_HEAD=" + local_head)
    print("PHASE174_R3R6R4R1_REMOTE_HEAD=" + remote_head)
    if branch != "develop" or local_head != REVIEWED_HEAD or remote_head != REVIEWED_HEAD:
        raise ValueError("Unreviewed HEAD or branch; no changes applied")
    for path in (PUBLIC_REF, SOURCE_REF):
        if _git("diff", "--cached", "--name-only", "--", path.as_posix()).strip():
            raise ValueError("Staged target changes require review: " + path.as_posix())
    if _git_blob(_git("show", f"{REVIEWED_HEAD}:{PUBLIC_REF.as_posix()}")) != REVIEWED_REMOTE_BLOB:
        raise ValueError("Public Reference baseline differs from reviewed GitHub")

    files = (
        (PUBLIC_REF, REVIEWED_R4_SHA256,
         Path("output/phase168_r3_37c_reference_projection.py.FULL.py")),
        (SOURCE_REF, REVIEWED_SOURCE_SHA256,
         Path("output/phase174_r3_r6_r4_common_reference__projection.py.FULL.py")),
    )
    reviewed = []
    for path, baseline_sha, generated in files:
        original = (ROOT / path).read_bytes()
        candidate = _reviewed_source(path, baseline_sha, generated)
        installed = candidate == original
        print("PHASE174_R3R6R4R1_TARGET_" + path.name.replace(".", "_")
              + "_ALREADY_INSTALLED=" + str(installed))
        reviewed.append((path, candidate, installed))
    return tuple(reviewed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    changes = reviewed_changes()
    print("PHASE174_R3R6R4R1_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6R4R1_PRODUCTION_TARGETS=2")
    print("PHASE174_R3R6R4R1_NEW_GIVEN=0")
    if args.dry_run:
        print("PHASE174_R3R6R4R1_DRY_RUN=PASS")
        return 0
    # All preflights have succeeded. No other files are touched.
    for path, new_content, installed in changes:
        if not installed:
            (ROOT / path).write_bytes(new_content)
    print("PHASE174_R3R6R4R1_APPLIED=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
