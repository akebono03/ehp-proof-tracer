from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_6_EQUALS_NU_7_FACT,
  NU_PRIME_NU_6_ZERO_COMPOSITION_FACT,
)
from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  TodaBracket,
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
from toda_rules import (
  TodaBracketDefinedStatement,
  indexed_toda_bracket_index1_defined_inference_rule,
)


def test_phase27_5_actual_base_zero_conditions_derive_index1_toda_definedness():
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

  expected = TodaBracketDefinedStatement(
    bracket=TodaBracket(
      first=(
        ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
        .lhs
        .left
      ),
      second=(
        ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
        .lhs
        .right
      ),
      third=E_NU_6_EQUALS_NU_7_FACT.rhs,
      index=1,
    ),
  )

  assert expected in tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase27_5_index1_definedness_preserves_actual_base_condition_provenance():
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

  defined_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaBracketDefinedStatement,
    )
  )

  assert defined_step.rule == (
    ProofRule.INFERENCE
  )

  assert defined_step.inference_rule == (
    rule
  )

  assert defined_step.premises == (
    first_zero_step,
    second_zero_step,
    suspension_step,
  )


def test_phase27_5_index1_definedness_requires_second_base_zero_condition():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
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
      suspension_step,
    ),
  )

  assert not any(
    isinstance(
      step.conclusion,
      TodaBracketDefinedStatement,
    )
    for step in result.steps
  )


def test_phase27_5_displayed_adjacent_zero_is_not_index1_defining_condition():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  displayed_adjacent_zero = relation_proof_step(
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
      displayed_adjacent_zero,
      suspension_step,
    ),
  )

  assert not any(
    isinstance(
      step.conclusion,
      TodaBracketDefinedStatement,
    )
    for step in result.steps
  )
