from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  WhiteheadProduct,
  Zero,
)
from homotopy_groups import (
  DirectSumGroup,
  FreeCyclicGroup,
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
  toda_lemma41_even_nonzero_case_inference_rule,
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


def test_phase44_3_generator_symbol_accepts_symbolic_index():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  generator = GeneratorSymbol(
    family="ι",
    index=n_minus_one,
  )

  assert generator.index == (
    n_minus_one
  )


def test_phase44_3_homotopy_element_accepts_symbolic_dimension():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  element = HomotopyElement(
    name="ι_(n-1)",
    dimension=n_minus_one,
    generator=GeneratorSymbol(
      family="ι",
      index=n_minus_one,
    ),
  )

  assert element.dimension == (
    n_minus_one
  )

  assert element.generator == (
    GeneratorSymbol(
      family="ι",
      index=n_minus_one,
    )
  )


def test_phase44_3_symbolic_whitehead_product_is_lossless():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  iota_n_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )
  )

  product = WhiteheadProduct(
    left=iota_n_minus_one,
    right=iota_n_minus_one,
  )

  assert product.left == (
    iota_n_minus_one
  )

  assert product.right == (
    iota_n_minus_one
  )


def test_phase44_3_symbolic_whitehead_zero_premise_is_representable():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  iota_n_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )
  )

  product = WhiteheadProduct(
    left=iota_n_minus_one,
    right=iota_n_minus_one,
  )

  premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert premise.lhs == product
  assert premise.rhs == Zero()

  assert (
    premise.relation_type
    == RelationType.ZERO
  )


def test_phase44_3_symbolic_whitehead_nonzero_premise_is_representable():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  iota_n_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )
  )

  product = WhiteheadProduct(
    left=iota_n_minus_one,
    right=iota_n_minus_one,
  )

  premise = Relation(
    lhs=product,
    rhs=Zero(),
    relation_type=(
      RelationType.INEQUALITY
    ),
  )

  assert premise.lhs == product
  assert premise.rhs == Zero()

  assert (
    premise.relation_type
    == RelationType.INEQUALITY
  )


def test_phase44_3_free_cyclic_group_preserves_generator_expression():
  n = ScalarSymbol(
    name="n",
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  iota_two_n_plus_one = (
    HomotopyElement(
      name="ι_(2n+1)",
      dimension=two_n_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=two_n_plus_one,
      ),
    )
  )

  p_iota = MapApplication(
    map=MapSymbol(
      name="P",
    ),
    expression=iota_two_n_plus_one,
  )

  group = FreeCyclicGroup(
    generator=p_iota,
  )

  assert group.generator == p_iota


def test_phase44_3_free_cyclic_group_preserves_alpha_generator():
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

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  group = FreeCyclicGroup(
    generator=alpha,
  )

  assert group.generator == alpha


