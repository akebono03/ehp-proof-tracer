"""Fail-closed repair of a single R43 source SHA literal. No production edits."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PREVIOUS_DIR = ROOT / "phase174_r3_r7_r43_public_ehp_map_property_wiring"
TARGET = PREVIOUS_DIR / "source_guard.py"
EXPECTED_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
REVIEWED_EHP_SOURCE_PATH = "phase174_r3_r7_r3_ehp_zero_rule/rule.py"
REVIEWED_EHP_SOURCE_BLOB = "8834cbefbfca5bcca18dc01f072c9738a05f7bdc"
WRONG_SHA = "8834cbefbfca18dc01f072c9738a05f7bdc"
CORRECT_SHA = REVIEWED_EHP_SOURCE_BLOB
PREVIOUS_PINS = {'install.py': '07591182c401643835b910be1c9f6f95aa0c084b871e1f4815c2c879925a0756', 'audit.py': 'c62bd6869f52d30b4fc764dad2884c061cc1cb6d0524fda4bd8895e770b5e0f2', 'run.ps1': '0ea5ce8b3282ad44a6d21199b51a41fe9b59e23cfb8dabc8106711b04e3f24ad', 'tests/test_guard.py': 'ad40a7e7f2a1623db18b9736a9ef55b8dc03f7ad3eb3abd172b1a75ded7e6839', 'tests/test_public.py': '1078a24393b48e998fb37b883b05232342c4d0fe0df9423f0905158b12fff2f5', 'tests/test_static.py': '0645503867844300715d8fea16b4ad3f5d3cb920760d5689685399be92f7774b'}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def normalize(content: bytes) -> bytes:
    return content.replace(b"\r\n", b"\n")


def sha256(content: bytes) -> str:
    return hashlib.sha256(normalize(content)).hexdigest()


def git_blob(content: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(content)).encode("ascii") + b"\0" + content,
    ).hexdigest()


def reviewed_source_blob(content: bytes) -> bool:
    canonical = normalize(content)
    return len(REVIEWED_EHP_SOURCE_BLOB) == 40 and REVIEWED_EHP_SOURCE_BLOB in (
        git_blob(content), git_blob(canonical),
        git_blob(canonical.replace(b"\n", b"\r\n")),
    )


def replacement_contract() -> tuple[bytes, bytes]:
    """Require literally one inserted five-character SHA segment."""
    baseline = normalize((PACKAGE / "baseline" / "source_guard.py").read_bytes())
    replacement = normalize((PACKAGE / "replacement" / "source_guard.py").read_bytes())
    old = ("\"" + WRONG_SHA + "\"").encode("ascii")
    new = ("\"" + CORRECT_SHA + "\"").encode("ascii")
    if (len(WRONG_SHA) != 35 or len(CORRECT_SHA) != 40
            or baseline.count(old) != 1
            or replacement != baseline.replace(old, new, 1)
            or baseline == replacement):
        raise RuntimeError("R43R1 change is not exactly the reviewed SHA correction")
    return baseline, replacement


def verify_checkout() -> dict[str, object]:
    """Refuse changed Git lineage, tracked edits, or unreviewed R43 package."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43R1 into the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43R1 requires develop")
    local = git("rev-parse", "HEAD")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    remote = remote_rows[0] if remote_rows else ""
    if local != EXPECTED_HEAD or remote != EXPECTED_HEAD:
        raise RuntimeError("Unreviewed HEAD; do not change files")
    if git("diff", "--cached", "--name-only") or git("diff", "--name-only"):
        raise RuntimeError("Tracked or staged changes must be independently reviewed")
    for relative, expected in PREVIOUS_PINS.items():
        item = PREVIOUS_DIR / relative
        if not item.is_file() or sha256(item.read_bytes()) != expected:
            raise RuntimeError("Existing R43 file changed: " + relative)
    if not reviewed_source_blob((ROOT / REVIEWED_EHP_SOURCE_PATH).read_bytes()):
        raise RuntimeError("The actual historical EHP source has changed")
    baseline, replacement = replacement_contract()
    if not TARGET.is_file():
        raise RuntimeError("Original R43 source_guard.py is absent")
    current = normalize(TARGET.read_bytes())
    if current == baseline:
        mode = "BASELINE"
    elif current == replacement:
        mode = "PATCHED"
    else:
        raise RuntimeError("R43 source_guard.py differs from both reviewed versions")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "old_sha_length": len(WRONG_SHA),
        "correct_sha_length": len(CORRECT_SHA),
        "correct_sha": CORRECT_SHA,
        "r43_source_guard_mode": mode,
        "production_files_changed": 0,
        "target_files": 1,
        "full_pytest": False,
    }


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if dry_run:
        state["mode"] = "DRYRUN"
        state["corrected_preview"] = True
        return state
    if state["r43_source_guard_mode"] == "BASELINE":
        _baseline, replacement = replacement_contract()
        old = TARGET.read_bytes()
        data = replacement.replace(b"\n", b"\r\n") if b"\r\n" in old else replacement
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=TARGET.parent, prefix="r43r1_", suffix=".tmp",
                delete=False,
            ) as stream:
                temp_path = stream.name
                stream.write(data)
            os.replace(temp_path, TARGET)
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.unlink(temp_path)
    checked = verify_checkout()
    if checked["r43_source_guard_mode"] != "PATCHED":
        raise RuntimeError("R43R1 correction did not persist")
    checked["mode"] = "INSTALLED"
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = install(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R43R1_"
    for key, value in result.items():
        print(prefix + key.upper() + "=" + str(value))
    print(prefix + "GATE=PASS_R43R1_REVIEWED_R3_SHA_PIN_REPAIRED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
