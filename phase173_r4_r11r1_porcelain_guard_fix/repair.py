"""Correct one R4-R11 install.preflight Git porcelain comparison, fail closed."""
from __future__ import annotations

import argparse
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import tempfile

REVIEWED_HEAD = "de390132fcdcb52d2d5c16d2259f2b1073f09ad9"
TARGET = "phase165_r55_nk_only_goal.py"
INSTALL = "phase173_r4_r11_zero_public_connection/install.py"
EXPECTED_BASE_BLOB = "b207b8169590e634229d412324d857ffb3857939"
ORIGINAL_HASH = "28c1933a415664e203511ee6c9494d58219ac6b0e176294f97afa7ee85986f2d"
PATCHED_HASH = "88257618307614d73824c20f5be4d65b9190f0d875baeeb4f57291c195bf8cd8"

PACKAGE_HASHES = {'route.py': 'c4bb399cbee1d25e01d74b98470309b8cfe23869e5a333af9e3c076fd0d3ae05', 'source.py': '38f185dd9be6b20794eedb859f3bf4f708d47593d2633a58308f02e276154390', 'verify.py': 'b7f3980a1958ed7fc1f087012cb0edc371b380cbef6d61cd65fb5a737f1d6d73', 'run.ps1': 'adaff4f1efc458ad7bea0e9ebeda699683978d7d342564bd1d203f1ecf0df02f', 'search_group_from_registered_goal_FULL.py.txt': 'be8ab5263a41bf07df6e5480ec3611feb7990bc5c55780929dc711fa20ac151b', 'tests/test_route.py': '247647c13bc7066eaca5eb8207d6ccde6b6285413abb30d35afc2dd4516bf797', 'tests/test_install.py': 'fedce0657679fd7731f6f228dbd02a8a099dc067a0013be8431ea46b57818145'}


def git(root: Path, *args: str) -> str:
    """Return Git output with leading porcelain whitespace preserved."""
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Git command failed: " + " ".join(args) + ": "
                           + result.stderr[:300])
    return result.stdout.rstrip("\r\n")


def checked_tracked_status(status: str) -> bool:
    """Permit exactly R4-R11's one unstaged production edit."""
    return status == " M " + TARGET


def prepared_replacement(original: bytes, replacement: bytes) -> bytes:
    """Verify the exact one-line repair, without changing imported code."""
    old_line = b'not in ("", " M " + TARGET):'
    new_line = b'not in ("", "M " + TARGET):'
    if sha256(original).hexdigest() != ORIGINAL_HASH:
        raise RuntimeError("Unreviewed original R4-R11 installer")
    if original.count(old_line) != 1 or replacement != original.replace(old_line, new_line):
        raise RuntimeError("Not the exact reviewed comparison repair")
    if sha256(replacement).hexdigest() != PATCHED_HASH:
        raise RuntimeError("Replacement installer digest mismatch")
    return replacement


def preflight(root: Path) -> tuple[Path, bytes, bytes, bool]:
    """Guard HEAD, all tracked changes, and exact previously installed code."""
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Run at the repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop")
    head = git(root, "rev-parse", "HEAD")
    if head != REVIEWED_HEAD:
        raise RuntimeError("Unexpected local HEAD: " + head)
    remote = git(root, "ls-remote", "--exit-code", "origin", "refs/heads/develop")
    if not remote.split() or remote.split()[0] != head:
        raise RuntimeError("Remote develop HEAD differs")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged files require review")
    if not checked_tracked_status(git(root, "status", "--porcelain", "--untracked-files=no")):
        raise RuntimeError("Unexpected tracked changes: no file has been overwritten")
    if git(root, "rev-parse", "HEAD:" + TARGET) != EXPECTED_BASE_BLOB:
        raise RuntimeError("Committed target source blob mismatch")

    for relative, digest in PACKAGE_HASHES.items():
        current = root / "phase173_r4_r11_zero_public_connection" / relative
        if not current.is_file() or sha256(current.read_bytes()).hexdigest() != digest:
            raise RuntimeError("R4-R11 package content differs: " + relative)

    from phase173_r4_r11_zero_public_connection import install as original_install
    from phase173_r4_r11_zero_public_connection.install import SOURCE_BLOBS

    for path, blob in SOURCE_BLOBS.items():
        if not (root / path).is_file() or git(root, "hash-object", "--", path) != blob:
            raise RuntimeError("Reviewed source differs: " + path)
    core = root / "phase173_r4_r10_general_toda56_core/core.py"
    if not core.is_file() or sha256(core.read_bytes()).hexdigest() != (
        "453b13c25a1b92e54ce574469734f547c6a52577b817c7bcd1d5ba2df7718f68"
    ):
        raise RuntimeError("R4-R10 inference core differs")
    baseline = subprocess.run(
        ["git", "show", "HEAD:" + TARGET], cwd=root,
        check=False, capture_output=True,
    )
    if baseline.returncode != 0:
        raise RuntimeError("Cannot read committed target source")
    replacement_fn = root / "phase173_r4_r11_zero_public_connection" / (
        "search_group_from_registered_goal_FULL.py.txt"
    )
    target_file = root / TARGET
    if not replacement_fn.is_file() or not target_file.is_file():
        raise RuntimeError("Installed R4-R11 files missing")
    expected_target = original_install.patched_source(
        baseline.stdout, replacement_fn.read_text(encoding="utf-8"),
    )
    if target_file.read_bytes() != expected_target:
        raise RuntimeError("Production code is not the exact installed R4-R11 function")

    installer_path = root / INSTALL
    original = installer_path.read_bytes()
    replacement = Path(__file__).with_name("replacement_install.py.txt").read_bytes()
    if sha256(replacement).hexdigest() != PATCHED_HASH:
        raise RuntimeError("Repair file differs from the reviewed package")
    if sha256(original).hexdigest() == PATCHED_HASH:
        return installer_path, original, replacement, True
    prepared_replacement(original, replacement)
    return installer_path, original, replacement, False


def apply_fix(root: Path, *, dry_run: bool) -> str:
    """Modify only the installer; never alter or reset production sources."""
    installer_path, original, replacement, already = preflight(root)
    print("PHASE173_R4_R11R1_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R11R1_HEAD=" + REVIEWED_HEAD, flush=True)
    print("PHASE173_R4_R11R1_EXISTING_PRODUCTION_PATCH=VERIFIED", flush=True)
    if already:
        print("PHASE173_R4_R11R1_ALREADY_INSTALLED=True", flush=True)
        return "ALREADY_INSTALLED"
    if dry_run:
        print("PHASE173_R4_R11R1_DRY_RUN=PASS", flush=True)
        return "DRY_RUN_PASS"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", dir=installer_path.parent, prefix=".r4r11r1_",
            suffix=".tmp", delete=False,
        ) as stream:
            temporary = stream.name
            stream.write(replacement)
            stream.flush()
            os.fsync(stream.fileno())
        if installer_path.read_bytes() != original:
            raise RuntimeError("Installer changed during verification")
        os.replace(temporary, installer_path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
    print("PHASE173_R4_R11R1_PATCHED=" + INSTALL, flush=True)
    return "PATCHED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    apply_fix(Path(args.root).resolve(), dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
