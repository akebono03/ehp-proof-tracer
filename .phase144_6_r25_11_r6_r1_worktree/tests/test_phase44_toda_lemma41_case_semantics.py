from typing import (
  get_type_hints,
)

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Suspension,
  WhiteheadProduct,
  Zero,
)
from map_facts import (
  EHP_H_MAP,
)
from homotopy_groups import (
  DirectSumGroup,
  FreeCyclicGroup,
  PrimaryComponent,
  PrimaryComponentMembershipStatement,
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
  find_applicable_inference_rules,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase44_capabilities import (
  build_phase44_representative_cases,
  primary_component_membership_text,
  relation_text,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
)
from toda_rules import (
  toda_lemma41_even_nonzero_case_inference_rule,
  toda_lemma41_even_zero_case_inference_rule,
  toda_lemma41_even_zero_h_alpha_inference_rule,
  toda_lemma41_even_zero_suspension_primary_inference_rule,
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


def build_phase44_5_even_zero_premises(
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

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=WhiteheadProduct(
        left=iota_n_minus_one,
        right=iota_n_minus_one,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  return (
    even_step,
    zero_step,
  )


def test_phase44_5_rule_has_even_and_zero_premises():
  rule = (
    toda_lemma41_even_zero_case_inference_rule()
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
    == RelationType.ZERO
  )


def test_phase44_5_matching_even_and_whitehead_zero_are_applicable():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      zero_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    even_step,
    zero_step,
  )


def test_phase44_5_derives_even_zero_group_structure():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        zero_step,
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

  expected = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=two_n_minus_one,
      sphere_dimension=n,
    ),
    rhs=DirectSumGroup(
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
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase44_5_derived_direct_sum_preserves_alpha_generator():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        zero_step,
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

  free_part = (
    direct_sum.summands[
      0
    ]
  )

  expected_degree = ScalarSum(
    left=ScalarProduct(
      left=2,
      right=n,
    ),
    right=-1,
  )

  assert isinstance(
    free_part,
    FreeCyclicGroup,
  )

  assert free_part.generator == (
    HomotopyElement(
      name="α",
      dimension=expected_degree,
    )
  )


def test_phase44_5_derived_direct_sum_preserves_primary_component():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        zero_step,
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

  primary_part = (
    derived_step.conclusion.rhs.summands[
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


def test_phase44_5_derived_step_keeps_both_premises():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        zero_step,
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
    zero_step,
  )

  assert (
    derived_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    derived_step.inference_rule
    == rule
  )


def test_phase44_5_zero_premise_without_even_statement_is_not_applicable():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is None


def test_phase44_5_even_statement_without_zero_premise_is_not_applicable():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
    ),
  )

  assert match is None


def test_phase44_5_nonzero_relation_does_not_match_zero_case():
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

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      nonzero_step,
    ),
  )

  assert match is None


def test_phase44_5_different_symbolic_index_is_not_applicable():
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

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=WhiteheadProduct(
        left=iota_m_minus_one,
        right=iota_m_minus_one,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      zero_step,
    ),
  )

  assert match is None


def test_phase44_5_arbitrary_zero_relation_does_not_match():
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

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=HomotopyElement(
        name="α",
        dimension=n,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      zero_step,
    ),
  )

  assert match is None


def test_phase44_5_odd_statement_does_not_replace_even_premise():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
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
    toda_lemma41_even_zero_case_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      odd_step,
      zero_step,
    ),
  )

  assert match is None


def test_phase44_6_representative_uses_all_three_case_rules():
  result = (
    build_phase44_representative_cases()
  )

  rule_names = tuple(
    rule.name
    for rule in result[
      "rules"
    ]
  )

  assert rule_names == (
    "Toda Lemma 4.1 odd case",
    (
      "Toda Lemma 4.1 even "
      "Whitehead nonzero case"
    ),
    (
      "Toda Lemma 4.1 even "
      "Whitehead zero case"
    ),
  )


def test_phase44_6_odd_case_has_exactly_one_applicable_rule():
  result = (
    build_phase44_representative_cases()
  )

  case = result[
    "cases"
  ][
    "odd"
  ]

  applicable = case[
    "applicable_rules"
  ]

  assert len(
    applicable
  ) == 1

  assert (
    applicable[
      0
    ].name
    == "Toda Lemma 4.1 odd case"
  )


