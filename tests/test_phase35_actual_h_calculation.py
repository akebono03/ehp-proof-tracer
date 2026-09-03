from barratt_hilton_rules import (
  TODA_PROP_3_1_REFERENCE,
  HomotopyGroupMembershipStatement,
  barratt_hilton_first_inference_rule,
  barratt_hilton_second_inference_rule,
)
from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  MapApplication,
  Multiple,
  ScalarPower,
  ScalarProduct,
  SmashProduct,
  Suspension,
)
from generator_facts import (
  GENERATOR_FACT_REPOSITORY,
)
from hopf_facts import (
  ETA_2,
  ETA_2_HOPF_INVARIANT_FACT,
  IOTA_3,
  TODA_PROP_5_1_REFERENCE,
)
from hopf_rules import (
  HopfInvariantStatement,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
  toda_prop22_left_inference_rule,
)
from map_facts import (
  EHP_H_MAP,
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
  ScalarSignEvaluationStatement,
  even_scalar_evaluates_minus_one_power_inference_rule,
  scalar_sign_evaluation_applies_to_multiple_inference_rule,
)



def test_phase35_1_iota_1_identity_is_representable_with_explicit_typing():
  iota_1_generator = GeneratorSymbol(
    family="ι",
    index=1,
  )

  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=iota_1_generator,
  )

  assert iota_1.generator == (
    iota_1_generator
  )

  assert iota_1.source == 1
  assert iota_1.target == 1


def test_phase35_1_iota_2_identity_is_representable_with_explicit_typing():
  iota_2_generator = GeneratorSymbol(
    family="ι",
    index=2,
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=iota_2_generator,
  )

  assert iota_2.generator == (
    iota_2_generator
  )

  assert iota_2.source == 2
  assert iota_2.target == 2


def test_phase35_1_iota_3_identity_is_representable_with_explicit_typing():
  iota_3_generator = GeneratorSymbol(
    family="ι",
    index=3,
  )

  iota_3 = HomotopyElement(
    name="ι₃",
    dimension=3,
    source=3,
    target=3,
    generator=iota_3_generator,
  )

  assert iota_3.generator == (
    iota_3_generator
  )

  assert iota_3.source == 3
  assert iota_3.target == 3


def test_phase35_1_eta_2_is_representable_with_explicit_typing():
  eta_2_generator = GeneratorSymbol(
    family="η",
    index=2,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=eta_2_generator,
  )

  assert eta_2.generator == (
    eta_2_generator
  )

  assert eta_2.source == 3
  assert eta_2.target == 2


def test_phase35_1_two_iota_1_is_representable_as_multiple():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1 == Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1.coefficient == 2
  assert two_iota_1.expression == iota_1


def test_phase35_1_two_iota_2_is_representable_as_multiple():
  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert two_iota_2 == Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert two_iota_2.coefficient == 2
  assert two_iota_2.expression == iota_2


