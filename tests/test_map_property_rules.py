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
  derive_inference_round_result,
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


def test_phase28_6_isomorphism_and_mapped_equality_run_end_to_end():
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

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
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

  isomorphism_rule = (
    isomorphism_implies_injective_inference_rule()
  )

  reflection_rule = (
    injective_map_reflects_equality_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      isomorphism_rule,
      reflection_rule,
    ),
    (
      isomorphism_step,
      mapped_equality_step,
    ),
  )

  expected_injectivity = InjectiveMapStatement(
    map=f,
  )

  expected_equality = Relation(
    lhs=a,
    rhs=b,
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected_injectivity in conclusions
  assert expected_equality in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase28_6_end_to_end_equality_preserves_full_provenance_chain():
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

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
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

  isomorphism_rule = (
    isomorphism_implies_injective_inference_rule()
  )

  reflection_rule = (
    injective_map_reflects_equality_inference_rule()
  )

  result = run_inference_until_stable_with_history(
    (
      isomorphism_rule,
      reflection_rule,
    ),
    (
      isomorphism_step,
      mapped_equality_step,
    ),
  )

  injective_step = next(
    step
    for step in result.steps
    if step.conclusion == InjectiveMapStatement(
      map=f,
    )
  )

  equality_step = next(
    step
    for step in result.steps
    if step.conclusion == Relation(
      lhs=a,
      rhs=b,
      relation_type=RelationType.EQUALITY,
    )
  )

  assert injective_step.rule == (
    ProofRule.INFERENCE
  )

  assert injective_step.inference_rule == (
    isomorphism_rule
  )

  assert injective_step.premises == (
    isomorphism_step,
  )

  assert equality_step.rule == (
    ProofRule.INFERENCE
  )

  assert equality_step.inference_rule == (
    reflection_rule
  )

  assert equality_step.premises == (
    injective_step,
    mapped_equality_step,
  )

  assert (
    equality_step
    .premises[0]
    .premises
    == (
      isomorphism_step,
    )
  )

  assert isomorphism_step.rule == (
    ProofRule.GIVEN
  )

  assert mapped_equality_step.rule == (
    ProofRule.GIVEN
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase28_7_injective_f_does_not_reflect_equality_under_g():
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
        map=g,
        expression=a,
      ),
      rhs=MapApplication(
        map=g,
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

  assert match is None


def test_phase28_7_mismatched_maps_on_equality_sides_do_not_reflect():
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

  injective_step = ProofStep(
    conclusion=InjectiveMapStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  mismatched_equality_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=f,
        expression=a,
      ),
      rhs=MapApplication(
        map=g,
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
      mismatched_equality_step,
    ),
  )

  assert match is None


def test_phase28_7_isomorphism_f_does_not_reflect_equality_under_g_end_to_end():
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

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
      map=f,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  mapped_equality_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=g,
        expression=a,
      ),
      rhs=MapApplication(
        map=g,
        expression=b,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rules = (
    isomorphism_implies_injective_inference_rule(),
    injective_map_reflects_equality_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      isomorphism_step,
      mapped_equality_step,
    ),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert InjectiveMapStatement(
    map=f,
  ) in conclusions

  assert Relation(
    lhs=a,
    rhs=b,
    relation_type=RelationType.EQUALITY,
  ) not in conclusions

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )


def test_phase28_7_plain_equality_is_not_treated_as_mapped_equality():
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

  plain_equality_step = ProofStep(
    conclusion=Relation(
      lhs=a,
      rhs=b,
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
      plain_equality_step,
    ),
  )

  assert match is None


def test_phase28_9_end_to_end_provenance_excludes_unrelated_fact():
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

  x = HomotopyElement(
    name="x",
    dimension=1,
  )

  y = HomotopyElement(
    name="y",
    dimension=1,
  )

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
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

  unrelated_step = ProofStep(
    conclusion=Relation(
      lhs=x,
      rhs=y,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rules = (
    isomorphism_implies_injective_inference_rule(),
    injective_map_reflects_equality_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      isomorphism_step,
      mapped_equality_step,
      unrelated_step,
    ),
  )

  injective_step = next(
    step
    for step in result.steps
    if step.conclusion == InjectiveMapStatement(
      map=f,
    )
  )

  equality_step = next(
    step
    for step in result.steps
    if step.conclusion == Relation(
      lhs=a,
      rhs=b,
      relation_type=RelationType.EQUALITY,
    )
  )

  assert injective_step.premises == (
    isomorphism_step,
  )

  assert equality_step.premises == (
    injective_step,
    mapped_equality_step,
  )

  assert unrelated_step not in (
    injective_step.premises
  )

  assert unrelated_step not in (
    equality_step.premises
  )

  assert all(
    unrelated_step not in premise.premises
    for premise in equality_step.premises
  )


def test_phase28_9_end_to_end_has_unique_derived_conclusions():
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

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
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

  rules = (
    isomorphism_implies_injective_inference_rule(),
    injective_map_reflects_equality_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      isomorphism_step,
      mapped_equality_step,
    ),
  )

  injectivity = InjectiveMapStatement(
    map=f,
  )

  equality = Relation(
    lhs=a,
    rhs=b,
    relation_type=RelationType.EQUALITY,
  )

  injective_steps = tuple(
    step
    for step in result.steps
    if step.conclusion == injectivity
  )

  equality_steps = tuple(
    step
    for step in result.steps
    if step.conclusion == equality
  )

  assert len(injective_steps) == 1
  assert len(equality_steps) == 1

  assert injective_steps[0].rule == (
    ProofRule.INFERENCE
  )

  assert equality_steps[0].rule == (
    ProofRule.INFERENCE
  )


def test_phase28_9_end_to_end_reaches_genuine_fixed_point():
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

  isomorphism_step = ProofStep(
    conclusion=IsomorphismStatement(
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

  rules = (
    isomorphism_implies_injective_inference_rule(),
    injective_map_reflects_equality_inference_rule(),
  )

  result = run_inference_until_stable_with_history(
    rules,
    (
      isomorphism_step,
      mapped_equality_step,
    ),
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  terminal_round = derive_inference_round_result(
    rules,
    result.steps,
  )

  assert terminal_round.new_steps == ()





