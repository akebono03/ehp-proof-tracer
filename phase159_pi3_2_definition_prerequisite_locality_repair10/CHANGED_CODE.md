# Phase 159 pi3_2 definition prerequisite locality repair10

## 変更対象

- `toda_group_proof_narrative_reason_renderer.py`
  - `order_toda_group_proof_narrative_injective_image_order_reason()` 全体
- `tests/test_phase159_pi3_2_exactness_reason_locality.py`
  - 全文更新

## import

import の変更はありません。

## 修正方針

`pi_3^3 = Z{iota_3}` は H の単射・全射の理由ではなく、
H が同型であることを得た後に eta_2 を一意に定義するための前提。

既存 `DEFINITION_APPLICABILITY` reason の

- `premise_steps`
- `conclusion_step`

を使用して、唯一の prerequisite paragraph を
definition paragraph の直前へ移動する。

## 期待する pi_3^2 本文順

1. `pi_2^1 = 0`
2. `完全性より H は単射`
3. `E は同型`
4. `E は単射`
5. `完全性より Delta は零写像`
6. `完全性より H は全射`
7. `H は同型`
8. `pi_3^3 = Z{iota_3}`
9. `この同型写像により eta_2 が一意に存在`
10. final group result

## 変更関数全文

```python
def order_toda_group_proof_narrative_injective_image_order_reason(
  markdown: str,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reason_sidecar,
    TodaGroupProofNarrativeReasonSidecar,
  ):
    raise TypeError(
      "reason_sidecar must be a "
      "TodaGroupProofNarrativeReasonSidecar"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def statement_match_key(
    line: str,
  ) -> str:
    if not isinstance(
      line,
      str,
    ):
      raise TypeError(
        "line must be a str"
      )

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

    return statement_match_key(
      stripped
    )

  def paragraph_index_for_step(
    proof_step,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = statement_match_key(
      rendered
    )

    matching = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matching
    ) != 1:
      return None

    return matching[
      0
    ]

  def visible_reason_paragraph(
    reason: TodaGroupProofNarrativeReason,
  ) -> str | None:
    sentence = (
      render_toda_group_proof_narrative_reason_sentence(
        reason
      )
    )

    if sentence is None:
      return None

    lines = sentence.splitlines()

    while (
      lines
      and lines[
        -1
      ].strip()
      in {
        "以上より,",
        "したがって,",
        "これより,",
        "これらより,",
      }
    ):
      lines.pop()

    rendered = "\n".join(
      lines
    ).strip()

    return (
      rendered
      if rendered
      else None
    )

  for reason in reason_sidecar.reasons:
    if (
      reason.kind
      is not TodaGroupProofNarrativeReasonKind
      .INJECTIVE_IMAGE_ORDER
    ):
      continue

    reason_paragraph = (
      visible_reason_paragraph(
        reason
      )
    )

    if reason_paragraph is None:
      continue

    reason_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == reason_paragraph
    )

    if len(
      reason_indices
    ) != 1:
      continue

    conclusion_index = (
      paragraph_index_for_step(
        reason.conclusion_step
      )
    )

    if conclusion_index is None:
      continue

    premise_indices = tuple(
      index
      for premise in reason.premise_steps
      for index in (
        paragraph_index_for_step(
          premise
        ),
      )
      if index is not None
    )

    if len(
      premise_indices
    ) != len(
      reason.premise_steps
    ):
      continue

    if max(
      premise_indices
    ) >= conclusion_index:
      continue

    reason_index = reason_indices[
      0
    ]

    if (
      reason_index
      == conclusion_index - 1
      and reason_index
      > max(
        premise_indices
      )
    ):
      continue

    paragraph = paragraphs.pop(
      reason_index
    )

    conclusion_index = (
      paragraph_index_for_step(
        reason.conclusion_step
      )
    )

    if conclusion_index is None:
      paragraphs.insert(
        reason_index,
        paragraph,
      )
      continue

    paragraphs.insert(
      conclusion_index,
      paragraph,
    )

  def map_identity(
    proof_step,
  ):
    statement = getattr(
      proof_step,
      "conclusion",
      None,
    )

    return getattr(
      statement,
      "map",
      None,
    )

  def visible_reason_index(
    reason: TodaGroupProofNarrativeReason,
  ) -> int | None:
    reason_paragraph = (
      visible_reason_paragraph(
        reason
      )
    )

    if reason_paragraph is None:
      return None

    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == reason_paragraph
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  connector_paragraphs = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }

  for node in reason_sidecar.presentation.nodes:
    isomorphism_step = node.proof_step
    isomorphism_line = (
      _render_generic_narrative_step(
        isomorphism_step
      )
    )

    if (
      not isomorphism_line
      or "は同型写像である."
      not in isomorphism_line
    ):
      continue

    isomorphism_map = map_identity(
      isomorphism_step
    )

    if isomorphism_map is None:
      continue

    injective_indices = []
    surjective_indices = []

    for reason in reason_sidecar.reasons:
      conclusion_step = reason.conclusion_step

      if map_identity(
        conclusion_step
      ) != isomorphism_map:
        continue

      conclusion_line = (
        _render_generic_narrative_step(
          conclusion_step
        )
      )

      if not conclusion_line:
        continue

      reason_index = visible_reason_index(
        reason
      )

      if reason_index is None:
        continue

      if "は単射である." in conclusion_line:
        injective_indices.append(
          reason_index
        )
        continue

      if "は全射である." in conclusion_line:
        surjective_indices.append(
          reason_index
        )

    if (
      not injective_indices
      or not surjective_indices
    ):
      continue

    isomorphism_index = (
      paragraph_index_for_step(
        isomorphism_step
      )
    )

    if isomorphism_index is None:
      continue

    latest_support_index = max(
      (
        *injective_indices,
        *surjective_indices,
      )
    )

    if isomorphism_index > latest_support_index:
      continue

    block_start = isomorphism_index

    if (
      block_start > 0
      and paragraphs[
        block_start - 1
      ].strip()
      in connector_paragraphs
    ):
      block_start -= 1

    block = paragraphs[
      block_start:
      isomorphism_index + 1
    ]

    del paragraphs[
      block_start:
      isomorphism_index + 1
    ]

    injective_indices = []
    surjective_indices = []

    for reason in reason_sidecar.reasons:
      conclusion_step = reason.conclusion_step

      if map_identity(
        conclusion_step
      ) != isomorphism_map:
        continue

      conclusion_line = (
        _render_generic_narrative_step(
          conclusion_step
        )
      )

      if not conclusion_line:
        continue

      reason_index = visible_reason_index(
        reason
      )

      if reason_index is None:
        continue

      if "は単射である." in conclusion_line:
        injective_indices.append(
          reason_index
        )
        continue

      if "は全射である." in conclusion_line:
        surjective_indices.append(
          reason_index
        )

    if (
      not injective_indices
      or not surjective_indices
    ):
      paragraphs[
        block_start:
        block_start
      ] = block
      continue

    insertion_index = (
      max(
        (
          *injective_indices,
          *surjective_indices,
        )
      )
      + 1
    )

    paragraphs[
      insertion_index:
      insertion_index
    ] = block

  rendered = "\n\n".join(
    paragraphs
  )

  for reason in reason_sidecar.reasons:
    rendered = (
      _normalize_exactness_to_map_property_reason_prose(
        rendered,
        reason,
      )
    )

  paragraphs = rendered.split(
    "\n\n"
  )

  def exactness_locality_match_key(
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

    return statement_match_key(
      stripped
    )

  def concise_step_line(
    proof_step,
  ) -> str | None:
    line = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not line:
      return None

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
      if line.endswith(
        verbose
      ):
        return (
          line[
            :-len(
              verbose
            )
          ]
          + concise
        )

    return line

  for node in reason_sidecar.presentation.nodes:
    proof_step = node.proof_step
    conclusion_line = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not conclusion_line:
      continue

    if not (
      conclusion_line.endswith(
        " は単射である."
      )
      or conclusion_line.endswith(
        " は全射である."
      )
    ):
      continue

    concise_conclusion = (
      concise_step_line(
        proof_step
      )
    )

    if concise_conclusion is None:
      continue

    expected_paragraph = (
      "完全性より, "
      + concise_conclusion
    )
    conclusion_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == expected_paragraph
    )

    if len(
      conclusion_matches
    ) != 1:
      continue

    conclusion_index = conclusion_matches[
      0
    ]
    visible_premise_indices = []

    for premise_step in proof_step.premises:
      premise_line = (
        concise_step_line(
          premise_step
        )
      )

      if premise_line is None:
        continue

      premise_key = (
        exactness_locality_match_key(
          premise_line
        )
      )
      premise_matches = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if (
          index != conclusion_index
          and exactness_locality_match_key(
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
      continue

    latest_premise_index = max(
      visible_premise_indices
    )

    if (
      conclusion_index
      <= latest_premise_index
    ):
      continue

    if (
      conclusion_index
      == latest_premise_index + 1
    ):
      continue

    paragraph = paragraphs.pop(
      conclusion_index
    )
    paragraphs.insert(
      latest_premise_index + 1,
      paragraph,
    )

  rendered = "\n\n".join(
    paragraphs
  )
  paragraphs = rendered.split(
    "\n\n"
  )

  def paragraph_index_for_reason_step(
    proof_step,
  ) -> int | None:
    line = (
      concise_step_line(
        proof_step
      )
    )

    if line is None:
      return None

    target_key = (
      exactness_locality_match_key(
        line
      )
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if (
        exactness_locality_match_key(
          paragraph
        )
        == target_key
      )
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  for reason in reason_sidecar.reasons:
    if (
      reason.kind
      is not TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    ):
      continue

    if len(
      reason.premise_steps
    ) != 1:
      continue

    prerequisite_index = (
      paragraph_index_for_reason_step(
        reason.premise_steps[
          0
        ]
      )
    )
    definition_index = (
      paragraph_index_for_reason_step(
        reason.conclusion_step
      )
    )

    if (
      prerequisite_index is None
      or definition_index is None
      or prerequisite_index
      == definition_index - 1
    ):
      continue

    prerequisite_paragraph = paragraphs.pop(
      prerequisite_index
    )

    definition_index = (
      paragraph_index_for_reason_step(
        reason.conclusion_step
      )
    )

    if definition_index is None:
      paragraphs.insert(
        prerequisite_index,
        prerequisite_paragraph,
      )
      continue

    paragraphs.insert(
      definition_index,
      prerequisite_paragraph,
    )

  return "\n\n".join(
    paragraphs
  )
```

## 完了条件

- zero group -> H injective が隣接
- Delta zero -> H surjective が隣接
- H injective / H surjective の後に H isomorphism
- H isomorphism の後に pi3 target
- pi3 target -> eta2 definition が隣接
- eta2 definition -> final result
- focused pytest 全 PASS
- QED が最後

## 次 Phase との境界

- proof graph は変更しない
- Argument ordering は変更しない
- fixed statement の内容は変更しない
- global statement-type priority は導入しない
- full suite は Phase 159 の最後にのみ実行する
