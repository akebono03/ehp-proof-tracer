"""Phase 171 R20R13R4: guarded test-only fix for list.count assertion.

No production code or mathematical inference is modified. The existing
R20R13R2/R3 workflow is rerun after repairing the single faulty assertion.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGET = Path("phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py")
PROJECTION = Path("phase171_r20r13_eta_sentence_layout/projection.py")
RENDERER = Path("phase168_r3_5_model_renderer.py")
ORIGINAL_SHA256 = "40cab7a2e70ccc1dec44b97a15c7706ffaa83e23cb22e0a75f93568a99e7be60"
CORRECTED_SHA256 = "319f9be268c49264a799d45f841ae0fd2a153399ff27dd7c4eafdd795660dbfe"
PROJECTION_SHA256 = "701c1ec9de253a8f0df68bae1ac711b449a4516ab6d03d6132be7ab84615d006"
OLD = '    assert actual.count("[R3]より, ") == 1\n'
NEW = '    assert sum(line.startswith("[R3]より, ") for line in actual) == 1\n'


def normalized(raw: bytes) -> str:
    return raw.decode("utf-8-sig").replace("\r\n", "\n")


def sha256(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def preflight() -> tuple[str, bytes, bytes, bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R20R13R4 requires the develop branch")
    head = git("rev-parse", "HEAD")
    path = ROOT / TARGET
    projection = ROOT / PROJECTION
    renderer = ROOT / RENDERER
    if not path.is_file() or not projection.is_file() or not renderer.is_file():
        raise RuntimeError("R20R13R2/R3 test, projection, or renderer is missing")
    if sha256(normalized(projection.read_bytes())) != PROJECTION_SHA256:
        raise RuntimeError("R20R13R2 projection is not the reviewed corrected content")
    if "format_complete_proof_sentences(lines, model)" not in renderer.read_text(encoding="utf-8-sig"):
        raise RuntimeError("R20R13 renderer hook is missing")
    source = path.read_bytes()
    plain = normalized(source)
    digest = sha256(plain)
    if digest == CORRECTED_SHA256:
        return head, source, source, True
    if digest != ORIGINAL_SHA256 or plain.count(OLD) != 1:
        raise RuntimeError("test source differs from reviewed R20R13R2; no overwrite")
    corrected = plain.replace(OLD, NEW, 1)
    if sha256(corrected) != CORRECTED_SHA256:
        raise RuntimeError("corrected test hash mismatch")
    bom = b"\xef\xbb\xbf" if source.startswith(b"\xef\xbb\xbf") else b""
    eol = "\r\n" if b"\r\n" in source else "\n"
    updated = bom + corrected.replace("\n", eol).encode("utf-8")
    return head, source, updated, False


def changed_test_function(source: str) -> str:
    import ast
    tree = ast.parse(source)
    candidates = [
        item for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        and item.name == "test_orphan_blank_lines_do_not_break_three_verified_eta_equations"
    ]
    if len(candidates) != 1:
        raise RuntimeError("expected exactly one corrected test function")
    node = candidates[0]
    return "\n".join(source.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def output_documentation(source: bytes) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    content = normalized(source)
    lines = [
        "# Phase 171 R20R13R4 — テストのみ修正\n\n",
        "変更対象：`phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py`。\n\n",
        "変更関数：`test_orphan_blank_lines_do_not_break_three_verified_eta_equations`（全文）。\n\n",
        "import の変更はない。変更後の import 全文：\n\n",
        "```python\n",
        "from __future__ import annotations\n\n",
        "from types import SimpleNamespace\n\n",
        "import pytest\n\n",
        "from phase171_r20r13_eta_sentence_layout.projection import (\n",
        "    combine_adjacent_verified_eta_sentences,\n",
        "    verified_eta_display_sentences,\n",
        ")\n",
        "```\n\n",
        "## 変更したテスト関数全文\n\n```python\n",
        changed_test_function(content), "```\n\n",
        "## 置換後のテストファイル全文\n\n```python\n",
        content, "\n```\n\n",
        "## 新規インストーラ全文\n\n```python\n",
        (HERE / "install.py").read_text(encoding="utf-8"), "\n```\n\n",
        "## 新規テスト全文\n\n```python\n",
        (HERE / "tests/test_install.py").read_text(encoding="utf-8"), "\n```\n",
    ]
    (OUTPUT / "CODE_FULL_JA.md").write_text("".join(lines), encoding="utf-8")
    (OUTPUT / "test_correction.py.FULL").write_bytes(source)


def run(*, dry_run: bool = False) -> None:
    head, before, after, already = preflight()
    print("PHASE171_R20R13R4_BRANCH=develop", flush=True)
    print("PHASE171_R20R13R4_HEAD=" + head, flush=True)
    print("PHASE171_R20R13R4_PROJECTION_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_R20R13R4_TEST_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_R20R13R4_ALREADY_INSTALLED=" + str(already), flush=True)
    if dry_run:
        print("PHASE171_R20R13R4_DRY_RUN=PASS", flush=True)
        return
    if not already:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        (OUTPUT / "test_correction.py.before_r4").write_bytes(before)
        (ROOT / TARGET).write_bytes(after)
        print("PHASE171_R20R13R4_PATCHED=" + TARGET.as_posix(), flush=True)
    output_documentation(after)
    print("PHASE171_R20R13R4_PRODUCTION_MODIFIED=False", flush=True)
    print("PHASE171_R20R13R4_RESULT=PASS_TEST_PATCHED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
