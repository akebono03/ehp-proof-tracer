from typing import (
  get_args,
  get_type_hints,
)

from algebra import Subgroup
from barratt_hilton_rules import (
  TODA_PROP_3_1_REFERENCE,
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  HomotopyElement,
  IteratedSuspension,
  Multiple,
  ScalarPower,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  SmashProduct,
)
from generator_facts import (
  GeneratorAmbientGroupFact,
)
from proof import (
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_transitivity_inference_rule,
)
from scalar_rules import (
  EvenScalarStatement,
  OddScalarStatement,
  ScalarSignEvaluationStatement,
  even_scalar_evaluates_minus_one_power_inference_rule,
  odd_scalar_evaluates_minus_one_power_inference_rule,
  scalar_sign_evaluation_applies_to_multiple_inference_rule,
)
from set_rules import (
  ImageSubgroupReference,
  KernelSubgroupReference,
  MembershipStatement,
)


def test_phase34_1_concrete_homotopy_element_typing_can_represent_concrete_membership():
  a = HomotopyElement(
    name="a",
    dimension=3,
    source=5,
    target=3,
  )

  assert a.source == 5
  assert a.target == 3

  assert a.generator is None


def test_phase34_1_concrete_barratt_hilton_parameter_instance_is_representable():
  p = 3
  k = 2

  a = HomotopyElement(
    name="a",
    dimension=p,
    source=p + k,
    target=p,
  )

  assert a.source == p + k
  assert a.target == p


def test_phase34_1_symbolic_p_plus_k_is_representable_as_scalar_structure():
  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  assert p_plus_k == ScalarSum(
    left=ScalarSymbol(
      name="p",
    ),
    right=ScalarSymbol(
      name="k",
    ),
  )


def test_phase34_1_homotopy_element_source_target_remain_concrete_integer_typing():
  type_hints = get_type_hints(
    HomotopyElement
  )

  assert type_hints["source"] == (
    int | None
  )

  assert type_hints["target"] == (
    int | None
  )


def test_phase34_1_generator_ambient_group_fact_is_generator_specific():
  type_hints = get_type_hints(
    GeneratorAmbientGroupFact
  )

  assert "generator" in type_hints
  assert "group_dimension" in type_hints
  assert "sphere_dimension" in type_hints

  assert "element" not in type_hints


def test_phase34_1_generator_ambient_group_dimensions_remain_concrete():
  type_hints = get_type_hints(
    GeneratorAmbientGroupFact
  )

  assert (
    type_hints["group_dimension"]
    is int
  )

  assert (
    type_hints["sphere_dimension"]
    is int
  )


def test_phase34_1_generic_membership_statement_is_subgroup_membership():
  type_hints = get_type_hints(
    MembershipStatement
  )

  subgroup_type = (
    type_hints["subgroup"]
  )

  assert set(
    get_args(
      subgroup_type
    )
  ) == {
    Subgroup,
    ImageSubgroupReference,
    KernelSubgroupReference,
  }


def test_phase34_1_current_membership_statement_has_no_homotopy_group_dimensions():
  type_hints = get_type_hints(
    MembershipStatement
  )

  assert "group_dimension" not in type_hints
  assert "sphere_dimension" not in type_hints


def test_phase34_1_symbolic_barratt_hilton_applicability_needs_additional_representation():
  homotopy_type_hints = get_type_hints(
    HomotopyElement
  )

  ambient_type_hints = get_type_hints(
    GeneratorAmbientGroupFact
  )

  membership_type_hints = get_type_hints(
    MembershipStatement
  )

  assert homotopy_type_hints["source"] == (
    int | None
  )

  assert ambient_type_hints[
    "group_dimension"
  ] is int

  assert "element" not in (
    ambient_type_hints
  )

  assert set(
    get_args(
      membership_type_hints[
        "subgroup"
      ]
    )
  ) == {
    Subgroup,
    ImageSubgroupReference,
    KernelSubgroupReference,
  }

  assert "group_dimension" not in (
    membership_type_hints
  )

  assert "sphere_dimension" not in (
    membership_type_hints
  )


