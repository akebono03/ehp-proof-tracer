"""Exact, source-guarded replacement of R18's per-profile evidence dependency."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase174_r3_r7_r18_delta_image_surjectivity/audit.py")
R18R1_PACKAGE = Path("phase174_r3_r7_r18r1_git_mixed_eol_guard")
R18R1_SOURCE = R18R1_PACKAGE / "replacement_audit.py.txt"
REPLACEMENT_SOURCE = Path(__file__).resolve().parent / "EXPECTED_REPLACEMENT_AUDIT.py.txt"
REPLACEMENT_FUNCTION = Path(__file__).resolve().parent / "REVIEWED_REPLACEMENT_VALIDATE_R17.py.txt"
EXPECTED_R18_ORIGINAL_SHA256 = "e0e0c986762f76dc601b0cdf6c01d81eece696dc2bb5f593ca0fd2debf045c73"
EXPECTED_R18R1_SHA256 = "7ff6ab7b4f4b7595c6e16216e8c3a8e1edf3845cc4dcfdb3165879e4c7f57aaa"
EXPECTED_R18R2_SHA256 = "7a70bd1368828b13ce7950da8d5fb246af3ddbc4775457d5ea5ba99555131222"
EXPECTED_LOCAL_R17_HEAD = "4d59298949c14dc02d8bfb6ec28da4624ed980da"
EXPECTED_R18_HEAD = "7ecd12f28b5943b105ac6a953be69b44eae4a26e"
R18_PREFIX = "phase174_r3_r7_r18_delta_image_surjectivity/"
FUNCTION_START = "def validate_prior_r17() -> dict[str, Any]:\n"
FUNCTION_END = "\ndef inspect_live_frontier() -> dict[str, Any]:\n"
BACKUP = (
    Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    / "EHPProofTracerAudit" / "phase174_r3_r7_r18r2" / "audit_r18r1_original.py"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=root, check=True, capture_output=True,
    ).stdout


def checked_replacement(root: Path = ROOT) -> tuple[bytes, bytes]:
    old_file = root / R18R1_SOURCE
    if not old_file.is_file():
        raise RuntimeError("Reviewed R18R1 package is required")
    before = old_file.read_bytes()
    if sha256(before) != EXPECTED_R18R1_SHA256:
        raise RuntimeError("R18R1 replacement was not the reviewed source")
    function = REPLACEMENT_FUNCTION.read_text(encoding="utf-8")
    after = REPLACEMENT_SOURCE.read_bytes()
    if (sha256(after) != EXPECTED_R18R2_SHA256
            or before.decode("utf-8").count(FUNCTION_START) != 1
            or before.decode("utf-8").count(FUNCTION_END) != 1
            or after != transform(before, function)):
        raise RuntimeError("Unreviewed R18R2 replacement source")
    compile(after, str(TARGET), "exec")
    return before, after


def transform(before: bytes, function: str) -> bytes:
    """Replace one complete function with no other source changes."""
    source = before.decode("utf-8")
    if source.count(FUNCTION_START) != 1 or source.count(FUNCTION_END) != 1:
        raise RuntimeError("Reviewed R18R1 function anchors missing or duplicated")
    if not function.startswith(FUNCTION_START) or not function.endswith("\n"):
        raise RuntimeError("Replacement must be the entire function")
    start = source.index(FUNCTION_START)
    end = source.index(FUNCTION_END, start)
    result = source[:start] + function + "\n" + source[end:]
    compile(result, str(TARGET), "exec")
    return result.encode("utf-8")


def source_state(root: Path = ROOT) -> str:
    contents = (root / TARGET).read_bytes()
    value = sha256(contents)
    if value == EXPECTED_R18_ORIGINAL_SHA256:
        return "REVIEWED_R18_ORIGINAL"
    if value == EXPECTED_R18R1_SHA256:
        return "R18R1_MIXED_EOL_CORRECTED"
    if value == EXPECTED_R18R2_SHA256:
        _, expected = checked_replacement(root=root)
        if contents == expected:
            return "R18R2_EVIDENCE_REVALIDATION_INSTALLED"
    raise RuntimeError("R18 audit.py has unexpected content")


def verify_git_and_source(root: Path = ROOT) -> dict[str, str]:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R18R2 directly below the repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Only the reviewed develop branch is allowed")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if remote != EXPECTED_R18_HEAD or local not in (
        EXPECTED_LOCAL_R17_HEAD, EXPECTED_R18_HEAD,
    ):
        raise RuntimeError("GitHub or local develop HEAD changed since review")
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged work requires separate review")
    changed = tuple(git("diff", "--name-only", root=root).splitlines())
    state = source_state(root=root)
    allowed = (TARGET.as_posix(),) if local == EXPECTED_R18_HEAD and state != "REVIEWED_R18_ORIGINAL" else ()
    if changed != allowed:
        raise RuntimeError("Unreviewed tracked changes: " + repr(changed))
    git_bytes("merge-base", "--is-ancestor", EXPECTED_LOCAL_R17_HEAD,
              EXPECTED_R18_HEAD, root=root)
    commits = git("rev-list", EXPECTED_LOCAL_R17_HEAD + ".." + EXPECTED_R18_HEAD,
                  root=root).splitlines()
    changed_in_commit = git("diff", "--name-only", EXPECTED_LOCAL_R17_HEAD,
                            EXPECTED_R18_HEAD, root=root).splitlines()
    if (len(commits) != 1 or not changed_in_commit
            or any(not name.startswith(R18_PREFIX) for name in changed_in_commit)):
        raise RuntimeError("Unreviewed R18 merge lineage")
    reviewed = git_bytes("show", "origin/develop:" + TARGET.as_posix(), root=root)
    if sha256(reviewed) != EXPECTED_R18_ORIGINAL_SHA256:
        raise RuntimeError("R18 original Git source was changed")
    if not (root / R18R1_PACKAGE / "patch.py").is_file():
        raise RuntimeError("Previously reviewed R18R1 patch is missing")
    checked_replacement(root=root)
    return {"local_head": local, "remote_head": remote, "source_state": state}


def apply(root: Path = ROOT) -> str:
    state = verify_git_and_source(root=root)["source_state"]
    if state == "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
        if not BACKUP.is_file() or sha256(BACKUP.read_bytes()) != EXPECTED_R18R1_SHA256:
            raise RuntimeError("Prior R18R2 backup is missing or differs")
        return "ALREADY_APPLIED"
    if state != "R18R1_MIXED_EOL_CORRECTED":
        raise RuntimeError("Apply the R18R1 EOL correction first")
    before, after = checked_replacement(root=root)
    if (root / TARGET).read_bytes() != before:
        raise RuntimeError("R18R1 audit source differs from reviewed replacement")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.is_file() and BACKUP.read_bytes() != before:
        raise RuntimeError("Existing R18R2 backup requires review")
    BACKUP.write_bytes(before)
    temporary = (root / TARGET).with_suffix(".r18r2.tmp")
    if temporary.exists():
        raise RuntimeError("R18R2 temporary patch file already exists")
    try:
        temporary.write_bytes(after)
        os.replace(temporary, root / TARGET)
    finally:
        if temporary.exists():
            temporary.unlink()
    if verify_git_and_source(root=root)["source_state"] != "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
        raise RuntimeError("R18R2 final source verification failed")
    return "APPLIED"


def rollback(root: Path = ROOT) -> str:
    state = source_state(root=root)
    if state in ("REVIEWED_R18_ORIGINAL", "R18R1_MIXED_EOL_CORRECTED"):
        return "NO_R18R2_CHANGE"
    if not BACKUP.is_file():
        raise RuntimeError("R18R2 backup missing; manual review required")
    old = BACKUP.read_bytes()
    if sha256(old) != EXPECTED_R18R1_SHA256:
        raise RuntimeError("R18R2 backup differs from reviewed R18R1 version")
    (root / TARGET).write_bytes(old)
    return "RESTORED_R18R1_SOURCE"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--apply", action="store_true")
    actions.add_argument("--verify", action="store_true")
    actions.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    if args.rollback:
        result = rollback()
    elif args.apply:
        result = apply()
    else:
        state = verify_git_and_source()["source_state"]
        if args.verify and state != "R18R2_EVIDENCE_REVALIDATION_INSTALLED":
            raise RuntimeError("R18R2 replacement not installed")
        result = "PREFLIGHT_" + state if args.dry_run else "VERIFIED_" + state
    print("PHASE174_R3R7R18R2_PATCH=" + result)
    print("PHASE174_R3R7R18R2_TARGET=" + TARGET.as_posix())
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
