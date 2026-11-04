# R15R13 共通表示契約 — 変更単位の全文

## 変更対象

- `web_group_proof_common.py`: `_build_group_proof_rendered_lines`（関数全体を置換）
- `phase173_r4_r15r13_unified_presentation/layout.py`: `canonicalize_proof_layout`（新規関数、モジュール全体）
- `phase173_r4_r15r13_unified_presentation/tests/test_contract.py`: 新規テスト関数（ファイル全体）
- `phase173_r4_r15r13_unified_presentation/tests/test_integration.py`: 新規テスト関数（ファイル全体）

既存 import の変更はありません。`_build_group_proof_rendered_lines` は関数内部で新しい共通レイアウトを import します。

### `web_group_proof_common.py` の変更後関数全文

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
  from phase173_r4_r15r13_unified_presentation.layout import (
    canonicalize_proof_layout,
  )
  for raw_line in canonicalize_proof_layout(markdown).splitlines():
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

### `layout.py` の全内容

```python
"""Status-independent presentation contract for all group proof narratives.

This is a structural presentation pass. It adds no ProofStep, inference,
literature reference, group conclusion, or proof status. The existing Markdown
API remains unchanged. One Web section hierarchy is produced for every status.
"""
from __future__ import annotations


def canonicalize_proof_layout(markdown: str) -> str:
    """Use one Reference/Proof section layout, preserving proof body verbatim.

    Both historical Markdown spellings (plain and ## headings) represent the
    same semantic sections. Only the outer Web-owned target and Proof headers
    are suppressed when duplicates are present inside the narrative. This
    transformation never reads status, n, k, references, or mathematical data.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be str")
    lines = markdown.splitlines()
    reference_indices = [
        i for i, line in enumerate(lines)
        if line.strip() in ("使用する結果", "## 使用する結果")
    ]
    if len(reference_indices) != 1:
        return markdown
    reference_index = reference_indices[0]
    proof_indices = [
        i for i in range(reference_index + 1, len(lines))
        if lines[i].strip() in ("証明", "## 証明")
    ]
    if len(proof_indices) != 1:
        return markdown
    proof_index = proof_indices[0]

    prelude = list(lines[:reference_index])
    # WebGroupProofView already presents the group target above the narrative.
    # Remove the second copy only when the entire prelude consists of that
    # exact heading and one displayable math target. Leave unknown preludes
    # intact rather than silently discarding source content.
    meaningful = [line.strip() for line in prelude if line.strip()]
    if (len(meaningful) == 2 and meaningful[0] == "## 証明対象"
            and meaningful[1].startswith("$") and meaningful[1].endswith("$")):
        prelude = []

    reference_body = list(lines[reference_index + 1:proof_index])
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    if reference_body and reference_body[-1].strip() == "---":
        reference_body.pop()
    while reference_body and not reference_body[-1].strip():
        reference_body.pop()
    while reference_body and not reference_body[0].strip():
        reference_body.pop(0)

    proof_body = list(lines[proof_index + 1:])
    while proof_body and not proof_body[0].strip():
        proof_body.pop(0)

    # The outer Web Proof heading owns the proof section title. All narratives
    # receive the same inner Reference heading and the same section separator.
    # Only headings and redundant duplicate-target presentation are modified.
    normalized = [*prelude, "## 使用する結果", "", *reference_body,
                  "", "---", "", *proof_body]
    result = "\n".join(normalized)
    return result.rstrip("\n") + ("\n" if markdown.endswith("\n") else "")
```
