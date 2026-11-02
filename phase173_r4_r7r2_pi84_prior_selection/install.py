"""Guarded installer for the single Phase 173 R4-R7R2 source-context change."""
from __future__ import annotations

import argparse
from hashlib import sha1, sha256
from pathlib import Path
import subprocess

REVIEWED_HEAD = "f83f45f50739eebe179a16fd127b45a019a262ab"
TARGET_RELATIVE = "phase173_r4_r7_source_first_rule/source.py"
EXPECTED_BLOB = "b9b2ddee9296a5eed44163694e28e7789b14aba9"
REPLACEMENT_BLOB = "abdc05c731e5ede1258962705bc577b5307b6f38"
REPLACEMENT_SHA256 = "a80f35c8f5de31a5d5ed3fbdb5f86cf41d789a0fd8c3e6cd64f19bf72df43504"
SOURCE_GUARDS = {
    "phase173_r4_r7_source_first_rule/rule.py": "5113c88e263c28b748c1543ec57bbcedb3eff5bf",
    "phase173_r4_r7_source_first_rule/source.py": EXPECTED_BLOB,
    "phase173_r4_r7_source_first_rule/tests/test_rule.py": "24f8be3c1407ba653547b2b987efa904fdb58347",
    "phase173_r4_r7r1_pi84_premise_diagnostic/audit.py": "bcaf8feb008113eba0e8cdc1661f9ed931728c92",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase173_r4_r1_public_connection/route.py": "fa79655aa24a88d5e7dd46d8c7a00ae04aeb15d4",
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if completed.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + completed.stderr.strip()[:700])
    return completed.stdout.strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def blob_hash(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def replacement_bytes() -> bytes:
    source = Path(__file__).with_name("replacement_source.py.txt").read_bytes()
    if (sha256(source).hexdigest() != REPLACEMENT_SHA256
            or blob_hash(source) != REPLACEMENT_BLOB):
        raise RuntimeError("unreviewed replacement source")
    return source


def preflight(root: Path, *, remote: bool) -> str:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("not repository root")
    branch = git(root, "branch", "--show-current")
    head = git(root, "rev-parse", "HEAD")
    if branch != "develop" or head != REVIEWED_HEAD:
        raise RuntimeError("unreviewed develop HEAD: " + head)
    for file_name, expected in SOURCE_GUARDS.items():
        if (not (root / file_name).is_file()
                or git(root, "rev-parse", "HEAD:" + file_name) != expected):
            raise RuntimeError("unreviewed committed source: " + file_name)
    if remote:
        current = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
        if not current or current.split()[0] != REVIEWED_HEAD:
            raise RuntimeError("origin/develop differs from reviewed HEAD")
    replacement_bytes()
    path = root / TARGET_RELATIVE
    current = blob_hash(normalize(path.read_bytes()))
    if current not in (EXPECTED_BLOB, REPLACEMENT_BLOB):
        raise RuntimeError("unreviewed working-tree source content")
    dirty = git(root, "status", "--porcelain", "--untracked-files=no")
    if current == EXPECTED_BLOB:
        if dirty:
            raise RuntimeError("tracked files are dirty before install")
        return "NEEDS_INSTALL"
    if dirty != "M " + TARGET_RELATIVE:
        raise RuntimeError("unexpected tracked changes after install: " + dirty)
    return "ALREADY_INSTALLED"


def install(root: Path, *, dry_run: bool, remote: bool) -> str:
    state = preflight(root, remote=remote)
    print("PHASE173_R4_R7R2_REVIEWED_HEAD=" + REVIEWED_HEAD, flush=True)
    print("PHASE173_R4_R7R2_INSTALL_STATE=" + state, flush=True)
    if dry_run:
        print("PHASE173_R4_R7R2_RESULT=DRY_RUN_PASS", flush=True)
        return state
    if state == "NEEDS_INSTALL":
        target = root / TARGET_RELATIVE
        before = target.read_bytes()
        proposed = replacement_bytes()
        if b"\r\n" in before:
            proposed = proposed.replace(b"\n", b"\r\n")
        try:
            target.write_bytes(proposed)
            if preflight(root, remote=False) != "ALREADY_INSTALLED":
                raise RuntimeError("post-install source guard failed")
        except BaseException:
            target.write_bytes(before)
            raise
    print("PHASE173_R4_R7R2_RESULT=INSTALLED", flush=True)
    return state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-remote-check", action="store_true")
    args = parser.parse_args()
    try:
        install(args.root.resolve(), dry_run=args.dry_run,
                remote=not args.skip_remote_check)
    except Exception as exc:
        print("PHASE173_R4_R7R2_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
