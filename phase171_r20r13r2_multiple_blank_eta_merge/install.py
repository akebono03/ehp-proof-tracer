"""Content-guarded, single-function R20R13R2 correction.

The source- and citation-verification rules remain unchanged.  Only a
Markdown-separator walk inside combine_adjacent_verified_eta_sentences changes.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGET = Path("phase171_r20r13_eta_sentence_layout/projection.py")
RENDERER = Path("phase168_r3_5_model_renderer.py")
ORIGINAL_SHA256 = "7a7b6d93a690a02763db003c5fc21e0255a0c8a4dfa240145d07dd1b66ebfc08"
CORRECTED_SHA256 = "701c1ec9de253a8f0df68bae1ac711b449a4516ab6d03d6132be7ab84615d006"
OLD = '        while cursor < len(lines):\n            # Standard narrative inserts precisely one empty line per sentence.\n            has_separator = lines[cursor] == ""\n            next_index = cursor + 1 if has_separator else cursor\n            if next_index >= len(lines):\n                break\n            candidate = allowed.get(lines[next_index])\n            if candidate is None or candidate[0] != tag:\n                break\n            terms.append(candidate[1])\n            cursor = next_index + 1\n'
NEW = '        while cursor < len(lines):\n            # Earlier presentation-only duplicate suppression can leave\n            # several empty Markdown separators between surviving lines.\n            # Ignore only empty lines, never a distinct mathematical step.\n            next_index = cursor\n            while next_index < len(lines) and lines[next_index] == "":\n                next_index += 1\n            if next_index >= len(lines):\n                break\n            candidate = allowed.get(lines[next_index])\n            if candidate is None or candidate[0] != tag:\n                break\n            terms.append(candidate[1])\n            cursor = next_index + 1\n'


def normalized(raw: bytes) -> bytes:
    return raw.decode("utf-8-sig").replace("\r\n", "\n").encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def transform(source: str) -> str:
    if source.count(OLD) != 1:
        raise RuntimeError("reviewed eta-merge function anchor not found once")
    updated = source.replace(OLD, NEW, 1)
    ast.parse(updated)
    return updated


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT, check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def committed_projection() -> bytes:
    """Read only the tracked target from HEAD; no checkout or branch mutation."""
    return subprocess.run(
        ("git", "show", "HEAD:" + TARGET.as_posix()),
        cwd=ROOT, check=True, capture_output=True,
    ).stdout


def preflight() -> tuple[str, bytes, bytes, bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R20R13R2 requires develop")
    head = git("rev-parse", "HEAD")
    # The branch may advance after the reviewed source is committed. Compare
    # the tracked source bytes instead of pinning an unrelated commit SHA.
    recorded = committed_projection()
    if sha256(normalized(recorded)) not in (ORIGINAL_SHA256, CORRECTED_SHA256):
        raise RuntimeError("HEAD projection content is not reviewed; no files modified")
    if not (ROOT / RENDERER).is_file() or not (ROOT / TARGET).is_file():
        raise RuntimeError("R20R13 renderer/projection not installed")
    renderer = (ROOT / RENDERER).read_text(encoding="utf-8-sig")
    if "format_complete_proof_sentences(lines, model)" not in renderer:
        raise RuntimeError("R20R13 renderer hook missing")
    reviewed = (HERE / "reviewed_projection.py").read_bytes()
    if sha256(normalized(reviewed)) != ORIGINAL_SHA256:
        raise RuntimeError("bundled original differs from reviewed source")
    expected = transform(normalized(reviewed).decode("utf-8"))
    if sha256(expected.encode("utf-8")) != CORRECTED_SHA256:
        raise RuntimeError("bundled corrected source hash mismatch")
    if normalized((HERE / "corrected_projection.py").read_bytes()).decode("utf-8") != expected:
        raise RuntimeError("bundled corrected projection differs from patch")
    current = (ROOT / TARGET).read_bytes()
    plain = normalized(current).decode("utf-8")
    if sha256(plain.encode("utf-8")) == CORRECTED_SHA256:
        return head, current, current, True
    if sha256(plain.encode("utf-8")) != ORIGINAL_SHA256:
        raise RuntimeError("target projection differs from reviewed R20R13; refusing overwrite")
    prefix = b"\xef\xbb\xbf" if current.startswith(b"\xef\xbb\xbf") else b""
    eol = "\r\n" if b"\r\n" in current else "\n"
    return head, current, prefix + expected.replace("\n", eol).encode("utf-8"), False


def full_function(source: str) -> str:
    tree = ast.parse(source)
    functions = [item for item in tree.body
                 if isinstance(item, ast.FunctionDef)
                 and item.name == "combine_adjacent_verified_eta_sentences"]
    if len(functions) != 1:
        raise RuntimeError("changed function is missing")
    item = functions[0]
    lines = source.splitlines(keepends=True)
    return "".join(lines[item.lineno - 1:item.end_lineno])


def imported_code(source: str) -> str:
    tree = ast.parse(source)
    imports = [item for item in tree.body
               if isinstance(item, (ast.Import, ast.ImportFrom))]
    lines = source.splitlines(keepends=True)
    if not imports:
        return "(no imports)\n"
    return "".join(lines[imports[0].lineno - 1:imports[-1].end_lineno])


def output_documentation(updated: bytes) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source = normalized(updated).decode("utf-8")
    tests = (HERE / "tests/test_correction.py").read_text(encoding="utf-8")
    guards = (HERE / "tests/test_install.py").read_text(encoding="utf-8")
    blocks = [
        "# Phase 171 R20R13R2 — 変更後コード全文\n\n",
        "変更対象ファイル：`phase171_r20r13_eta_sentence_layout/projection.py`。\n",
        "変更関数：`combine_adjacent_verified_eta_sentences` 全体。\n",
        "既存 import・Proof Tree・Reference・Renderer 本体は変更しない。\n",
        "新規ファイル：`phase171_r20r13r2_multiple_blank_eta_merge/` の installer, audit, tests。\n\n",
        "## 変更対象 import 全文\n\n```python\n", imported_code(source), "\n```\n\n",
        "## 変更関数全文\n\n```python\n", full_function(source), "\n```\n\n",
        "## 修正後 projection.py 全文\n\n```python\n", source, "\n```\n\n",
        "## 新規テスト全文\n\n```python\n", guards, "\n```\n\n",
        "```python\n", tests, "\n```\n",
    ]
    (OUTPUT / "CODE_FULL_JA.md").write_text("".join(blocks), encoding="utf-8")
    (OUTPUT / "projection.py.FULL").write_bytes(updated)


def run(*, dry_run: bool = False) -> None:
    head, current, edited, already = preflight()
    print("PHASE171_R20R13R2_BRANCH=develop", flush=True)
    print("PHASE171_R20R13R2_HEAD=" + head, flush=True)
    print("PHASE171_R20R13R2_SOURCE_GUARD=PASS", flush=True)
    print("PHASE171_R20R13R2_RENDERER_UNCHANGED=True", flush=True)
    print("PHASE171_R20R13R2_ALREADY_INSTALLED=" + str(already), flush=True)
    if dry_run:
        print("PHASE171_R20R13R2_DRY_RUN=PASS", flush=True)
        return
    if not already:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT / "projection.py.before_r2").write_bytes(current)
        (ROOT / TARGET).write_bytes(edited)
        print("PHASE171_R20R13R2_PATCHED=" + TARGET.as_posix(), flush=True)
    output_documentation(edited)
    print("PHASE171_R20R13R2_FULL_CODE=" + str(OUTPUT / "CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R20R13R2_RESULT=PASS_PATCHED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
