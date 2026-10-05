# Phase 158-R5-5b repair1d changed code

## 変更対象

`toda_group_proof_narrative_argument_multi_renderer.py`

変更関数:
`render_toda_group_proof_narrative_multi_argument_markdown()`

import の変更はありません。

変更対象の merge 部分:

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

    if (
      argument.conclusion_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .TARGET
    ):
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
    else:
      local_body_blocks = tuple(
        block
        for block in blocks
        if (
          id(
            block
          ) in local_body_block_ids
          or id(
            block
          ) in evidence_block_ids
        )
      )
```

Phase boundary:
- root TARGET ordering のみ修正
- equation numbering algorithm は変更しない
- proof graph は変更しない
- semantic dependency は変更しない
- Argument ordering は変更しない
- group n/k special case は追加しない
- repository-wide pytest は実行しない
