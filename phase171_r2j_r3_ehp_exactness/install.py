"""Safe R2J-R3 installer from a committed, audited R2J-R2 baseline."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
OUTPUT = HERE / "output"
BACKUP = OUTPUT / "phase165_r52_r9_shared_math.py.before_r2j_r3"
STATE = OUTPUT / "state.json"
R2J_R2_COMMIT = "8b8deb6ef064e11a230b420d8ae4ae54704e6078"
R2J_R2_SHARED_BLOB = "912b5f4cd03b7bded097bedf8f7b4cbd36b5207b"
ANCHOR = (
    "        options.extend(expand_cited_cyclic_hopf_surjectivity(\n"
    "            goal, tuple(available), proof_target=proof_target,\n"
    "        ))\n"
)
HOOK = "expand_cited_ehp_surjectivity_consequences"
ADDITION = (
    "        from phase171_r2j_r3_ehp_exactness.source import (\n"
    "            expand_cited_ehp_surjectivity_consequences,\n"
    "        )\n"
    "        options.extend(expand_cited_ehp_surjectivity_consequences(goal))\n"
)


def _git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def _git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
    ).stdout


def _git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _insert_hook(before: bytes) -> bytes:
    source = before.decode("utf-8-sig")
    normalized = source.replace("\r\n", "\n")
    if normalized.count(ANCHOR) != 1 or HOOK in normalized:
        raise RuntimeError("R2J-R2 anchor absent, duplicated, or R2J-R3 already present")
    updated = normalized.replace(ANCHOR, ANCHOR + ADDITION)
    ast.parse(updated)
    newline = "\r\n" if b"\r\n" in before else "\n"
    return (b"\xef\xbb\xbf" if before.startswith(b"\xef\xbb\xbf") else b"") + updated.replace("\n", newline).encode("utf-8")


def _exact_r2j_r2_baseline() -> bytes:
    """Read the audited committed file; never import a transient package installer."""
    original = _git_bytes(
        "show", R2J_R2_COMMIT + ":phase165_r52_r9_shared_math.py"
    )
    if _git_blob_sha(original) != R2J_R2_SHARED_BLOB:
        raise RuntimeError("audited R2J-R2 Git blob changed")
    normalized = original.decode("utf-8-sig").replace("\r\n", "\n")
    if normalized.count(ANCHOR) != 1 or HOOK in normalized:
        raise RuntimeError("committed R2J-R2 baseline has an unexpected hook boundary")
    return original


def _same_audited_content(local: bytes, source: bytes) -> bool:
    """Allow only checkout EOL normalization; preserve the local encoding/EOL."""
    return (
        local.startswith(b"\xef\xbb\xbf") == source.startswith(b"\xef\xbb\xbf")
        and local.decode("utf-8-sig").replace("\r\n", "\n")
        == source.decode("utf-8-sig").replace("\r\n", "\n")
    )


def _changed_function(source: str) -> str:
    tree = ast.parse(source)
    nodes = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == "shared_expansion_provider"]
    if len(nodes) != 1:
        raise RuntimeError("shared_expansion_provider was not unique")
    lines = source.splitlines()
    return "\n".join(lines[nodes[0].lineno - 1:nodes[0].end_lineno]) + "\n"


def _full_code(shared: str) -> str:
    marker = "def build_shared_typed_bridge("
    if shared.count(marker) != 1:
        raise RuntimeError("shared import boundary changed")
    additions = (
        ("新規 source.py", HERE / "source.py"),
        ("新規 audit.py", HERE / "audit.py"),
        ("新規テスト", HERE / "tests" / "test_r2j_r3_exactness.py"),
        ("インストーラー回帰テスト", HERE / "tests" / "test_installer.py"),
        ("コミット済み基準回帰テスト", HERE / "tests" / "test_r2j_r3_committed_baseline.py"),
        ("新規 install.py", HERE / "install.py"),
    )
    chunks = [
        "# Phase 171 R2J-R3 — 変更コード全文\n",
        "変更対象: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`。",
        "追加位置: R2J-R2 `expand_cited_cyclic_hopf_surjectivity` 呼出し直後。",
        "モジュール冒頭の import 変更なし。新規ファイルの import は各全文に含む。",
        "\n## 本番ファイルの冒頭 import 全文\n\n```python\n" + shared[:shared.index(marker)] + "\n```",
        "\n## 変更後の関数全文\n\n```python\n" + _changed_function(shared) + "\n```",
    ]
    for label, path in additions:
        chunks.append("\n## " + label + " 全文\n\n```python\n" + path.read_text(encoding="utf-8") + "\n```")
    chunks.append("\n## 新規 PowerShell 全文\n\n```powershell\n" + (HERE / "run.ps1").read_text(encoding="utf-8") + "\n```")
    return "\n".join(chunks) + "\n"


def preflight() -> tuple[bytes, bool]:
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    print("PHASE171_R2J_R3_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R3_HEAD=" + head, flush=True)
    if branch != "develop":
        raise RuntimeError("develop branch required; never checkout/reset")
    ancestor = subprocess.run(
        ("git", "merge-base", "--is-ancestor", R2J_R2_COMMIT, "HEAD"),
        cwd=ROOT, check=False, capture_output=True,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("HEAD does not contain the audited R2J-R2 commit")
    if _git("rev-parse", "HEAD:phase165_r52_r9_shared_math.py") != R2J_R2_SHARED_BLOB:
        raise RuntimeError("committed shared module differs from audited R2J-R2 blob")
    expected = _exact_r2j_r2_baseline()
    if not TARGET.is_file():
        raise RuntimeError("shared module missing")
    current = TARGET.read_bytes()
    if _same_audited_content(current, expected):
        if _git("diff", "--", "phase165_r52_r9_shared_math.py"):
            raise RuntimeError("existing uncommitted shared-module edit; preserve and audit")
        _insert_hook(current)
        applied = False
    elif _same_audited_content(current, _insert_hook(expected)):
        applied = True
    else:
        raise RuntimeError("unexpected shared-module bytes; preserve local changes and re-audit")
    if not applied and (BACKUP.exists() or STATE.exists()):
        raise RuntimeError("previous R2J-R3 backup exists: inspect before applying")
    print("PHASE171_R2J_R3_R2J_R2_PRESERVED=PASS", flush=True)
    print("PHASE171_R2J_R3_PREFLIGHT=PASS", flush=True)
    print("PHASE171_R2J_R3_ALREADY_INSTALLED=" + str(applied), flush=True)
    return current, applied


def apply(dry_run: bool) -> None:
    raw, installed = preflight()
    if dry_run:
        print("PHASE171_R2J_R3_RESULT=PASS_DRY_RUN", flush=True)
        return
    if installed:
        print("PHASE171_R2J_R3_RESULT=PASS_ALREADY_APPLIED", flush=True)
        return
    altered = _insert_hook(raw)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    BACKUP.write_bytes(raw)
    try:
        TARGET.write_bytes(altered)
        revised = altered.decode("utf-8-sig").replace("\r\n", "\n")
        (OUTPUT / "CHANGED_CODE_FULL_JA.md").write_text(_full_code(revised), encoding="utf-8")
        STATE.write_text(json.dumps({
            "before_sha256": _sha256(raw), "after_sha256": _sha256(altered),
        }, indent=2) + "\n", encoding="utf-8")
    except Exception:
        if TARGET.read_bytes() == altered:
            TARGET.write_bytes(raw)
        raise
    print("PHASE171_R2J_R3_PATCHED=" + TARGET.name, flush=True)
    print("PHASE171_R2J_R3_BACKUP=" + str(BACKUP), flush=True)
    print("PHASE171_R2J_R3_CHANGED_CODE=" + str(OUTPUT / "CHANGED_CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R2J_R3_RESULT=PASS_APPLY", flush=True)


def restore() -> None:
    if not BACKUP.is_file() or not STATE.is_file():
        raise RuntimeError("no verified backup")
    previous = json.loads(STATE.read_text(encoding="utf-8"))
    before = BACKUP.read_bytes()
    if (_sha256(before) != previous["before_sha256"]
            or _sha256(TARGET.read_bytes()) != previous["after_sha256"]):
        raise RuntimeError("current file or backup no longer matches; manual inspection needed")
    TARGET.write_bytes(before)
    STATE.unlink()
    print("PHASE171_R2J_R3_RESULT=PASS_RESTORE", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    if args.restore:
        restore()
    else:
        apply(args.dry_run)


if __name__ == "__main__":
    main()
