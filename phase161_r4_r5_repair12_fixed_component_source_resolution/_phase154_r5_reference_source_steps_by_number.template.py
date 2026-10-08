def _phase154_r5_reference_source_steps_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    ProofStep,
    ...,
  ],
]:
  source_steps_by_number = {}

  presentation_steps = tuple(
    node.proof_step
    for node in presentation.nodes
  )

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not rendered_statement:
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    effective_selected_steps = []
    replaced_selected_step_ids = set()

    for proof_step in selected_steps:
      component = (
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          proof_step,
        )
      )

      if component is None:
        effective_selected_steps.append(
          proof_step
        )
        continue

      fixed_component_steps = []

      for candidate_step in presentation_steps:
        if candidate_step.conclusion != component:
          continue

        boundary = (
          classify_toda_literature_statement_step(
            candidate_step
          )
        )

        if (
          boundary is None
          or boundary.classification
          is not TodaLiteratureStatementClassification.FIXED_STATEMENT
          or boundary.reference_locator
          != entry.reference.locator
          or boundary.component_key is None
        ):
          continue

        fixed_component_steps.append(
          candidate_step
        )

      unique_fixed_component_steps = tuple(
        dict.fromkeys(
          fixed_component_steps
        )
      )

      if len(
        unique_fixed_component_steps
      ) != 1:
        effective_selected_steps.append(
          proof_step
        )
        continue

      effective_selected_steps.append(
        unique_fixed_component_steps[
          0
        ]
      )
      replaced_selected_step_ids.add(
        id(
          proof_step
        )
      )

    ordered_source_steps = []
    seen_step_ids = set()

    fallback_entry_steps = tuple(
      proof_step
      for proof_step in entry.proof_steps
      if id(
        proof_step
      )
      not in replaced_selected_step_ids
    )

    for proof_step in (
      *effective_selected_steps,
      *fallback_entry_steps,
    ):
      proof_step_id = id(
        proof_step
      )

      if proof_step_id in seen_step_ids:
        continue

      seen_step_ids.add(
        proof_step_id
      )
      ordered_source_steps.append(
        proof_step
      )

    if ordered_source_steps:
      source_steps_by_number[
        entry.number
      ] = tuple(
        ordered_source_steps
      )

  return source_steps_by_number
