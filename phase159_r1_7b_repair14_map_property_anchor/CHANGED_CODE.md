# Phase 159-R1-7b repair14

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_normalize_public_exact_sequences`

### Test
- 新規:
  - `tests/test_phase159_r1_7b_repair14_map_property_anchor.py`

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

  line_index = 0

  while line_index < len(
    lines
  ):
    signature = (
      _phase159_r1_7b_map_property_signature(
        lines[
          line_index
        ]
      )
    )

    if signature is None:
      line_index += 1
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
      line_index += 1
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
      ] < line_index
    ):
      line_index += 1
      continue

    if existing_span is not None:
      span_start, span_end = existing_span

      del lines[
        span_start:span_end
      ]

      if span_start < line_index:
        line_index -= (
          span_end
          - span_start
        )

    display_lines = list(
      _phase159_r1_7b_display_math_lines(
        matching_latex
      )
    )

    lines[
      line_index:line_index
    ] = display_lines

    line_index += (
      len(
        display_lines
      )
      + 1
    )

  return lines
```

## 新規テスト全文

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render_pi11_4() -> str:
  report = build_standard_toda_report(
    n=4,
    k=7,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7b_repair14_exactness_precedes_visible_delta_property():
  rendered = _render_pi11_4()

  exactness = (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
  )
  surjectivity = (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$"
    " は全射."
  )

  assert exactness in rendered
  assert surjectivity in rendered
  assert rendered.index(
    exactness
  ) < rendered.index(
    surjectivity
  )


def test_phase159_r1_7b_repair14_matching_exactness_is_not_duplicated():
  rendered = _render_pi11_4()

  exactness = (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
  )

  assert rendered.count(
    exactness
  ) == 1
```

## 修正理由

repair13 runtime diagnosis で pi11_4 baseline body は次の順序だった。

1. `$Delta: pi_10^5 -> pi_8^2$ は全射である.`
2. `[R1] より, pi_9^2 = 0.`
3. E-H exactness
4. `$Delta: pi_10^5 -> pi_8^2$ は単射である.`

`完全性より,` connector は存在しない。

一方:
- H-Delta exactness candidate は semantic closure に存在する。
- Delta 全射 line の map-property signature は取得できる。
- その signature と H-Delta exactness candidate の matching は成功する。

したがって connector 文字列を anchor とする設計を廃止し、
visible map-property line を anchor とする。

map-property signature と一致する typed exactness candidate があり、
その exactness がまだ前に表示されていなければ、
map-property の直前へ display math として挿入する。

後続の同じ map-property signature では、
既に exactness display が前にあるため重複挿入しない。

group / proposition 固有分岐は追加しない。

## 実行する pytest

- `tests/test_phase159_r1_7b_repair14_map_property_anchor.py`
- `tests/test_phase159_r1_7b_repair11_inline_connector.py`
- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase148_rc2_3_exactness_exposure.py`
- `tests/test_phase148_rc2_3_repair_r1.py`

full pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi11_4 H-Delta exactness が Delta 全射より前に display math。
- 同じ H-Delta exactness を重複表示しない。
- E-H exactness display を維持。
- pi6_3 short exact display を維持。
- focused tests PASS。

## 次 Phase との境界

R1-7b は exact-sequence display/order のみ。
連続等式統合、equation numbering、
Reference aggregate suppression、map-property prose 全体統一は対象外。
