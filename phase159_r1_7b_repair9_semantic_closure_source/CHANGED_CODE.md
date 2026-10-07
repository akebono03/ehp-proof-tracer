# Phase 159-R1-7b repair9

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_normalize_public_exact_sequences`

### Tests
新規変更なし。

## import

production import の変更はありません。
`build_toda_group_proof_narrative_semantic_closure_presentation` は既に import 済みです。

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

  connector_index = 0

  while connector_index < len(
    lines
  ):
    if lines[
      connector_index
    ].strip() != "完全性より,":
      connector_index += 1
      continue

    property_index = (
      _phase159_r1_7b_next_nonblank_index(
        lines,
        connector_index + 1,
      )
    )

    if property_index is None:
      break

    signature = (
      _phase159_r1_7b_map_property_signature(
        lines[
          property_index
        ]
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

repair8 の smoke check は original `root_step` ancestry を探索していたが、
public Narrative baseline は semantic-closure presentation を用いて本文を生成する。

R1-7b normalizer も同じ semantic-closure presentation の selected nodes を
typed exactness source として使うべきである。

full ancestry を無制限に使わず、Narrative が意味的依存関係として選択した
nodes に限定するため、既存 exactness exposure contract とも整合する。

## 実行する pytest

- tests/test_phase159_r1_7b_exact_sequence_display_order.py
- tests/test_phase157_r20_repair37_short_exact_after_map_support.py
- tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py
- tests/test_phase148_rc2_3_exactness_exposure.py
- tests/test_phase148_rc2_3_repair_r1.py

full pytest は Phase 159 最後まで実行しない。

## 完了条件

- semantic closure に H-Delta exactness が存在する smoke check PASS
- `$...$.` parser smoke check PASS
- focused tests PASS
- pi6_3 short exact sequence の中央表示維持
- pi11_4 E-H exactness の中央表示
- pi11_4 H-Delta exactness が Delta 全射の前に中央表示

## 次 Phase との境界

R1-7b は exact-sequence display/order のみ。
連続等式統合、equation numbering、Reference aggregate suppression、
map-property prose 全体統一は次の repair/step。
