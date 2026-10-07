# Phase 159 R1-7c R3 repair4 repair3

## 変更対象

- `tests/test_phase157_r5_r6_53_bracket_definition_reference.py`
- production code の変更なし。
- import の変更なし。

## 変更 test function 全文

```python
def test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _pi6_3_presentation()
    )
  )
  reference_part = (
    rendered.split(
      "---\n\n## 証明",
      1,
    )[
      0
    ]
  )

  assert (
    re.search(
      r"\*\*\[R\d+\] \(5\.3\)\.\*\*",
      reference_part,
    )
    is not None
  )
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )
```

## Phase boundary

- repair4 component pruning production logic は変更しない。
- pi_6^3 special case は追加しない。
- locator `(5.3)` は維持する。
- stale `[R1]` 固定だけを除去する。
