"""Review, preview, install and restore a single whole-function renderer patch.

Production files are never staged, committed, reset or cleaned by this package.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from .patch import transform

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = "phase168_r3_5_model_renderer.py"
TARGET_PATH = ROOT / TARGET
REVIEWED_BLOB = "6dd75099bb2c71fb9873477cb36c11bdb7dad410"
REVIEWED_REMOTE = "11fdf0f5c52ce2de786e36c3a3d0abe7a0d0fa26"
ALLOWED_HEADS = frozenset((
    "d57fa2e880c3fbdffea5d310252626d360f4fe25",
    "874c6f63ad85374cd19e00e92600c92c5c056cb3",
    REVIEWED_REMOTE,
))
R1_STATE = ROOT / "phase173_r4_r15r17_unified_model" / "installed_state.json"
STATE = PACKAGE / "installed_state.json"
BACKUP = PACKAGE / "renderer_original.backup"
REVIEW = PACKAGE / "FULL_CHANGED_UNITS.md"


def git(*args: str) -> str:
    process = subprocess.run(
        ["git", "--no-pager", *args], cwd=ROOT, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    )
    if process.returncode:
        raise RuntimeError(
            "Git command failed: " + " ".join(args) + " : " + process.stderr.strip()
        )
    return process.stdout.strip()


def sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def ensure_r1_is_still_installed() -> None:
    if not R1_STATE.is_file():
        raise RuntimeError("R15R17-R1 installed_state.json is missing")
    state = json.loads(R1_STATE.read_text(encoding="utf-8"))
    files = state.get("files")
    if not isinstance(files, dict) or len(files) != 5:
        raise RuntimeError("R15R17-R1 installed state has an unexpected file set")
    for relative, metadata in files.items():
        target = ROOT / relative
        if not target.is_file():
            raise RuntimeError(f"missing R1 production file: {relative}")
        if sha(target.read_bytes()) != metadata.get("installed"):
            raise RuntimeError(f"R1 installed content has changed: {relative}")


def reviewed_proposal() -> tuple[bytes, bytes]:
    branch = git("branch", "--show-current")
    head = git("rev-parse", "HEAD")
    remote = git("rev-parse", "origin/develop")
    if branch != "develop" or head not in ALLOWED_HEADS:
        raise RuntimeError(f"unreviewed branch or local HEAD: {branch} {head}")
    if remote != REVIEWED_REMOTE:
        raise RuntimeError(f"remote develop has advanced: {remote}")
    if git("rev-parse", f"HEAD:{TARGET}") != REVIEWED_BLOB:
        raise RuntimeError("renderer HEAD blob changed since code review")
    if git("diff", "--name-only", "--", TARGET):
        raise RuntimeError("renderer has an existing unstaged change")
    if git("diff", "--cached", "--name-only", "--", TARGET):
        raise RuntimeError("renderer has an existing staged change")
    ensure_r1_is_still_installed()
    original = TARGET_PATH.read_bytes()
    if b"\r\n" in original and b"\n" in original.replace(b"\r\n", b""):
        raise RuntimeError("renderer has mixed line endings")
    text = original.replace(b"\r\n", b"\n").decode("utf-8")
    proposed = transform(text)
    ast.parse(proposed, filename=TARGET)
    output = proposed.encode("utf-8")
    if b"\r\n" in original:
        output = output.replace(b"\n", b"\r\n")
    if output == original:
        raise RuntimeError("renderer patch produced no change")
    return original, output


def complete_function(source: str, name: str) -> str:
    parsed = ast.parse(source)
    funcs = [n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(funcs) != 1:
        raise RuntimeError(f"missing unique function {name}")
    function = funcs[0]
    start = min((x.lineno for x in function.decorator_list), default=function.lineno)
    return "\n".join(source.splitlines()[start - 1:function.end_lineno])


def write_review(proposed: bytes) -> None:
    code = proposed.decode("utf-8").replace("\r\n", "\n")
    body = complete_function(code, "render_model_backed_narrative_markdown")
    lines = [
        "# Phase 173 R15R17-R2 — 変更関数全文", "",
        "## 変更対象", "",
        f"- `{TARGET}` — `render_model_backed_narrative_markdown()` のみ", "",
        "import 変更はない. 新しいクラス・関数は本番モジュールへ追加しない.", "",
        "## 関数全文 (そのまま置換可能)", "", "```python", body,
        "```", "", "## 新規テスト全文", "",
    ]
    for name in ("test_patch_contract.py", "test_public_narrative.py"):
        path = PACKAGE / "tests" / name
        lines.extend((f"### `tests/{name}`", "", "```python",
                      path.read_text(encoding="utf-8"), "```", ""))
    REVIEW.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("R15R17R2_FULL_CHANGED_UNITS=" + str(REVIEW.relative_to(ROOT)))


def install(proposal: tuple[bytes, bytes], index_before: str) -> None:
    if STATE.exists() or BACKUP.exists():
        raise RuntimeError("existing R2 installation or backup; refusing overwrite")
    original, modified = proposal
    BACKUP.write_bytes(original)
    state = {"original_sha256": sha(original), "installed_sha256": sha(modified),
             "git_index_tree": index_before, "target": TARGET}
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    try:
        TARGET_PATH.write_bytes(modified)
        if sha(TARGET_PATH.read_bytes()) != state["installed_sha256"]:
            raise RuntimeError("installed renderer hash mismatch")
        if git("write-tree") != index_before:
            raise RuntimeError("Git index changed during install")
    except BaseException:
        TARGET_PATH.write_bytes(original)
        BACKUP.unlink(missing_ok=True)
        STATE.unlink(missing_ok=True)
        raise
    print("R15R17R2_INSTALL=PASS")
    print("R15R17R2_GIT_INDEX_PRESERVED=PASS")


def restore() -> None:
    if not STATE.is_file() or not BACKUP.is_file():
        raise RuntimeError("R2 installation state or backup is missing")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    original = BACKUP.read_bytes()
    if state.get("target") != TARGET or sha(original) != state.get("original_sha256"):
        raise RuntimeError("R2 backup integrity check failed")
    if sha(TARGET_PATH.read_bytes()) != state.get("installed_sha256"):
        raise RuntimeError("installed renderer has user modifications; refusing restore")
    before = git("write-tree")
    if before != state.get("git_index_tree"):
        raise RuntimeError("Git index differs from R2 install snapshot")
    TARGET_PATH.write_bytes(original)
    if git("write-tree") != before:
        raise RuntimeError("Git index changed during restore")
    STATE.unlink()
    BACKUP.unlink()
    print("R15R17R2_RESTORE=PASS")
    print("R15R17R2_GIT_INDEX_PRESERVED=PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")
    options = parser.parse_args()
    if options.restore:
        restore()
        return 0
    index_before = git("write-tree")
    proposal = reviewed_proposal()
    write_review(proposal[1])
    if git("write-tree") != index_before:
        raise RuntimeError("Git index changed in preflight")
    if options.dry_run:
        print("R15R17R2_DRY_RUN=PASS")
        print("R15R17R2_PRODUCTION_WRITES=NONE")
        print("R15R17R2_GIT_INDEX_PRESERVED=PASS")
        return 0
    install(proposal, index_before)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, OSError, SyntaxError) as error:
        print("R15R17R2_ERROR=" + str(error), file=sys.stderr)
        raise SystemExit(1)
