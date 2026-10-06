# Phase 159-R1-7b repair11

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7b_normalize_public_exact_sequences`

### Test
- 新規:
  - `tests/test_phase159_r1_7b_repair11_inline_connector.py`

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

    if connector_line == connector_prefix:
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
    elif connector_line.startswith(
      connector_prefix + " "
    ):
      property_index = connector_index
      property_line = connector_line[
        len(
          connector_prefix
        ):
      ].strip()
    else:
      connector_index += 1
      continue

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

## 新規テスト全文

```python
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7b_map_property_signature,
)


def test_phase159_r1_7b_repair11_inline_connector_property_signature():
  line = (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$"
    " は全射."
  )

  assert (
    _phase159_r1_7b_map_property_signature(
      line
    )
    == (
      r"\Delta",
      r"\pi_{10}^{5}",
      r"\pi_{8}^{2}",
    )
  )
```

## 修正理由

repair10 で以下は確認済み。

- canonical H-Delta exactness candidate 取得: PASS
- canonical E-H exactness candidate 取得: PASS
- `$...$.` exactness parser: PASS
- E-H exactness display: PASS
- H-Delta exactness display: FAIL のみ

残る差は connector の形である。

旧 normalizer は

```text
完全性より,

$Delta: ...$ は全射.
```

だけを扱った。

public Narrative には

```text
完全性より, $Delta: ...$ は全射.
```

という同一行形式も存在する。

repair11 は両方を同じ generic rule で扱い、
map-property 本文そのものは変更せず、
対応 exactness display を connector の直前に挿入する。

## pytest

focused tests のみ実行する。
full pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi11_4 H-Delta exactness が display math。
- H-Delta exactness が Delta 全射より前。
- E-H exactness display を維持。
- pi6_3 short exact display を維持。
- focused tests PASS。

## 次 Phase との境界

R1-7b は exact-sequence display/order のみ。
連続等式統合、equation numbering、Reference aggregate suppression、
map-property prose 全体統一は対象外。
