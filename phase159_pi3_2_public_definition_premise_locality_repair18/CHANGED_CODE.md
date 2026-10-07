# Phase 159 pi3_2 public definition-premise locality repair18

## 変更対象

1. `toda_group_proof_narrative_renderer.py`
   - 新規関数 `_phase159_order_public_unique_preimage_definition_premises()`
   - `render_toda_group_proof_narrative_markdown()` 全体

2. `tests/test_phase159_pi3_2_public_definition_premise_locality.py`
   - 新規追加

## import

import の変更はありません。

## 原因

`_phase158_normalize_public_narrative_contract()` 内で、

`_phase159_project_generic_semantics_to_public_proof()`

が contribution renderer の後に実行される。

したがって contribution renderer 内では definition paragraph はまだ

`$H(eta_2)=iota_3$ を満たす ... を定める.`

という generic prose であり、

`この同型写像により, ... が一意に存在する.`

という public prose ではない。

audit17 では active reason function 内に definition locality が存在し、
最終 return より前に置かれていることも確認済み。

## 新規関数の追加位置

`_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions()`
の後、

`render_toda_group_proof_narrative_markdown()`
の直前。

## 新規関数全文

```python
def _phase159_order_public_unique_preimage_definition_premises(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]
  had_trailing_newline = rendered.endswith(
    "\n"
  )
  paragraphs = proof_body.rstrip(
    "\n"
  ).split(
    "\n\n"
  )

  def match_key(
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

        for reference_prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            reference_prefix
          ):
            stripped = suffix[
              len(
                reference_prefix
              ):
            ]
            break

    for prose_prefix in (
      "完全性より, ",
      "以上より, ",
      "したがって, ",
      "これより, ",
      "これらより, ",
    ):
      if stripped.startswith(
        prose_prefix
      ):
        stripped = stripped[
          len(
            prose_prefix
          ):
        ]
        break

    for verbose, concise in (
      (
        " は単射である.",
        " は単射.",
      ),
      (
        " は全射である.",
        " は全射.",
      ),
      (
        " は零写像である.",
        " は零写像.",
      ),
      (
        " は同型写像である.",
        " は同型.",
      ),
    ):
      if stripped.endswith(
        verbose
      ):
        stripped = (
          stripped[
            :-len(
              verbose
            )
          ]
          + concise
        )
        break

    return stripped.rstrip(
      ".,"
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    line = _render_generic_narrative_step(
      proof_step
    )

    if not line:
      return None

    target_key = match_key(
      line
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  for node in presentation.nodes:
    proof_step = node.proof_step
    definition_line = (
      _phase159_unique_preimage_definition_line(
        proof_step
      )
    )

    if definition_line is None:
      continue

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == definition_line
    )

    if len(
      definition_matches
    ) != 1:
      continue

    visible_premise_records = tuple(
      (
        premise_step,
        paragraph_index_for_step(
          premise_step
        ),
      )
      for premise_step in proof_step.premises
    )

    if any(
      premise_index is None
      for (
        _,
        premise_index,
      ) in visible_premise_records
    ):
      continue

    premise_indices = tuple(
      premise_index
      for (
        _,
        premise_index,
      ) in visible_premise_records
      if premise_index is not None
    )

    if len(
      premise_indices
    ) != len(
      proof_step.premises
    ):
      continue

    definition_index = definition_matches[
      0
    ]
    expected_indices = tuple(
      range(
        definition_index
        - len(
          premise_indices
        ),
        definition_index,
      )
    )

    if premise_indices == expected_indices:
      continue

    premise_paragraphs = tuple(
      paragraphs[
        premise_index
      ]
      for premise_index in premise_indices
    )

    for premise_index in sorted(
      premise_indices,
      reverse=True,
    ):
      paragraphs.pop(
        premise_index
      )

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == definition_line
    )

    if len(
      definition_matches
    ) != 1:
      continue

    definition_index = definition_matches[
      0
    ]
    paragraphs[
      definition_index:
      definition_index
    ] = premise_paragraphs

  result = (
    prefix
    + "\n\n".join(
      paragraphs
    )
  )

  if had_trailing_newline:
    result += "\n"

  return result

```

## 変更関数全文

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

  return (
    _phase159_order_public_unique_preimage_definition_premises(
      presentation,
      rendered,
    )
  )

```

## テスト

`tests/test_phase159_pi3_2_public_definition_premise_locality.py`

を新規追加。

確認内容:

- `pi_2^1=0 -> H injective`
- `Delta=0 -> H surjective`
- `E isomorphism -> E injective -> Delta=0 -> H surjective`
- `H injective`, `H surjective` の後に `H isomorphism`
- `H isomorphism -> pi_3^3=Z{iota_3} -> eta_2 definition`
- eta2 definition -> final group
- QED が最後

## 完了条件

audit が全 PASS。
focused pytest が全 PASS。
public narrative が最終的に

`H isomorphism -> pi_3^3=Z{iota_3} -> eta_2 definition`

となること。

## 次 Phase との境界

- contribution renderer は変更しない
- reason renderer は変更しない
- proof graph は変更しない
- semantic sidecar は変更しない
- fixed literature statement は変更しない
- full suite は Phase 159 最後にのみ実行する
