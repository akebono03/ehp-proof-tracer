def extract_toda_group_proof_step_literature_reference(
  proof_step: ProofStep,
) -> LiteratureReference | None:
  if not isinstance(proof_step, ProofStep):
    raise TypeError("proof_step must be a ProofStep")

  inference_rule = proof_step.inference_rule
  if inference_rule is None:
    return None

  boundary = classify_toda_literature_statement_step(
    proof_step
  )

  if (
    boundary is not None
    and boundary.classification
    == TodaLiteratureStatementClassification.FIXED_STATEMENT
  ):
    fixed_locator = boundary.reference_locator
    existing_reference = (
      inference_rule.literature_reference
    )

    if (
      existing_reference is not None
      and existing_reference.locator
      == fixed_locator
    ):
      return existing_reference

    if existing_reference is not None:
      return replace(
        existing_reference,
        label="Toda " + fixed_locator,
        locator=fixed_locator,
      )

    return LiteratureReference(
      label="Toda " + fixed_locator,
      locator=fixed_locator,
    )

  if inference_rule.literature_reference is not None:
    return inference_rule.literature_reference

  return _infer_toda_group_proof_literature_reference_from_rule_name(
    inference_rule.name
  )
