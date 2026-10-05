# Phase 158-R5-5b repair1b changed code

## 変更対象

Production code:
- 変更なし

Test:
- `tests/test_phase158_r5_5b_public_generic_order_route.py`
  - `_web_text()` 全体を修正

import の変更はありません。

変更後の `_web_text()`:

```python
def _web_text(
  n: int,
  k: int,
) -> str:
  view = build_standard_web_group_proof_view(
    n,
    k,
    max_depth=2,
    mode="narrative",
  )
  parts = []
  in_proof = False

  for line in view.rendered_lines:
    if (
      line.kind == "heading"
      and line.prefix == "証明"
    ):
      in_proof = True
      continue

    if not in_proof:
      continue

    if line.segments:
      parts.append(
        "".join(
          segment.value
          for segment in line.segments
        )
      )
    else:
      parts.append(
        line.prefix
        + (
          ""
          if line.statement_latex is None
          else line.statement_latex
        )
        + line.suffix
      )

  return "\n".join(
    parts
  )
```

Phase boundary:
- Production ordering repair は既存状態を維持
- proof graph 変更なし
- semantic model 変更なし
- Argument ordering 変更なし
- repository-wide pytest なし
