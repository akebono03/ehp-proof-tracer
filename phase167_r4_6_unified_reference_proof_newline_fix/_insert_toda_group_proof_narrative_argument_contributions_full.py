def _insert_toda_group_proof_narrative_argument_contributions(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> str:
  insertion_indices = (
    _contribution_insertion_indices(
      markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  connector_by_target_step_id = (
    _contribution_connector_lines(
      presentation,
      ordered_contributions,
    )
  )

  # A cited general statement remains a proof premise and belongs to the
  # Reference section. Its typed specialization is the visible body step.
  from proof import ProofRule
  from phase165_r57_r20_general_specialization import (
    specialize_typed_statement,
  )

  specialized_source_ids = {
    id(source_step)
    for contributions in ordered_contributions
    for contribution in contributions
    for source_step in contribution.proof_step.premises
    if (
      source_step.rule is ProofRule.GIVEN
      and contribution.proof_step.rule is ProofRule.INFERENCE
      and specialize_typed_statement(
        source_step.conclusion,
        contribution.proof_step.conclusion,
      ) is not None
    )
  }
  insertions_by_index = {}

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    for contribution_index, contribution in enumerate(
      contributions
    ):
      if id(contribution.proof_step) in specialized_source_ids:
        continue
      contribution_line = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )

      if not contribution_line:
        continue

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          contribution.proof_step,
          contribution_line,
        )
      ):
        continue

      if contribution_line in markdown:
        continue

      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]

      if insertion_index is None:
        continue

      connector = (
        connector_by_target_step_id.get(
          id(
            contribution.proof_step
          )
        )
      )
      if any(
        id(premise) in specialized_source_ids
        and specialize_typed_statement(
          premise.conclusion,
          contribution.proof_step.conclusion,
        ) is not None
        for premise in contribution.proof_step.premises
      ):
        connector = None
      lines = []

      if connector is not None:
        lines.append(
          connector
        )

      lines.append(
        contribution_line
      )

      insertions_by_index.setdefault(
        insertion_index,
        [],
      ).append(
        "\n\n".join(
          lines
        )
      )

  rendered = markdown

  for insertion_index in sorted(
    insertions_by_index,
    reverse=True,
  ):
    contribution_fragments = insertions_by_index[
      insertion_index
    ]
    insertion = (
      "\n\n"
      + "\n\n".join(
        contribution_fragments
      )
    )

    if (
      insertion_index < len(
        markdown
      )
      and not markdown[
        insertion_index:
      ].startswith(
        "\n\n"
      )
    ):
      insertion += "\n\n"

    rendered = (
      rendered[
        :insertion_index
      ]
      + insertion
      + rendered[
        insertion_index:
      ]
    )

  return rendered
