# Phase 159-R1-7b repair12

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_normalize_public_exact_sequences`

### Tests
変更なし。
既存の R1-7b integration test が regression test として残る。

## import

production import の変更はありません。

## 変更後関数全文

```python
def _phase159_r1_7b_normalize_public_exact_sequences(
  presentation: TodaGroupProofPresentation,
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  exactness_latex = tuple(
    latex
    for latex in (
      _phase159_r1_7b_exactness_step_latex(
        node.proof_step
      )
      for node in semantic_presentation.nodes
    )
    if latex is not None
  )

  lines = []

  for line in proof_body:
    inline_exactness = (
      _phase159_r1_7b_inline_exactness_latex(
        line
      )
    )

    if inline_exactness is not None:
      lines.extend(
        _phase159_r1_7b_display_math_lines(
          inline_exactness
        )
      )
      continue

    inline_short_exact = (
      _phase159_r1_7b_inline_short_exact_latex(
        line
      )
    )

    if inline_short_exact is not None:
      lines.extend(
        _phase159_r1_7b_display_math_lines(
          inline_short_exact
        )
      )
      continue

    lines.append(
      line
    )

  connector_prefix = "完全性より,"
  connector_index = 0

  while connector_index < len(
    lines
  ):
    connector_line = lines[
      connector_index
    ].strip()

    if not connector_line.startswith(
      connector_prefix
    ):
      connector_index += 1
      continue

    inline_property_line = connector_line[
      len(
        connector_prefix
      ):
    ].strip()

    if inline_property_line:
      property_index = connector_index
      property_line = inline_property_line
    else:
      property_index = (
        _phase159_r1_7b_next_nonblank_index(
          lines,
          connector_index + 1,
        )
      )

      if property_index is None:
        break

      property_line = lines[
        property_index
      ]

    signature = (
      _phase159_r1_7b_map_property_signature(
        property_line
      )
    )

    if signature is None:
      connector_index += 1
      continue

    matching_latex = next(
      (
        latex
        for latex in exactness_latex
        if (
          _phase159_r1_7b_exactness_matches_map_property(
            latex,
            signature,
          )
        )
      ),
      None,
    )

    if matching_latex is None:
      connector_index += 1
      continue

    existing_span = (
      _phase159_r1_7b_find_display_math_span(
        lines,
        matching_latex,
      )
    )

    if (
      existing_span is not None
      and existing_span[
        0
      ] < connector_index
    ):
      connector_index += 1
      continue

    if existing_span is not None:
      span_start, span_end = existing_span

      del lines[
        span_start:span_end
      ]

      if span_start < connector_index:
        connector_index -= (
          span_end
          - span_start
        )

    display_lines = list(
      _phase159_r1_7b_display_math_lines(
        matching_latex
      )
    )

    lines[
      connector_index:connector_index
    ] = display_lines

    connector_index += (
      len(
        display_lines
      )
      + 1
    )

  return lines
```

## 修正理由

repair10 までで:
- canonical H-Delta exactness candidate: PASS
- canonical E-H exactness candidate: PASS
- `$...$.` exactness parser: PASS
- E-H display: PASS

repair11 後も H-Delta 挿入だけが失敗した。

repair11 は同一行 connector を

`完全性より, `

のようにカンマ後の半角スペースまで固定して認識していた。

しかし renderer contract はその空白を保証しない。

repair12 では行が `完全性より,` で始まるかだけを確認し、
その後ろの残りを `strip()` する。

残りがあれば同一行 map-property として使い、
空なら従来通り次の nonblank line を map-property として使う。

group / proposition 固有分岐は追加しない。

## 実行する pytest

- `tests/test_phase159_r1_7b_repair11_inline_connector.py`
- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase148_rc2_3_exactness_exposure.py`
- `tests/test_phase148_rc2_3_repair_r1.py`

full pytest は Phase 159 最後まで実行しない。

## 完了条件

- focused tests PASS
- pi11_4 H-Delta exactness display
- pi11_4 H-Delta exactness が Delta 全射より前
- pi11_4 E-H exactness display 維持
- pi6_3 short exact display 維持

## 次 Phase との境界

R1-7b は exact-sequence display/order のみ。
連続等式統合、equation numbering、
Reference aggregate suppression、map-property prose 全体統一は対象外。
