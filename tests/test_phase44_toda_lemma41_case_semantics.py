from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  PrimaryComponent,
  TodaPrimaryGroup,
)
from models import (
  AbelianGroup,
  GroupComponent,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
)
from toda_rules import (
  toda_lemma41_odd_case_inference_rule,
)


def build_phase44_1_symbolic_critical_degree():
  n = ScalarSymbol(
    name="n",
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  return (
    n,
    two_n_minus_one,
  )


def test_phase44_1_current_parity_represents_symbolic_n():
  n = ScalarSymbol(
    name="n",
  )

  odd_statement = OddScalarStatement(
    scalar=n,
  )

  even_statement = EvenScalarStatement(
    scalar=n,
  )

  assert odd_statement.scalar == n
  assert even_statement.scalar == n


def test_phase44_1_symbolic_critical_degree_is_representable():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  assert two_n_minus_one == ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )


def test_phase44_1_toda_group_represents_symbolic_critical_degree():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  group = TodaPrimaryGroup(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
  )

  assert group.group_dimension == (
    two_n_minus_one
  )

  assert group.sphere_dimension == n


def test_phase44_1_primary_component_represents_symbolic_critical_degree():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  component = PrimaryComponent(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  assert component.group_dimension == (
    two_n_minus_one
  )

  assert component.sphere_dimension == n
  assert component.prime == 2


def test_phase44_1_odd_case_group_conclusion_is_representable_as_relation():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  conclusion = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    ),
    rhs=PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert conclusion.lhs == (
    TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    )
  )

  assert conclusion.rhs == (
    PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    )
  )

  assert (
    conclusion.relation_type
    == RelationType.EQUALITY
  )


def test_phase44_1_homotopy_element_dimension_remains_concrete_integer():
  type_hints = get_type_hints(
    HomotopyElement
  )

  assert type_hints[
    "dimension"
  ] is int


def test_phase44_1_generator_symbol_index_remains_concrete_integer_or_none():
  type_hints = get_type_hints(
    GeneratorSymbol
  )

  assert type_hints[
    "index"
  ] == (
    int | None
  )


def test_phase44_1_general_symbolic_whitehead_identity_is_not_yet_lossless():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  homotopy_element_hints = (
    get_type_hints(
      HomotopyElement
    )
  )

  generator_symbol_hints = (
    get_type_hints(
      GeneratorSymbol
    )
  )

  assert (
    homotopy_element_hints[
      "dimension"
    ]
    is int
  )

  assert (
    generator_symbol_hints[
      "index"
    ]
    == (
      int | None
    )
  )

  assert not isinstance(
    n_minus_one,
    int,
  )


def test_phase44_1_abelian_group_components_use_string_generator_labels():
  type_hints = get_type_hints(
    GroupComponent
  )

  assert type_hints[
    "generator"
  ] is str


def test_phase44_1_abelian_group_uses_concrete_integer_dimensions():
  type_hints = get_type_hints(
    AbelianGroup
  )

  assert type_hints[
    "n"
  ] is int

  assert type_hints[
    "k"
  ] is int


def test_phase44_1_abelian_group_component_cannot_preserve_primary_component_as_summand():
  n, two_n_minus_one = (
    build_phase44_1_symbolic_critical_degree()
  )

  primary_component = PrimaryComponent(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  component_hints = get_type_hints(
    GroupComponent
  )

  assert component_hints[
    "generator"
  ] is str

  assert not isinstance(
    primary_component,
    str,
  )


def test_phase44_1_current_group_layer_has_no_structural_direct_sum_term():
  group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  component = PrimaryComponent(
    group_dimension=9,
    sphere_dimension=5,
    prime=2,
  )

  for value in (
    group,
    component,
  ):
    assert not hasattr(
      value,
      "left_summand",
    )

    assert not hasattr(
      value,
      "right_summand",
    )

    assert not hasattr(
      value,
      "summands",
    )


def test_phase44_1_has_no_toda_lemma_4_1_case_semantics_yet():
  n = ScalarSymbol(
    name="n",
  )

  statements = (
    OddScalarStatement(
      scalar=n,
    ),
    EvenScalarStatement(
      scalar=n,
    ),
    TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=ScalarProduct(
          left=2,
          right=n,
        ),
        right=-1,
      ),
      sphere_dimension=n,
    ),
  )

  for statement in statements:
    assert not hasattr(
      statement,
      "toda_lemma_4_1",
    )

    assert not hasattr(
      statement,
      "case",
    )

    assert not hasattr(
      statement,
      "result_group",
    )


def test_phase44_2_odd_case_rule_has_only_odd_scalar_premise():
  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 1

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is OddScalarStatement
  )


def test_phase44_2_odd_symbolic_n_matches_rule():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    odd_step,
  )


def test_phase44_2_odd_case_derives_toda_primary_group_equality():
  n = ScalarSymbol(
    name="n",
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        odd_step,
      ),
    )
  )

  expected = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    ),
    rhs=PrimaryComponent(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
      prime=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase44_2_derived_relation_preserves_symbolic_n_structure():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        odd_step,
      ),
    )
  )

  derived_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Relation,
    )
    and isinstance(
      step.conclusion.lhs,
      TodaPrimaryGroup,
    )
  )

  relation = derived_step.conclusion

  expected_degree = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  assert (
    relation.lhs.group_dimension
    == expected_degree
  )

  assert (
    relation.lhs.sphere_dimension
    == n
  )

  assert (
    relation.rhs.group_dimension
    == expected_degree
  )

  assert (
    relation.rhs.sphere_dimension
    == n
  )

  assert relation.rhs.prime == 2


def test_phase44_2_derived_step_keeps_odd_premise_provenance():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        odd_step,
      ),
    )
  )

  derived_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Relation,
    )
    and isinstance(
      step.conclusion.lhs,
      TodaPrimaryGroup,
    )
  )

  assert (
    derived_step.rule
    == ProofRule.INFERENCE
  )

  assert derived_step.premises == (
    odd_step,
  )

  assert (
    derived_step.inference_rule
    == rule
  )


def test_phase44_2_even_statement_does_not_match_odd_case_rule():
  n = ScalarSymbol(
    name="n",
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is None

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
      ),
    )
  )

  derived_relations = tuple(
    step.conclusion
    for step in result.steps
    if isinstance(
      step.conclusion,
      Relation,
    )
  )

  assert derived_relations == ()

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase44_2_odd_case_does_not_require_whitehead_premise():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        odd_step,
      ),
    )
  )

  expected_degree = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  expected = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=expected_degree,
      sphere_dimension=n,
    ),
    rhs=PrimaryComponent(
      group_dimension=expected_degree,
      sphere_dimension=n,
      prime=2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase44_2_odd_case_does_not_create_direct_sum_semantics():
  n = ScalarSymbol(
    name="n",
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_odd_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        odd_step,
      ),
    )
  )

  derived_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Relation,
    )
    and isinstance(
      step.conclusion.lhs,
      TodaPrimaryGroup,
    )
  )

  relation = derived_step.conclusion

  assert not hasattr(
    relation.rhs,
    "summands",
  )

  assert not hasattr(
    relation.rhs,
    "left_summand",
  )

  assert not hasattr(
    relation.rhs,
    "right_summand",
  )




