from expression import (
  HomotopyElement,
  MapApplication,
  MapSymbol,
)
from map_facts import (
  HOPF_MAP,
  HOPF_MAP_ISOMORPHISM_FACT,
  HOPF_MAP_TYPING_FACT,
  MAP_ISOMORPHISM_FACT_REPOSITORY,
  MapIsomorphismFact,
  MapIsomorphismFactRepository,
  MapTypingFact,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  injective_map_reflects_equality_inference_rule,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  run_inference_until_stable_with_history,
)


def test_phase29_1_hopf_map_is_map_symbol():
  assert isinstance(
    HOPF_MAP,
    MapSymbol,
  )


def test_phase29_1_hopf_map_has_expected_name():
  assert HOPF_MAP.name == "H"


def test_phase29_1_hopf_map_matches_structural_h_identity():
  assert HOPF_MAP == MapSymbol(
    name="H",
  )


def test_phase29_1_hopf_map_does_not_equal_different_map():
  assert HOPF_MAP != MapSymbol(
    name="E",
  )


def test_phase29_2_map_typing_fact_preserves_map():
  h = MapSymbol(
    name="H",
  )

  fact = MapTypingFact(
    map=h,
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.map == h


def test_phase29_2_map_typing_fact_preserves_domain_dimensions():
  fact = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.source_group_dimension == 3
  assert fact.source_sphere_dimension == 2


def test_phase29_2_map_typing_fact_preserves_codomain_dimensions():
  fact = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.target_group_dimension == 3
  assert fact.target_sphere_dimension == 3


def test_phase29_2_map_typing_fact_has_structural_equality():
  left = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  right = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert left == right


def test_phase29_2_map_identity_is_part_of_typing_fact_identity():
  h_fact = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  f_fact = MapTypingFact(
    map=MapSymbol(
      name="f",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert h_fact != f_fact


def test_phase29_2_source_group_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=4,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert original != different


def test_phase29_2_source_sphere_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=3,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert original != different


def test_phase29_2_target_group_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=4,
    target_sphere_dimension=3,
  )

  assert original != different


def test_phase29_2_target_sphere_dimension_is_structural():
  original = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  different = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=4,
  )

  assert original != different


def test_phase29_2_map_symbol_does_not_contain_typing_implicitly():
  h = MapSymbol(
    name="H",
  )

  fact = MapTypingFact(
    map=h,
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert fact.map == h
  assert not hasattr(
    h,
    "source_group_dimension",
  )
  assert not hasattr(
    h,
    "source_sphere_dimension",
  )
  assert not hasattr(
    h,
    "target_group_dimension",
  )
  assert not hasattr(
    h,
    "target_sphere_dimension",
  )


def test_phase29_3_hopf_map_typing_fact_is_map_typing_fact():
  assert isinstance(
    HOPF_MAP_TYPING_FACT,
    MapTypingFact,
  )


def test_phase29_3_hopf_map_typing_fact_uses_production_hopf_map():
  assert HOPF_MAP_TYPING_FACT.map is (
    HOPF_MAP
  )


def test_phase29_3_hopf_map_typing_fact_has_expected_domain():
  assert (
    HOPF_MAP_TYPING_FACT
    .source_group_dimension
    == 3
  )

  assert (
    HOPF_MAP_TYPING_FACT
    .source_sphere_dimension
    == 2
  )


def test_phase29_3_hopf_map_typing_fact_has_expected_codomain():
  assert (
    HOPF_MAP_TYPING_FACT
    .target_group_dimension
    == 3
  )

  assert (
    HOPF_MAP_TYPING_FACT
    .target_sphere_dimension
    == 3
  )


def test_phase29_3_hopf_map_typing_fact_has_expected_structure():
  expected = MapTypingFact(
    map=HOPF_MAP,
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert HOPF_MAP_TYPING_FACT == (
    expected
  )


def test_phase29_3_hopf_map_typing_fact_does_not_change_map_symbol():
  assert HOPF_MAP == MapSymbol(
    name="H",
  )

  assert not hasattr(
    HOPF_MAP,
    "source_group_dimension",
  )

  assert not hasattr(
    HOPF_MAP,
    "source_sphere_dimension",
  )

  assert not hasattr(
    HOPF_MAP,
    "target_group_dimension",
  )

  assert not hasattr(
    HOPF_MAP,
    "target_sphere_dimension",
  )


def test_phase29_4_map_isomorphism_fact_preserves_typing():
  typing = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  fact = MapIsomorphismFact(
    typing=typing,
  )

  assert fact.typing == typing


def test_phase29_4_map_isomorphism_fact_has_structural_equality():
  typing = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  first = MapIsomorphismFact(
    typing=typing,
  )

  second = MapIsomorphismFact(
    typing=typing,
  )

  assert first == second


def test_phase29_4_map_isomorphism_fact_distinguishes_map():
  h_typing = MapTypingFact(
    map=MapSymbol(
      name="H",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  f_typing = MapTypingFact(
    map=MapSymbol(
      name="f",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert MapIsomorphismFact(
    typing=h_typing,
  ) != MapIsomorphismFact(
    typing=f_typing,
  )


def test_phase29_4_map_isomorphism_fact_distinguishes_domain_context():
  original = MapIsomorphismFact(
    typing=MapTypingFact(
      map=MapSymbol(
        name="H",
      ),
      source_group_dimension=3,
      source_sphere_dimension=2,
      target_group_dimension=3,
      target_sphere_dimension=3,
    ),
  )

  different = MapIsomorphismFact(
    typing=MapTypingFact(
      map=MapSymbol(
        name="H",
      ),
      source_group_dimension=4,
      source_sphere_dimension=2,
      target_group_dimension=3,
      target_sphere_dimension=3,
    ),
  )

  assert original != different


def test_phase29_4_map_isomorphism_fact_distinguishes_codomain_context():
  original = MapIsomorphismFact(
    typing=MapTypingFact(
      map=MapSymbol(
        name="H",
      ),
      source_group_dimension=3,
      source_sphere_dimension=2,
      target_group_dimension=3,
      target_sphere_dimension=3,
    ),
  )

  different = MapIsomorphismFact(
    typing=MapTypingFact(
      map=MapSymbol(
        name="H",
      ),
      source_group_dimension=3,
      source_sphere_dimension=2,
      target_group_dimension=3,
      target_sphere_dimension=4,
    ),
  )

  assert original != different


def test_phase29_4_map_isomorphism_fact_can_use_production_h_typing():
  fact = MapIsomorphismFact(
    typing=HOPF_MAP_TYPING_FACT,
  )

  assert fact.typing is (
    HOPF_MAP_TYPING_FACT
  )

  assert fact.typing.map is (
    HOPF_MAP
  )


def test_phase29_5_hopf_map_isomorphism_fact_uses_production_typing():
  assert (
    HOPF_MAP_ISOMORPHISM_FACT.typing
    is HOPF_MAP_TYPING_FACT
  )

  assert (
    HOPF_MAP_ISOMORPHISM_FACT
    .typing
    .map
    is HOPF_MAP
  )


def test_phase29_5_hopf_map_isomorphism_fact_has_expected_structure():
  expected = MapIsomorphismFact(
    typing=HOPF_MAP_TYPING_FACT,
  )

  assert (
    HOPF_MAP_ISOMORPHISM_FACT
    == expected
  )


def test_phase29_5_map_isomorphism_repository_is_empty_by_default():
  repository = (
    MapIsomorphismFactRepository()
  )

  assert repository.facts == ()


def test_phase29_5_production_repository_preserves_actual_hopf_isomorphism_fact():
  assert (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .facts
    == (
      HOPF_MAP_ISOMORPHISM_FACT,
    )
  )


def test_phase29_5_repository_lookup_returns_actual_hopf_isomorphism_fact():
  result = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  assert result is (
    HOPF_MAP_ISOMORPHISM_FACT
  )


def test_phase29_5_repository_lookup_returns_none_for_unknown_typing():
  unknown_typing = MapTypingFact(
    map=HOPF_MAP,
    source_group_dimension=4,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      unknown_typing
    )
    is None
  )


def test_phase29_5_repository_lookup_distinguishes_map_identity():
  different_map_typing = MapTypingFact(
    map=MapSymbol(
      name="f",
    ),
    source_group_dimension=3,
    source_sphere_dimension=2,
    target_group_dimension=3,
    target_sphere_dimension=3,
  )

  assert (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      different_map_typing
    )
    is None
  )


def test_phase29_5_repository_rejects_duplicate_typing_context():
  try:
    MapIsomorphismFactRepository(
      facts=(
        HOPF_MAP_ISOMORPHISM_FACT,
        HOPF_MAP_ISOMORPHISM_FACT,
      ),
    )
  except ValueError as error:
    assert str(error) == (
      "duplicate map isomorphism fact"
    )
  else:
    raise AssertionError(
      "duplicate map isomorphism fact "
      "was not rejected"
    )


def test_phase29_5_repository_allows_same_map_in_different_typing_context():
  different_typing = MapTypingFact(
    map=HOPF_MAP,
    source_group_dimension=4,
    source_sphere_dimension=2,
    target_group_dimension=4,
    target_sphere_dimension=3,
  )

  different_fact = MapIsomorphismFact(
    typing=different_typing,
  )

  repository = (
    MapIsomorphismFactRepository(
      facts=(
        HOPF_MAP_ISOMORPHISM_FACT,
        different_fact,
      ),
    )
  )

  assert repository.facts == (
    HOPF_MAP_ISOMORPHISM_FACT,
    different_fact,
  )

  assert repository.lookup(
    HOPF_MAP_TYPING_FACT
  ) is HOPF_MAP_ISOMORPHISM_FACT

  assert repository.lookup(
    different_typing
  ) is different_fact


def test_phase29_6_map_isomorphism_fact_materializes_isomorphism_statement():
  step = (
    HOPF_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert step.conclusion == (
    IsomorphismStatement(
      map=HOPF_MAP,
    )
  )


def test_phase29_6_materialized_isomorphism_statement_preserves_actual_map():
  step = (
    HOPF_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert isinstance(
    step.conclusion,
    IsomorphismStatement,
  )

  assert step.conclusion.map is (
    HOPF_MAP
  )


def test_phase29_6_materialized_isomorphism_step_is_given():
  step = (
    HOPF_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert step.rule == (
    ProofRule.GIVEN
  )


def test_phase29_6_materialized_isomorphism_step_has_no_premises():
  step = (
    HOPF_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert step.premises == ()


def test_phase29_6_materialized_isomorphism_step_has_no_inference_rule():
  step = (
    HOPF_MAP_ISOMORPHISM_FACT
    .to_proof_step()
  )

  assert step.inference_rule is None


def test_phase29_6_repository_lookup_materializes_actual_hopf_isomorphism_step():
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  assert fact is (
    HOPF_MAP_ISOMORPHISM_FACT
  )

  step = fact.to_proof_step()

  assert step.conclusion == (
    IsomorphismStatement(
      map=HOPF_MAP,
    )
  )

  assert step.rule == (
    ProofRule.GIVEN
  )

  assert step.premises == ()


def test_phase29_7_actual_hopf_isomorphism_fact_derives_injectivity():
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  assert fact is (
    HOPF_MAP_ISOMORPHISM_FACT
  )

  isomorphism_step = (
    fact.to_proof_step()
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

  expected = InjectiveMapStatement(
    map=HOPF_MAP,
  )

  assert expected in tuple(
    step.conclusion
    for step in result.steps
  )


def test_phase29_7_actual_hopf_injectivity_preserves_isomorphism_provenance():
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  assert fact is not None

  isomorphism_step = (
    fact.to_proof_step()
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

  injective_step = next(
    step
    for step in result.steps
    if step.conclusion
    == InjectiveMapStatement(
      map=HOPF_MAP,
    )
  )

  assert isomorphism_step.conclusion == (
    IsomorphismStatement(
      map=HOPF_MAP,
    )
  )

  assert isomorphism_step.rule == (
    ProofRule.GIVEN
  )

  assert injective_step.rule == (
    ProofRule.INFERENCE
  )

  assert injective_step.inference_rule == (
    rule
  )

  assert injective_step.premises == (
    isomorphism_step,
  )


def test_phase29_8_actual_hopf_fact_and_mapped_equality_run_end_to_end():
  fact = (
    MAP_ISOMORPHISM_FACT_REPOSITORY
    .lookup(
      HOPF_MAP_TYPING_FACT
    )
  )

  assert fact is (
    HOPF_MAP_ISOMORPHISM_FACT
  )

  isomorphism_step = (
    fact.to_proof_step()
  )

  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  mapped_equality_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      rhs=MapApplication(
        map=HOPF_MAP,
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

  assert IsomorphismStatement(
    map=HOPF_MAP,
  ) in conclusions

  assert InjectiveMapStatement(
    map=HOPF_MAP,
  ) in conclusions

  assert Relation(
    lhs=a,
    rhs=b,
    relation_type=RelationType.EQUALITY,
  ) in conclusions





