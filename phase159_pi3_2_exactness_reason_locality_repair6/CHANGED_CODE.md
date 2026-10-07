# Phase 159 pi3_2 exactness reason locality repair6

## 変更対象

1. `toda_group_proof_narrative_reason_renderer.py`
   - `_normalize_exactness_to_map_property_reason_prose()` 全体を変更

2. `tests/test_phase159_pi3_2_exactness_reason_locality.py`
   - 新規追加

## import

import の変更はありません。

## 変更する関数全文

```python
def _normalize_exactness_to_map_property_reason_prose(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
) -> str:
  if (
    reason.kind
    is not TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    return markdown

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  if sentence is None:
    return markdown

  lines = sentence.splitlines()

  while (
    lines
    and lines[-1].strip()
    in {
      "以上より,",
      "したがって,",
      "これより,",
      "これらより,",
    }
  ):
    lines.pop()

  reason_body = "\n".join(
    lines
  ).strip()

  if not reason_body:
    return markdown

  paragraphs = markdown.split(
    "\n\n"
  )
  prefixed_reason_body = (
    "これより, "
    + reason_body
  )
  matching_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if paragraph.strip()
    in {
      reason_body,
      prefixed_reason_body,
    }
  )

  if len(matching_indices) != 1:
    return markdown

  reason_index = matching_indices[0]
  reason_paragraph = paragraphs[
    reason_index
  ].strip()

  if reason_paragraph == prefixed_reason_body:
    paragraphs[
      reason_index
    ] = reason_body

  if (
    reason_index > 0
    and paragraphs[
      reason_index - 1
    ].strip()
    == "これより,"
  ):
    paragraphs.pop(
      reason_index - 1
    )
    reason_index -= 1

  def statement_match_key(
    line: str,
  ) -> str:
    normalized = line.strip().rstrip(
      ".,"
    )
    marker = r"\tag{"

    while True:
      marker_index = normalized.find(
        marker
      )

      if marker_index < 0:
        break

      number_start = (
        marker_index
        + len(
          marker
        )
      )
      number_end = normalized.find(
        "}",
        number_start,
      )

      if number_end < 0:
        break

      number_text = normalized[
        number_start:
        number_end
      ]

      if not number_text.isdigit():
        break

      normalized = (
        normalized[
          :marker_index
        ]
        + normalized[
          number_end + 1:
        ]
      )

    return normalized

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            stripped = suffix[
              len(
                prefix
              ):
            ]
            break

    for prefix in (
      "完全性より, ",
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
    ):
      if stripped.startswith(
        prefix
      ):
        stripped = stripped[
          len(
            prefix
          ):
        ]
        break

    return statement_match_key(
      stripped
    )

  visible_premise_indices = []

  for premise_step in reason.premise_steps:
    premise_line = (
      _render_generic_narrative_step(
        premise_step
      )
    )

    if not premise_line:
      continue

    premise_key = statement_match_key(
      premise_line
    )
    premise_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if (
        index != reason_index
        and paragraph_match_key(
          paragraph
        )
        == premise_key
      )
    )

    if len(
      premise_matches
    ) != 1:
      continue

    visible_premise_indices.append(
      premise_matches[
        0
      ]
    )

  if not visible_premise_indices:
    return "\n\n".join(
      paragraphs
    )

  latest_premise_index = max(
    visible_premise_indices
  )

  if (
    reason_index
    == latest_premise_index + 1
  ):
    return "\n\n".join(
      paragraphs
    )

  if reason_index <= latest_premise_index:
    return "\n\n".join(
      paragraphs
    )

  paragraph = paragraphs.pop(
    reason_index
  )

  paragraphs.insert(
    latest_premise_index + 1,
    paragraph,
  )

  return "\n\n".join(
    paragraphs
  )
```

## 一般規則

`EXACTNESS_TO_MAP_PROPERTY` reason について、

1. 既存 `premise_steps` を使う。
2. Narrative に一意に見えている premise paragraph を取得する。
3. 最後に見えている premise の直後へ `完全性より, ...` paragraph を移す。
4. premise が見つからない、または一意でない場合は無理に移動しない。
5. reason paragraph が premise より前にある場合も移動しない。
6. proof graph に新しい edge を追加しない。

pi_3^2 ではこれにより:

- `[R1]より, pi_2^1=0.` の直後に `完全性より, H は単射.`
- `完全性より, Delta は零写像.` の直後に `完全性より, H は全射.`

となる。

## 新規テスト全文

`payload/tests/test_phase159_pi3_2_exactness_reason_locality.py` をそのまま
`tests/` にコピーする。

確認内容:

- zero group -> H injective が隣接
- Delta zero -> H surjective が隣接
- E isomorphism -> E injective -> Delta zero -> H surjective
- H injective / H surjective -> H isomorphism
- H isomorphism -> eta_2 definition -> final result

## 実行する pytest

```powershell
python -m pytest `
  ".\tests\test_phase159_pi3_2_exactness_reason_locality.py" `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q
```

全体テストは実行しない。

## 完了条件

- locality audit が2項目とも PASS
- focused pytest が全 PASS
- `[R1]より, pi_2^1=0.` の直後に `完全性より, H は単射.`
- `Delta=0` の直後に `完全性より, H は全射.`
- `H 同型 -> eta_2 定義 -> 最終結果` を維持
- `□` が最後

## 次 Phase との境界

今回扱うのは reason-to-conclusion locality のみ。

- visible-step global reorder は変更しない
- Argument ordering は変更しない
- proof graph は変更しない
- statement type 固定順位は追加しない
- full suite は Phase 159 終了時まで実行しない