def test_phase44_3_nonzero_case_direct_sum_is_lossless():
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

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  iota_two_n_plus_one = (
    HomotopyElement(
      name="ι_(2n+1)",
      dimension=two_n_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=two_n_plus_one,
      ),
    )
  )

  free_part = FreeCyclicGroup(
    generator=MapApplication(
      map=MapSymbol(
        name="P",
      ),
      expression=iota_two_n_plus_one,
    ),
  )

  primary_part = PrimaryComponent(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  group = DirectSumGroup(
    summands=(
      free_part,
      primary_part,
    ),
  )

  assert group.summands == (
    free_part,
    primary_part,
  )


def test_phase44_3_zero_case_direct_sum_is_lossless():
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

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  free_part = FreeCyclicGroup(
    generator=alpha,
  )

  primary_part = PrimaryComponent(
    group_dimension=two_n_minus_one,
    sphere_dimension=n,
    prime=2,
  )

  group = DirectSumGroup(
    summands=(
      free_part,
      primary_part,
    ),
  )

  assert group.summands == (
    free_part,
    primary_part,
  )


def test_phase44_3_direct_sum_is_not_concrete_abelian_group():
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

  group = DirectSumGroup(
    summands=(
      FreeCyclicGroup(
        generator=HomotopyElement(
          name="α",
          dimension=two_n_minus_one,
        ),
      ),
      PrimaryComponent(
        group_dimension=two_n_minus_one,
        sphere_dimension=n,
        prime=2,
      ),
    ),
  )

  assert not isinstance(
    group,
    AbelianGroup,
  )


def test_phase44_3_free_cyclic_group_is_not_group_component():
  alpha = HomotopyElement(
    name="α",
    dimension=9,
  )

  group = FreeCyclicGroup(
    generator=alpha,
  )

  assert not isinstance(
    group,
    GroupComponent,
  )


def test_phase44_3_group_representation_has_no_theorem_semantics():
  alpha = HomotopyElement(
    name="α",
    dimension=9,
  )

  free_group = FreeCyclicGroup(
    generator=alpha,
  )

  direct_sum = DirectSumGroup(
    summands=(
      free_group,
      PrimaryComponent(
        group_dimension=9,
        sphere_dimension=5,
        prime=2,
      ),
    ),
  )

  for value in (
    free_group,
    direct_sum,
  ):
    assert not hasattr(
      value,
      "theorem",
    )

    assert not hasattr(
      value,
      "source",
    )

    assert not hasattr(
      value,
      "provenance",
    )

    assert not hasattr(
      value,
      "case",
    )


def test_phase44_3_group_representation_does_not_evaluate_toda_lemma():
  n = ScalarSymbol(
    name="n",
  )

  even_statement = (
    EvenScalarStatement(
      scalar=n,
    )
  )

  assert not hasattr(
    even_statement,
    "result_group",
  )

  assert not hasattr(
    even_statement,
    "direct_sum",
  )


def build_phase44_4_even_nonzero_premises(
  n,
):
  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  iota_n_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nonzero_step = ProofStep(
    conclusion=Relation(
      lhs=WhiteheadProduct(
        left=iota_n_minus_one,
        right=iota_n_minus_one,
      ),
      rhs=Zero(),
      relation_type=(
        RelationType.INEQUALITY
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  return (
    even_step,
    nonzero_step,
  )


def test_phase44_4_rule_has_even_and_nonzero_premises():
  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 2

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is EvenScalarStatement
  )

  assert (
    rule.premise_patterns[
      1
    ].statement_type
    is Relation
  )

  assert (
    rule.premise_patterns[
      1
    ].relation_type
    == RelationType.INEQUALITY
  )


def test_phase44_4_matching_even_and_whitehead_nonzero_are_applicable():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      nonzero_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    even_step,
    nonzero_step,
  )


def test_phase44_4_derives_even_nonzero_group_structure():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        nonzero_step,
      ),
    )
  )

  two_n_minus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  two_n_plus_one = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=1,
  )

  iota_two_n_plus_one = (
    HomotopyElement(
      name="ι_(2n+1)",
      dimension=two_n_plus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=two_n_plus_one,
      ),
    )
  )

  expected = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    ),
    rhs=DirectSumGroup(
      summands=(
        FreeCyclicGroup(
          generator=MapApplication(
            map=MapSymbol(
              name="P",
            ),
            expression=(
              iota_two_n_plus_one
            ),
          ),
        ),
        PrimaryComponent(
          group_dimension=two_n_minus_one,
          sphere_dimension=n,
          prime=2,
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase44_4_derived_direct_sum_preserves_free_generator_structure():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        nonzero_step,
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
      step.conclusion.rhs,
      DirectSumGroup,
    )
  )

  direct_sum = (
    derived_step.conclusion.rhs
  )

  free_part = direct_sum.summands[
    0
  ]

  assert isinstance(
    free_part,
    FreeCyclicGroup,
  )

  assert isinstance(
    free_part.generator,
    MapApplication,
  )

  assert (
    free_part.generator.map
    == MapSymbol(
      name="P",
    )
  )


def test_phase44_4_derived_direct_sum_preserves_primary_component():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        nonzero_step,
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
      step.conclusion.rhs,
      DirectSumGroup,
    )
  )

  direct_sum = (
    derived_step.conclusion.rhs
  )

  primary_part = (
    direct_sum.summands[
      1
    ]
  )

  expected_degree = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  assert primary_part == (
    PrimaryComponent(
      group_dimension=expected_degree,
      sphere_dimension=n,
      prime=2,
    )
  )


def test_phase44_4_derived_step_keeps_both_premises():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        nonzero_step,
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
      step.conclusion.rhs,
      DirectSumGroup,
    )
  )

  assert derived_step.premises == (
    even_step,
    nonzero_step,
  )

  assert (
    derived_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    derived_step.inference_rule
    == rule
  )


def test_phase44_4_nonzero_premise_without_even_statement_is_not_applicable():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      nonzero_step,
    ),
  )

  assert match is None


def test_phase44_4_even_statement_without_nonzero_premise_is_not_applicable():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is None


def test_phase44_4_zero_relation_does_not_match_nonzero_case():
  n = ScalarSymbol(
    name="n",
  )

  n_minus_one = ScalarSum(
    left=n,
    right=-1,
  )

  iota_n_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=n_minus_one,
      ),
    )
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=WhiteheadProduct(
        left=iota_n_minus_one,
        right=iota_n_minus_one,
      ),
      rhs=Zero(),
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      zero_step,
    ),
  )

  assert match is None


def test_phase44_4_different_symbolic_index_is_not_applicable():
  n = ScalarSymbol(
    name="n",
  )

  m = ScalarSymbol(
    name="m",
  )

  m_minus_one = ScalarSum(
    left=m,
    right=-1,
  )

  iota_m_minus_one = (
    HomotopyElement(
      name="ι_(n-1)",
      dimension=m_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=m_minus_one,
      ),
    )
  )

  even_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  nonzero_step = ProofStep(
    conclusion=Relation(
      lhs=WhiteheadProduct(
        left=iota_m_minus_one,
        right=iota_m_minus_one,
      ),
      rhs=Zero(),
      relation_type=(
        RelationType.INEQUALITY
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      nonzero_step,
    ),
  )

  assert match is None


def test_phase44_4_arbitrary_inequality_does_not_match():
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

  inequality_step = ProofStep(
    conclusion=Relation(
      lhs=HomotopyElement(
        name="α",
        dimension=n,
      ),
      rhs=Zero(),
      relation_type=(
        RelationType.INEQUALITY
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      inequality_step,
    ),
  )

  assert match is None


def test_phase44_4_odd_statement_does_not_replace_even_premise():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    nonzero_step,
  ) = (
    build_phase44_4_even_nonzero_premises(
      n
    )
  )

  odd_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=n,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    toda_lemma41_even_nonzero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
      nonzero_step,
    ),
  )

  assert match is None





