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

ローカル関数全体は維持し、次だけ変更する。

1. fix2 の final graph suppression を削除
2. fix2 の post-selection relink を削除
3. `generic_used_step_ids` の直前に literal reflexive suppression を追加
4. 最終 `reference_section` 作成直前に orphan Reference suppression を追加

追加コード:

```python
  if "[R" not in rendered:
    reference_entries = ()
    statement_lines_by_reference_number = {}
```

## テスト

追加:
`test_phase159_r1_7c_r4_repair9_fix4.py`

既存 focused:
- `tests/test_phase157_r20_repair30_final_reflexive_suppression.py`
- `tests/test_phase158_r5_5b_public_generic_order_route.py`
- `tests/test_phase157_r20_repair12_map_property_reference_support.py`

全体 pytest は実行しない。