def test_phase34_2_homotopy_group_membership_represents_symbolic_barratt_hilton_typing():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  k = ScalarSymbol(
    name="k",
  )

  statement = (
    HomotopyGroupMembershipStatement(
      element=a,
      group_dimension=ScalarSum(
        left=p,
        right=k,
      ),
      sphere_dimension=p,
    )
  )

  assert statement.element == a

  assert statement.group_dimension == (
    ScalarSum(
      left=p,
      right=k,
    )
  )

  assert statement.sphere_dimension == p


def test_phase34_2_barratt_hilton_first_theorem_rule_derives_first_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=ScalarSum(
            left=p,
            right=k,
          ),
          right=h,
        ),
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=a,
          exponent=q,
        ),
        right=IteratedSuspension(
          expression=b,
          exponent=ScalarSum(
            left=p,
            right=k,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
    source=TODA_PROP_3_1_REFERENCE,
    note=(
      "Toda Prop.3.1 "
      "Barratt-Hilton first formula."
    ),
  )


def test_phase34_2_barratt_hilton_first_theorem_rule_preserves_inference_premises():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule == rule

  assert step.premises == (
    a_membership_step,
    b_membership_step,
  )

  assert step.inference_rule.name == (
    "Toda Prop.3.1 "
    "Barratt-Hilton first formula"
  )


def test_phase34_3_first_rule_ignores_unrelated_available_membership_premise():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  unrelated_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=c,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
      unrelated_membership_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    a_membership_step,
    b_membership_step,
  )

  assert unrelated_membership_step not in (
    match.premises
  )

  step = apply_inference_match(
    match
  )

  assert step.premises == (
    a_membership_step,
    b_membership_step,
  )


def test_phase34_3_first_rule_rejects_missing_b_membership():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
    ),
  )

  assert match is None


def test_phase34_3_first_rule_rejects_wrong_a_group_dimension():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  wrong_a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=h,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      wrong_a_membership_step,
      b_membership_step,
    ),
  )

  assert match is None


def test_phase34_3_first_rule_rejects_wrong_a_sphere_dimension():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  wrong_a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      wrong_a_membership_step,
      b_membership_step,
    ),
  )

  assert match is None


def test_phase34_3_first_rule_rejects_wrong_b_group_dimension():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  wrong_b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=k,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      wrong_b_membership_step,
    ),
  )

  assert match is None


def test_phase34_3_first_rule_rejects_wrong_b_sphere_dimension():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  wrong_b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      wrong_b_membership_step,
    ),
  )

  assert match is None


def test_phase34_3_first_rule_rejects_membership_of_different_element():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  c_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=c,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      c_membership_step,
      b_membership_step,
    ),
  )

  assert match is None


def test_phase34_4_barratt_hilton_second_theorem_rule_derives_second_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_second_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=ScalarProduct(
          left=p,
          right=h,
        ),
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=b,
          exponent=p,
        ),
        right=IteratedSuspension(
          expression=a,
          exponent=ScalarSum(
            left=q,
            right=h,
          ),
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
    source=TODA_PROP_3_1_REFERENCE,
    note=(
      "Toda Prop.3.1 "
      "Barratt-Hilton second formula."
    ),
  )


def test_phase34_4_second_theorem_rule_reuses_barratt_hilton_membership_premises():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_second_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule == rule

  assert step.premises == (
    a_membership_step,
    b_membership_step,
  )

  assert step.inference_rule.name == (
    "Toda Prop.3.1 "
    "Barratt-Hilton second formula"
  )


