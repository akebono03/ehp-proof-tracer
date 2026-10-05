# Phase 158-R5-5b repair1a changed code

## 変更対象

### Production

`toda_group_proof_narrative_argument_multi_renderer.py`

変更関数:
`render_toda_group_proof_narrative_multi_argument_markdown()`

repair1 が既に途中まで適用されている場合は Production を変更しない。
未適用の場合だけ local-body / method-evidence merge を修正する。

import の変更はありません。

### Test

`tests/test_phase158_r5_5b_public_generic_order_route.py`

変更関数全文:

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

## Phase boundary

- proof graph 変更なし
- semantic dependency 変更なし
- Argument ordering 変更なし
- pi_8^5 dedicated route 変更なし
- repository-wide pytest なし
