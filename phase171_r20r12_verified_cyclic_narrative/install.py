"""Guarded, minimal R20R12 renderer-only installer with full-code export."""
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
EXPECTED_BLOB = "4b4478ccbc20a4264be86e61b7a2c72f69b1e5b0"

ANCHOR_PREPARE = "    displayed_cyclic_math = set()\n"
INSERT_PREPARE = '''    from phase171_r20r12_verified_cyclic_narrative.projection import (
        verified_order_four_summary,
        suppress_exact_duplicate_body_lines,
    )
    order_summary = verified_order_four_summary(model) if not incomplete else None
'''
ANCHOR_ROOT = '''    for index in order:
        if direct_sum_display is not None and index == direct_sum_display.root_index:
'''
INSERT_ROOT = '''    for index in order:
        if order_summary is not None and index == model.root_index:
            lines.extend((order_summary, ""))
        if direct_sum_display is not None and index == direct_sum_display.root_index:
'''
ANCHOR_NOTICE = '''            if notice is not None:
                if notice:
                    lines.extend((notice, ""))
                continue
'''
INSERT_NOTICE = '''            if notice is not None:
                # The duplicate has already been displayed; its provenance
                # remains in Reference and the verified Proof Tree.
                if notice and order_summary is None:
                    lines.extend((notice, ""))
                continue
'''
ANCHOR_RETURN = '''    return "\\n".join(lines).rstrip() + "\\n"
'''
INSERT_RETURN = '''    if order_summary is not None:
        lines = suppress_exact_duplicate_body_lines(lines)
    return "\\n".join(lines).rstrip() + "\\n"
'''


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True,
        text=True, capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def matches_reviewed_blob(data: bytes) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return EXPECTED_BLOB in (
        git_blob_sha(data), git_blob_sha(normalized),
        git_blob_sha(normalized.replace(b"\n", b"\r\n")),
    )


def replace_once(source: str, old: str, new: str, label: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError("R20R12 unexpected renderer: " + label)
    return source.replace(old, new, 1)


def transform_source(source: str) -> str:
    """Change only one complete renderer function, not proof/search modules."""
    source = replace_once(source, ANCHOR_PREPARE,
                          ANCHOR_PREPARE + INSERT_PREPARE, "projection insertion")
    source = replace_once(source, ANCHOR_ROOT, INSERT_ROOT, "root prose insertion")
    source = replace_once(source, ANCHOR_NOTICE, INSERT_NOTICE, "duplicate notice")
    source = replace_once(source, ANCHOR_RETURN, INSERT_RETURN, "line deduplication")
    ast.parse(source)
    return source


def preserve_format(original: bytes, transformed: str) -> bytes:
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    endline = "\r\n" if b"\r\n" in original else "\n"
    return bom + transformed.replace("\n", endline).encode("utf-8")


def full_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    nodes = [node for node in tree.body
             if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
             and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("expected exactly one renderer function")
    lines = source.splitlines(keepends=True)
    return "".join(lines[nodes[0].lineno - 1:nodes[0].end_lineno])


def top_level_imports(source: str) -> str:
    tree = ast.parse(source)
    imports = [node for node in tree.body
               if isinstance(node, (ast.Import, ast.ImportFrom))]
    if not imports:
        return "(no module-level imports)\n"
    lines = source.splitlines(keepends=True)
    return "".join(lines[imports[0].lineno - 1:imports[-1].end_lineno])


def preflight() -> tuple[str, bytes]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R20R12 requires develop branch; no change applied")
    head = git("rev-parse", "HEAD")
    path = ROOT / TARGET
    if not path.is_file():
        raise RuntimeError("target renderer not found")
    original = path.read_bytes()
    if not matches_reviewed_blob(original):
        raise RuntimeError("renderer differs from reviewed GitHub develop")
    committed = subprocess.run(
        ["git", "show", "HEAD:" + TARGET.as_posix()],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    if not matches_reviewed_blob(committed):
        raise RuntimeError("renderer HEAD content differs from reviewed GitHub")
    if original.replace(b"\r\n", b"\n") != committed.replace(b"\r\n", b"\n"):
        raise RuntimeError("renderer already modified; refusing overwrite")
    return head, original


def write_full_code(new_bytes: bytes) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    raw = new_bytes.decode("utf-8-sig").replace("\r\n", "\n")
    (OUTPUT / "phase168_r3_5_model_renderer.py.FULL").write_text(raw, encoding="utf-8")
    helper = (HERE / "projection.py").read_text(encoding="utf-8")
    text = (
        "# Phase 171 R20R12 — 完全な変更コード\n\n"
        "変更対象: `phase168_r3_5_model_renderer.py` / "
        "`render_model_backed_narrative_markdown`。\n\n"
        "新規モジュール: `phase171_r20r12_verified_cyclic_narrative/projection.py`。\n\n"
        "変更した Renderer の import（トップレベル）全文:\n\n```python\n"
        + top_level_imports(raw) + "```\n\n"
        "変更した Renderer 関数全文（そのまま置換可能）:\n\n```python\n"
        + full_function(raw, "render_model_backed_narrative_markdown") + "\n```\n\n"
        "新規の projection.py 全文（パッケージ内新規追加）:\n\n```python\n"
        + helper + "\n```\n\n"
        "テスト関数全文は ZIP の tests 以下を参照。\n"
        "Renderer のファイル全体は `output/phase168_r3_5_model_renderer.py.FULL` に保存。\n"
    )
    (OUTPUT / "CODE_FULL_JA.md").write_text(text, encoding="utf-8")


def run(*, dry_run: bool = False) -> None:
    head, original = preflight()
    edited = transform_source(original.decode("utf-8-sig").replace("\r\n", "\n"))
    new_bytes = preserve_format(original, edited)
    print("PHASE171_R20R12_BRANCH=develop", flush=True)
    print("PHASE171_R20R12_HEAD=" + head, flush=True)
    print("PHASE171_R20R12_SOURCE_GUARD=PASS", flush=True)
    print("PHASE171_R20R12_CHANGED_FILE=" + TARGET.as_posix(), flush=True)
    if dry_run:
        print("PHASE171_R20R12_DRY_RUN=PASS", flush=True)
        return
    write_full_code(new_bytes)
    path = ROOT / TARGET
    path.write_bytes(new_bytes)
    print("PHASE171_R20R12_PATCHED=" + TARGET.as_posix(), flush=True)
    print("PHASE171_R20R12_FULL_CODE=" + str(OUTPUT / "CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R20R12_RESULT=PASS_PATCHED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    run(dry_run=arguments.dry_run)


if __name__ == "__main__":
    main()
