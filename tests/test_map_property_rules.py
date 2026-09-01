from expression import (
  HomotopyElement,
  MapApplication,
  MapSymbol,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  injective_map_reflects_equality_inference_rule,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
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


def test_phase28_4_map_application_represents_f_of_a():
  f = MapSymbol(
    name="f",
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  application = MapApplication(
    map=f,
    expression=a,
  )

  assert application.map == f
  assert application.expression == a


def test_phase28_4_map_application_equality_represents_f_a_equals_f_b():
  f = MapSymbol(
    name="f",
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  relation = Relation(
    lhs=MapApplication(
      map=f,
      expression=a,
    ),
    rhs=MapApplication(
      map=f,
      expression=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    relation.lhs,
    MapApplication,
  )

  assert isinstance(
    relation.rhs,
    MapApplication,
  )

  assert relation.lhs.map == f
  assert relation.rhs.map == f

  assert relation.lhs.expression == a
  assert relation.rhs.expression == b

  assert relation.relation_type == (
    RelationType.EQUALITY
  )


def test_phase28_4_map_application_equality_preserves_same_map_structure():
  f = MapSymbol(
    name="f",
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  relation = Relation(
    lhs=MapApplication(
      map=f,
      expression=a,
    ),
    rhs=MapApplication(
      map=f,
      expression=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert relation.lhs.map == (
    relation.rhs.map
  )


def test_phase28_4_map_application_equality_distinguishes_mismatched_maps():
  f = MapSymbol(
    name="f",
  )

  g = MapSymbol(
    name="g",
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  same_map_relation = Relation(
    lhs=MapApplication(
      map=f,
      expression=a,
    ),
    rhs=MapApplication(
      map=f,
      expression=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  mismatched_map_relation = Relation(
    lhs=MapApplication(
      map=f,
      expression=a,
    ),
    rhs=MapApplication(
      map=g,
      expression=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    same_map_relation
    != mismatched_map_relation
  )

  assert (
    mismatched_map_relation.lhs.map
    != mismatched_map_relation.rhs.map
  )


def test_phase28_5_injective_map_reflects_map_application_equality():
  f = MapSymbol(
    name="f",
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  injective_step = ProofStep(
    conclusion=InjectiveMapStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  mapped_equality_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=f,
        expression=a,
      ),
      rhs=MapApplication(
        map=f,
        expression=b,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    injective_map_reflects_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      injective_step,
      mapped_equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == Relation(
    lhs=a,
    rhs=b,
    relation_type=RelationType.EQUALITY,
  )





