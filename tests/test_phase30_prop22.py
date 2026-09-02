from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  Suspension,
)
from hopf_rules import (
  HopfInvariantStatement,
  hopf_composition_formula_inference_rule,
  hopf_composition_law_inference_rule,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
)
from map_facts import (
  EHP_H_MAP,
  HOPF_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_right_composition_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)


def test_phase30_1_right_hopf_formula_is_structurally_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs == MapApplication(
    map=HOPF_MAP,
    expression=Composition(
      left=a,
      right=Suspension(
        expression=b,
      ),
    ),
  )

  assert statement.rhs == Composition(
    left=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    right=Suspension(
      expression=b,
    ),
  )

  assert statement.relation_type == (
    RelationType.EQUALITY
  )


def test_phase30_1_right_hopf_formula_preserves_suspension_structure():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    statement.lhs.expression,
    Composition,
  )

  assert isinstance(
    statement.lhs.expression.right,
    Suspension,
  )

  assert statement.lhs.expression.right.expression == b

  assert isinstance(
    statement.rhs,
    Composition,
  )

  assert isinstance(
    statement.rhs.right,
    Suspension,
  )

  assert statement.rhs.right.expression == b


def test_phase30_1_right_hopf_formula_preserves_actual_hopf_map_identity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs.map is HOPF_MAP
  assert statement.rhs.left.map is HOPF_MAP


def test_phase30_1_right_hopf_formula_distinguishes_unsuspended_right_factor():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  different = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=b,
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula != different


def test_phase30_2_phase11_hopf_statement_is_distinct_from_map_application_relation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  value = HomotopyElement(
    name="value",
    dimension=1,
  )

  phase11_statement = HopfInvariantStatement(
    expression=a,
    value=value,
  )

  map_application_relation = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )

  assert phase11_statement != (
    map_application_relation
  )


def test_phase30_2_phase11_hopf_statement_preserves_expression_and_value_without_map_symbol():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  value = HomotopyElement(
    name="value",
    dimension=1,
  )

  statement = HopfInvariantStatement(
    expression=a,
    value=value,
  )

  assert statement.expression == a
  assert statement.value == value

  assert not hasattr(
    statement,
    "map",
  )


def test_phase30_2_map_application_representation_preserves_actual_hopf_map():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  application = MapApplication(
    map=HOPF_MAP,
    expression=a,
  )

  assert application.map is HOPF_MAP
  assert application.expression == a


def test_phase30_2_phase11_right_formula_and_map_application_formula_have_matching_mathematical_parts():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  h_a = HomotopyElement(
    name="H(a)",
    dimension=1,
  )

  suspended_b = Suspension(
    expression=b,
  )

  phase11_formula = HopfInvariantStatement(
    expression=Composition(
      left=a,
      right=suspended_b,
    ),
    value=Composition(
      left=h_a,
      right=suspended_b,
    ),
  )

  map_application_formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=a,
        right=suspended_b,
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      right=suspended_b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    phase11_formula.expression
    == map_application_formula.lhs.expression
  )

  assert (
    phase11_formula.value.right
    == map_application_formula.rhs.right
  )

  assert isinstance(
    phase11_formula.value,
    Composition,
  )

  assert isinstance(
    map_application_formula.rhs,
    Composition,
  )

  assert isinstance(
    map_application_formula.rhs.left,
    MapApplication,
  )


def test_phase30_2_no_implicit_bridge_exists_between_phase11_and_actual_hopf_map_representation():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  value = HomotopyElement(
    name="value",
    dimension=1,
  )

  phase11_statement = HopfInvariantStatement(
    expression=a,
    value=value,
  )

  assert phase11_statement != Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )


def test_phase30_3b_prop22_right_formula_reaches_actual_ehp_h_map_equality():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  beta = HomotopyElement(
    name="beta",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  law_rule = (
    hopf_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
    ),
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  b_step = ProofStep(
    conclusion=b,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  formula_rule = (
    hopf_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    (
      law_step,
      b_step,
    ),
  )

  assert formula_match is not None

  formula_step = apply_inference_match(
    formula_match
  )

  expected_phase11_formula = (
    HopfInvariantStatement(
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
      value=Composition(
        left=beta,
        right=Suspension(
          expression=b,
        ),
      ),
    )
  )

  assert formula_step.conclusion == (
    expected_phase11_formula
  )

  bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  bridge_match = find_inference_match(
    bridge_rule,
    (
      formula_step,
    ),
  )

  assert bridge_match is not None

  actual_equality_step = (
    apply_inference_match(
      bridge_match
    )
  )

  expected_actual_equality = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=a,
        right=Suspension(
          expression=b,
        ),
      ),
    ),
    rhs=Composition(
      left=beta,
      right=Suspension(
        expression=b,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert actual_equality_step.conclusion == (
    expected_actual_equality
  )

  assert (
    actual_equality_step
    .conclusion
    .lhs
    .map
    is EHP_H_MAP
  )

  assert actual_equality_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    actual_equality_step.inference_rule
    == bridge_rule
  )

  assert actual_equality_step.premises == (
    formula_step,
  )

  assert formula_step.premises == (
    law_step,
    b_step,
  )

  assert law_step.premises == (
    hopf_step,
  )


def test_phase30_4_actual_h_equality_extends_through_right_composition():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  beta = HomotopyElement(
    name="beta",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  bridge_match = find_inference_match(
    bridge_rule,
    (
      hopf_step,
    ),
  )

  assert bridge_match is not None

  actual_h_equality_step = (
    apply_inference_match(
      bridge_match
    )
  )

  assert actual_h_equality_step.conclusion == Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=a,
    ),
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      actual_h_equality_step,
    ),
  )

  assert symmetry_match is not None

  reversed_equality_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  expected_reversed_equality = Relation(
    lhs=beta,
    rhs=MapApplication(
      map=EHP_H_MAP,
      expression=a,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert reversed_equality_step.conclusion == (
    expected_reversed_equality
  )

  suspended_b = Suspension(
    expression=b,
  )

  composition_rule = (
    equality_preserved_under_right_composition_inference_rule(
      suspended_b
    )
  )

  composition_match = find_inference_match(
    composition_rule,
    (
      reversed_equality_step,
    ),
  )

  assert composition_match is not None

  composition_step = apply_inference_match(
    composition_match
  )

  expected_composition_equality = Relation(
    lhs=Composition(
      left=beta,
      right=suspended_b,
    ),
    rhs=Composition(
      left=MapApplication(
        map=EHP_H_MAP,
        expression=a,
      ),
      right=suspended_b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert composition_step.conclusion == (
    expected_composition_equality
  )

  assert composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert composition_step.inference_rule == (
    composition_rule
  )

  assert composition_step.premises == (
    reversed_equality_step,
  )

  assert reversed_equality_step.premises == (
    actual_h_equality_step,
  )

  assert actual_h_equality_step.premises == (
    hopf_step,
  )


def test_phase30_5_prop22_right_formula_closes_as_actual_ehp_h_equality():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  b = HomotopyElement(
    name="b",
    dimension=1,
  )

  beta = HomotopyElement(
    name="beta",
    dimension=1,
  )

  suspended_b = Suspension(
    expression=b,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  law_rule = (
    hopf_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
    ),
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  b_step = ProofStep(
    conclusion=b,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  formula_rule = (
    hopf_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    (
      law_step,
      b_step,
    ),
  )

  assert formula_match is not None

  formula_step = apply_inference_match(
    formula_match
  )

  bridge_rule = (
    hopf_invariant_statement_to_ehp_h_equality_inference_rule()
  )

  formula_bridge_match = find_inference_match(
    bridge_rule,
    (
      formula_step,
    ),
  )

  assert formula_bridge_match is not None

  composed_h_equality_step = (
    apply_inference_match(
      formula_bridge_match
    )
  )

  expected_composed_h_equality = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=a,
        right=suspended_b,
      ),
    ),
    rhs=Composition(
      left=beta,
      right=suspended_b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    composed_h_equality_step.conclusion
    == expected_composed_h_equality
  )

  base_bridge_match = find_inference_match(
    bridge_rule,
    (
      hopf_step,
    ),
  )

  assert base_bridge_match is not None

  base_h_equality_step = (
    apply_inference_match(
      base_bridge_match
    )
  )

  expected_base_h_equality = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=a,
    ),
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  assert base_h_equality_step.conclusion == (
    expected_base_h_equality
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    (
      base_h_equality_step,
    ),
  )

  assert symmetry_match is not None

  reversed_base_h_equality_step = (
    apply_inference_match(
      symmetry_match
    )
  )

  expected_reversed_base_h_equality = (
    Relation(
      lhs=beta,
      rhs=MapApplication(
        map=EHP_H_MAP,
        expression=a,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert (
    reversed_base_h_equality_step
    .conclusion
    == expected_reversed_base_h_equality
  )

  composition_rule = (
    equality_preserved_under_right_composition_inference_rule(
      suspended_b
    )
  )

  composition_match = find_inference_match(
    composition_rule,
    (
      reversed_base_h_equality_step,
    ),
  )

  assert composition_match is not None

  right_composition_step = (
    apply_inference_match(
      composition_match
    )
  )

  expected_right_composition_equality = (
    Relation(
      lhs=Composition(
        left=beta,
        right=suspended_b,
      ),
      rhs=Composition(
        left=MapApplication(
          map=EHP_H_MAP,
          expression=a,
        ),
        right=suspended_b,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert (
    right_composition_step.conclusion
    == expected_right_composition_equality
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      composed_h_equality_step,
      right_composition_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  expected_final_formula = Relation(
    lhs=MapApplication(
      map=EHP_H_MAP,
      expression=Composition(
        left=a,
        right=suspended_b,
      ),
    ),
    rhs=Composition(
      left=MapApplication(
        map=EHP_H_MAP,
        expression=a,
      ),
      right=suspended_b,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.conclusion == (
    expected_final_formula
  )

  assert final_step.rule == (
    ProofRule.INFERENCE
  )

  assert final_step.inference_rule == (
    transitivity_rule
  )

  assert final_step.premises == (
    composed_h_equality_step,
    right_composition_step,
  )

  assert composed_h_equality_step.premises == (
    formula_step,
  )

  assert formula_step.premises == (
    law_step,
    b_step,
  )

  assert law_step.premises == (
    hopf_step,
  )

  assert right_composition_step.premises == (
    reversed_base_h_equality_step,
  )

  assert (
    reversed_base_h_equality_step.premises
    == (
      base_h_equality_step,
    )
  )

  assert base_h_equality_step.premises == (
    hopf_step,
  )