def test_phase34_4_first_and_second_theorem_rules_derive_distinct_formulas():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  second_rule = (
    barratt_hilton_second_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  first_match = find_inference_match(
    first_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  second_match = find_inference_match(
    second_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert first_match is not None
  assert second_match is not None

  first_step = apply_inference_match(
    first_match
  )

  second_step = apply_inference_match(
    second_match
  )

  assert first_step.conclusion != (
    second_step.conclusion
  )

  assert first_step.conclusion.lhs == (
    SmashProduct(
      left=a,
      right=b,
    )
  )

  assert second_step.conclusion.lhs == (
    SmashProduct(
      left=a,
      right=b,
    )
  )

  assert first_step.conclusion.rhs != (
    second_step.conclusion.rhs
  )


def test_phase34_5_toda_prop_3_1_reference_is_structured_literature_reference():
  assert isinstance(
    TODA_PROP_3_1_REFERENCE,
    LiteratureReference,
  )

  assert (
    TODA_PROP_3_1_REFERENCE.label
    == "Toda Prop.3.1"
  )

  assert (
    TODA_PROP_3_1_REFERENCE.author
    == "H. Toda"
  )

  assert (
    TODA_PROP_3_1_REFERENCE.title
    == (
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    )
  )

  assert (
    TODA_PROP_3_1_REFERENCE.year
    == 1962
  )

  assert (
    TODA_PROP_3_1_REFERENCE.locator
    == "Proposition 3.1"
  )


def test_phase34_5_first_formula_preserves_toda_prop_3_1_provenance():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion.source == (
    TODA_PROP_3_1_REFERENCE
  )

  assert step.conclusion.note == (
    "Toda Prop.3.1 "
    "Barratt-Hilton first formula."
  )

  assert step.rule == ProofRule.INFERENCE

  assert step.inference_rule == rule

  assert step.premises == (
    a_membership_step,
    b_membership_step,
  )


def test_phase34_5_second_formula_preserves_toda_prop_3_1_provenance():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_second_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  match = find_inference_match(
    rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion.source == (
    TODA_PROP_3_1_REFERENCE
  )

  assert step.conclusion.note == (
    "Toda Prop.3.1 "
    "Barratt-Hilton second formula."
  )

  assert step.rule == ProofRule.INFERENCE

  assert step.inference_rule == rule

  assert step.premises == (
    a_membership_step,
    b_membership_step,
  )


def test_phase34_6_first_formula_even_sign_reduction_connects_to_theorem_rhs():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  exponent = ScalarProduct(
    left=p_plus_k,
    right=h,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=p_plus_k,
    ),
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=p_plus_k,
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert theorem_match is not None

  theorem_step = apply_inference_match(
    theorem_match
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  sign_match = find_inference_match(
    sign_rule,
    (
      parity_step,
    ),
  )

  assert sign_match is not None

  sign_step = apply_inference_match(
    sign_match
  )

  assert sign_step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=sign,
      value=1,
    )
  )

  reduction_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=composition,
    )
  )

  reduction_match = find_inference_match(
    reduction_rule,
    (
      sign_step,
    ),
  )

  assert reduction_match is not None

  reduction_step = apply_inference_match(
    reduction_match
  )

  assert theorem_step.conclusion.rhs == (
    reduction_step.conclusion.lhs
  )

  assert reduction_step.conclusion == Relation(
    lhs=Multiple(
      coefficient=sign,
      expression=composition,
    ),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )

  assert reduction_step.premises == (
    sign_step,
  )

  assert sign_step.premises == (
    parity_step,
  )


def test_phase34_6_first_formula_odd_sign_reduction_connects_to_inverse():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  exponent = ScalarProduct(
    left=p_plus_k,
    right=h,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=p_plus_k,
    ),
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=p_plus_k,
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert theorem_match is not None

  theorem_step = apply_inference_match(
    theorem_match
  )

  parity_step = ProofStep(
    conclusion=OddScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_rule = (
    odd_scalar_evaluates_minus_one_power_inference_rule()
  )

  sign_match = find_inference_match(
    sign_rule,
    (
      parity_step,
    ),
  )

  assert sign_match is not None

  sign_step = apply_inference_match(
    sign_match
  )

  assert sign_step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=sign,
      value=-1,
    )
  )

  reduction_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=composition,
    )
  )

  reduction_match = find_inference_match(
    reduction_rule,
    (
      sign_step,
    ),
  )

  assert reduction_match is not None

  reduction_step = apply_inference_match(
    reduction_match
  )

  assert theorem_step.conclusion.rhs == (
    reduction_step.conclusion.lhs
  )

  assert reduction_step.conclusion == Relation(
    lhs=Multiple(
      coefficient=sign,
      expression=composition,
    ),
    rhs=Multiple(
      coefficient=-1,
      expression=composition,
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_phase34_6_first_formula_even_sign_reduction_closes_by_equality_transitivity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  p_plus_k = ScalarSum(
    left=p,
    right=k,
  )

  exponent = ScalarProduct(
    left=p_plus_k,
    right=h,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=a,
      exponent=q,
    ),
    right=IteratedSuspension(
      expression=b,
      exponent=p_plus_k,
    ),
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=p_plus_k,
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_first_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert theorem_match is not None

  theorem_step = apply_inference_match(
    theorem_match
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  sign_match = find_inference_match(
    sign_rule,
    (
      parity_step,
    ),
  )

  assert sign_match is not None

  sign_step = apply_inference_match(
    sign_match
  )

  reduction_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=composition,
    )
  )

  reduction_match = find_inference_match(
    reduction_rule,
    (
      sign_step,
    ),
  )

  assert reduction_match is not None

  reduction_step = apply_inference_match(
    reduction_match
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      theorem_step,
      reduction_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  assert final_step.conclusion == Relation(
    lhs=SmashProduct(
      left=a,
      right=b,
    ),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.inference_rule == (
    transitivity_rule
  )

  assert final_step.premises == (
    theorem_step,
    reduction_step,
  )

  assert theorem_step.conclusion.source == (
    TODA_PROP_3_1_REFERENCE
  )

  assert reduction_step.premises == (
    sign_step,
  )

  assert sign_step.premises == (
    parity_step,
  )


def test_phase34_6_second_formula_even_sign_reduction_connects_to_theorem_rhs():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  p = ScalarSymbol(
    name="p",
  )

  q = ScalarSymbol(
    name="q",
  )

  k = ScalarSymbol(
    name="k",
  )

  h = ScalarSymbol(
    name="h",
  )

  exponent = ScalarProduct(
    left=p,
    right=h,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=b,
      exponent=p,
    ),
    right=IteratedSuspension(
      expression=a,
      exponent=ScalarSum(
        left=q,
        right=h,
      ),
    ),
  )

  a_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=a,
        group_dimension=ScalarSum(
          left=p,
          right=k,
        ),
        sphere_dimension=p,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  b_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=b,
        group_dimension=ScalarSum(
          left=q,
          right=h,
        ),
        sphere_dimension=q,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_second_inference_rule(
      alpha=a,
      beta=b,
      p=p,
      q=q,
      k=k,
      h=h,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      a_membership_step,
      b_membership_step,
    ),
  )

  assert theorem_match is not None

  theorem_step = apply_inference_match(
    theorem_match
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  sign_rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  sign_match = find_inference_match(
    sign_rule,
    (
      parity_step,
    ),
  )

  assert sign_match is not None

  sign_step = apply_inference_match(
    sign_match
  )

  reduction_rule = (
    scalar_sign_evaluation_applies_to_multiple_inference_rule(
      sign=sign,
      expression=composition,
    )
  )

  reduction_match = find_inference_match(
    reduction_rule,
    (
      sign_step,
    ),
  )

  assert reduction_match is not None

  reduction_step = apply_inference_match(
    reduction_match
  )

  assert theorem_step.conclusion.rhs == (
    reduction_step.conclusion.lhs
  )

  assert reduction_step.conclusion == Relation(
    lhs=Multiple(
      coefficient=sign,
      expression=composition,
    ),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )




