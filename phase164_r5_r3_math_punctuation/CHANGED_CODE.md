# Phase 164 R5-R3 — 変更コード全文

## 変更対象

- `web_group_proof.py` の `_build_group_proof_inline_segments()` 全体を置換。
- 同ファイルの `_build_group_proof_rendered_lines()` 全体を置換。
- `tests/test_phase164_r5_r3_math_punctuation.py` を新規追加（テストファイル全文）。
- `apply_patch.py`、`run.ps1` を新規追加。
- **import の変更なし、クラスの変更なし。**

## `_build_group_proof_inline_segments()` — 全文

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

## `_build_group_proof_rendered_lines()` — 全文

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

## 追加テスト — `tests/test_phase164_r5_r3_math_punctuation.py` 全文

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

## 適用コード — `apply_patch.py` 全文

```python
"""Install focused shared Web parser changes without replacing unrelated code."""
import ast
from pathlib import Path


REPLACEMENTS = {
    "_build_group_proof_inline_segments": "replacement_inline_segments.txt",
    "_build_group_proof_rendered_lines": "replacement_rendered_lines.txt",
}


def main() -> None:
    bundle = Path(__file__).resolve().parent
    target = bundle.parent / "web_group_proof.py"
    source = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    lines = source.splitlines(keepends=True)
    replacements = []
    for name, filename in REPLACEMENTS.items():
        if name not in functions:
            raise ValueError(f"Required function missing: {name}")
        node = functions[name]
        old = ast.get_source_segment(source, node)
        if name == "_build_group_proof_inline_segments":
            if "tag_position = math_value.rfind" in old:
                print("Shared punctuation parser already installed")
                return
            if 'if r"\\tag{" in math_value' not in old:
                raise ValueError("Unexpected inline parser baseline")
        else:
            if 'stripped.startswith("## ")' not in old:
                raise ValueError("Unexpected line parser baseline")
        new = (bundle / filename).read_text(encoding="utf-8")
        ast.parse(new)
        replacements.append((sum(map(len, lines[:node.lineno-1])),
                             sum(map(len, lines[:node.end_lineno])),new))

    updated = source
    for start, end, replacement in sorted(replacements, reverse=True):
        updated = updated[:start] + replacement + updated[end:]
    ast.parse(updated)
    backup = bundle.parent / "web_group_proof.phase164_r5_r3_backup.py"
    if not backup.exists():
        backup.write_text(source, encoding="utf-8")
    target.write_text(updated, encoding="utf-8")
    print("Updated common Web math parser; backup:", backup.name)


if __name__ == "__main__":
    main()
```

## 実行コード — `run.ps1` 全文

```powershell
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
python -B ".\phase164_r5_r3_math_punctuation\apply_patch.py"
if ($LASTEXITCODE -ne 0) { throw 'Web parser patch failed' }
python -B -m pytest -q tests/test_phase164_r5_r3_math_punctuation.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R3 targeted tests failed' }
Write-Host 'Phase 164 R5-R3 shared math punctuation fixed. Full pytest NOT run.'
```

## 変更・検証・Phase 境界

- 文献命題・ProofStep・Narrative Renderer の本文生成は変更しない。
- 番号式の末尾句読点のみ KaTeX の `\text{...}` として式の内側に移す。
- `###` の見出しが通常文字列にならないよう共通パーサーで認識する。
- 局所テストのみ実施。全体 pytest は Phase 164 終了時に実施する。
- 今後の証明の数学的内容・Reference や重複の改善は対象外。