def test_phase44_6_even_nonzero_has_exactly_one_applicable_rule():
  result = (
    build_phase44_representative_cases()
  )

  case = result[
    "cases"
  ][
    "even_nonzero"
  ]

  applicable = case[
    "applicable_rules"
  ]

  assert len(
    applicable
  ) == 1

  assert (
    applicable[
      0
    ].name
    == (
      "Toda Lemma 4.1 even "
      "Whitehead nonzero case"
    )
  )


def test_phase44_6_even_zero_has_exactly_one_applicable_rule():
  result = (
    build_phase44_representative_cases()
  )

  case = result[
    "cases"
  ][
    "even_zero"
  ]

  applicable = case[
    "applicable_rules"
  ]

  assert len(
    applicable
  ) == 1

  assert (
    applicable[
      0
    ].name
    == (
      "Toda Lemma 4.1 even "
      "Whitehead zero case"
    )
  )


def test_phase44_6_all_cases_preserve_exact_premise_provenance():
  result = (
    build_phase44_representative_cases()
  )

  cases = result[
    "cases"
  ]

  for name in (
    "odd",
    "even_nonzero",
    "even_zero",
  ):
    case = cases[
      name
    ]

    derived_step = case[
      "derived_step"
    ]

    assert (
      derived_step.rule
      == ProofRule.INFERENCE
    )

    assert (
      derived_step.premises
      == case[
        "premises"
      ]
    )

    assert (
      derived_step.inference_rule
      is case[
        "applicable_rules"
      ][
        0
      ]
    )


def test_phase44_6_all_cases_reach_fixed_point_after_one_derived_round():
  result = (
    build_phase44_representative_cases()
  )

  cases = result[
    "cases"
  ]

  for name in (
    "odd",
    "even_nonzero",
    "even_zero",
  ):
    inference_result = cases[
      name
    ][
      "result"
    ]

    assert (
      inference_result.termination_reason
      == InferenceTerminationReason.FIXED_POINT
    )

    assert (
      inference_result.round_count
      == 1
    )

    assert len(
      inference_result.round_results[
        0
      ].new_steps
    ) == 1


def test_phase44_6_three_case_conclusions_remain_structurally_distinct():
  result = (
    build_phase44_representative_cases()
  )

  cases = result[
    "cases"
  ]

  odd_conclusion = (
    cases[
      "odd"
    ][
      "derived_step"
    ].conclusion
  )

  nonzero_conclusion = (
    cases[
      "even_nonzero"
    ][
      "derived_step"
    ].conclusion
  )

  zero_conclusion = (
    cases[
      "even_zero"
    ][
      "derived_step"
    ].conclusion
  )

  assert (
    odd_conclusion
    != nonzero_conclusion
  )

  assert (
    odd_conclusion
    != zero_conclusion
  )

  assert (
    nonzero_conclusion
    != zero_conclusion
  )

  assert isinstance(
    odd_conclusion.rhs,
    PrimaryComponent,
  )

  assert isinstance(
    nonzero_conclusion.rhs,
    DirectSumGroup,
  )

  assert isinstance(
    zero_conclusion.rhs,
    DirectSumGroup,
  )


def test_phase44_6_representative_probe_displays_three_conclusions():
  result = (
    build_phase44_representative_cases()
  )

  cases = result[
    "cases"
  ]

  assert relation_text(
    cases[
      "odd"
    ][
      "derived_step"
    ].conclusion
  ) == (
    "π_{2n-1}^{n} = "
    "π_{2n-1}(S^{n};2)"
  )

  assert relation_text(
    cases[
      "even_nonzero"
    ][
      "derived_step"
    ].conclusion
  ) == (
    "π_{2n-1}^{n} = "
    "Z{P(ι_{2n+1})} ⊕ "
    "π_{2n-1}(S^{n};2)"
  )

  assert relation_text(
    cases[
      "even_zero"
    ][
      "derived_step"
    ].conclusion
  ) == (
    "π_{2n-1}^{n} = "
    "Z{α} ⊕ "
    "π_{2n-1}(S^{n};2)"
  )


