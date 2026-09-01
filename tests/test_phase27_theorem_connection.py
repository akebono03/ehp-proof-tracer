from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_6_EQUALS_NU_7_FACT,
  NU_PRIME_NU_6_ZERO_COMPOSITION_FACT,
)
from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  Zero,
)
from generator_facts import (
  NU_7_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  Relation,
  RelationType,
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


def test_phase27_7_corrected_epsilon_3_membership_runs_end_to_end():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  second_zero_step = relation_proof_step(
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )

  suspension_step = relation_proof_step(
    E_NU_6_EQUALS_NU_7_FACT
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  theorem_step = entry.to_proof_step()

  definedness_rule = (
    indexed_toda_bracket_index1_defined_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      definedness_rule,
      membership_rule,
    ),
    (
      first_zero_step,
      second_zero_step,
      suspension_step,
      theorem_step,
    ),
  )

  expected_definedness = (
    TodaBracketDefinedStatement(
      bracket=entry.statement.bracket,
    )
  )

  expected_membership = (
    TodaBracketMembershipStatement(
      element=entry.statement.element,
      bracket=entry.statement.bracket,
      source=entry.reference,
      note=entry.statement.note,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected_definedness in conclusions
  assert expected_membership in conclusions

  matching_memberships = tuple(
    step
    for step in result.steps
    if step.conclusion == expected_membership
  )

  assert len(matching_memberships) == 1

  membership_step = matching_memberships[0]

  assert membership_step.rule == (
    ProofRule.INFERENCE
  )

  assert membership_step.inference_rule == (
    membership_rule
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase27_7_end_to_end_membership_preserves_full_provenance_chain():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  second_zero_step = relation_proof_step(
    NU_PRIME_NU_6_ZERO_COMPOSITION_FACT
  )

  suspension_step = relation_proof_step(
    E_NU_6_EQUALS_NU_7_FACT
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  theorem_step = entry.to_proof_step()

  definedness_rule = (
    indexed_toda_bracket_index1_defined_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      definedness_rule,
      membership_rule,
    ),
    (
      first_zero_step,
      second_zero_step,
      suspension_step,
      theorem_step,
    ),
  )

  definedness = TodaBracketDefinedStatement(
    bracket=entry.statement.bracket,
  )

  membership = TodaBracketMembershipStatement(
    element=entry.statement.element,
    bracket=entry.statement.bracket,
    source=entry.reference,
    note=entry.statement.note,
  )

  defined_step = next(
    step
    for step in result.steps
    if step.conclusion == definedness
  )

  membership_step = next(
    step
    for step in result.steps
    if step.conclusion == membership
  )

  assert defined_step.rule == (
    ProofRule.INFERENCE
  )

  assert defined_step.inference_rule == (
    definedness_rule
  )

  assert defined_step.premises == (
    first_zero_step,
    second_zero_step,
    suspension_step,
  )

  assert membership_step.rule == (
    ProofRule.INFERENCE
  )

  assert membership_step.inference_rule == (
    membership_rule
  )

  assert membership_step.premises == (
    theorem_step,
    defined_step,
  )

  assert theorem_step.rule == (
    ProofRule.GIVEN
  )

  assert theorem_step.premises == ()

  assert theorem_step.conclusion.source == (
    entry.reference
  )

  assert (
    membership_step
    .premises[1]
    .premises
    == (
      first_zero_step,
      second_zero_step,
      suspension_step,
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase27_7_end_to_end_requires_correct_second_base_zero_condition():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  displayed_adjacent_zero_step = (
    relation_proof_step(
      Relation(
        lhs=Composition(
          left=Suspension(
            expression=HomotopyElement(
              name="ν′",
              dimension=3,
              generator=NU_PRIME_GENERATOR,
            ),
          ),
          right=HomotopyElement(
            name="ν₇",
            dimension=7,
            generator=NU_7_GENERATOR,
          ),
        ),
        rhs=Zero(),
        relation_type=RelationType.ZERO,
      )
    )
  )

  suspension_step = relation_proof_step(
    E_NU_6_EQUALS_NU_7_FACT
  )

  entry = THEOREM_FACT_REPOSITORY.lookup(
    EPSILON_3_TODA_MEMBERSHIP_FACT.statement
  )

  assert entry is not None

  theorem_step = entry.to_proof_step()

  definedness_rule = (
    indexed_toda_bracket_index1_defined_inference_rule()
  )

  membership_rule = (
    toda_bracket_membership_from_theorem_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      definedness_rule,
      membership_rule,
    ),
    (
      first_zero_step,
      displayed_adjacent_zero_step,
      suspension_step,
      theorem_step,
    ),
  )

  expected_definedness = (
    TodaBracketDefinedStatement(
      bracket=entry.statement.bracket,
    )
  )

  expected_membership = (
    TodaBracketMembershipStatement(
      element=entry.statement.element,
      bracket=entry.statement.bracket,
      source=entry.reference,
      note=entry.statement.note,
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected_definedness not in conclusions
  assert expected_membership not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )






