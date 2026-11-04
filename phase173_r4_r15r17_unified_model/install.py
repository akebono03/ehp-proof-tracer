"""Guarded, reversible R15R17 source installation; never stages or commits."""
from __future__ import annotations

import argparse
import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

from .patches import EXPECTED_BLOBS, TRANSFORMS, BINDING, MODEL, WEB, PROJECTION, ADAPTER


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
STATE = PACKAGE / "installed_state.json"
BACKUP = PACKAGE / "backups"
REVIEW = PACKAGE / "FULL_CHANGED_UNITS.md"
REVIEWED_REMOTE = "874c6f63ad85374cd19e00e92600c92c5c056cb3"
ALLOWED_LOCAL_HEADS = {
    "d57fa2e880c3fbdffea5d310252626d360f4fe25",
    REVIEWED_REMOTE,
}
UNITS = {
    MODEL: ("verified_narrative_steps", "build_proof_narrative_model"),
    BINDING: ("build_narrative_body_lines",),
    WEB: ("_group_proof_statement_latex",),
    PROJECTION: ("render_certified_abstract_model_section",),
    ADAPTER: ("build_partial_web_group_proof_view",),
}


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "--no-pager", *args], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if check and proc.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def index_tree() -> str:
    return git("write-tree")


def reviewed_sources() -> dict[str, tuple[bytes, bytes]]:
    branch = git("branch", "--show-current")
    local_head = git("rev-parse", "HEAD")
    remote_head = git("rev-parse", "origin/develop")
    if branch != "develop" or local_head not in ALLOWED_LOCAL_HEADS:
        raise RuntimeError(f"unreviewed local branch/HEAD: {branch} {local_head}")
    if remote_head != REVIEWED_REMOTE:
        raise RuntimeError(f"GitHub develop has advanced: {remote_head}")

    proposal: dict[str, tuple[bytes, bytes]] = {}
    for relative, transform in TRANSFORMS.items():
        path = ROOT / relative
        if git("rev-parse", f"HEAD:{relative}") != EXPECTED_BLOBS[relative]:
            raise RuntimeError(f"unreviewed committed file: {relative}")
        if git("diff", "--name-only", "--", relative):
            raise RuntimeError(f"unstaged user changes in source file: {relative}")
        if git("diff", "--cached", "--name-only", "--", relative):
            raise RuntimeError(f"staged user changes in source file: {relative}")
        raw = path.read_bytes()
        if b"\r\n" in raw and raw.replace(b"\r\n", b"").find(b"\n") != -1:
            raise RuntimeError(f"mixed LF/CRLF in source file: {relative}")
        normalized = raw.replace(b"\r\n", b"\n")
        source = normalized.decode("utf-8")
        replacement = transform(source)
        if source == replacement:
            raise RuntimeError(f"empty source change: {relative}")
        ast.parse(replacement, filename=relative)
        proposed = replacement.encode("utf-8")
        if b"\r\n" in raw:
            proposed = proposed.replace(b"\n", b"\r\n")
        proposal[relative] = (raw, proposed)
    return proposal


def _function_source(source: str, function_name: str) -> str:
    parsed = ast.parse(source)
    nodes = [item for item in parsed.body
             if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
             and item.name == function_name]
    if len(nodes) != 1:
        raise RuntimeError(f"missing complete function: {function_name}")
    node = nodes[0]
    start = min((d.lineno for d in node.decorator_list), default=node.lineno)
    return "\n".join(source.splitlines()[start - 1:node.end_lineno])


