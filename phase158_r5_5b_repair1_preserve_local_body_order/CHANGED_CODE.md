# Phase 158-R5-5b repair1 changed code

## 変更対象

### Production

`toda_group_proof_narrative_argument_multi_renderer.py`

変更関数:
`render_toda_group_proof_narrative_multi_argument_markdown()`

import の変更はありません。

変更箇所は関数内部の local-body / method-evidence merge です。

変更後の置換単位:

```python
    local_body_block_ids = {
      id(
        block
      )
      for block in local_body_blocks
    }
    evidence_block_ids = {
      id(
        block
      )
      for block in evidence
    }
    missing_evidence_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in evidence_block_ids
        and id(
          block
        ) not in local_body_block_ids
      )
    )

    if missing_evidence_blocks:
      conclusion_position = next(
        (
          index
          for index, block in enumerate(
            local_body_blocks
          )
          if block is argument.conclusion_block
        ),
        len(
          local_body_blocks
        ),
      )
      local_body_blocks = (
        local_body_blocks[
          :conclusion_position
        ]
        + missing_evidence_blocks
        + local_body_blocks[
          conclusion_position:
        ]
      )
```

### Test

`tests/test_phase158_r5_5b_public_generic_order_route.py`

変更関数:
`_web_text()`

変更後全文:

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

- route cutover は前段 R5-5b の変更を維持
- proof graph 変更なし
- semantic dependency 変更なし
- Argument ordering 変更なし
- pi_8^5 dedicated route 変更なし
- repository-wide pytest なし
