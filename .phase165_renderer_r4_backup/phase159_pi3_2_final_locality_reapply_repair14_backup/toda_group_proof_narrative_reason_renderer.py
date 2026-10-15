from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_expression_latex,
  _render_generic_narrative_step,
)
from toda_rules import (
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
  TodaGroupProofNarrativeReasonSidecar,
)
from toda_proof_narrative_renderer import (
  render_toda_raw_group_structure_latex,
  render_toda_primary_group_latex,
)


def render_toda_group_proof_narrative_reason_sentence(
  reason: TodaGroupProofNarrativeReason,
) -> str | None:
  if not isinstance(
    reason,
    TodaGroupProofNarrativeReason,
  ):
    raise TypeError(
      "reason must be a "
      "TodaGroupProofNarrativeReason"
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  ):
    application = reason.reference_application

    if application is None or len(application.bindings) != 1:
      return (
        "この前提条件を満たすので, "
        "次の定義を用いる."
      )

    binding = application.bindings[0]
    reference_label = application.reference.label
    formal_latex = render_toda_expression_latex(
      binding.formal_variable
    )
    instantiated_latex = render_toda_expression_latex(
      binding.instantiated_expression
    )

    return (
      "この前提条件を満たすので, "
      f"{reference_label} を適用できる.\n"
      f"{reference_label} の "
      f"${formal_latex}$ を "
      f"${instantiated_latex}$ と定めると, "
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    if len(reason.premise_steps) != 2:
      return None

    conclusion = (
      _render_generic_narrative_step(
        reason.conclusion_step
      )
    )
    if not conclusion:
      return None

    concise_conclusion = conclusion

    for verbose, concise in (
      (" は単射である.", " は単射."),
      (" は全射である.", " は全射."),
    ):
      if concise_conclusion.endswith(
        verbose
      ):
        concise_conclusion = (
          concise_conclusion[
            :-len(verbose)
          ]
          + concise
        )
        break

    return (
      "完全性より, "
      + concise_conclusion
    )


  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_KERNEL
  ):
    if len(reason.premise_steps) != 2:
      return None

    image_statement = (
      reason.premise_steps[0].conclusion
    )
    exactness_statement = (
      reason.premise_steps[1].conclusion
    )
    conclusion = (
      reason.conclusion_step.conclusion
    )
    window = exactness_statement.window
    first_map_name = window.first_map.name
    second_map_name = window.second_map.name
    group_latex = (
      render_toda_raw_group_structure_latex(
        conclusion.kernel_group
      )
    )

    if (
      image_statement.image_group
      != conclusion.kernel_group
    ):
      return None

    return (
      "完全性より, "
      f"$\\ker {second_map_name}"
      f"=\\operatorname{{Im}}{first_map_name}"
      f"={group_latex}$."
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .INJECTIVE_IMAGE_ORDER
  ):
    if len(
      reason.premise_steps
    ) != 2:
      return None

    group_statement = (
      reason.premise_steps[
        0
      ].conclusion
    )
    injective_statement = (
      reason.premise_steps[
        1
      ].conclusion
    )
    order_statement = (
      reason.conclusion_step.conclusion
    )

    finite_group = group_statement.rhs
    source_generator_latex = (
      _render_generic_narrative_expression_latex(
        finite_group.generator
      )
    )
    target_latex = (
      _render_generic_narrative_expression_latex(
        order_statement.lhs
      )
    )
    order = finite_group.order

    if (
      not source_generator_latex
      or not target_latex
    ):
      return None

    if (
      type(
        injective_statement.map
      ).__name__
      not in (
        "TodaSuspensionMap",
        "TodaIteratedSuspensionMap",
      )
    ):
      return None

    group_structure = (
      _render_generic_narrative_step(
        reason.premise_steps[
          0
        ]
      )
    )

    return (
      f"{group_structure} と $E$ の単射性より, "
      f"$E({source_generator_latex})"
      f"={target_latex}\\neq0$ であり, "
      "単射写像は元の位数を保つ.\n"
      "したがって, "
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .MULTIPLE_RELATION_TO_ORDER
  ):
    if len(reason.premise_steps) != 2:
      return None

    order_statement = reason.premise_steps[0].conclusion
    equality_statement = reason.premise_steps[1].conclusion
    ordered_latex = (
      _render_generic_narrative_expression_latex(
        order_statement.lhs
      )
    )
    target_latex = (
      _render_generic_narrative_expression_latex(
        equality_statement.lhs.expression
      )
    )

    return (
      f"$\\operatorname{{ord}}({ordered_latex})=2$ "
      f"かつ $2{target_latex}={ordered_latex}$ より, "
      f"$4{target_latex}=0$ かつ "
      f"$2{target_latex}\\neq0$.\n"
      "したがって, "
    )

  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .FINAL_GROUP_STRUCTURE
  ):
    if len(reason.premise_steps) != 7:
      return None

    left_group_statement = reason.premise_steps[0].conclusion
    right_group_statement = reason.premise_steps[4].conclusion
    order_statement = reason.premise_steps[5].conclusion
    membership_statement = reason.premise_steps[6].conclusion

    left_order = left_group_statement.rhs.order
    right_order = right_group_statement.rhs.order
    middle_order = left_order * right_order
    generator_latex = render_toda_expression_latex(
      membership_statement.element
    )

    return (
      "この短完全列と両端の群の位数より, "
      f"中央の群の位数は ${left_order}\\cdot"
      f"{right_order}={middle_order}$.\n"
      f"また, ${generator_latex}$ は中央の群に属し, "
      f"$\\operatorname{{ord}}({generator_latex})"
      f"={middle_order}$ より, "
      f"${generator_latex}$ は中央の群を生成する.\n"
      "したがって, "
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.MAP_STRUCTURE_DERIVATION:
    return (
      "この完全性, 既知の群構造, および写像の像に関する結果を合わせると, "
      "対象となる写像の像と核が決まる.\nしたがって, "
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.GROUP_ORDER_DERIVATION:
    return (
      "群構造に関する結果と写像による移送の結果を合わせると, "
      "対象の群の位数と写像の単射性が決まる.\nしたがって, "
    )

  if reason.kind is TodaGroupProofNarrativeReasonKind.FINAL_RESULT_DERIVATION:
    return None

  return None



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

  def unique_preimage_definition_line(
    proof_step,
  ) -> str | None:
    statement = getattr(
      proof_step,
      "conclusion",
      None,
    )
    group_map = getattr(
      statement,
      "map",
      None,
    )
    element = getattr(
      statement,
      "element",
      None,
    )
    image = getattr(
      statement,
      "image",
      None,
    )

    if (
      group_map is None
      or element is None
      or image is None
    ):
      return None

    isomorphism_premises = tuple(
      premise_step
      for premise_step in proof_step.premises
      if (
        getattr(
          getattr(
            premise_step,
            "conclusion",
            None,
          ),
          "map",
          None,
        )
        == group_map
        and "同型"
        in (
          _render_generic_narrative_step(
            premise_step
          )
          or ""
        )
      )
    )

    if len(
      isomorphism_premises
    ) != 1:
      return None

    map_name = getattr(
      group_map,
      "name",
      None,
    )

    if not isinstance(
      map_name,
      str,
    ):
      return None

    source_group = getattr(
      group_map,
      "source_group",
      None,
    )

    if source_group is None:
      return None

    return (
      "この同型写像により, $"
      + map_name
      + "("
      + render_toda_expression_latex(
        element
      )
      + ") = "
      + render_toda_expression_latex(
        image
      )
      + "$ となる $"
      + render_toda_expression_latex(
        element
      )
      + r" \in "
      + render_toda_primary_group_latex(
        source_group
      )
      + "$ が一意に存在する."
    )

  for node in reason_sidecar.presentation.nodes:
    proof_step = node.proof_step
    definition_line = (
      unique_preimage_definition_line(
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

  return "\n\n".join(
    paragraphs
  )

def _toda_group_proof_narrative_reason_insertion_index(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> int | None:
  conclusion_line = _render_generic_narrative_step(
    reason.conclusion_step
  )
  if conclusion_line:
    conclusion_index = markdown.find(conclusion_line)
    if conclusion_index >= 0:
      return conclusion_index

  children_by_step_id = {}
  for edge in reason_sidecar.presentation.edges:
    children_by_step_id.setdefault(
      id(edge.premise_step),
      [],
    ).append(edge.parent_step)

  queue = list(
    children_by_step_id.get(
      id(reason.conclusion_step),
      (),
    )
  )
  visited_step_ids = {
    id(reason.conclusion_step),
  }

  while queue:
    next_queue = []
    for proof_step in queue:
      proof_step_id = id(proof_step)
      if proof_step_id in visited_step_ids:
        continue
      visited_step_ids.add(proof_step_id)

      rendered_line = _render_generic_narrative_step(
        proof_step
      )
      if rendered_line:
        rendered_index = markdown.find(rendered_line)
        if rendered_index >= 0:
          return rendered_index

      next_queue.extend(
        children_by_step_id.get(
          proof_step_id,
          (),
        )
      )
    queue = next_queue

  return None




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

def _normalize_exactness_to_kernel_reason_prose(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
) -> str:
  if (
    reason.kind
    is not TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_KERNEL
  ):
    return markdown

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  if sentence is None:
    return markdown

  reason_lines = sentence.splitlines()

  while (
    reason_lines
    and reason_lines[-1].strip()
    in {
      "以上より,",
      "したがって,",
      "これより,",
      "これらより,",
    }
  ):
    reason_lines.pop()

  reason_body = "\n".join(
    reason_lines
  ).strip()

  if not reason_body:
    return markdown

  paragraphs = markdown.split(
    "\n\n"
  )
  reason_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if paragraph.strip() == reason_body
  )

  if len(reason_indices) != 1:
    return markdown

  reason_index = reason_indices[0]

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

  image_line = (
    _render_generic_narrative_step(
      reason.premise_steps[0]
    )
    if reason.premise_steps
    else ""
  )
  kernel_line = (
    _render_generic_narrative_step(
      reason.conclusion_step
    )
  )
  covered_lines = {
    line.strip()
    for line in (
      image_line,
      kernel_line,
    )
    if line
  }

  retained = paragraphs[
    :reason_index + 1
  ]

  for paragraph in paragraphs[
    reason_index + 1:
  ]:
    if paragraph.strip() in covered_lines:
      continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


def insert_toda_group_proof_narrative_reason_prose(
  markdown: str,
  reason_sidecar: TodaGroupProofNarrativeReasonSidecar,
) -> str:
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a str")
  if not isinstance(
    reason_sidecar,
    TodaGroupProofNarrativeReasonSidecar,
  ):
    raise TypeError(
      "reason_sidecar must be a "
      "TodaGroupProofNarrativeReasonSidecar"
    )

  rendered = markdown
  emitted_final_result_sentences = set()

  for reason in reason_sidecar.reasons:
    sentence = render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    if sentence is None:
      continue

    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .FINAL_RESULT_DERIVATION
    ):
      if sentence in emitted_final_result_sentences:
        continue

      emitted_final_result_sentences.add(
        sentence
      )

    insertion_index = (
      _toda_group_proof_narrative_reason_insertion_index(
        rendered,
        reason,
        reason_sidecar,
      )
    )
    if insertion_index is None:
      continue

    prefix = sentence + "\n\n"
    if rendered[
      max(0, insertion_index - len(prefix)):
      insertion_index
    ] == prefix:
      continue

    rendered = (
      rendered[:insertion_index]
      + prefix
      + rendered[insertion_index:]
    )

  for reason in reason_sidecar.reasons:
    rendered = (
      _normalize_exactness_to_map_property_reason_prose(
        rendered,
        reason,
      )
    )

  for reason in reason_sidecar.reasons:
    rendered = (
      _normalize_exactness_to_kernel_reason_prose(
        rendered,
        reason,
      )
    )

  return rendered