def build_phase44_6a_alpha_condition_objects():
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

  two_n = ScalarProduct(
    left=2,
    right=n,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  iota_two_n_minus_one = (
    HomotopyElement(
      name="ι_(2n-1)",
      dimension=two_n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=two_n_minus_one,
      ),
    )
  )

  h_condition = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=alpha,
    ),
    rhs=iota_two_n_minus_one,
    relation_type=RelationType.EQUALITY,
  )

  suspended_alpha = Suspension(
    expression=alpha,
  )

  ordinary_membership = (
    HomotopyGroupMembershipStatement(
      element=suspended_alpha,
      group_dimension=two_n,
      sphere_dimension=n_plus_one,
    )
  )

  primary_component = PrimaryComponent(
    group_dimension=two_n,
    sphere_dimension=n_plus_one,
    prime=2,
  )

  return {
    "n": n,
    "alpha": alpha,
    "two_n_minus_one": two_n_minus_one,
    "two_n": two_n,
    "n_plus_one": n_plus_one,
    "iota_two_n_minus_one": (
      iota_two_n_minus_one
    ),
    "h_condition": h_condition,
    "suspended_alpha": suspended_alpha,
    "ordinary_membership": (
      ordinary_membership
    ),
    "primary_component": (
      primary_component
    ),
  }


def test_phase44_6a_h_alpha_condition_is_losslessly_representable():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  assert result[
    "h_condition"
  ] == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=result[
        "alpha"
      ],
    ),
    rhs=result[
      "iota_two_n_minus_one"
    ],
    relation_type=RelationType.EQUALITY,
  )


def test_phase44_6a_h_alpha_condition_uses_canonical_h():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  lhs = result[
    "h_condition"
  ].lhs

  assert isinstance(
    lhs,
    MapApplication,
  )

  assert lhs.map is EHP_H_MAP

  assert lhs.expression == (
    result[
      "alpha"
    ]
  )


def test_phase44_6a_iota_two_n_minus_one_preserves_symbolic_index():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  iota = result[
    "iota_two_n_minus_one"
  ]

  assert iota.generator == (
    GeneratorSymbol(
      family="ι",
      index=result[
        "two_n_minus_one"
      ],
    )
  )

  assert iota.dimension == (
    result[
      "two_n_minus_one"
    ]
  )


def test_phase44_6a_suspension_alpha_is_expression_compatible_with_membership():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = result[
    "ordinary_membership"
  ]

  assert membership.element == (
    Suspension(
      expression=result[
        "alpha"
      ],
    )
  )


def test_phase44_6a_e_alpha_ordinary_homotopy_membership_is_representable():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = result[
    "ordinary_membership"
  ]

  assert membership == (
    HomotopyGroupMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      group_dimension=result[
        "two_n"
      ],
      sphere_dimension=result[
        "n_plus_one"
      ],
    )
  )


def test_phase44_6a_e_alpha_membership_preserves_symbolic_dimensions():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = result[
    "ordinary_membership"
  ]

  assert membership.group_dimension == (
    ScalarProduct(
      left=2,
      right=result[
        "n"
      ],
    )
  )

  assert membership.sphere_dimension == (
    ScalarSum(
      left=result[
        "n"
      ],
      right=1,
    )
  )


def test_phase44_6a_target_primary_component_is_separately_representable():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  assert result[
    "primary_component"
  ] == PrimaryComponent(
    group_dimension=result[
      "two_n"
    ],
    sphere_dimension=result[
      "n_plus_one"
    ],
    prime=2,
  )


def test_phase44_6a_ordinary_membership_does_not_encode_primary_prime():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = result[
    "ordinary_membership"
  ]

  assert not hasattr(
    membership,
    "prime",
  )


def test_phase44_6a_primary_component_does_not_encode_membership_element():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  component = result[
    "primary_component"
  ]

  assert not hasattr(
    component,
    "element",
  )


def test_phase44_6b_e_alpha_primary_membership_is_lossless():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  assert membership.element == (
    Suspension(
      expression=result[
        "alpha"
      ],
    )
  )

  assert membership.component == (
    PrimaryComponent(
      group_dimension=result[
        "two_n"
      ],
      sphere_dimension=result[
        "n_plus_one"
      ],
      prime=2,
    )
  )


def test_phase44_6b_primary_membership_preserves_element():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  assert membership.element == (
    result[
      "suspended_alpha"
    ]
  )


def test_phase44_6b_primary_membership_preserves_prime():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  assert (
    membership.component.prime
    == 2
  )


def test_phase44_6b_primary_membership_preserves_symbolic_dimensions():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  assert (
    membership.component.group_dimension
    == ScalarProduct(
      left=2,
      right=result[
        "n"
      ],
    )
  )

  assert (
    membership.component.sphere_dimension
    == ScalarSum(
      left=result[
        "n"
      ],
      right=1,
    )
  )


