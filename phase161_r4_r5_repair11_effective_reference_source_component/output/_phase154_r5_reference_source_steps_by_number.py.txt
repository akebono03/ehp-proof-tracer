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

      component_premises = tuple(
        premise_step
        for premise_step in proof_step.premises
        if premise_step.conclusion == component
      )

      if len(
        component_premises
      ) == 1:
        effective_selected_steps.append(
          component_premises[
            0
          ]
        )
        continue

      effective_selected_steps.append(
        proof_step
      )

    ordered_source_steps = []
    seen_step_ids = set()

    for proof_step in (
      *effective_selected_steps,
      *entry.proof_steps,
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
