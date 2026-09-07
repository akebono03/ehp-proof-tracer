from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
  Suspension,
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
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  toda_eta3_suspension_relation_inference_rule,
  toda_eta_family_definition_statement,
  toda_higher_eta_family_bridge_inference_rule,
)


def test_phase54_2_symbolic_eta_family_definition_is_representable():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  assert isinstance(
    definition,
    TodaEtaFamilyDefinitionStatement,
  )

  assert definition.index == n


def test_phase54_2_symbolic_eta_n_has_expected_structure():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  expected_eta_n = HomotopyElement(
    name="η_n",
    dimension=n,
    source=ScalarSum(
      left=n,
      right=1,
    ),
    target=n,
    generator=GeneratorSymbol(
      family="η",
      index=n,
    ),
  )

  assert (
    definition.element
    == expected_eta_n
  )


def test_phase54_2_symbolic_eta_n_preserves_n_index():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  assert (
    definition
    .element
    .generator
    .family
    == "η"
  )

  assert (
    definition
    .element
    .generator
    .index
    == n
  )


def test_phase54_2_symbolic_eta_n_has_source_n_plus_1_and_target_n():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  assert (
    definition.element.source
    == ScalarSum(
      left=n,
      right=1,
    )
  )

  assert (
    definition.element.target
    == n
  )


def test_phase54_2_symbolic_eta_definition_represents_e_n_minus_2_eta2():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
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

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=ScalarSum(
        left=n,
        right=-2,
      ),
    )
  )


def test_phase54_2_symbolic_eta_definition_does_not_build_higher_bridge():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  higher_eta_suspension = (
    IteratedSuspension(
      expression=eta_3,
      exponent=ScalarSum(
        left=n,
        right=-3,
      ),
    )
  )

  assert (
    definition.iterated_suspension
    != higher_eta_suspension
  )


def test_phase54_2_existing_eta3_definition_remains_compatible():
  definition = (
    toda_eta_family_definition_statement(
      3
    )
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

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  assert definition.index == 3

  assert (
    definition.element
    == eta_3
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=1,
    )
  )


def test_phase54_2_existing_eta2_definition_remains_compatible():
  definition = (
    toda_eta_family_definition_statement(
      2
    )
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

  assert definition.index == 2

  assert (
    definition.element
    == eta_2
  )

  assert (
    definition.iterated_suspension
    == IteratedSuspension(
      expression=eta_2,
      exponent=0,
    )
  )


def test_phase54_3_higher_eta_bridge_matches_valid_specific_instance():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta_3_definition_step = ProofStep(
    conclusion=eta_3_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  eta_3_result = (
    run_inference_until_stable_with_history(
      toda_eta3_suspension_relation_inference_rule(),
      (
        eta_3_definition_step,
      ),
    )
  )

  eta_3_relation_step = next(
    step
    for step in eta_3_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
    )
  )

  steps = (
    ProofStep(
      conclusion=definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    eta_3_relation_step,
  )

  assert find_inference_match(
    toda_higher_eta_family_bridge_inference_rule(),
    steps,
  ) is not None


def test_phase54_3_higher_eta_bridge_derives_e_n_minus_3_eta3_equals_eta_n():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta_3_result = (
    run_inference_until_stable_with_history(
      toda_eta3_suspension_relation_inference_rule(),
      (
        ProofStep(
          conclusion=eta_3_definition,
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  eta_3_relation_step = next(
    step
    for step in eta_3_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
    )
  )

  result = (
    run_inference_until_stable_with_history(
      toda_higher_eta_family_bridge_inference_rule(),
      (
        ProofStep(
          conclusion=definition,
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        eta_3_relation_step,
      ),
    )
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  expected_relation = Relation(
    lhs=IteratedSuspension(
      expression=eta_3,
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    ),
    rhs=definition.element,
    relation_type=RelationType.EQUALITY,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected_relation in conclusions


def test_phase54_3_higher_eta_bridge_result_is_inference():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta_3_result = (
    run_inference_until_stable_with_history(
      toda_eta3_suspension_relation_inference_rule(),
      (
        ProofStep(
          conclusion=eta_3_definition,
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  eta_3_relation_step = next(
    step
    for step in eta_3_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
    )
  )

  steps = (
    ProofStep(
      conclusion=definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    eta_3_relation_step,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_higher_eta_family_bridge_inference_rule(),
      steps,
    )
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  expected_relation = Relation(
    lhs=IteratedSuspension(
      expression=eta_3,
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=3,
        ),
      ),
    ),
    rhs=definition.element,
    relation_type=RelationType.EQUALITY,
  )

  derived = next(
    step
    for step in result.steps
    if (
      step.conclusion
      == expected_relation
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.inference_rule is not None

  assert (
    derived.inference_rule.name
    == (
      "Toda higher eta-family "
      "iterated suspension bridge"
    )
  )

  assert derived.premises == steps


def test_phase54_3_higher_eta_bridge_reaches_fixed_point_in_one_round():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3_definition = (
    toda_eta_family_definition_statement(
      3
    )
  )

  eta_3_result = (
    run_inference_until_stable_with_history(
      toda_eta3_suspension_relation_inference_rule(),
      (
        ProofStep(
          conclusion=eta_3_definition,
          premises=(),
          rule=ProofRule.GIVEN,
        ),
      ),
    )
  )

  eta_3_relation_step = next(
    step
    for step in eta_3_result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
    )
  )

  result = (
    run_inference_until_stable_with_history(
      toda_higher_eta_family_bridge_inference_rule(),
      (
        ProofStep(
          conclusion=definition,
          premises=(),
          rule=ProofRule.GIVEN,
        ),
        eta_3_relation_step,
      ),
    )
  )

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


def test_phase54_3_rejects_concrete_eta_family_index():
  definition = (
    toda_eta_family_definition_statement(
      4
    )
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

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  eta_3_relation = Relation(
    lhs=eta_3,
    rhs=Suspension(
      expression=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=eta_3_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_higher_eta_family_bridge_inference_rule(),
    steps,
  ) is None


def test_phase54_3_rejects_wrong_eta3_base():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
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

  eta_4 = HomotopyElement(
    name="η₄",
    dimension=4,
    source=5,
    target=4,
    generator=GeneratorSymbol(
      family="η",
      index=4,
    ),
  )

  wrong_relation = Relation(
    lhs=eta_4,
    rhs=Suspension(
      expression=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_higher_eta_family_bridge_inference_rule(),
    steps,
  ) is None


def test_phase54_3_rejects_wrong_eta3_suspension_base():
  n = ScalarSymbol(
    name="n",
  )

  definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  wrong_eta_2 = HomotopyElement(
    name="η₂'",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η'",
      index=2,
    ),
  )

  wrong_relation = Relation(
    lhs=eta_3,
    rhs=Suspension(
      expression=wrong_eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=wrong_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_higher_eta_family_bridge_inference_rule(),
    steps,
  ) is None


def test_phase54_3_rejects_wrong_symbolic_eta_definition_exponent():
  n = ScalarSymbol(
    name="n",
  )

  valid_definition = (
    toda_eta_family_definition_statement(
      n
    )
  )

  wrong_definition = (
    TodaEtaFamilyDefinitionStatement(
      index=n,
      element=valid_definition.element,
      iterated_suspension=IteratedSuspension(
        expression=(
          valid_definition
          .iterated_suspension
          .expression
        ),
        exponent=ScalarSum(
          left=n,
          right=-3,
        ),
      ),
    )
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

  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  eta_3_relation = Relation(
    lhs=eta_3,
    rhs=Suspension(
      expression=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  steps = (
    ProofStep(
      conclusion=wrong_definition,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=eta_3_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_higher_eta_family_bridge_inference_rule(),
    steps,
  ) is None