def test_phase44_6b_primary_membership_is_distinct_from_ordinary_membership():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  primary_membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  ordinary_membership = (
    result[
      "ordinary_membership"
    ]
  )

  assert (
    primary_membership
    != ordinary_membership
  )

  assert not isinstance(
    primary_membership,
    HomotopyGroupMembershipStatement,
  )


def test_phase44_6b_primary_membership_is_distinct_from_primary_component():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  assert (
    membership
    != result[
      "primary_component"
    ]
  )

  assert not isinstance(
    membership,
    PrimaryComponent,
  )


def test_phase44_6b_primary_membership_distinguishes_prime():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  two_primary = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=PrimaryComponent(
        group_dimension=result[
          "two_n"
        ],
        sphere_dimension=result[
          "n_plus_one"
        ],
        prime=2,
      ),
    )
  )

  three_primary = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=PrimaryComponent(
        group_dimension=result[
          "two_n"
        ],
        sphere_dimension=result[
          "n_plus_one"
        ],
        prime=3,
      ),
    )
  )

  assert (
    two_primary
    != three_primary
  )


def test_phase44_6b_primary_membership_distinguishes_element():
  result = (
    build_phase44_6a_alpha_condition_objects()
  )

  alpha_membership = (
    PrimaryComponentMembershipStatement(
      element=result[
        "suspended_alpha"
      ],
      component=result[
        "primary_component"
      ],
    )
  )

  beta = HomotopyElement(
    name="β",
    dimension=result[
      "two_n_minus_one"
    ],
  )

  beta_membership = (
    PrimaryComponentMembershipStatement(
      element=Suspension(
        expression=beta,
      ),
      component=result[
        "primary_component"
      ],
    )
  )

  assert (
    alpha_membership
    != beta_membership
  )


def test_phase44_6c_h_alpha_rule_matches_even_zero_case():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_h_alpha_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      zero_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    even_step,
    zero_step,
  )


def test_phase44_6c_h_alpha_condition_is_theorem_derived():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_h_alpha_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        zero_step,
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

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  expected = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=alpha,
    ),
    rhs=HomotopyElement(
      name="ι_(2n-1)",
      dimension=two_n_minus_one,
      generator=GeneratorSymbol(
        family="ι",
        index=two_n_minus_one,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase44_6c_suspension_primary_rule_matches_even_zero_case():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_suspension_primary_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      even_step,
      zero_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    even_step,
    zero_step,
  )


def test_phase44_6c_suspension_primary_condition_is_theorem_derived():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rule = (
    toda_lemma41_even_zero_suspension_primary_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        even_step,
        zero_step,
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

  two_n = ScalarProduct(
    left=2,
    right=n,
  )

  n_plus_one = ScalarSum(
    left=n,
    right=1,
  )

  alpha = HomotopyElement(
    name="α",
    dimension=two_n_minus_one,
  )

  expected = (
    PrimaryComponentMembershipStatement(
      element=Suspension(
        expression=alpha,
      ),
      component=PrimaryComponent(
        group_dimension=two_n,
        sphere_dimension=n_plus_one,
        prime=2,
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase44_6c_zero_case_three_conclusions_share_same_alpha():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rules = (
    toda_lemma41_even_zero_case_inference_rule(),
    toda_lemma41_even_zero_h_alpha_inference_rule(),
    toda_lemma41_even_zero_suspension_primary_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        even_step,
        zero_step,
      ),
    )
  )

  group_step = next(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.rhs,
        DirectSumGroup,
      )
    )
  )

  h_step = next(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.lhs,
        MapApplication,
      )
      and step.conclusion.lhs.map
      is EHP_H_MAP
    )
  )

  membership_step = next(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
      and isinstance(
        step.conclusion,
        PrimaryComponentMembershipStatement,
      )
    )
  )

  group_alpha = (
    group_step
    .conclusion
    .rhs
    .summands[
      0
    ]
    .generator
  )

  h_alpha = (
    h_step
    .conclusion
    .lhs
    .expression
  )

  suspension_alpha = (
    membership_step
    .conclusion
    .element
    .expression
  )

  assert (
    group_alpha
    == h_alpha
  )

  assert (
    group_alpha
    == suspension_alpha
  )


def test_phase44_6c_zero_case_alpha_conditions_preserve_provenance():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rules = (
    toda_lemma41_even_zero_case_inference_rule(),
    toda_lemma41_even_zero_h_alpha_inference_rule(),
    toda_lemma41_even_zero_suspension_primary_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        even_step,
        zero_step,
      ),
    )
  )

  derived_steps = tuple(
    step
    for step in result.steps
    if (
      step.rule
      == ProofRule.INFERENCE
    )
  )

  assert len(
    derived_steps
  ) == 3

  for step in derived_steps:
    assert step.premises == (
      even_step,
      zero_step,
    )

    assert (
      step.inference_rule
      in rules
    )


