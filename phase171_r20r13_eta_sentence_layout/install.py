"""Content-guarded R20R13 installation; preserve complete renderer replacement code."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGET = Path("phase168_r3_5_model_renderer.py")
REVIEWED_BLOB = "6da35e58c4e73d7152a594dd0d21f1659e619aef"
REVIEWED_PREVIOUS_BLOB = "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0"
OLD = '''    if order_summary is not None:
        lines = suppress_exact_duplicate_body_lines(lines)
    return "\\n".join(lines).rstrip() + "\\n"
'''
NEW = '''    if order_summary is not None:
        lines = suppress_exact_duplicate_body_lines(lines)
    if not incomplete:
        from phase171_r20r13_eta_sentence_layout.projection import (
            format_complete_proof_sentences,
        )
        lines = format_complete_proof_sentences(lines, model)
    return "\\n".join(lines).rstrip() + "\\n"
'''


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True,
        encoding="utf-8", errors="replace", capture_output=True,
    ).stdout.strip()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def matches_blob(data: bytes) -> bool:
    plain = normalize(data)
    return REVIEWED_BLOB in (
        git_blob(data), git_blob(plain), git_blob(plain.replace(b"\n", b"\r\n")),
    )


def transform(source: str) -> str:
    if source.count(OLD) != 1:
        raise RuntimeError("reviewed renderer return anchor differs; no changes applied")
    target = source.replace(OLD, NEW, 1)
    ast.parse(target)
    return target


def preserve_eol(original: bytes, text: str) -> bytes:
    prefix = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    eol = "\r\n" if b"\r\n" in original else "\n"
    return prefix + text.replace("\n", eol).encode("utf-8")


def full_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    functions = [item for item in tree.body
                 if isinstance(item, ast.FunctionDef) and item.name == name]
    if len(functions) != 1:
        raise RuntimeError("renderer function missing or ambiguous")
    lines = source.splitlines(keepends=True)
    return "".join(lines[functions[0].lineno - 1:functions[0].end_lineno])


def top_imports(source: str) -> str:
    tree = ast.parse(source)
    imports = [item for item in tree.body
               if isinstance(item, (ast.Import, ast.ImportFrom))]
    if not imports:
        return "(no module-level imports)\n"
    lines = source.splitlines(keepends=True)
    return "".join(lines[imports[0].lineno - 1:imports[-1].end_lineno])


def write_documentation(edited: bytes) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    raw = edited.decode("utf-8-sig").replace("\r\n", "\n")
    helper = (HERE / "projection.py").read_text(encoding="utf-8")
    (OUTPUT / "phase168_r3_5_model_renderer.py.FULL").write_text(raw, encoding="utf-8")
    items = [
        "# Phase 171 R20R13 — 全変更コード\n\n",
        "変更ファイル: `phase168_r3_5_model_renderer.py` の関数 `render_model_backed_narrative_markdown` 全体。\n",
        "新規追加: `phase171_r20r13_eta_sentence_layout/projection.py`（パッケージルート）。\n",
        "既存の import 変更はありません。\n\n",
        "## 既存 Renderer の import 全文\n\n```python\n",
        top_imports(raw), "\n```\n\n",
        "## 変更した関数全文\n\n```python\n",
        full_function(raw, "render_model_backed_narrative_markdown"), "\n```\n\n",
        "## 新規 projection.py 全文（import を含む）\n\n```python\n",
        helper, "\n```\n\n",
        "## テスト全文\n\n",
    ]
    for file in sorted((HERE / "tests").glob("test_*.py")):
        items.extend((f"### {file.name}\n\n```python\n",
                      file.read_text(encoding="utf-8"), "\n```\n\n"))
    (OUTPUT / "CODE_FULL_JA.md").write_text("".join(items), encoding="utf-8")


def run(*, dry_run: bool = False) -> None:
    branch = git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R20R13 requires develop; no files modified")
    head = git("rev-parse", "HEAD")
    target = ROOT / TARGET
    if not target.is_file():
        raise RuntimeError("renderer missing")
    committed = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.as_posix()],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout
    # Two known user states are supported: pre-R20R12 HEAD with the exact
    # reviewed R20R12 patch in the working tree, or the later committed HEAD.
    if not (matches_blob(committed) or REVIEWED_PREVIOUS_BLOB in (
            git_blob(committed), git_blob(normalize(committed)),
            git_blob(normalize(committed).replace(b"\n", b"\r\n")))):
        raise RuntimeError("HEAD renderer differs from both reviewed baselines")
    original = target.read_bytes()
    if not matches_blob(original):
        # Installed version can also be reused, but only if HEAD already
        # contains the exact reviewed renderer and transformed text matches.
        if not matches_blob(committed):
            raise RuntimeError("working renderer differs from reviewed R20R12 baseline")
        expected = transform(committed.decode("utf-8-sig").replace("\r\n", "\n"))
        target_text = original.decode("utf-8-sig").replace("\r\n", "\n")
        if target_text != expected:
            raise RuntimeError("renderer has unrelated modifications; refusing to overwrite")
        already = True
        edited_text = expected
    else:
        reviewed_text = original.decode("utf-8-sig").replace("\r\n", "\n")
        edited_text = transform(reviewed_text)
        already = False
    prepared = preserve_eol(original, edited_text)
    ast.parse(edited_text)
    print("PHASE171_R20R13_BRANCH=" + branch, flush=True)
    print("PHASE171_R20R13_HEAD=" + head, flush=True)
    print("PHASE171_R20R13_SOURCE_GUARD=PASS", flush=True)
    print("PHASE171_R20R13_ALREADY_INSTALLED=" + str(already), flush=True)
    print("PHASE171_R20R13_CHANGED_FILE=" + TARGET.as_posix(), flush=True)
    if dry_run:
        print("PHASE171_R20R13_DRY_RUN=PASS", flush=True)
        return
    if not already:
        target.write_bytes(prepared)
        print("PHASE171_R20R13_PATCHED=" + TARGET.as_posix(), flush=True)
    write_documentation(prepared if not already else original)
    print("PHASE171_R20R13_FULL_CODE=" + str(OUTPUT / "CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R20R13_RESULT=PASS_PATCHED", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