def test_phase35_1_actual_generators_are_structurally_distinct():
  iota_1 = GeneratorSymbol(
    family="ι",
    index=1,
  )

  iota_2 = GeneratorSymbol(
    family="ι",
    index=2,
  )

  iota_3 = GeneratorSymbol(
    family="ι",
    index=3,
  )

  eta_2 = GeneratorSymbol(
    family="η",
    index=2,
  )

  assert iota_1 != iota_2
  assert iota_2 != iota_3
  assert iota_2 != eta_2


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_1():
  iota_1_generator = GeneratorSymbol(
    family="ι",
    index=1,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_1_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_2():
  iota_2_generator = GeneratorSymbol(
    family="ι",
    index=2,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_2_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_iota_3():
  iota_3_generator = GeneratorSymbol(
    family="ι",
    index=3,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      iota_3_generator
    )
    is None
  )


def test_phase35_1_current_generator_repository_does_not_yet_type_eta_2():
  eta_2_generator = GeneratorSymbol(
    family="η",
    index=2,
  )

  assert (
    GENERATOR_FACT_REPOSITORY
    .lookup_typing(
      eta_2_generator
    )
    is None
  )


def test_phase35_1_generator_notation_does_not_implicitly_add_typing():
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  assert eta_2.source is None
  assert eta_2.target is None


def test_phase35_1_representative_actual_elements_need_no_new_expression_type():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  iota_3 = HomotopyElement(
    name="ι₃",
    dimension=3,
    source=3,
    target=3,
    generator=GeneratorSymbol(
      family="ι",
      index=3,
    ),
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  assert isinstance(
    iota_1,
    HomotopyElement,
  )

  assert isinstance(
    iota_2,
    HomotopyElement,
  )

  assert isinstance(
    iota_3,
    HomotopyElement,
  )

  assert isinstance(
    eta_2,
    HomotopyElement,
  )

  assert isinstance(
    two_iota_1,
    Multiple,
  )

  assert isinstance(
    two_iota_2,
    Multiple,
  )

  assert two_iota_1.expression == (
    iota_1
  )

  assert two_iota_2.expression == (
    iota_2
  )


def test_phase35_2_toda_prop_5_1_reference_is_structured_literature_reference():
  assert isinstance(
    TODA_PROP_5_1_REFERENCE,
    LiteratureReference,
  )

  assert (
    TODA_PROP_5_1_REFERENCE.label
    == "Toda Prop.5.1"
  )

  assert (
    TODA_PROP_5_1_REFERENCE.author
    == "H. Toda"
  )

  assert (
    TODA_PROP_5_1_REFERENCE.title
    == (
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    )
  )

  assert (
    TODA_PROP_5_1_REFERENCE.year
    == 1962
  )

  assert (
    TODA_PROP_5_1_REFERENCE.locator
    == "Proposition 5.1"
  )


def test_phase35_2_eta_2_hopf_fact_represents_h_eta_2_equals_iota_3():
  assert isinstance(
    ETA_2_HOPF_INVARIANT_FACT,
    HopfInvariantStatement,
  )

  assert (
    ETA_2_HOPF_INVARIANT_FACT.expression
    == ETA_2
  )

  assert (
    ETA_2_HOPF_INVARIANT_FACT.value
    == IOTA_3
  )

  assert ETA_2.source == 3
  assert ETA_2.target == 2

  assert IOTA_3.source == 3
  assert IOTA_3.target == 3


def test_phase35_2_eta_2_hopf_fact_preserves_toda_prop_5_1_provenance():
  assert (
    ETA_2_HOPF_INVARIANT_FACT.source
    == TODA_PROP_5_1_REFERENCE
  )

  assert (
    ETA_2_HOPF_INVARIANT_FACT.note
    == (
      "Toda Prop.5.1 "
      "H(η₂)=ι₃."
    )
  )


def test_phase35_2_eta_2_hopf_fact_materializes_as_given_proof_step():
  step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  assert step.conclusion == (
    ETA_2_HOPF_INVARIANT_FACT
  )

  assert step.rule == ProofRule.GIVEN
  assert step.premises == ()
  assert step.inference_rule is None

  assert (
    step.conclusion.source
    == TODA_PROP_5_1_REFERENCE
  )


def test_phase35_2_eta_2_hopf_fact_bridges_to_actual_ehp_h_equality():
  hopf_step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=ETA_2,
    ),
    rhs=IOTA_3,
    relation_type=RelationType.EQUALITY,
  )

  assert (
    step.conclusion.lhs.map
    is EHP_H_MAP
  )


def test_phase35_2_actual_h_equality_preserves_fact_provenance_through_premise():
  hopf_step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
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
    hopf_step,
  )

  assert (
    step.premises[0]
    .conclusion
    .source
    == TODA_PROP_5_1_REFERENCE
  )

  assert (
    step.premises[0]
    .conclusion
    .note
    == (
      "Toda Prop.5.1 "
      "H(η₂)=ι₃."
    )
  )


def test_phase35_3_two_iota_1_is_available_for_concrete_prop22_left_application():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  assert two_iota_1 == Multiple(
    coefficient=2,
    expression=iota_1,
  )


def test_phase35_3_prop22_left_rule_accepts_two_iota_1_and_eta_2():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  rule = toda_prop22_left_inference_rule(
    alpha=ETA_2,
    gamma=two_iota_1,
  )

  match = find_inference_match(
    rule,
    (),
  )

  assert match is not None


def test_phase35_3_prop22_left_derives_concrete_actual_h_equality():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  rule = toda_prop22_left_inference_rule(
    alpha=ETA_2,
    gamma=two_iota_1,
  )

  match = find_inference_match(
    rule,
    (),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=Suspension(
          expression=two_iota_1,
        ),
        right=ETA_2,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=two_iota_1,
          right=two_iota_1,
        ),
      ),
      right=MapApplication(
        map=EHP_H_MAP,
        expression=ETA_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )


