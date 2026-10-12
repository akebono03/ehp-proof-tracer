# Phase 164 R5-R3 — パッチ前提判定の修正

変更対象: `apply_patch.py` の `_check_original_shape`, `main`; 共通パーサーの `_build_group_proof_inline_segments`, `_build_group_proof_rendered_lines`; 新規テスト12件。既存 Renderer・証明木・文献は変更しない。

AST によって複数行に分かれた現行コードも判定できる。変更前バックアップを保存し、既適用時は再適用しない。局所 pytest はバンドル内のテストを実行する。

## apply_patch.py

```python
"""Install two shared Web display-parser functions with AST-backed baseline checks."""
import ast
from pathlib import Path

REPLACEMENTS = {
    "_build_group_proof_inline_segments": "replacement_inline_segments.txt",
    "_build_group_proof_rendered_lines": "replacement_rendered_lines.txt",
}


def _check_original_shape(name: str, node: ast.FunctionDef) -> bool:
    """Accept multiline formatting without confusing unrelated implementations."""
    calls = (
        {"find", "append"}
        if name == "_build_group_proof_inline_segments"
        else {"splitlines", "append"}
    )
    called = {
        part.func.attr
        for part in ast.walk(node)
        if isinstance(part, ast.Call) and isinstance(part.func, ast.Attribute)
    }
    text_values = {
        part.value
        for part in ast.walk(node)
        if isinstance(part, ast.Constant) and isinstance(part.value, str)
    }
    if not calls.issubset(called):
        return False
    if name == "_build_group_proof_inline_segments":
        return r"\tag{" in text_values and "inline_math" in text_values
    return "## " in text_values and r"\[" in text_values


def main() -> None:
    bundle = Path(__file__).resolve().parent
    target = bundle.parent / "web_group_proof.py"
    source = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    functions = {
        node.name: node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    lines = source.splitlines(keepends=True)
    planned = []
    installed_count = 0

    for name, filename in REPLACEMENTS.items():
        if name not in functions:
            raise ValueError(f"Required function missing: {name}")
        node = functions[name]
        old = ast.get_source_segment(source, node)
        new = (bundle / filename).read_text(encoding="utf-8")
        new_tree = ast.parse(new)
        if len(new_tree.body) != 1 or not isinstance(new_tree.body[0], ast.FunctionDef):
            raise ValueError(f"Replacement must contain one complete function: {name}")
        if new_tree.body[0].name != name:
            raise ValueError(f"Replacement function name mismatch: {name}")
        if ast.dump(node, include_attributes=False) == ast.dump(new_tree.body[0], include_attributes=False):
            installed_count += 1
            continue
        if not _check_original_shape(name, node):
            raise ValueError(f"Unexpected parser structure: {name}")
        planned.append((
            sum(map(len, lines[:node.lineno - 1])),
            sum(map(len, lines[:node.end_lineno])),
            new,
        ))

    if installed_count == len(REPLACEMENTS):
        print("Shared Web math parser already installed; no changes")
        return

    updated = source
    for start, end, new in sorted(planned, reverse=True):
        updated = updated[:start] + new + updated[end:]
    ast.parse(updated)
    backup = bundle.parent / "web_group_proof.phase164_r5_r3_backup.py"
    if not backup.exists():
        backup.write_text(source, encoding="utf-8")
    target.write_text(updated, encoding="utf-8")
    print("Updated common Web math parser; backup:", backup.name)


if __name__ == "__main__":
    main()

```

## replacement_inline_segments.txt

```python
def _build_group_proof_inline_segments(
  line: str,
) -> tuple[
  WebGroupProofInlineSegmentView,
  ...,
]:
  if not isinstance(line, str):
    raise TypeError("line must be a str")

  segments = []
  cursor = 0
  while cursor < len(line):
    next_math = line.find("$", cursor)
    next_strong = line.find("**", cursor)
    delimiters = tuple(
      (position, kind)
      for position, kind in (
        (next_math, "inline_math"),
        (next_strong, "strong"),
      )
      if position >= 0
    )
    if not delimiters:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[cursor:]
      ))
      break

    position, kind = min(delimiters, key=lambda item: item[0])
    if position > cursor:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[cursor:position]
      ))

    if kind == "inline_math":
      closing = line.find("$", position + 1)
      if closing < 0:
        segments.append(WebGroupProofInlineSegmentView(
          kind="text", value=line[position:]
        ))
        break
      math_value = line[position + 1:closing]
      if not math_value:
        segments.append(WebGroupProofInlineSegmentView(
          kind="text", value="$$"
        ))
        cursor = closing + 1
        continue

      is_tagged = r"\tag{" in math_value
      cursor = closing + 1
      if is_tagged:
        # A tagged equation renders as a display block.  A standalone
        # punctuation suffix otherwise becomes an orphaned HTML text span.
        # Keep the punctuation with the equation, before its equation tag.
        suffix = line[cursor:]
        if suffix.strip() in (".", "。", ",", "、"):
          mark = "." if suffix.strip() in (".", "。") else ","
          tag_position = math_value.rfind(r"\tag{")
          math_value = (
            math_value[:tag_position]
            + r"\text{" + mark + "}"
            + math_value[tag_position:]
          )
          cursor = len(line)

      segments.append(WebGroupProofInlineSegmentView(
        kind="display_math" if is_tagged else "inline_math",
        value=math_value,
      ))
      continue

    closing = line.find("**", position + 2)
    if closing < 0:
      segments.append(WebGroupProofInlineSegmentView(
        kind="text", value=line[position:]
      ))
      break
    strong_value = line[position + 2:closing]
    segments.append(WebGroupProofInlineSegmentView(
      kind="strong" if strong_value else "text",
      value=strong_value if strong_value else "****",
    ))
    cursor = closing + 2

  return tuple(segments)

```

