# 変更対象

## Production

`toda_group_proof_narrative_contribution_renderer.py`

### import

変更なし。

### 新規関数

追加位置:
既存
`suppress_toda_group_proof_narrative_reflexive_equalities()`
の直前。

```python
def suppress_toda_group_proof_narrative_literal_reflexive_equalities(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  retained = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    comparable = paragraph.strip()

    if comparable.startswith(
      "[R"
    ):
      marker_end = comparable.find(
        "]"
      )

      if marker_end >= 0:
        suffix = comparable[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            comparable = suffix[
              len(
                prefix
              ):
            ]
            break

    comparable = comparable.rstrip(
      "."
    ).strip()

    if (
      comparable.startswith(
        "$"
      )
      and comparable.endswith(
        "$"
      )
    ):
      equation = comparable[
        1:-1
      ]

      if equation.count(
        "="
      ) == 1:
        lhs, rhs = equation.split(
          "=",
          1,
        )

        if (
          lhs.strip()
          == rhs.strip()
        ):
          continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )
```

### 変更関数

`render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()`

ローカル repair8 後の関数全体を維持したまま、apply script が:

1. fix2 の2つの追加 call を削除
2. final literal reflexive suppression を追加
3. final body marker が0件なら orphan Reference を空にする

という最小変更だけを行う。

## Tests

追加:
`test_phase159_r1_7c_r4_repair9_fix3.py`

既存:
- `tests/test_phase157_r20_repair30_final_reflexive_suppression.py`
- `tests/test_phase158_r5_5b_public_generic_order_route.py`
- `tests/test_phase157_r20_repair12_map_property_reference_support.py`

repository-wide pytest は実行しない。
