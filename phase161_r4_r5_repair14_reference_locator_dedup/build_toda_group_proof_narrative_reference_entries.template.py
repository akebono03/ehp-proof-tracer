def build_toda_group_proof_narrative_reference_entries(
  presentation: TodaGroupProofPresentation,
) -> tuple[TodaGroupProofNarrativeReferenceEntry, ...]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  references = []
  steps_by_reference = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    reference = (
      extract_toda_group_proof_step_literature_reference(
        proof_step
      )
    )

    if reference is None:
      continue

    matching_index = next(
      (
        index
        for index, existing_reference in enumerate(
          references
        )
        if _same_toda_group_proof_literature_reference(
          existing_reference,
          reference,
        )
      ),
      None,
    )

    if matching_index is None:
      references.append(
        reference
      )
      steps_by_reference.append(
        [
          proof_step,
        ]
      )
      continue

    steps_by_reference[
      matching_index
    ].append(
      proof_step
    )

  return tuple(
    TodaGroupProofNarrativeReferenceEntry(
      number=number,
      reference=reference,
      proof_steps=tuple(
        proof_steps
      ),
    )
    for number, (
      reference,
      proof_steps,
    ) in enumerate(
      zip(
        references,
        steps_by_reference,
      ),
      start=1,
    )
  )