def _imports_source(source: str) -> str:
    parsed = ast.parse(source)
    imports = [node for node in parsed.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    if not imports:
        raise RuntimeError("modified module lacks imports")
    return "\n".join(source.splitlines()[:max(node.end_lineno for node in imports)])


def write_full_review(proposal: dict[str, tuple[bytes, bytes]]) -> None:
    lines = [
        "# Phase 173 R15R17 — 完全な変更単位", "",
        "この文書は、Source Guard 合格後のローカル実ファイルから生成した。",
        "省略はなく、変更後の関数は全行を掲載する。", "",
        "## 変更対象", "",
    ]
    for relative in TRANSFORMS:
        lines.append(f"- `{relative}`: {', '.join(UNITS[relative])}")
    lines.extend(("", "## Import 変更後の全文", ""))
    binding_src = proposal[BINDING][1].decode("utf-8").replace("\r\n", "\n")
    lines.extend((f"### `{BINDING}`", "", "```python", _imports_source(binding_src), "```", ""))
    lines.extend(("## 変更後の関数全文", ""))
    for relative, (_, changed) in proposal.items():
        source = changed.decode("utf-8").replace("\r\n", "\n")
        for function in UNITS[relative]:
            lines.extend((f"### `{relative}` — `{function}`", "", "```python",
                          _function_source(source, function), "```", ""))
    lines.extend(("## 新規テストファイルの全文", ""))
    for test_name in ("test_unified_web.py", "test_patch_contract.py"):
        lines.extend((f"### `tests/{test_name}`", "", "```python",
                      (PACKAGE / "tests" / test_name).read_text(encoding="utf-8"),
                      "```", ""))
    REVIEW.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"R15R17_FULL_CHANGED_UNITS={REVIEW.relative_to(ROOT)}")


def restore() -> None:
    if not STATE.exists():
        raise RuntimeError("no R15R17 installed state to restore")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    for relative, hashes in state["files"].items():
        path = ROOT / relative
        current = path.read_bytes()
        if sha256(current).hexdigest() != hashes["installed"]:
            raise RuntimeError(f"user-modified installed file; refusing restore: {relative}")
        original = (BACKUP / hashes["backup"]).read_bytes()
        if sha256(original).hexdigest() != hashes["original"]:
            raise RuntimeError(f"backup integrity mismatch: {relative}")
    before = index_tree()
    for relative, hashes in state["files"].items():
        (ROOT / relative).write_bytes((BACKUP / hashes["backup"]).read_bytes())
    if index_tree() != before or before != state["index_tree"]:
        raise RuntimeError("Git index changed during restore")
    STATE.unlink()
    print("R15R17_RESTORE=PASS")
    print("R15R17_GIT_INDEX_PRESERVED=PASS")


def apply(proposal: dict[str, tuple[bytes, bytes]], original_index: str) -> None:
    if STATE.exists():
        raise RuntimeError("existing installed state: restore or audit it before reinstall")
    BACKUP.mkdir(parents=True, exist_ok=True)
    saved: dict[str, dict[str, str]] = {}
    for index, (relative, (original, changed)) in enumerate(proposal.items()):
        filename = f"source_{index}.backup"
        (BACKUP / filename).write_bytes(original)
        saved[relative] = {
            "backup": filename,
            "original": sha256(original).hexdigest(),
            "installed": sha256(changed).hexdigest(),
        }
    STATE.write_text(json.dumps({"index_tree": original_index, "files": saved},
                                ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        for relative, (_, changed) in proposal.items():
            (ROOT / relative).write_bytes(changed)
        for relative, hashes in saved.items():
            if sha256((ROOT / relative).read_bytes()).hexdigest() != hashes["installed"]:
                raise RuntimeError(f"post-install hash mismatch: {relative}")
        if index_tree() != original_index:
            raise RuntimeError("installer changed the Git stage")
    except BaseException:
        for relative, (original, _) in proposal.items():
            (ROOT / relative).write_bytes(original)
        STATE.unlink(missing_ok=True)
        raise
    print("R15R17_INSTALL=PASS")
    print("R15R17_GIT_INDEX_PRESERVED=PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--restore", action="store_true")
    opts = parser.parse_args()
    if opts.restore:
        restore()
        return 0
    before = index_tree()
    proposal = reviewed_sources()
    write_full_review(proposal)
    if index_tree() != before:
        raise RuntimeError("Git stage unexpectedly changed in DryRun")
    print(f"R15R17_REVIEWED_FILES={len(proposal)}")
    print("R15R17_NO_NK_SPECIAL_CASES=True")
    if opts.dry_run:
        print("R15R17_DRY_RUN=PASS")
        print("R15R17_PRODUCTION_WRITES=NONE")
        print("R15R17_GIT_INDEX_PRESERVED=PASS")
        return 0
    apply(proposal, before)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ValueError, SyntaxError, OSError) as exc:
        print(f"R15R17_ERROR={exc}", file=sys.stderr)
        raise SystemExit(1)
