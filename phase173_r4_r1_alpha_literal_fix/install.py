"""One-line, reviewed, idempotent fix for the pi_7^4 narrative raw f-string."""
from __future__ import annotations

import argparse
import ast
import hashlib
from hashlib import sha256
import os
from pathlib import Path
import shutil
import subprocess

TARGET = Path("phase173_r4_r1_narrative_source_fix/projection.py")
BASE_SHA256 = "f3032c14acb454004a4ab494ffaff23772431213cbcc64d2dc199d98f04ebceb"
PATCHED_SHA256 = "1d99e8b135fb49868a185e5edac4b294478ca4c2c6794e36e61242cc544e15a3"
OLD = 'f"[R{prop_n}]を $n=4$, $i=7$, $\\alpha=\\nu_4$ に適用する. "'
NEW = 'rf"[R{prop_n}]を $n=4$, $i=7$, $\\alpha=\\nu_4$ に適用する. "'


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def source_state(data: bytes) -> str:
    digest = sha256(normalize(data)).hexdigest()
    if digest == BASE_SHA256:
        return "NEW"
    if digest == PATCHED_SHA256:
        return "ALREADY_INSTALLED"
    raise RuntimeError("Unreviewed pi_7^4 projection content; refusing to modify")


def transform(source: str) -> str:
    if source.count(OLD) != 1 or source.count(NEW) != 0:
        raise RuntimeError("Reviewed raw-f-string anchor is missing or duplicated")
    functions = [
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef)
        and node.name == "project_verified_pi74_narrative"
    ]
    if len(functions) != 1:
        raise RuntimeError("The canonical pi_7^4 narrative function is not unique")
    lines = source.splitlines(keepends=True)
    section = "".join(lines[functions[0].lineno - 1:functions[0].end_lineno])
    if section.count(OLD) != 1:
        raise RuntimeError("The raw-string correction is outside the reviewed function")
    updated = source.replace(OLD, NEW, 1)
    ast.parse(updated)
    if sha256(updated.encode("utf-8")).hexdigest() != PATCHED_SHA256:
        raise RuntimeError("The patch differs from its reviewed full-function source")
    return updated


def git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments), cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=True,
    ).stdout.strip()


COMMITTED_NARRATIVE_ADAPTER_BLOB = "cfe2c244567535ffaf1e1c2e3ac27dc539ed3c21"
COMMITTED_NARRATIVE_INSTALLER_BLOB = "7ceb3bf57eceac7ca1b33986a61dd63ed3034b17"
COMMITTED_NARRATIVE_PROJECTION_BLOB = "4e2e921af6049e1557ac9d53949d4840f4ac0df2"


def reviewed_narrative_state(root: Path) -> str:
    """Verify the installed narrative hook in its original or committed state.

    The narrative installer itself expects the original adapter blob, so it
    cannot serve as a preflight after that reviewed hook has been committed.
    """
    from phase173_r4_r1_narrative_source_fix import install as narrative

    adapter = narrative.TARGET.as_posix()
    committed_blob = git(root, "rev-parse", "HEAD:" + adapter)
    if committed_blob == narrative.EXPECTED_TARGET_BLOB:
        status, _ = narrative.preflight(root)
        if status != "ALREADY_INSTALLED":
            raise RuntimeError("The reviewed narrative hook has not been installed")
        return "WORKTREE_INSTALLED"
    if committed_blob != COMMITTED_NARRATIVE_ADAPTER_BLOB:
        raise RuntimeError("Unreviewed committed narrative Web adapter")

    # Match the exact registered Narrative module and public search state.
    # The projection itself is allowed to have only the independent one-line
    # TeX repair; source_state() performs that full-content verification.
    checked_paths = {
        "phase173_r4_r1_narrative_source_fix/install.py":
            COMMITTED_NARRATIVE_INSTALLER_BLOB,
        TARGET.as_posix(): COMMITTED_NARRATIVE_PROJECTION_BLOB,
    }
    for path, expected_blob in checked_paths.items():
        if git(root, "rev-parse", "HEAD:" + path) != expected_blob:
            raise RuntimeError("Reviewed committed narrative dependency changed: " + path)
    if normalize((root / "phase173_r4_r1_narrative_source_fix/install.py").read_bytes()) != normalize(
        narrative.git_bytes(root, "phase173_r4_r1_narrative_source_fix/install.py")
    ):
        raise RuntimeError("Reviewed narrative installer worktree changed")
    if narrative.reviewed_public_state(root) != "COMMITTED_INSTALLED":
        raise RuntimeError("The reviewed public proof connection is missing")

    recorded = normalize(narrative.git_bytes(root, adapter))
    worktree = normalize((root / adapter).read_bytes())
    if recorded != worktree or recorded.count(narrative.HOOK.encode("utf-8")) != 1:
        raise RuntimeError("Committed narrative Web adapter differs from reviewed source")
    restored = recorded.replace(narrative.HOOK.encode("utf-8"), b"", 1)
    blob = hashlib.sha1(
        b"blob " + str(len(restored)).encode("ascii") + b"\x00" + restored
    ).hexdigest()
    if blob != narrative.EXPECTED_TARGET_BLOB:
        raise RuntimeError("Committed narrative hook differs from the reviewed adapter")
    return "COMMITTED_INSTALLED"


def preflight(root: Path) -> tuple[str, bytes]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Only the develop branch is eligible")
    if git(root, "rev-parse", "HEAD") != git(root, "rev-parse", "origin/develop"):
        raise RuntimeError("HEAD differs from origin/develop")
    narrative_state = reviewed_narrative_state(root)
    print("PHASE173_R4_R1_ALPHA_NARRATIVE_STATE=" + narrative_state)
    if git(root, "diff", "--cached", "--name-only", "--", TARGET.as_posix()):
        raise RuntimeError("Refusing to overwrite staged narrative projection")
    data = (root / TARGET).read_bytes()
    state = source_state(data)
    if state == "NEW":
        updated = transform(normalize(data).decode("utf-8"))
        if sha256(updated.encode("utf-8")).hexdigest() != PATCHED_SHA256:
            raise RuntimeError("The reviewed raw-string patch does not match")
    return state, data


def install(root: Path) -> str:
    state, data = preflight(root)
    if state == "ALREADY_INSTALLED":
        return state
    amended = transform(normalize(data).decode("utf-8"))
    output = (
        amended.replace("\n", "\r\n").encode("utf-8")
        if b"\r\n" in data else amended.encode("utf-8")
    )
    backup = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_alpha_literal_fix/"
        + sha256(data).hexdigest() + ".py"
    )
    backup.parent.mkdir(parents=True, exist_ok=True)
    if backup.exists() and backup.read_bytes() != data:
        raise RuntimeError("Existing recovery backup differs; refusing to overwrite")
    if not backup.exists():
        shutil.copy2(root / TARGET, backup)
    (root / TARGET).write_bytes(output)
    return "INSTALLED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state, _ = preflight(args.root.resolve())
    print("PHASE173_R4_R1_ALPHA_SOURCE_GUARD=PASS")
    print("PHASE173_R4_R1_ALPHA_PATCH_STATE=" + state)
    if args.dry_run:
        print("PHASE173_R4_R1_ALPHA_DRY_RUN=PASS")
        return 0
    print("PHASE173_R4_R1_ALPHA_INSTALL=" + install(args.root.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