def test_phase44_6c_zero_case_three_theorem_results_reach_fixed_point():
  n = ScalarSymbol(
    name="n",
  )

  (
    even_step,
    zero_step,
  ) = (
    build_phase44_5_even_zero_premises(
      n
    )
  )

  rules = (
    toda_lemma41_even_zero_case_inference_rule(),
    toda_lemma41_even_zero_h_alpha_inference_rule(),
    toda_lemma41_even_zero_suspension_primary_inference_rule(),
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        even_step,
        zero_step,
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 1
  )

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 3


def test_phase44_6c_alpha_condition_rules_do_not_match_nonzero_case():
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

  rules = (
    toda_lemma41_even_zero_h_alpha_inference_rule(),
    toda_lemma41_even_zero_suspension_primary_inference_rule(),
  )

  for rule in rules:
    match = find_inference_match(
      rule,
      (
        even_step,
        nonzero_step,
      ),
    )

    assert match is None


def test_phase44_6d_zero_case_bundle_has_three_applicable_rules():
  result = (
    build_phase44_representative_cases()
  )

  zero_case = result[
    "cases"
  ][
    "even_zero"
  ]

  applicable = zero_case[
    "zero_case_applicable_rules"
  ]

  assert len(
    applicable
  ) == 3

  assert tuple(
    rule.name
    for rule in applicable
  ) == (
    (
      "Toda Lemma 4.1 even "
      "Whitehead zero case"
    ),
    (
      "Toda Lemma 4.1 even zero "
      "alpha Hopf condition"
    ),
    (
      "Toda Lemma 4.1 even zero "
      "alpha suspension primary condition"
    ),
  )


def test_phase44_6d_zero_case_bundle_reaches_fixed_point_with_three_results():
  result = (
    build_phase44_representative_cases()
  )

  zero_result = result[
    "cases"
  ][
    "even_zero"
  ][
    "zero_case_result"
  ]

  assert (
    zero_result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    zero_result.round_count
    == 1
  )

  assert len(
    zero_result.round_results[
      0
    ].new_steps
  ) == 3


def test_phase44_6d_probe_formats_h_alpha_condition():
  result = (
    build_phase44_representative_cases()
  )

  h_alpha_step = result[
    "cases"
  ][
    "even_zero"
  ][
    "alpha_condition_steps"
  ][
    0
  ]

  assert relation_text(
    h_alpha_step.conclusion
  ) == (
    "H(α) = ι_{2n-1}"
  )


def test_phase44_6d_probe_formats_e_alpha_primary_membership():
  result = (
    build_phase44_representative_cases()
  )

  membership_step = result[
    "cases"
  ][
    "even_zero"
  ][
    "alpha_condition_steps"
  ][
    1
  ]

  assert (
    primary_component_membership_text(
      membership_step.conclusion
    )
    == (
      "Eα ∈ π_{2n}(S^{n+1};2)"
    )
  )


def test_phase44_6d_probe_zero_case_shares_structural_alpha():
  result = (
    build_phase44_representative_cases()
  )

  zero_case = result[
    "cases"
  ][
    "even_zero"
  ]

  group_alpha = (
    zero_case[
      "derived_step"
    ]
    .conclusion
    .rhs
    .summands[
      0
    ]
    .generator
  )

  (
    h_alpha_step,
    membership_step,
  ) = zero_case[
    "alpha_condition_steps"
  ]

  h_alpha = (
    h_alpha_step
    .conclusion
    .lhs
    .expression
  )

  suspension_alpha = (
    membership_step
    .conclusion
    .element
    .expression
  )

  assert group_alpha == h_alpha

  assert (
    group_alpha
    == suspension_alpha
  )


def test_phase44_6d_existing_three_case_probe_contract_remains_unchanged():
  result = (
    build_phase44_representative_cases()
  )

  cases = result[
    "cases"
  ]

  for name in (
    "odd",
    "even_nonzero",
    "even_zero",
  ):
    assert len(
      cases[
        name
      ][
        "applicable_rules"
      ]
    ) == 1

    assert (
      cases[
        name
      ][
        "result"
      ].round_count
      == 1
    )

    assert len(
      cases[
        name
      ][
        "result"
      ].round_results[
        0
      ].new_steps
    ) == 1