def test_phase35_3_concrete_prop22_left_result_is_theorem_derived_proof_step():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  rule = toda_prop22_left_inference_rule(
    alpha=ETA_2,
    gamma=two_iota_1,
  )

  match = find_inference_match(
    rule,
    (),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert step.inference_rule == rule

  assert step.premises == ()

  assert (
    step.inference_rule.name
    == "Toda Prop.2.2 left formula"
  )


def test_phase35_3_concrete_prop22_left_uses_canonical_actual_h_map():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  rule = toda_prop22_left_inference_rule(
    alpha=ETA_2,
    gamma=two_iota_1,
  )

  match = find_inference_match(
    rule,
    (),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert (
    step.conclusion.lhs.map
    is EHP_H_MAP
  )

  assert (
    step.conclusion
    .rhs
    .right
    .map
    is EHP_H_MAP
  )


def test_phase35_3_prop22_left_rhs_connects_structurally_to_h_eta_2_fact():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  prop22_rule = (
    toda_prop22_left_inference_rule(
      alpha=ETA_2,
      gamma=two_iota_1,
    )
  )

  prop22_match = find_inference_match(
    prop22_rule,
    (),
  )

  assert prop22_match is not None

  prop22_step = apply_inference_match(
    prop22_match
  )

  hopf_step = hopf_invariant_proof_step(
    ETA_2_HOPF_INVARIANT_FACT
  )

  h_bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  h_bridge_match = find_inference_match(
    h_bridge_rule,
    (
      hopf_step,
    ),
  )

  assert h_bridge_match is not None

  h_eta_2_step = apply_inference_match(
    h_bridge_match
  )

  assert (
    prop22_step
    .conclusion
    .rhs
    .right
    == h_eta_2_step.conclusion.lhs
  )

  assert h_eta_2_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=ETA_2,
    ),
    rhs=IOTA_3,
    relation_type=RelationType.EQUALITY,
  )


