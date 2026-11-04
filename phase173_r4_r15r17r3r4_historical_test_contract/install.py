"""R15R17-R3R4: reviewed, reversible TEST-ONLY contract correction."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from .patches import CHANGES, FILES, transform

ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "a4e01bcafcd2afd295c61843bbaa597a6262f75a"
STATE = PKG / "installed_state.json"
BACKUPS = PKG / "backups"
REVIEW = PKG / "FULL_CHANGED_UNITS.md"
R3R3_STATE = ROOT / "phase173_r4_r15r17r3r3_typed_goal_display" / "installed_state.json"
RENDERER = ROOT / "phase168_r3_5_model_renderer.py"


def git(*args: str, check: bool = True) -> str:
    command = subprocess.run(
        ["git", "--no-pager", *args], cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if check and command.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + command.stderr.strip())
    return command.stdout.strip() if command.returncode == 0 else ""


def sha256(source: bytes) -> str:
    return hashlib.sha256(source).hexdigest()


def current_index() -> str:
    return git("write-tree")


def check_repo() -> None:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("extract the ZIP into the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("only develop branch is reviewed")
    for ref in ("HEAD", "origin/develop"):
        result = subprocess.run(
            ["git", "--no-pager", "merge-base", "--is-ancestor", BASE, ref],
            cwd=ROOT, capture_output=True,
        )
        if result.returncode:
            raise RuntimeError(ref + " is not a descendant of reviewed HEAD " + BASE)
    print("R15R17R3R4_LOCAL_HEAD=" + git("rev-parse", "HEAD"))
    print("R15R17R3R4_REMOTE_HEAD=" + git("rev-parse", "origin/develop"))
    for path, blob in FILES.items():
        if git("rev-parse", "HEAD:" + path) != blob:
            raise RuntimeError("unreviewed HEAD test blob: " + path)
        if git("rev-parse", "origin/develop:" + path) != blob:
            raise RuntimeError("unreviewed REMOTE test blob: " + path)
        if git("diff", "--name-only", "HEAD", "--", path):
            raise RuntimeError("existing staged or unstaged test changes: " + path)
    if not R3R3_STATE.is_file():
        raise RuntimeError("R15R17-R3R3 installation state is required")
    state = json.loads(R3R3_STATE.read_text(encoding="utf-8"))
    if (state.get("target") != "phase168_r3_5_model_renderer.py"
            or sha256(RENDERER.read_bytes()) != state.get("installed_sha256")):
        raise RuntimeError("R3R3 renderer must be installed unchanged")
    print("R15R17R3R4_PRIOR_PHASE_INTEGRITY=PASS")


def candidate_files() -> dict[str, tuple[bytes, bytes]]:
    check_repo()
    proposal = {}
    for path in FILES:
        original = (ROOT / path).read_bytes()
        if b"\r\n" in original and b"\n" in original.replace(b"\r\n", b""):
            raise RuntimeError("mixed test file line endings: " + path)
        normalized = original.replace(b"\r\n", b"\n").decode("utf-8")
        patched = transform(path, normalized)
        ast.parse(patched, filename=path)
        updated = patched.encode("utf-8")
        if b"\r\n" in original:
            updated = updated.replace(b"\n", b"\r\n")
        proposal[path] = (original, updated)
    return proposal


def changed_functions(source: bytes, names: set[str]) -> list[tuple[str, str]]:
    text = source.decode("utf-8").replace("\r\n", "\n")
    code = ast.parse(text)
    lines = text.splitlines()
    result = []
    for node in code.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or node.name not in names:
            continue
        first = min([node.lineno] + [deco.lineno for deco in node.decorator_list])
        result.append((node.name, "\n".join(lines[first-1:node.end_lineno])))
    if {n for n, _ in result} != names:
        raise RuntimeError("changed test functions missing from review")
    return result


def make_review(proposal: dict[str, tuple[bytes, bytes]]) -> None:
    notes = [
        "# Phase 173 R15R17-R3R4: Full Changed Test Functions", "",
        "Only historical test contracts change. All production modules are byte-for-byte unchanged.", "",
        "The named-generator proof remains incomplete where its typed open goals are unresolved.",
        "Verified abstract ProofSteps remain cited once in the canonical public Narrative.",
        "Explicit legacy APIs and their own tests keep their independent historical output.", "",
    ]
    for path, (_, changed) in proposal.items():
        notes.extend(("## `" + path + "`", "", "### Import block (unchanged)", "", "```python"))
        source = changed.decode("utf-8").replace("\r\n", "\n")
        first_class = next(
            (i for i, line in enumerate(source.splitlines())
             if line.startswith("def ") or line.startswith("class ")
             or line.startswith("@pytest.mark") or line.startswith("@pytest.fixture")),
            len(source.splitlines()),
        )
        notes.extend(("\n".join(source.splitlines()[:first_class]), "```", ""))
        for name, function in changed_functions(changed, {v.function for v in CHANGES[path]}):
            notes.extend(("### Complete test function: `" + name + "`", "", "```python", function, "```", ""))
    notes.extend(("## New test files (complete)", ""))
    for file in sorted((PKG / "tests").glob("test_*.py")):
        notes.extend(("### `" + file.name + "`", "", "```python", file.read_text(encoding="utf-8"), "```", ""))
    REVIEW.write_text("\n".join(notes), encoding="utf-8", newline="\n")
    print("R15R17R3R4_FULL_CHANGED_UNITS=" + str(REVIEW.relative_to(ROOT)))


def install(proposal: dict[str, tuple[bytes, bytes]], index: str) -> None:
    if STATE.exists() or BACKUPS.exists():
        raise RuntimeError("installation already has backups/state")
    if any((ROOT / path).read_bytes() != before for path, (before, _) in proposal.items()):
        raise RuntimeError("a reviewed test changed while preparing installation")
    BACKUPS.mkdir()
    payload = {"index_tree": index, "files": {}}
    for number, (path, (before, changed)) in enumerate(proposal.items()):
        name = "source_" + str(number) + ".backup"
        (BACKUPS / name).write_bytes(before)
        payload["files"][path] = {
            "backup": name, "original_sha256": sha256(before),
            "installed_sha256": sha256(changed),
        }
    STATE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    touched = []
    try:
        for path, (before, changed) in proposal.items():
            target = ROOT / path
            if target.read_bytes() != before:
                raise RuntimeError("concurrent edit detected: " + path)
            temporary = target.with_name(target.name + ".r15r17r3r4.tmp")
            temporary.write_bytes(changed)
            os.replace(temporary, target)
            touched.append(path)
            if sha256(target.read_bytes()) != sha256(changed):
                raise RuntimeError("post-install content hash mismatch: " + path)
        if current_index() != index:
            raise RuntimeError("git index changed during install")
    except BaseException:
        for path in reversed(touched):
            (ROOT / path).write_bytes(proposal[path][0])
        STATE.unlink(missing_ok=True)
        for child in BACKUPS.glob("*"):
            child.unlink()
        BACKUPS.rmdir()
        raise
    print("R15R17R3R4_INSTALL=PASS")
    print("R15R17R3R4_GIT_INDEX_PRESERVED=PASS")


def restore() -> None:
    if not STATE.exists() or not BACKUPS.is_dir():
        raise RuntimeError("backups and installation state are required")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if set(state.get("files", {})) != set(FILES):
        raise RuntimeError("unrecognized restore manifest")
    before = current_index()
    if state.get("index_tree") != before:
        raise RuntimeError("Git index has changed; refusing restoration")
    for path, info in state["files"].items():
        if sha256((ROOT / path).read_bytes()) != info["installed_sha256"]:
            raise RuntimeError("test changed after install; refusing restore: " + path)
        if sha256((BACKUPS / info["backup"]).read_bytes()) != info["original_sha256"]:
            raise RuntimeError("invalid backup: " + path)
    for path, info in state["files"].items():
        (ROOT / path).write_bytes((BACKUPS / info["backup"]).read_bytes())
    STATE.unlink()
    for child in BACKUPS.glob("*"):
        child.unlink()
    BACKUPS.rmdir()
    if current_index() != before:
        raise RuntimeError("git index changed during restoration")
    print("R15R17R3R4_RESTORE=PASS")
    print("R15R17R3R4_GIT_INDEX_PRESERVED=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        restore()
        return
    index = current_index()
    proposal = candidate_files()
    make_review(proposal)
    if current_index() != index:
        raise RuntimeError("git index changed during dry-run")
    if args.dry_run:
        print("R15R17R3R4_REVIEWED_TEST_FILES=" + str(len(FILES)))
        print("R15R17R3R4_DRY_RUN=PASS")
        print("R15R17R3R4_PRODUCTION_WRITES=NONE")
        print("R15R17R3R4_GIT_INDEX_PRESERVED=PASS")
        return
    install(proposal, index)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, TypeError, ValueError, OSError, SyntaxError) as error:
        print("R15R17R3R4_ERROR=" + str(error), file=sys.stderr)
        sys.exit(1)
