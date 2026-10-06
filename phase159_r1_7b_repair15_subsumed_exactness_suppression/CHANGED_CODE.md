# Phase 159-R1-7b repair15

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_normalize_public_exact_sequences`

### Test
- 新規:
  - `tests/test_phase159_r1_7b_repair15_subsumed_exactness.py`

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

  def canonical_exactness(
    latex: str,
  ) -> str:
    return (
      latex
      .replace(
        r"\xrightarrow{Δ}",
        r"\xrightarrow{\Delta}",
      )
      .strip()
      .removesuffix(
        "."
      )
      .strip()
    )

  canonical_exactness_latex = tuple(
    canonical_exactness(
      latex
    )
    for latex in exactness_latex
  )

  def canonical_typed_exactness(
    latex: str,
  ) -> str:
    canonical = canonical_exactness(
      latex
    )

    for (
      typed_latex,
      typed_canonical,
    ) in zip(
      exactness_latex,
      canonical_exactness_latex,
    ):
      if canonical == typed_canonical:
        return typed_latex

    return canonical

  def prior_display_covers(
    lines: list[
      str
    ],
    latex: str,
    before_index: int,
  ) -> bool:
    target = canonical_exactness(
      latex
    )
    index = 0

    while index < min(
      before_index,
      len(
        lines
      ),
    ):
      if (
        lines[
          index
        ].strip()
        == r"\["
        and index + 2
        < len(
          lines
        )
        and lines[
          index + 2
        ].strip()
        == r"\]"
      ):
        displayed = (
          canonical_exactness(
            lines[
              index + 1
            ]
          )
        )

        if target in displayed:
          return True

        index += 3
        continue

      index += 1

    return False

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
          canonical_typed_exactness(
            inline_exactness
          )
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

    if prior_display_covers(
      lines,
      matching_latex,
      line_index,
    ):
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

  result = []
  displayed_exactness = []
  line_index = 0

  while line_index < len(
    lines
  ):
    if (
      lines[
        line_index
      ].strip()
      == r"\["
      and line_index + 2
      < len(
        lines
      )
      and lines[
        line_index + 2
      ].strip()
      == r"\]"
    ):
      content = canonical_exactness(
        lines[
          line_index + 1
        ]
      )

      is_typed_exactness = (
        content
        in canonical_exactness_latex
      )

      if (
        is_typed_exactness
        and any(
          content in earlier
          for earlier in displayed_exactness
        )
      ):
        line_index += 3
        continue

      displayed_exactness.append(
        content
      )

      result.extend(
        lines[
          line_index:line_index + 3
        ]
      )
      line_index += 3
      continue

    result.append(
      lines[
        line_index
      ]
    )
    line_index += 1

  return result
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


def _render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def test_phase159_r1_7b_repair15_pi6_3_subsumed_windows_are_not_repeated():
  rendered = _render(
    3,
    3,
  )

  h_delta = (
    "\\[\n"
    r"\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} "
    r"\xrightarrow{\Delta} \pi_{5}^{2}."
    "\n\\]"
  )
  delta_e = (
    "\\[\n"
    r"\pi_{7}^{5} \xrightarrow{\Delta} \pi_{5}^{2} "
    r"\xrightarrow{E} \pi_{6}^{3}."
    "\n\\]"
  )

  assert h_delta not in rendered
  assert delta_e not in rendered

  assert (
    "\\[\n"
    r"\pi_{7}^{3} \xrightarrow{H} \pi_{7}^{5} "
    r"\xrightarrow{\Delta} \pi_{5}^{2} "
    r"\xrightarrow{E} \pi_{6}^{3}."
    "\n\\]"
    in rendered
  )


def test_phase159_r1_7b_repair15_pi6_3_exactness_uses_canonical_delta():
  rendered = _render(
    3,
    3,
  )

  assert r"\xrightarrow{Δ}" not in rendered


def test_phase159_r1_7b_repair15_pi11_4_keeps_distinct_exactness_windows():
  rendered = _render(
    4,
    7,
  )

  h_delta = (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
  )
  e_h = (
    "\\[\n"
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}."
    "\n\\]"
  )

  assert rendered.count(
    h_delta
  ) == 1
  assert rendered.count(
    e_h
  ) == 1
```

## 修正理由

repair14 focused tests は 18/18 PASS したが、
visual verification で pi6_3 に次の残件が確認された。

- 最初の4項完全列に含まれる H-Delta 3項窓が後で再表示される。
- 同じく Delta-E 3項窓が後で再表示される。
- inline exactness 由来の再表示だけ Unicode `Δ` が残る。

repair15 では、
1. inline exactness を semantic-closure の typed candidate に照合し、
   canonical LaTeX に揃える。
2. ある typed exactness window が既に前方のより長い display-math
   exact sequence に連続部分列として含まれている場合は再表示しない。
3. pi11_4 の H-Delta と E-H のように互いに包含関係のない
   distinct windows は維持する。

group / proposition 固有分岐は追加しない。

## 実行する pytest

- `tests/test_phase159_r1_7b_repair15_subsumed_exactness.py`
- `tests/test_phase159_r1_7b_repair14_map_property_anchor.py`
- `tests/test_phase159_r1_7b_repair11_inline_connector.py`
- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py`
- `tests/test_phase148_rc2_3_exactness_exposure.py`
- `tests/test_phase148_rc2_3_repair_r1.py`

full pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi6_3 の4項完全列は維持。
- その部分窓 H-Delta / Delta-E は重複表示しない。
- exactness 表示に Unicode `Δ` を残さない。
- pi11_4 H-Delta / E-H は各1回維持。
- focused tests PASS。

## 次 Phase との境界

repair15 で R1-7b exact-sequence display/order を閉じる。
次は R1-7c の連続等式・不要 equation numbering 整理へ進む。
Reference aggregate suppression と map-property prose 全体統一は別 scope。
