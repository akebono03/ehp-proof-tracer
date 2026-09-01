from composition_facts import (
  ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT,
  E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT,
  ZERO_COMPOSITION_FACT_REPOSITORY,
)
from expression import (
  Composition,
  HomotopyElement,
  Suspension,
  TodaBracket,
)
from generator_facts import (
  ETA_3_GENERATOR,
  GENERATOR_FACT_REPOSITORY,
  NU_7_GENERATOR,
  NU_PRIME_GENERATOR,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaBracketDefinedStatement,
  toda_bracket_defined_by_zero_compositions_inference_rule,
)


def test_phase27_5_actual_typed_compositions_derive_indexed_toda_definedness():
  eta_3 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="η₃",
        dimension=3,
        generator=ETA_3_GENERATOR,
      )
    )
  )

  nu_prime = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν′",
        dimension=3,
        generator=NU_PRIME_GENERATOR,
      )
    )
  )

  nu_7 = (
    GENERATOR_FACT_REPOSITORY
    .materialize_typed_element(
      HomotopyElement(
        name="ν₇",
        dimension=7,
        generator=NU_7_GENERATOR,
      )
    )
  )

  assert eta_3 is not None
  assert nu_prime is not None
  assert nu_7 is not None

  e_nu_prime = Suspension(
    expression=nu_prime,
  )

  first_composition = Composition(
    left=eta_3,
    right=e_nu_prime,
  )

  second_composition = Composition(
    left=e_nu_prime,
    right=nu_7,
  )

  first_fact = (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      first_composition
    )
  )

  second_fact = (
    ZERO_COMPOSITION_FACT_REPOSITORY
    .lookup_by_untyped_structure(
      second_composition
    )
  )

  assert first_fact is (
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  assert second_fact is (
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
  )

  first_zero_step = relation_proof_step(
    first_fact
  )

  second_zero_step = relation_proof_step(
    second_fact
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule(
      index=1,
    )
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
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
      third=(
        E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
        .lhs
        .right
      ),
      index=1,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions

  assert expected.bracket.index == 1

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase27_5_indexed_definedness_preserves_zero_fact_provenance():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  second_zero_step = relation_proof_step(
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule(
      index=1,
    )
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
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
      third=(
        E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
        .lhs
        .right
      ),
      index=1,
    ),
  )

  defined_step = next(
    step
    for step in result.steps
    if step.conclusion == expected
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
  )


def test_phase27_5_actual_indexed_definedness_requires_both_zero_facts():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule(
      index=1,
    )
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
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
      third=(
        E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
        .lhs
        .right
      ),
      index=1,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase27_5_default_definedness_rule_remains_unindexed():
  first_zero_step = relation_proof_step(
    ETA_3_E_NU_PRIME_ZERO_COMPOSITION_FACT
  )

  second_zero_step = relation_proof_step(
    E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
  )

  rule = (
    toda_bracket_defined_by_zero_compositions_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    rule,
    (
      first_zero_step,
      second_zero_step,
    ),
  )

  unindexed = TodaBracketDefinedStatement(
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
      third=(
        E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
        .lhs
        .right
      ),
    ),
  )

  indexed = TodaBracketDefinedStatement(
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
      third=(
        E_NU_PRIME_NU_7_ZERO_COMPOSITION_FACT
        .lhs
        .right
      ),
      index=1,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert unindexed in conclusions
  assert indexed not in conclusions



