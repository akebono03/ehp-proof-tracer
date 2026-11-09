"""R43R2: apply an exact fail-closed allowance for a reviewed R43 change."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PREVIOUS = ROOT / "phase174_r3_r7_r43r1_r3_sha_pin_fix"
R43 = ROOT / "phase174_r3_r7_r43_public_ehp_map_property_wiring"
TARGET = PREVIOUS / "install.py"
EXPECTED_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
PUBLIC_TARGET = "phase165_r52_r9_shared_math.py"
ORIGINAL_INSTALL_SHA256 = "dbf35b58f5a23747cec9f9da401cf00f58f157bd83ef508d280804c6934f63ba"
REVIEWED_R43_GUARD_SHA256 = "6b030ba62b36dea14f08b8823974c485853f9101652a26236b12710b80d43c8a"
CORRECTED_R43_GUARD_SHA256 = "52bda02f8f63c217bb7b90fb11fc2d58a4e852a0645c460322872faa3685543c"


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def normalized(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n")


def sha256(content: bytes) -> str:
    return hashlib.sha256(normalized(content)).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Only one exactly reviewed R43 target edit is an approved exception."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43R2 at the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43R2 requires develop")
    local = git("rev-parse", "HEAD")
    remote_data = git("ls-remote", "origin", "refs/heads/develop").split()
    remote = remote_data[0] if remote_data else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError(
            "Unreviewed Git HEAD; local=" + local + "; remote=" + remote
        )
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    changed = tuple(git("diff", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged changes require review: " + repr(staged))
    if changed and changed != (PUBLIC_TARGET,):
        raise RuntimeError("Unreviewed tracked changes: " + repr(changed))
    guard = R43 / "source_guard.py"
    if (not guard.is_file()
            or sha256(guard.read_bytes()) not in (
                REVIEWED_R43_GUARD_SHA256, CORRECTED_R43_GUARD_SHA256,
            )):
        raise RuntimeError("R43 Source Guard differs from both reviewed versions")
    if changed:
        from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
            expected_replacement,
        )
        baseline = subprocess.run(
            ("git", "show", "HEAD:" + PUBLIC_TARGET),
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        expected = expected_replacement(baseline)
        target = ROOT / PUBLIC_TARGET
        if not target.is_file() or normalized(target.read_bytes()) != expected:
            raise RuntimeError("R43 target differs from the exact reviewed patch")
    base, replacement = reviewed_contract()
    if not TARGET.is_file():
        raise RuntimeError("Prior R43R1 installer is absent")
    actual = normalized(TARGET.read_bytes())
    if actual == base:
        mode = "BASELINE"
    elif actual == replacement:
        mode = "PATCHED"
    else:
        raise RuntimeError("Prior R43R1 installer changed outside reviewed function")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "tracked_paths": list(changed),
        "staged_paths": list(staged),
        "reviewed_r43_target_state": "EXACT_INSTALLED" if changed else "CLEAN",
        "r43r1_installer_state": mode,
        "production_files_changed_by_r43r2": 0,
        "full_pytest": False,
    }


def reviewed_contract() -> tuple[bytes, bytes]:
    """Only replace the complete verify_checkout function, not the other code."""
    base = normalized((PACKAGE / "baseline" / "install.py").read_bytes())
    new = normalized((PACKAGE / "replacement" / "install.py").read_bytes())
    if sha256(base) != ORIGINAL_INSTALL_SHA256 or base == new:
        raise RuntimeError("Reviewed R43R1 baseline installer does not match")
    import ast
    old_tree = ast.parse(base.decode("utf-8"))
    new_tree = ast.parse(new.decode("utf-8"))
    def function_map(tree):
        return {node.name: ast.dump(node) for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}
    old_fns, new_fns = function_map(old_tree), function_map(new_tree)
    if (set(old_fns) != set(new_fns)
            or any(old_fns[key] != new_fns[key] for key in old_fns
                   if key != "verify_checkout")
            or old_fns["verify_checkout"] == new_fns["verify_checkout"]):
        raise RuntimeError("Unexpected changes outside full verify_checkout")
    expected_guard = b'    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):'
    if base.count(expected_guard) != 1 or expected_guard in new:
        raise RuntimeError("Guard replacement is not the exact reviewed change")
    for literal in (
        b'if staged:',
        b'if modified and modified != (reviewed_target,):',
        b'if actual != expected:',
        b'raise RuntimeError(',
    ):
        if literal not in new:
            raise RuntimeError("Safety constraint missing in replacement installer")
    return base, new


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if dry_run:
        state["mode"] = "DRYRUN"
        return state
    if state["r43r1_installer_state"] == "BASELINE":
        _base, replacement = reviewed_contract()
        original = TARGET.read_bytes()
        selected = replacement.replace(b"\n", b"\r\n") if b"\r\n" in original else replacement
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=TARGET.parent, prefix="r43r2_", suffix=".tmp", delete=False,
            ) as stream:
                temporary = stream.name
                stream.write(selected)
            os.replace(temporary, TARGET)
        finally:
            if temporary and os.path.exists(temporary):
                os.unlink(temporary)
    checked = verify_checkout()
    if checked["r43r1_installer_state"] != "PATCHED":
        raise RuntimeError("R43R2 guarded installer correction was not installed")
    checked["mode"] = "INSTALLED"
    return checked


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    result = install(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R43R2_"
    for key, value in result.items():
        print(prefix + key.upper() + "=" + str(value))
    print(prefix + "GATE=PASS_R43R2_REVIEWED_TRACKED_CHANGE_GUARD_CORRECTED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
