from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_6_EQUALS_NU_7_FACT,
  NU_PRIME_NU_6_ZERO_COMPOSITION_FACT,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from theorem_facts import (
  EPSILON_3_TODA_MEMBERSHIP_FACT,
  THEOREM_FACT_REPOSITORY,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  TodaBracketMembershipStatement,
  indexed_toda_bracket_index1_defined_inference_rule,
  toda_bracket_membership_from_theorem_inference_rule,
)


def derive_actual_indexed_definedness_step():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  second_zero_step = relation_proof_step(
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )

  suspension_step = relation_proof_step(
    E_NU_6_EQUALS_NU_7_FACT
  )

  rule = (
    indexed_toda_bracket_index1_defined_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
      suspension_step,
    ),
  )

  defined_steps = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaBracketDefinedStatement,
    )
  )

  assert len(defined_steps) == 1

  return defined_steps[0]


def test_phase27_6_derived_definedness_matches_production_theorem_bracket():
  defined_step = (
    derive_actual_indexed_definedness_step()
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  assert (
    defined_step.conclusion.bracket
    == entry.statement.bracket
  )


def test_phase27_6_theorem_repository_materializes_matching_theorem_step():
  defined_step = (
    derive_actual_indexed_definedness_step()
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  theorem_step = entry.to_proof_step()

  assert theorem_step.rule == (
    ProofRule.GIVEN
  )

  assert (
    theorem_step.conclusion.bracket
    == defined_step.conclusion.bracket
  )

  assert theorem_step.conclusion.source == (
    entry.reference
  )


def test_phase27_6_existing_theorem_rule_accepts_actual_derived_definedness():
  defined_step = (
    derive_actual_indexed_definedness_step()
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  theorem_step = entry.to_proof_step()

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    membership_rule,
    (
      theorem_step,
      defined_step,
    ),
  )

  expected = TodaBracketMembershipStatement(
    element=entry.statement.element,
    bracket=entry.statement.bracket,
    source=entry.reference,
    note=entry.statement.note,
  )

  matching_steps = tuple(
    step
    for step in result.steps
    if step.conclusion == expected
  )

  assert len(matching_steps) == 1

  derived_step = matching_steps[0]

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == (
    membership_rule
  )

  assert derived_step.premises == (
    theorem_step,
    defined_step,
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase27_6_theorem_rule_does_not_apply_without_actual_definedness():
  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  theorem_step = entry.to_proof_step()

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    membership_rule,
    (
      theorem_step,
    ),
  )

  expected = TodaBracketMembershipStatement(
    element=entry.statement.element,
    bracket=entry.statement.bracket,
    source=entry.reference,
    note=entry.statement.note,
  )

  assert expected not in tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )
