# Phase 158-R5-5b repair1v

## 変更対象

1. `toda_group_proof_narrative_argument_multi_renderer.py`
   - `render_toda_group_proof_narrative_multi_argument_markdown()`
   - import 変更なし
   - local-body merge 部分を、Argument role に依存しない dependency-order preservation に変更

変更する local-body 部分:

```python
    missing_evidence_blocks = tuple(
      block
      for block in blocks
      if (
        id(
          block
        ) in evidence_block_ids
        and id(
          block
        ) not in local_body_block_ids
      )
    )

    if missing_evidence_blocks:
      conclusion_position = next(
        (
          index
          for index, block in enumerate(
            local_body_blocks
          )
          if block is argument.conclusion_block
        ),
        len(
          local_body_blocks
        ),
      )
      local_body_blocks = (
        local_body_blocks[
          :conclusion_position
        ]
        + missing_evidence_blocks
        + local_body_blocks[
          conclusion_position:
        ]
      )
```

この関数のその他の処理は変更しない。

2. `toda_group_proof_narrative_equation_numbering.py`
   - `number_toda_group_proof_narrative_equations()`
   - import 変更なし

変更後関数全文:

```python
def number_toda_group_proof_narrative_equations(
  markdown: str,
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
) -> str:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a string")

  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(blocks, tuple):
    raise TypeError("blocks must be a tuple")

  transitions = (
    extract_toda_group_proof_narrative_step_transitions(
      presentation,
      blocks,
    )
  )
  sources_by_target = {}

  for transition in transitions:
    target_id = id(
      transition.target_step
    )
    current = sources_by_target.get(
      target_id,
      (),
    )

    if any(
      step is transition.source_step
      for step in current
    ):
      continue

    sources_by_target[
      target_id
    ] = (
      *current,
      transition.source_step,
    )

  step_by_id = {
    id(
      proof_step
    ): proof_step
    for block in blocks
    for proof_step in block.steps
  }
  lines = markdown.splitlines()
  plain_by_id = {
    step_id: _render_generic_narrative_step(
      proof_step
    )
    for step_id, proof_step in step_by_id.items()
  }

  reference_plans = []
  line_index_by_id = {}

  for target_id, source_steps in sources_by_target.items():
    target_plain = plain_by_id.get(
      target_id
    )

    if not target_plain:
      continue

    target_index = next(
      (
        index
        for index, line in enumerate(
          lines
        )
        if line == target_plain
      ),
      None,
    )

    if target_index is None:
      continue

    connector_index = next(
      (
        index
        for index in range(
          target_index - 1,
          -1,
          -1,
        )
        if lines[index] == "これらより, "
      ),
      None,
    )

    if connector_index is None:
      continue

    visible_source_ids = []

    for source_step in source_steps:
      source_id = id(
        source_step
      )
      source_plain = plain_by_id.get(
        source_id
      )

      if not source_plain:
        continue

      source_index = next(
        (
          index
          for index in range(
            connector_index - 1,
            -1,
            -1,
          )
          if lines[index] == source_plain
        ),
        None,
      )

      if source_index is None:
        continue

      visible_source_ids.append(
        source_id
      )
      current_index = line_index_by_id.get(
        source_id
      )

      if (
        current_index is None
        or source_index < current_index
      ):
        line_index_by_id[
          source_id
        ] = source_index

    if not visible_source_ids:
      continue

    current_target_index = line_index_by_id.get(
      target_id
    )

    if (
      current_target_index is None
      or target_index < current_target_index
    ):
      line_index_by_id[
        target_id
      ] = target_index

    reference_plans.append(
      (
        connector_index,
        tuple(
          visible_source_ids
        ),
      )
    )

  ordered_step_ids = tuple(
    step_id
    for step_id, _line_index in sorted(
      line_index_by_id.items(),
      key=lambda item: item[1],
    )
  )
  number_by_id = {
    step_id: number
    for number, step_id in enumerate(
      ordered_step_ids,
      start=1,
    )
  }

  occupied_line_indices = set()

  for step_id in ordered_step_ids:
    line_index = line_index_by_id[
      step_id
    ]

    if line_index in occupied_line_indices:
      continue

    proof_step = step_by_id.get(
      step_id
    )

    if proof_step is None:
      continue

    tagged_line = _numbered_step_line(
      proof_step,
      number_by_id[
        step_id
      ],
    )

    if tagged_line == lines[
      line_index
    ]:
      continue

    lines[
      line_index
    ] = tagged_line
    occupied_line_indices.add(
      line_index
    )

  for connector_index, source_ids in reference_plans:
    references = tuple(
      toda_group_proof_narrative_equation_reference(
        number_by_id[
          source_id
        ]
      )
      for source_id in source_ids
      if (
        source_id in number_by_id
        and line_index_by_id[
          source_id
        ] < connector_index
      )
    )

    if not references:
      continue

    if len(
      references
    ) == 1:
      reference_text = references[
        0
      ]
    else:
      reference_text = (
        ", ".join(
          references[
            :-1
          ]
        )
        + " と "
        + references[
          -1
        ]
      )

    lines[
      connector_index
    ] = (
      reference_text
      + " より, "
    )

  return "\n".join(
    lines
  )
```

