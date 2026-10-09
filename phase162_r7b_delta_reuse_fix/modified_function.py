def insert_toda_group_proof_narrative_map_property_dependencies(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  reference_entries=(),
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reference_entries,
    tuple,
  ):
    raise TypeError(
      "reference_entries must be a tuple"
    )

  paragraphs = markdown.split(
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
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def reference_entry_for_step(
    proof_step: ProofStep,
  ):
    direct = tuple(
      entry
      for entry in reference_entries
      if any(
        candidate is proof_step
        for candidate in entry.proof_steps
      )
    )

    if len(
      direct
    ) == 1:
      return direct[
        0
      ]

    reference = (
      extract_toda_group_proof_step_literature_reference(
        proof_step
      )
    )

    if (
      reference is None
      or reference.locator is None
    ):
      return None

    by_locator = tuple(
      entry
      for entry in reference_entries
      if (
        entry.reference.locator
        == reference.locator
      )
    )

    if len(
      by_locator
    ) != 1:
      return None

    return by_locator[
      0
    ]

  def reference_number_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    entry = reference_entry_for_step(
      proof_step
    )

    if entry is None:
      return None

    return entry.number

  def display_line(
    proof_step: ProofStep,
  ) -> str | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    entry = reference_entry_for_step(
      proof_step
    )

    if entry is not None:
      rendered = (
        _phase153_r6_render_reference_statement(
          presentation,
          entry,
          proof_step,
          rendered,
        )
      )
      rendered = (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          rendered,
        )
      )

    reference_number = (
      reference_number_for_step(
        proof_step
      )
    )

    if reference_number is None:
      return rendered

    return (
      "[R"
      + str(
        reference_number
      )
      + "]より, "
      + rendered
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = display_line(
      proof_step
    )

    if not rendered:
      return None

    target_key = match_key(
      rendered
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

    if not matches:
      return None

    return matches[
      0
    ]

  relevant_roles = {
    TodaProofDependencyRole.EHP_EXACTNESS,
    TodaProofDependencyRole.EHP_WINDOW,
    TodaProofDependencyRole.GROUP_STRUCTURE,
    TodaProofDependencyRole.MAP_PROPERTY,
    TodaProofDependencyRole.RELATION,
  }

  visiting = set()

  def ensure_before(
    proof_step: ProofStep,
    anchor_index: int,
  ) -> int:
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in visiting:
      return anchor_index

    visiting.add(
      proof_step_id
    )

    boundary = (
      classify_toda_literature_statement_step(
        proof_step
      )
    )
    is_fixed_boundary = (
      boundary is not None
      and boundary.classification
      is TodaLiteratureStatementClassification.FIXED_STATEMENT
    )

    if not is_fixed_boundary:
      for premise in proof_step.premises:
        premise_role = (
          classify_toda_proof_step_role(
            premise
          )
        )

        if premise_role not in relevant_roles:
          continue

        anchor_index = ensure_before(
          premise,
          anchor_index,
        )

    line = display_line(
      proof_step
    )

    if line is None:
      visiting.remove(
        proof_step_id
      )
      return anchor_index

    current_index = (
      paragraph_index_for_step(
        proof_step
      )
    )

    if current_index is not None:
      if current_index < anchor_index:
        visiting.remove(
          proof_step_id
        )
        return anchor_index

      paragraph = paragraphs.pop(
        current_index
      )
      paragraphs.insert(
        anchor_index,
        paragraph,
      )

      visiting.remove(
        proof_step_id
      )
      return anchor_index + 1

    paragraphs.insert(
      anchor_index,
      line,
    )

    visiting.remove(
      proof_step_id
    )
    return anchor_index + 1

  visible_map_steps = []

  for node in presentation.nodes:
    proof_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        proof_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    if (
      paragraph_index_for_step(
        proof_step
      )
      is None
    ):
      continue

    visible_map_steps.append(
      proof_step
    )

  for map_step in visible_map_steps:
    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    for premise in map_step.premises:
      role = classify_toda_proof_step_role(
        premise
      )

      if role not in relevant_roles:
        continue

      map_index = ensure_before(
        premise,
        map_index,
      )

  return "\n\n".join(
    paragraphs
  )
