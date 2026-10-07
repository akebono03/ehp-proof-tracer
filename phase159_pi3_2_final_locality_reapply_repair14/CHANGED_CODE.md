# Phase 159 pi3_2 final locality re-apply repair14

## 変更対象

1. `toda_group_proof_narrative_reason_renderer.py`
   - `order_toda_group_proof_narrative_injective_image_order_reason()` 全体を変更。

2. `toda_group_proof_narrative_contribution_renderer.py`
   - `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()` を変更。
   - `suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements()` の直後に
     final locality re-apply を1回追加。

3. `tests/test_phase159_pi3_2_final_locality_reapply.py`
   - 新規追加。

## import

import の変更はありません。

## audit13 の結論

最終 public body に
`order_toda_group_proof_narrative_injective_image_order_reason()`
を単独再適用すると、

`pi_2^1=0 -> H injective`

は正しく隣接した。

したがって exactness locality の判定自体は正しく、
pipeline 後段で順序が崩れている。

definition step については direct premises が public body に両方存在する:

1. `H` isomorphism
2. `pi_3^3 = Z{iota_3}`

しかし definition locality は発火していなかった。

## reason renderer の変更関数全文

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
  paragraphs = rendered.split(
    "\n\n"
  )

  def locality_match_key(
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

  def paragraph_index_for_line(
    line: str,
  ) -> int | None:
    target_key = locality_match_key(
      line
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if locality_match_key(
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

  for reason in reason_sidecar.reasons:
    if (
      reason.kind
      is not TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    ):
      continue

    reason_paragraph = (
      visible_reason_paragraph(
        reason
      )
    )

    if reason_paragraph is None:
      continue

    conclusion_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph.strip()
      == reason_paragraph
    )

    if len(
      conclusion_matches
    ) != 1:
      continue

    conclusion_index = conclusion_matches[
      0
    ]
    visible_premise_indices = []

    for premise_step in reason.premise_steps:
      premise_line = (
        _render_generic_narrative_step(
          premise_step
        )
      )

      if not premise_line:
        continue

      premise_index = paragraph_index_for_line(
        premise_line
      )

      if premise_index is None:
        continue

      visible_premise_indices.append(
        premise_index
      )

    if not visible_premise_indices:
      continue

    latest_premise_index = max(
      visible_premise_indices
    )

    if (
      conclusion_index
      <= latest_premise_index
      or conclusion_index
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

  def math_spans(
    text: str,
  ) -> tuple[
    str,
    ...,
  ]:
    spans = []
    search_start = 0

    while True:
      open_index = text.find(
        "$",
        search_start,
      )

      if open_index < 0:
        break

      close_index = text.find(
        "$",
        open_index + 1,
      )

      if close_index < 0:
        break

      spans.append(
        text[
          open_index:
          close_index + 1
        ]
      )
      search_start = close_index + 1

    return tuple(
      spans
    )

  for node in reason_sidecar.presentation.nodes:
    proof_step = node.proof_step
    generic_definition = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not generic_definition:
      continue

    if (
      "を満たす" not in generic_definition
      or "を定める." not in generic_definition
    ):
      continue

    premise_lines = tuple(
      _render_generic_narrative_step(
        premise_step
      )
      for premise_step in proof_step.premises
    )
    isomorphism_premises = tuple(
      premise_line
      for premise_line in premise_lines
      if (
        premise_line
        and "同型写像である."
        in premise_line
      )
    )

    if len(
      isomorphism_premises
    ) != 1:
      continue

    definition_spans = math_spans(
      generic_definition
    )

    if not definition_spans:
      continue

    definition_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if (
        paragraph.strip().startswith(
          "この同型写像により, "
        )
        and all(
          span in paragraph
          for span in definition_spans
        )
      )
    )

    if len(
      definition_matches
    ) != 1:
      continue

    visible_premise_records = []

    for premise_step in proof_step.premises:
      premise_line = (
        _render_generic_narrative_step(
          premise_step
        )
      )

      if not premise_line:
        continue

      premise_index = paragraph_index_for_line(
        premise_line
      )

      if premise_index is None:
        continue

      visible_premise_records.append(
        (
          premise_step,
          premise_index,
        )
      )

    if not visible_premise_records:
      continue

    premise_paragraphs = [
      paragraphs[
        premise_index
      ]
      for (
        _,
        premise_index,
      ) in visible_premise_records
    ]

    for premise_index in sorted(
      (
        premise_index
        for (
          _,
          premise_index,
        ) in visible_premise_records
      ),
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
      if (
        paragraph.strip().startswith(
          "この同型写像により, "
        )
        and all(
          span in paragraph
          for span in definition_spans
        )
      )
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

  return "\n\n".join(
    paragraphs
  )
```

## contribution renderer の変更

変更後の該当部分:

```python
  rendered = (
    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )

  generic_used_step_ids = (
    build_toda_group_proof_narrative_generic_used_step_ids(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      ordered_contributions,
    )
  )
```

この変更以外の同関数本体は変更しない。

## definition locality 規則

generic definition paragraph が

- `を満たす`
- `を定める.`

を含み、
同じ ProofStep に isomorphism premise がちょうど1つある場合だけ対象。

generic definition 文に含まれる `$...$` math spans を抽出し、
public prose の

`この同型写像により, ...`

で始まる paragraph のうち、
すべての math spans を含む唯一の paragraph と対応付ける。

その後、visible direct premises を `ProofStep.premises` の保存順で
definition paragraph の直前へ連続配置する。

pi3_2 では:

1. `H` isomorphism
2. `pi_3^3 = Z{iota_3}`
3. eta2 definition

となる。

## focused pytest

```powershell
python -m pytest `
  ".\tests\test_phase159_pi3_2_final_locality_reapply.py" `
  ".\tests\test_phase159_pi3_2_proofstep_premise_locality.py" `
  ".\tests\test_phase159_pi3_2_map_property_order.py" `
  ".\tests\test_phase159_pi3_2_visible_dependency_topological_order.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase159_r1_2_hopf_injective_dependency_role.py" `
  ".\tests\test_phase159_r1_2_hopf_isomorphism_dependency_role.py" `
  -q
```

## 完了条件

- `pi_2^1=0 -> H injective` が隣接
- `E isomorphism -> E injective -> Delta=0 -> H surjective`
- `Delta=0 -> H surjective` が隣接
- `H injective`, `H surjective` の後に `H isomorphism`
- `H isomorphism -> pi_3^3 -> eta_2 definition` が連続
- eta2 definition の後に final group
- QED が最後
- focused pytest 全 PASS

## 次 Phase との境界

- proof graph は変更しない
- semantic sidecar は変更しない
- fixed literature statement は変更しない
- Argument ordering は変更しない
- global statement-type priority は追加しない
- full suite は Phase 159 の最後にのみ実行する
