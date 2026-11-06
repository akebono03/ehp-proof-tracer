"""Guarded R17R1 source-guard correction; never change tracked proof code."""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = Path("phase174_r3_r7_r17r1_historical_test_contract/audit.py")
PRIOR_RUNNER = Path("phase174_r3_r7_r17r1_historical_test_contract/run.ps1")
EXPECTED_HEAD = "388f63797a6aba61418bb93e734b8ce5999dc7f6"
OLD_SHA256 = "8e06ed616290600ca8de431e5fe9c8f1662ee4795b413fb857f5c4a20fdd7d03"
RUNNER_SHA256 = "a483de03c09de729a36e6ec97afa302cdbc81d750f36a01a19169e8d2b2e16f7"
AUDITED_TRACKED = (
    "phase173_r4_r15r17r3r3_typed_goal_display/tests/test_open_goals.py",
    "web_group_proof_common.py",
)
OLD_LINE = "    expected_changed = tuple(sorted((str(TEST_TARGET), str(DISPLAY_TARGET)))) if applied else ()\n"
NEW_LINE = "    expected_changed = expected_tracked_paths(applied=applied)\n"
INSERT_BEFORE = "def verify_source_and_state(*, applied: bool, root: Path = ROOT) -> dict[str, object]:\n"
NEW_HELPER = '''def expected_tracked_paths(*, applied: bool) -> tuple[str, ...]:
    """Use Git's repository-relative forward slash paths on every OS."""
    if type(applied) is not bool:
        raise TypeError("applied must be bool")
    if not applied:
        return ()
    return tuple(sorted((TEST_TARGET.as_posix(), DISPLAY_TARGET.as_posix())))


'''
BACKUP = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) /
          "EHPProofTracerAudit" / "phase174_r3_r7_r17r2" / "r17r1_audit.original.py")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def transform(source: str) -> str:
    """Change only the OS-sensitive worktree-file comparison."""
    if source.count(OLD_LINE) != 1 or source.count(INSERT_BEFORE) != 1:
        raise RuntimeError("Reviewed R17R1 guard anchor missing or duplicated")
    if "def expected_tracked_paths(" in source:
        raise RuntimeError("R17R2 guard already installed")
    transformed = source.replace(OLD_LINE, NEW_LINE, 1)
    transformed = transformed.replace(INSERT_BEFORE, NEW_HELPER + INSERT_BEFORE, 1)
    if transformed.count(NEW_LINE) != 1:
        raise RuntimeError("R17R2 guard did not install exactly once")
    compile(transformed, str(TARGET), "exec")
    return transformed


def normalized(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("Unexpected BOM in R17R1 audit source")
    text = data.decode("utf-8")
    if b"\r\n" in data:
        if b"\n" in data.replace(b"\r\n", b""):
            raise RuntimeError("Mixed EOLs are not accepted")
        text = text.replace("\r\n", "\n")
    elif "\r" in text:
        raise RuntimeError("Bare carriage return in source")
    return text


def patched_bytes(original: bytes) -> bytes:
    content = transform(normalized(original))
    if b"\r\n" in original:
        return content.replace("\n", "\r\n").encode("utf-8")
    return content.encode("utf-8")


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(("git",) + args, cwd=root, check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def verify_git_and_package(*, applied: bool = False, root: Path = ROOT) -> None:
    if Path(git("rev-parse", "--show-toplevel", root=root)).resolve() != root.resolve():
        raise RuntimeError("Extract R17R2 directly into the repo root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Only the reviewed develop branch is permitted")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Local and origin/develop must match the reviewed R17 HEAD")
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require review")
    modified = tuple(sorted(git("diff", "--name-only", root=root).splitlines()))
    expected = AUDITED_TRACKED if applied else ()
    if modified != expected:
        raise RuntimeError("Unexpected tracked changes during R17R2: " + str(modified))
    runner = root / PRIOR_RUNNER
    if not runner.is_file() or sha256(runner.read_bytes()) != RUNNER_SHA256:
        raise RuntimeError("The previously reviewed R17R1 runner has changed")
    if not (root / "phase174_r3_r7_r17_typed_map_open_goal" / "run.ps1").is_file():
        raise RuntimeError("Previously extracted R17 package is required")


def checked_state(*, root: Path = ROOT) -> str:
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("Previously extracted R17R1 audit.py is required")
    raw = path.read_bytes()
    old = sha256(raw) == OLD_SHA256
    new = False
    if not old:
        try:
            source = normalized(raw)
            new = (NEW_LINE in source and NEW_HELPER in source
                   and OLD_LINE not in source)
            if new and BACKUP.is_file():
                original = BACKUP.read_bytes()
                new = sha256(original) == OLD_SHA256 and raw == patched_bytes(original)
        except (RuntimeError, UnicodeError):
            new = False
    if old:
        return "REVIEWED_ORIGINAL"
    if new:
        return "EXACT_REVIEWED_PATCH"
    raise RuntimeError("The R17R1 audit script does not match the reviewed state")


def apply(*, root: Path = ROOT) -> str:
    verify_git_and_package(root=root)
    status = checked_state(root=root)
    if status == "EXACT_REVIEWED_PATCH":
        return "ALREADY_APPLIED"
    path = root / TARGET
    original = path.read_bytes()
    transformed = patched_bytes(original)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if BACKUP.exists() and BACKUP.read_bytes() != original:
        raise RuntimeError("Existing R17R2 backup differs; manual review required")
    BACKUP.write_bytes(original)
    temporary = path.with_suffix(".r17r2.tmp")
    if temporary.exists():
        raise RuntimeError("Temporary R17R2 file already exists")
    try:
        temporary.write_bytes(transformed)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    if checked_state(root=root) != "EXACT_REVIEWED_PATCH":
        raise RuntimeError("R17R2 patch verification failed")
    return "APPLIED"


def rollback(*, root: Path = ROOT) -> str:
    state = checked_state(root=root)
    if state == "REVIEWED_ORIGINAL":
        return "ALREADY_ORIGINAL"
    original = BACKUP.read_bytes()
    if sha256(original) != OLD_SHA256:
        raise RuntimeError("Stored R17R1 script backup is not the reviewed original")
    (root / TARGET).write_bytes(original)
    return "RESTORED"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    mode.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    if args.rollback:
        value = rollback()
    else:
        verify_git_and_package(applied=args.verify)
        if args.dry_run:
            status = checked_state()
            if status != "REVIEWED_ORIGINAL":
                raise RuntimeError("DryRun expects the original R17R1 audit script")
            predicted = patched_bytes((ROOT / TARGET).read_bytes())
            value = "PASS_PREFLIGHT_SHA=" + sha256(predicted)
        elif args.apply:
            value = apply()
        else:
            value = checked_state()
            if value != "EXACT_REVIEWED_PATCH":
                raise RuntimeError("R17R2 guard not yet applied")
    print("PHASE174_R3R7R17R2_GUARD=" + value)
    print("PHASE174_R3R7R17R2_TARGET=" + TARGET.as_posix())
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
