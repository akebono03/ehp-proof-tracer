# Phase 159-R1-7b repair6

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_normalize_public_exact_sequences`

### Tests
新規変更なし。既存 focused tests を実行する。

## import

production import の変更はありません。

## 変更後の関数全文

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

  ancestry_steps = []
  seen_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in seen_step_ids:
      return

    seen_step_ids.add(
      proof_step_id
    )

    for premise_step in proof_step.premises:
      visit(
        premise_step
      )

    ancestry_steps.append(
      proof_step
    )

  visit(
    presentation.root_step
  )

  exactness_latex = tuple(
    latex
    for latex in (
      _phase159_r1_7b_exactness_step_latex(
        proof_step
      )
      for proof_step in ancestry_steps
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

repair5 で R1-7b normalizer 自体は実行されるようになり、
pi6_3 の short exact sequence は PASS した。

一方 pi11_4 では、
- visible relocated exactness が inline のまま
- H-Delta exactness が public body から欠落

していた。

現行 R1-7b normalizer は `presentation.nodes` のみから
`TodaProp42ExactnessStatement` を集めていたが、
pi11_4 が再利用する pi10_3 証明の H-Delta exactness は
recursive proof ancestry に存在する。

repair6 は `presentation.root_step` から premises を再帰走査し、
exactness source を集める。

group 名・Proposition 名・pi11_4 固有分岐は追加しない。

## 実行する pytest

- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase148_rc2_3_exactness_exposure.py`
- `tests/test_phase148_rc2_3_repair_r1.py`

full pytest は実行しない。

## 完了条件

- pi6_3 short exact sequence が display math。
- pi11_4 H-Delta exactness が Delta 全射の前。
- pi11_4 E-H exactness が display math。
- existing exactness exposure tests を壊さない。
- focused tests PASS。

## 次 Phase との境界

R1-7b repair6 では exact-sequence display/order のみ。

未着手:
- pi6_3 の連続等式統合
- equation numbering policy
- Reference aggregate suppression
- map-property prose 全体統一
