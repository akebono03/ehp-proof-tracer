from expression import (
  MapSymbol,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  apply_inference_match,
  find_inference_match,
  run_inference_until_stable_with_history,
)


def test_phase28_1_injective_map_statement_preserves_map():
  f = MapSymbol(
    name="f",
  )

  statement = InjectiveMapStatement(
    map=f,
  )

  assert statement.map == f


def test_phase28_1_injective_map_statement_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  first = InjectiveMapStatement(
    map=f,
  )

  second = InjectiveMapStatement(
    map=f,
  )

  assert first == second


def test_phase28_1_injective_map_statement_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_statement = InjectiveMapStatement(
    map=f,
  )

  g_statement = InjectiveMapStatement(
    map=g,
  )

  assert f_statement != g_statement


def test_phase28_1_map_symbol_does_not_imply_injectivity():
  f = MapSymbol(
    name="f",
  )

  statement = InjectiveMapStatement(
    map=f,
  )

  assert f != statement


def test_phase28_2_isomorphism_statement_preserves_map():
  f = MapSymbol(
    name="f",
  )

  statement = IsomorphismStatement(
    map=f,
  )

  assert statement.map == f


def test_phase28_2_isomorphism_statement_has_structural_equality():
  f = MapSymbol(
    name="f",
  )

  first = IsomorphismStatement(
    map=f,
  )

  second = IsomorphismStatement(
    map=f,
  )

  assert first == second


def test_phase28_2_isomorphism_statement_distinguishes_map():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  f_statement = IsomorphismStatement(
    map=f,
  )

  g_statement = IsomorphismStatement(
    map=g,
  )

  assert f_statement != g_statement


def test_phase28_2_isomorphism_and_injectivity_remain_distinct_statements():
  f = MapSymbol(
    name="f",
  )

  isomorphism = IsomorphismStatement(
    map=f,
  )

  injectivity = InjectiveMapStatement(
    map=f,
  )

  assert isomorphism != injectivity


def test_phase28_3_isomorphism_derives_injectivity():
  f = MapSymbol(
    name="f",
  )

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      isomorphism_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    InjectiveMapStatement(
      map=f,
    )
  )


def test_phase28_3_isomorphism_to_injectivity_preserves_provenance():
  f = MapSymbol(
    name="f",
  )

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      isomorphism_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == (
    rule
  )

  assert derived_step.premises == (
    isomorphism_step,
  )


def test_phase28_3_isomorphism_derives_injectivity_for_same_map_only():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        isomorphism_step,
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert InjectiveMapStatement(
    map=f,
  ) in conclusions

  assert InjectiveMapStatement(
    map=g,
  ) not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase28_3_injectivity_is_not_derived_without_isomorphism():
  f = MapSymbol(
    name="f",
  )

  unrelated_step = ProofStep(
    conclusion=InjectiveMapStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    isomorphism_implies_injective_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
    ),
  )

  assert match is None