3. `toda_group_proof_narrative_renderer.py`
   - `_phase158_normalize_public_equation_numbers()`
   - import 変更なし

変更後関数全文:

```python
def _phase158_normalize_public_equation_numbers(
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  connector_numbers_by_index = {}
  referenced_numbers = set()

  for index, line in enumerate(
    proof_body
  ):
    numbers = (
      _phase158_public_equation_connector_numbers(
        line
      )
    )

    if numbers is None:
      continue

    connector_numbers_by_index[
      index
    ] = numbers
    referenced_numbers.update(
      numbers
    )

  derivation_target_numbers = set()

  for connector_index in connector_numbers_by_index:
    target_index = next(
      (
        index
        for index in range(
          connector_index + 1,
          len(
            proof_body
          ),
        )
        if proof_body[
          index
        ].strip()
      ),
      None,
    )

    if target_index is None:
      continue

    target_number = (
      _phase158_public_equation_tag_number(
        proof_body[
          target_index
        ]
      )
    )

    if target_number is not None:
      derivation_target_numbers.add(
        target_number
      )

  retained_numbers = (
    referenced_numbers
    | derivation_target_numbers
  )
  retained_old_numbers = []
  seen_old_numbers = set()

  for line in proof_body:
    number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if (
      number is None
      or number not in retained_numbers
      or number in seen_old_numbers
    ):
      continue

    retained_old_numbers.append(
      number
    )
    seen_old_numbers.add(
      number
    )

  number_map = {
    old_number: new_number
    for new_number, old_number in enumerate(
      retained_old_numbers,
      start=1,
    )
  }

  result = []
  emitted_old_numbers = set()

  for index, source_line in enumerate(
    proof_body
  ):
    line = source_line
    tag_number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if tag_number is not None:
      old_marker = (
        r"\tag{"
        + str(
          tag_number
        )
        + "}"
      )

      if (
        tag_number not in number_map
        or tag_number in emitted_old_numbers
      ):
        line = line.replace(
          old_marker,
          "",
          1,
        )
      else:
        line = line.replace(
          old_marker,
          (
            r"\tag{"
            + str(
              number_map[
                tag_number
              ]
            )
            + "}"
          ),
          1,
        )
        emitted_old_numbers.add(
          tag_number
        )

    connector_numbers = (
      connector_numbers_by_index.get(
        index
      )
    )

    if connector_numbers is not None:
      if all(
        number in number_map
        for number in connector_numbers
      ):
        line = (
          _phase158_render_public_equation_connector(
            tuple(
              number_map[
                number
              ]
              for number in connector_numbers
            )
          )
        )
      else:
        line = (
          "これより,"
          if len(
            connector_numbers
          ) == 1
          else "これらより,"
        )

    result.append(
      line
    )

  return result
```

## Tests

新規・変更なし。

既存 canonical tests を使用する。

## 完了条件

- dependency source が conclusion より前
- source equation / connector / target equation が1つの chain
- target equation も番号付き
- public normalization が valid target tag を保持
- dangling / reflexive cleanup を維持
- group-specific hardcoding なし
- repository-wide pytest は Phase 158 最後まで実行しない
