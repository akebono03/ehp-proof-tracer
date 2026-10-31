"""Guarded one-file correction for R20R12's unindexed nu-prime display."""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUT = HERE / "output"
TARGET = Path("phase171_r20r12_verified_cyclic_narrative/projection.py")
RENDERER = Path("phase168_r3_5_model_renderer.py")
EXPECTED_ORIGINAL_SHA256 = "f110d25ebf6835358d1ea638498dabff32d830fc9117f7be29b70b8079e19ab1"
SOURCE_OLD_IMPORT = (
    "from phase168_r3_27_typed_statement_projection import element_tex, group_tex\n"
)
SOURCE_NEW_IMPORT = (
    "from phase168_r3_27_typed_statement_projection import group_tex\n"
)
SOURCE_OLD_LINE = "    element = element_tex(order.element)\n"
SOURCE_NEW_LINE = "    element = render_toda_expression_latex(order.element)\n"


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT, check=True, capture_output=True,
        encoding="utf-8", errors="replace",
    ).stdout.strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def corrected_source(original: bytes) -> bytes:
    text = original.decode("utf-8-sig")
    normalized = text.replace("\r\n", "\n")
    for old, name in ((SOURCE_OLD_IMPORT, "import"), (SOURCE_OLD_LINE, "generator")):
        if normalized.count(old) != 1:
            raise RuntimeError("reviewed projection anchor mismatch: " + name)
    changed = normalized.replace(SOURCE_OLD_IMPORT, SOURCE_NEW_IMPORT, 1)
    changed = changed.replace(SOURCE_OLD_LINE, SOURCE_NEW_LINE, 1)
    ast.parse(changed)
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    eol = "\r\n" if b"\r\n" in original else "\n"
    return bom + changed.replace("\n", eol).encode("utf-8")


def normalized(data: bytes) -> bytes:
    return data.decode("utf-8-sig").replace("\r\n", "\n").encode("utf-8")


def render_full_code(updated: bytes) -> str:
    content = updated.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(content)
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                 and n.name == "verified_order_four_summary"]
    if len(functions) != 1:
        raise RuntimeError("verified_order_four_summary function missing")
    source_lines = content.splitlines(keepends=True)
    fn = functions[0]
    fn_text = "".join(source_lines[fn.lineno - 1:fn.end_lineno])
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    if not imports:
        raise RuntimeError("missing imports")
    import_text = "".join(source_lines[imports[0].lineno - 1:imports[-1].end_lineno])
    tests_path = HERE / "tests/test_correction.py"
    tests = tests_path.read_text(encoding="utf-8")
    return (
        "# Phase 171 R20R12R2 — 変更後コード全文\n\n"
        "変更対象: `phase171_r20r12_verified_cyclic_narrative/projection.py`。\n"
        "変更関数: `verified_order_four_summary`。\n"
        "数学的証明規則および Renderer 本体は変更しない。\n\n"
        "## 変更後 import 全文\n\n```python\n" + import_text + "```\n\n"
        "## 変更関数全文\n\n```python\n" + fn_text + "\n```\n\n"
        "## 修正後ファイル全文\n\n```python\n" + content + "\n```\n\n"
        "## 新規テスト全文\n\n```python\n" + tests + "\n```\n"
    )


def preflight() -> tuple[str, bytes, bytes, bool]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R20R12R2 requires develop branch")
    head = git("rev-parse", "HEAD")
    source_path = ROOT / TARGET
    if not source_path.is_file():
        raise RuntimeError("R20R12 original projection module is absent")
    current = source_path.read_bytes()
    # Accept only the exact reviewed R20R12 module, or this exact correction.
    old_package = HERE.parent / "phase171_r20r12_verified_cyclic_narrative"
    if not (old_package / "tests/test_projection.py").is_file():
        raise RuntimeError("R20R12 original tests not installed")
    from phase171_r20r12_verified_cyclic_narrative.install import (
        matches_reviewed_blob, transform_source, preserve_format,
    )
    committed = subprocess.run(
        ("git", "show", "HEAD:" + RENDERER.as_posix()), cwd=ROOT,
        check=True, capture_output=True,
    ).stdout
    if not matches_reviewed_blob(committed):
        raise RuntimeError("the committed renderer is no longer the reviewed baseline")
    patched = preserve_format(
        committed, transform_source(committed.decode("utf-8-sig").replace("\r\n", "\n")),
    )
    installed = (ROOT / RENDERER).read_bytes()
    if normalized(installed) != normalized(patched):
        raise RuntimeError("installed renderer differs from R20R12; refusing changes")
    if sha256(current) == EXPECTED_ORIGINAL_SHA256:
        replacement = corrected_source(current)
        already = False
    else:
        # Already installed with stable original newline/BOM form.
        reviewed_original = (HERE / "original_projection.py.reviewed").read_bytes()
        if sha256(reviewed_original) != EXPECTED_ORIGINAL_SHA256:
            raise RuntimeError("bundled reviewed R20R12 projection mismatch")
        replacement = corrected_source(reviewed_original)
        if normalized(current) != normalized(replacement):
            raise RuntimeError("projection contains unrelated edits; refusing overwrite")
        already = True
    return head, current, replacement, already


def run(*, dry_run: bool = False) -> None:
    head, current, replacement, already = preflight()
    print("PHASE171_R20R12R2_BRANCH=develop", flush=True)
    print("PHASE171_R20R12R2_HEAD=" + head, flush=True)
    print("PHASE171_R20R12R2_SOURCE_GUARD=PASS", flush=True)
    print("PHASE171_R20R12R2_RENDERER_UNCHANGED=True", flush=True)
    print("PHASE171_R20R12R2_ALREADY_INSTALLED=" + str(already), flush=True)
    if dry_run:
        print("PHASE171_R20R12R2_DRY_RUN=PASS", flush=True)
        return
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "CODE_FULL_JA.md").write_text(render_full_code(replacement), encoding="utf-8")
    (OUTPUT / "projection.py.FULL").write_bytes(replacement)
    if not already:
        (OUTPUT / "projection.py.before_r2").write_bytes(current)
        (ROOT / TARGET).write_bytes(replacement)
    print("PHASE171_R20R12R2_PATCHED=" + TARGET.as_posix(), flush=True)
    print("PHASE171_R20R12R2_FULL_CODE=" + str(OUTPUT / "CODE_FULL_JA.md"), flush=True)
    print("PHASE171_R20R12R2_RESULT=PASS_PATCHED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