def test_phase35_3_does_not_identify_suspension_two_iota_1_with_two_iota_2_yet():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  iota_2 = HomotopyElement(
    name="ι₂",
    dimension=2,
    source=2,
    target=2,
    generator=GeneratorSymbol(
      family="ι",
      index=2,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  two_iota_2 = Multiple(
    coefficient=2,
    expression=iota_2,
  )

  suspended_two_iota_1 = Suspension(
    expression=two_iota_1,
  )

  assert suspended_two_iota_1 != (
    two_iota_2
  )


def test_phase35_3_does_not_evaluate_two_iota_1_smash_product_yet():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  smash = SmashProduct(
    left=two_iota_1,
    right=two_iota_1,
  )

  assert isinstance(
    smash,
    SmashProduct,
  )

  assert smash.left == two_iota_1
  assert smash.right == two_iota_1


def test_phase35_4_two_iota_1_can_be_actual_barratt_hilton_membership_element():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  statement = (
    HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    )
  )

  assert statement.element == (
    two_iota_1
  )

  assert statement.group_dimension == 1
  assert statement.sphere_dimension == 1


def test_phase35_4_first_barratt_hilton_rule_accepts_two_iota_1_in_pi_1_s_1():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  match = find_inference_match(
    rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  assert match is not None


def test_phase35_4_first_barratt_hilton_rule_derives_concrete_two_iota_1_smash_formula():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  match = find_inference_match(
    rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  sign_exponent = ScalarProduct(
    left=1,
    right=0,
  )

  assert step.conclusion == Relation(
    lhs=SmashProduct(
      left=two_iota_1,
      right=two_iota_1,
    ),
    rhs=Multiple(
      coefficient=ScalarPower(
        base=-1,
        exponent=sign_exponent,
      ),
      expression=Composition(
        left=IteratedSuspension(
          expression=two_iota_1,
          exponent=1,
        ),
        right=IteratedSuspension(
          expression=two_iota_1,
          exponent=1,
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


def test_phase35_4_concrete_barratt_hilton_step_preserves_toda_prop_3_1_provenance():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  match = find_inference_match(
    rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule

  assert step.premises == (
    alpha_membership_step,
    beta_membership_step,
  )

  assert (
    step.conclusion.source
    == TODA_PROP_3_1_REFERENCE
  )


def test_phase35_4_second_barratt_hilton_formula_agrees_in_symmetric_two_iota_1_case():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  second_rule = (
    barratt_hilton_second_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  first_match = find_inference_match(
    first_rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  second_match = find_inference_match(
    second_rule,
    (
      alpha_membership_step,
      beta_membership_step,
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

  assert (
    first_step.conclusion.lhs
    == second_step.conclusion.lhs
  )

  assert (
    first_step.conclusion.rhs
    == second_step.conclusion.rhs
  )

  assert (
    first_step.inference_rule
    != second_step.inference_rule
  )


def test_phase35_4_concrete_barratt_hilton_does_not_reduce_sign_yet():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=(
      HomotopyGroupMembershipStatement(
        element=two_iota_1,
        group_dimension=1,
        sphere_dimension=1,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  match = find_inference_match(
    rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert (
    step.conclusion.rhs.coefficient
    == ScalarPower(
      base=-1,
      exponent=ScalarProduct(
        left=1,
        right=0,
      ),
    )
  )

  assert (
    step.conclusion.rhs.coefficient
    != 1
  )


def test_phase35_5_concrete_barratt_hilton_exponent_can_be_given_even_parity():
  exponent = ScalarProduct(
    left=1,
    right=0,
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert parity_step.conclusion == (
    EvenScalarStatement(
      scalar=ScalarProduct(
        left=1,
        right=0,
      ),
    )
  )

  assert parity_step.rule == (
    ProofRule.GIVEN
  )


def test_phase35_5_concrete_even_exponent_evaluates_barratt_hilton_sign_to_one():
  exponent = ScalarProduct(
    left=1,
    right=0,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  parity_step = ProofStep(
    conclusion=EvenScalarStatement(
      scalar=exponent,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    even_scalar_evaluates_minus_one_power_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      parity_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    ScalarSignEvaluationStatement(
      expression=sign,
      value=1,
    )
  )

  assert step.premises == (
    parity_step,
  )


def test_phase35_5_concrete_sign_evaluation_reduces_barratt_hilton_multiple():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  exponent = ScalarProduct(
    left=1,
    right=0,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
    right=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
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


def test_phase35_5_concrete_sign_reduction_connects_to_barratt_hilton_theorem_rhs():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  assert theorem_match is not None

  theorem_step = apply_inference_match(
    theorem_match
  )

  exponent = ScalarProduct(
    left=1,
    right=0,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
    right=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
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

  assert (
    theorem_step.conclusion.rhs
    == reduction_step.conclusion.lhs
  )


def test_phase35_5_concrete_barratt_hilton_sign_reduction_closes_by_transitivity():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  alpha_membership_step = ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  beta_membership_step = ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=two_iota_1,
      group_dimension=1,
      sphere_dimension=1,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  theorem_rule = (
    barratt_hilton_first_inference_rule(
      alpha=two_iota_1,
      beta=two_iota_1,
      p=1,
      q=1,
      k=0,
      h=0,
    )
  )

  theorem_match = find_inference_match(
    theorem_rule,
    (
      alpha_membership_step,
      beta_membership_step,
    ),
  )

  assert theorem_match is not None

  theorem_step = apply_inference_match(
    theorem_match
  )

  exponent = ScalarProduct(
    left=1,
    right=0,
  )

  sign = ScalarPower(
    base=-1,
    exponent=exponent,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
    right=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
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
      left=two_iota_1,
      right=two_iota_1,
    ),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.premises == (
    theorem_step,
    reduction_step,
  )


def test_phase35_5_reduced_barratt_hilton_formula_still_keeps_suspended_multiples():
  iota_1 = HomotopyElement(
    name="ι₁",
    dimension=1,
    source=1,
    target=1,
    generator=GeneratorSymbol(
      family="ι",
      index=1,
    ),
  )

  two_iota_1 = Multiple(
    coefficient=2,
    expression=iota_1,
  )

  composition = Composition(
    left=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
    right=IteratedSuspension(
      expression=two_iota_1,
      exponent=1,
    ),
  )

  assert isinstance(
    composition.left,
    IteratedSuspension,
  )

  assert isinstance(
    composition.right,
    IteratedSuspension,
  )

  assert composition.left.expression == (
    two_iota_1
  )

  assert composition.right.expression == (
    two_iota_1
  )

  assert composition.left != Multiple(
    coefficient=2,
    expression=HomotopyElement(
      name="ι₂",
      dimension=2,
      source=2,
      target=2,
      generator=GeneratorSymbol(
        family="ι",
        index=2,
      ),
    ),
  )