## replacement_rendered_lines.txt

```python
def _build_group_proof_rendered_lines(
  markdown: str,
) -> tuple[
  WebGroupProofRenderedLineView,
  ...,
]:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a str")

  lines = []
  display_math_lines = None
  display_math_indent_level = 0
  for raw_line in markdown.splitlines():
    stripped = raw_line.lstrip(" ")
    indent_level = (len(raw_line) - len(stripped)) // 2

    if stripped == "---":
      lines.append(WebGroupProofRenderedLineView(
        kind="separator", indent_level=0, prefix="",
        statement_latex=None, suffix="",
      ))
      continue

    if display_math_lines is not None:
      if stripped == r"\]":
        statement_latex = "\n".join(display_math_lines)
        lines.append(WebGroupProofRenderedLineView(
          kind="text", indent_level=display_math_indent_level,
          prefix="", statement_latex=statement_latex, suffix="",
          segments=(WebGroupProofInlineSegmentView(
            kind="display_math", value=statement_latex,
          ),),
        ))
        display_math_lines = None
        display_math_indent_level = 0
        continue
      if stripped:
        display_math_lines.append(stripped)
      continue

    if not raw_line:
      continue
    if raw_line.startswith("# "):
      continue
    if stripped.startswith("### "):
      lines.append(WebGroupProofRenderedLineView(
        kind="heading", indent_level=indent_level,
        prefix=stripped[4:], statement_latex=None, suffix="",
      ))
      continue
    if stripped.startswith("## "):
      lines.append(WebGroupProofRenderedLineView(
        kind="heading", indent_level=0,
        prefix=stripped[3:], statement_latex=None, suffix="",
      ))
      continue
    if stripped == r"\[":
      display_math_lines = []
      display_math_indent_level = indent_level
      continue

    prefix, statement_latex, suffix = _split_group_proof_rendered_line(stripped)
    lines.append(WebGroupProofRenderedLineView(
      kind="text", indent_level=indent_level, prefix=prefix,
      statement_latex=statement_latex, suffix=suffix,
      segments=_build_group_proof_inline_segments(stripped),
    ))

  if display_math_lines is not None:
    raise ValueError("unterminated display-math block in rendered group proof")
  return tuple(lines)

```

## tests/test_phase164_r5_r3_math_punctuation.py

```python
"""R5-R3: shared Web math punctuation regression tests."""
import pytest

from web_group_proof import (
    _build_group_proof_inline_segments,
    _build_group_proof_rendered_lines,
)


@pytest.mark.parametrize("mark", [".", "。", ",", "、"])
def test_tagged_equation_keeps_trailing_punctuation_in_display_math(mark):
    segments = _build_group_proof_inline_segments(
        r"$2\nu'=\eta_3\eta_4\eta_5\tag{1}$" + mark
    )
    assert len(segments) == 1
    assert segments[0].kind == "display_math"
    expected = "." if mark in (".", "。") else ","
    assert segments[0].value.endswith(r"\text{" + expected + r"}\tag{1}")


def test_tagged_equation_punctuation_with_space_is_not_orphaned():
    segments = _build_group_proof_inline_segments(r"$x=y\tag{2}$ .")
    assert len(segments) == 1
    assert segments[0].value == r"x=y\text{.}\tag{2}"


def test_tagged_equation_without_punctuation_is_unchanged():
    segments = _build_group_proof_inline_segments(r"$x=y\tag{2}$")
    assert [(s.kind, s.value) for s in segments] == [
        ("display_math", r"x=y\tag{2}"),
    ]


def test_tagged_equation_followed_by_prose_is_not_modified():
    segments = _build_group_proof_inline_segments(r"$x=y\tag{2}$, therefore")
    assert [(s.kind, s.value) for s in segments] == [
        ("display_math", r"x=y\tag{2}"),
        ("text", ", therefore"),
    ]


def test_untagged_inline_equation_keeps_sentence_punctuation():
    segments = _build_group_proof_inline_segments(r"Therefore $x=y$.")
    assert [(s.kind, s.value) for s in segments] == [
        ("text", "Therefore "), ("inline_math", "x=y"), ("text", "."),
    ]


def test_markdown_line_parser_handles_tagged_equation_without_orphan():
    lines = _build_group_proof_rendered_lines(r"$x=y\tag{1}$.")
    assert len(lines) == 1
    assert [(s.kind, s.value) for s in lines[0].segments] == [
        ("display_math", r"x=y\text{.}\tag{1}"),
    ]


def test_third_level_markdown_heading_is_rendered_as_heading():
    lines = _build_group_proof_rendered_lines("### 単射性\n$x=y$.\n")
    assert lines[0].kind == "heading"
    assert lines[0].prefix == "単射性"
    assert lines[1].segments[-1].value == "."


def test_second_level_heading_and_separator_unchanged():
    lines = _build_group_proof_rendered_lines("## 証明\n---\n")
    assert [line.kind for line in lines] == ["heading", "separator"]


def test_unterminated_math_block_still_rejected():
    with pytest.raises(ValueError, match="unterminated display-math"):
        _build_group_proof_rendered_lines("\\[\n x=y")

```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B '.\phase164_r5_r3_patch_guard_fix\apply_patch.py'
if ($LASTEXITCODE -ne 0) { throw 'Web parser patch failed' }
python -B -m pytest -q phase164_r5_r3_patch_guard_fix/tests/test_phase164_r5_r3_math_punctuation.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R3 targeted tests failed' }
Write-Host 'Phase 164 R5-R3 shared punctuation parser installed; full pytest NOT run.'

```

