from expression import (
  Composition,
  HomotopyElement,
  MapApplication,
  SmashProduct,
  Suspension,
)
from hopf_rules import (
  HopfInvariantStatement,
  HopfLeftCompositionLawStatement,
  hopf_invariant_proof_step,
  hopf_invariant_statement_to_ehp_h_equality_inference_rule,
  hopf_left_composition_formula_inference_rule,
  hopf_left_composition_law_inference_rule,
)
from map_facts import (
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
  equality_preserved_under_left_composition_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
)


def test_phase32_1_left_hopf_formula_is_structurally_representable():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  suspended_c = Suspension(
    expression=c,
  )

  suspended_c_smash_c = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=suspended_c,
        right=a,
      ),
    ),
    rhs=Composition(
      left=suspended_c_smash_c,
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs == MapApplication(
    map=HOPF_MAP,
    expression=Composition(
      left=Suspension(
        expression=c,
      ),
      right=a,
    ),
  )

  assert statement.rhs == Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
  )

  assert statement.relation_type == (
    RelationType.EQUALITY
  )


def test_phase32_1_left_hopf_formula_preserves_suspended_left_factor():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    statement.lhs.expression,
    Composition,
  )

  assert isinstance(
    statement.lhs.expression.left,
    Suspension,
  )

  assert (
    statement
    .lhs
    .expression
    .left
    .expression
    == c
  )

  assert statement.lhs.expression.right == a


def test_phase32_1_left_hopf_formula_preserves_suspended_smash_product():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    statement.rhs,
    Composition,
  )

  assert isinstance(
    statement.rhs.left,
    Suspension,
  )

  assert isinstance(
    statement.rhs.left.expression,
    SmashProduct,
  )

  assert (
    statement
    .rhs
    .left
    .expression
    .left
    == c
  )

  assert (
    statement
    .rhs
    .left
    .expression
    .right
    == c
  )

  assert isinstance(
    statement.rhs.right,
    MapApplication,
  )

  assert statement.rhs.right.map is HOPF_MAP
  assert statement.rhs.right.expression == a


def test_phase32_1_left_hopf_formula_preserves_actual_hopf_map_identity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert statement.lhs.map is HOPF_MAP
  assert statement.rhs.right.map is HOPF_MAP


def test_phase32_1_left_hopf_formula_distinguishes_unsuspended_left_factor():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  different = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=c,
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula != different


def test_phase32_1_left_hopf_formula_distinguishes_unsuspended_smash_product():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  formula = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  different = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=SmashProduct(
        left=c,
        right=c,
      ),
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert formula != different


def test_phase32_2_hopf_statement_and_actual_h_equality_are_distinct():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  composed_expression = Composition(
    left=Suspension(
      expression=c,
    ),
    right=a,
  )

  value = Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=beta,
  )

  hopf_statement = HopfInvariantStatement(
    expression=composed_expression,
    value=value,
  )

  actual_h_equality = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=composed_expression,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )

  assert hopf_statement != actual_h_equality


def test_phase32_2_hopf_statement_preserves_left_formula_structure_without_map_identity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  hopf_statement = HopfInvariantStatement(
    expression=Composition(
      left=Suspension(
        expression=c,
      ),
      right=a,
    ),
    value=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=beta,
    ),
  )

  assert hopf_statement.expression == Composition(
    left=Suspension(
      expression=c,
    ),
    right=a,
  )

  assert hopf_statement.value == Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=beta,
  )

  assert not hasattr(
    hopf_statement,
    "map",
  )


def test_phase32_2_actual_h_equality_explicitly_preserves_hopf_map_identity():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  composed_expression = Composition(
    left=Suspension(
      expression=c,
    ),
    right=a,
  )

  value = Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=beta,
  )

  actual_h_equality = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=composed_expression,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )

  assert isinstance(
    actual_h_equality.lhs,
    MapApplication,
  )

  assert actual_h_equality.lhs.map is HOPF_MAP

  assert (
    actual_h_equality
    .lhs
    .expression
    == composed_expression
  )

  assert actual_h_equality.rhs == value

  assert (
    actual_h_equality.relation_type
    == RelationType.EQUALITY
  )


def test_phase32_2_same_expression_and_value_do_not_collapse_statement_families():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  expression = Composition(
    left=Suspension(
      expression=c,
    ),
    right=a,
  )

  value = Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=beta,
  )

  hopf_statement = HopfInvariantStatement(
    expression=expression,
    value=value,
  )

  actual_h_equality = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=expression,
    ),
    rhs=value,
    relation_type=RelationType.EQUALITY,
  )

  assert hopf_statement.expression == (
    actual_h_equality
    .lhs
    .expression
  )

  assert hopf_statement.value == (
    actual_h_equality.rhs
  )

  assert hopf_statement != actual_h_equality


def test_phase32_3_left_composition_law_statement_preserves_minimum_structure():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  statement = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=c,
  )

  assert statement.alpha == a
  assert statement.beta == beta
  assert statement.gamma == c


def test_phase32_3_left_composition_law_statement_has_structural_equality():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  first = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=c,
  )

  second = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=c,
  )

  assert first == second


def test_phase32_3_left_composition_law_statement_distinguishes_alpha():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  other_a = HomotopyElement(
    name="a′",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  first = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=c,
  )

  second = HopfLeftCompositionLawStatement(
    alpha=other_a,
    beta=beta,
    gamma=c,
  )

  assert first != second


def test_phase32_3_left_composition_law_statement_distinguishes_beta():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  other_beta = HomotopyElement(
    name="γ",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  first = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=c,
  )

  second = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=other_beta,
    gamma=c,
  )

  assert first != second


def test_phase32_3_left_composition_law_statement_distinguishes_gamma():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  other_c = HomotopyElement(
    name="d",
    dimension=1,
  )

  first = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=c,
  )

  second = HopfLeftCompositionLawStatement(
    alpha=a,
    beta=beta,
    gamma=other_c,
  )

  assert first != second


def test_phase32_4_hopf_invariant_and_c_derive_left_composition_law():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  c_step = ProofStep(
    conclusion=c,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_left_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
      c_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfLeftCompositionLawStatement(
      alpha=a,
      beta=beta,
      gamma=c,
    )
  )

  assert step.premises == (
    hopf_step,
    c_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_phase32_4_left_composition_law_derives_hopf_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  law_step = ProofStep(
    conclusion=HopfLeftCompositionLawStatement(
      alpha=a,
      beta=beta,
      gamma=c,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_left_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    law_step,
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfInvariantStatement(
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
      value=Composition(
        left=Suspension(
          expression=SmashProduct(
            left=c,
            right=c,
          ),
        ),
        right=beta,
      ),
    )
  )

  assert step.premises == (
    law_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_phase32_4_hopf_invariant_and_c_reach_left_composition_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  c_step = ProofStep(
    conclusion=c,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  law_rule = (
    hopf_left_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
      c_step,
    ),
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  formula_rule = (
    hopf_left_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    law_step,
  )

  assert formula_match is not None

  formula_step = apply_inference_match(
    formula_match
  )

  expected = HopfInvariantStatement(
    expression=Composition(
      left=Suspension(
        expression=c,
      ),
      right=a,
    ),
    value=Composition(
      left=Suspension(
        expression=SmashProduct(
          left=c,
          right=c,
        ),
      ),
      right=beta,
    ),
  )

  assert formula_step.conclusion == expected

  assert formula_step.premises == (
    law_step,
  )

  assert law_step.premises == (
    hopf_step,
    c_step,
  )


def test_phase32_4_left_composition_formula_preserves_provenance():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  c_step = ProofStep(
    conclusion=c,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  law_rule = (
    hopf_left_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
      c_step,
    ),
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  formula_rule = (
    hopf_left_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    law_step,
  )

  assert formula_match is not None

  formula_step = apply_inference_match(
    formula_match
  )

  assert formula_step.premises == (
    law_step,
  )

  assert formula_step.premises[0].premises == (
    hopf_step,
    c_step,
  )

  assert (
    formula_step
    .premises[0]
    .premises[0]
    == hopf_step
  )

  assert (
    formula_step
    .premises[0]
    .premises[1]
    == c_step
  )


def test_phase32_4_left_composition_law_rejects_missing_c():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  rule = (
    hopf_left_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    hopf_step,
  )

  assert match is None


def test_phase32_4_left_formula_rejects_plain_hopf_statement():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  rule = (
    hopf_left_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    hopf_step,
  )

  assert match is None


def test_phase32_5_base_hopf_statement_bridges_to_actual_h_equality():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
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
    hopf_step,
  )

  assert bridge_match is not None

  actual_h_step = apply_inference_match(
    bridge_match
  )

  assert actual_h_step.conclusion == Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    rhs=beta,
    relation_type=RelationType.EQUALITY,
  )

  assert actual_h_step.premises == (
    hopf_step,
  )

  assert actual_h_step.inference_rule == (
    bridge_rule
  )


def test_phase32_5_actual_h_equality_reverses_to_beta_equals_h_of_a():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
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
    hopf_step,
  )

  assert bridge_match is not None

  actual_h_step = apply_inference_match(
    bridge_match
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    actual_h_step,
  )

  assert symmetry_match is not None

  reversed_step = apply_inference_match(
    symmetry_match
  )

  assert reversed_step.conclusion == Relation(
    lhs=beta,
    rhs=MapApplication(
      map=HOPF_MAP,
      expression=a,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert reversed_step.premises == (
    actual_h_step,
  )

  assert reversed_step.inference_rule == (
    symmetry_rule
  )


def test_phase32_5_beta_equals_h_of_a_composes_on_left_by_suspended_smash():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  beta_equals_h_step = ProofStep(
    conclusion=Relation(
      lhs=beta,
      rhs=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  left_composition_rule = (
    equality_preserved_under_left_composition_inference_rule(
      suspended_smash,
    )
  )

  match = find_inference_match(
    left_composition_rule,
    beta_equals_h_step,
  )

  assert match is not None

  composed_step = apply_inference_match(
    match
  )

  assert composed_step.conclusion == Relation(
    lhs=Composition(
      left=suspended_smash,
      right=beta,
    ),
    rhs=Composition(
      left=suspended_smash,
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert composed_step.premises == (
    beta_equals_h_step,
  )

  assert composed_step.inference_rule == (
    left_composition_rule
  )


def test_phase32_5_base_hopf_fact_reaches_left_composed_actual_h_equality():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
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
    hopf_step,
  )

  assert bridge_match is not None

  actual_h_step = apply_inference_match(
    bridge_match
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    actual_h_step,
  )

  assert symmetry_match is not None

  reversed_step = apply_inference_match(
    symmetry_match
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  left_composition_rule = (
    equality_preserved_under_left_composition_inference_rule(
      suspended_smash,
    )
  )

  left_composition_match = find_inference_match(
    left_composition_rule,
    reversed_step,
  )

  assert left_composition_match is not None

  composed_step = apply_inference_match(
    left_composition_match
  )

  expected = Relation(
    lhs=Composition(
      left=suspended_smash,
      right=beta,
    ),
    rhs=Composition(
      left=suspended_smash,
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert composed_step.conclusion == expected

  assert composed_step.premises == (
    reversed_step,
  )

  assert reversed_step.premises == (
    actual_h_step,
  )

  assert actual_h_step.premises == (
    hopf_step,
  )


def test_phase32_6_transitivity_closes_left_prop22_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  middle = Composition(
    left=suspended_smash,
    right=beta,
  )

  first_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=HOPF_MAP,
        expression=Composition(
          left=Suspension(
            expression=c,
          ),
          right=a,
        ),
      ),
      rhs=middle,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=Relation(
      lhs=middle,
      rhs=Composition(
        left=suspended_smash,
        right=MapApplication(
          map=HOPF_MAP,
          expression=a,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    equality_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert match is not None

  final_step = apply_inference_match(
    match
  )

  assert final_step.conclusion == Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=suspended_smash,
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.premises == (
    first_step,
    second_step,
  )

  assert final_step.rule == ProofRule.INFERENCE
  assert final_step.inference_rule == rule


def test_phase32_6_base_hopf_fact_closes_left_prop22_formula():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  c_step = ProofStep(
    conclusion=c,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  law_rule = (
    hopf_left_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
      c_step,
    ),
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  formula_rule = (
    hopf_left_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    law_step,
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
    formula_step,
  )

  assert formula_bridge_match is not None

  left_equality_step = apply_inference_match(
    formula_bridge_match
  )

  base_bridge_match = find_inference_match(
    bridge_rule,
    hopf_step,
  )

  assert base_bridge_match is not None

  base_actual_h_step = apply_inference_match(
    base_bridge_match
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    base_actual_h_step,
  )

  assert symmetry_match is not None

  reversed_step = apply_inference_match(
    symmetry_match
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  left_composition_rule = (
    equality_preserved_under_left_composition_inference_rule(
      suspended_smash,
    )
  )

  left_composition_match = find_inference_match(
    left_composition_rule,
    reversed_step,
  )

  assert left_composition_match is not None

  right_equality_step = apply_inference_match(
    left_composition_match
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      left_equality_step,
      right_equality_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  expected = Relation(
    lhs=MapApplication(
      map=HOPF_MAP,
      expression=Composition(
        left=Suspension(
          expression=c,
        ),
        right=a,
      ),
    ),
    rhs=Composition(
      left=suspended_smash,
      right=MapApplication(
        map=HOPF_MAP,
        expression=a,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert final_step.conclusion == expected

  assert final_step.premises == (
    left_equality_step,
    right_equality_step,
  )


def test_phase32_6_left_prop22_final_formula_preserves_both_branches():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  c_step = ProofStep(
    conclusion=c,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  law_rule = (
    hopf_left_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    (
      hopf_step,
      c_step,
    ),
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  formula_rule = (
    hopf_left_composition_formula_inference_rule()
  )

  formula_match = find_inference_match(
    formula_rule,
    law_step,
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
    formula_step,
  )

  assert formula_bridge_match is not None

  left_equality_step = apply_inference_match(
    formula_bridge_match
  )

  base_bridge_match = find_inference_match(
    bridge_rule,
    hopf_step,
  )

  assert base_bridge_match is not None

  base_actual_h_step = apply_inference_match(
    base_bridge_match
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  symmetry_match = find_inference_match(
    symmetry_rule,
    base_actual_h_step,
  )

  assert symmetry_match is not None

  reversed_step = apply_inference_match(
    symmetry_match
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  left_composition_rule = (
    equality_preserved_under_left_composition_inference_rule(
      suspended_smash,
    )
  )

  left_composition_match = find_inference_match(
    left_composition_rule,
    reversed_step,
  )

  assert left_composition_match is not None

  right_equality_step = apply_inference_match(
    left_composition_match
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  transitivity_match = find_inference_match(
    transitivity_rule,
    (
      left_equality_step,
      right_equality_step,
    ),
  )

  assert transitivity_match is not None

  final_step = apply_inference_match(
    transitivity_match
  )

  assert final_step.premises == (
    left_equality_step,
    right_equality_step,
  )

  assert left_equality_step.premises == (
    formula_step,
  )

  assert formula_step.premises == (
    law_step,
  )

  assert law_step.premises == (
    hopf_step,
    c_step,
  )

  assert right_equality_step.premises == (
    reversed_step,
  )

  assert reversed_step.premises == (
    base_actual_h_step,
  )

  assert base_actual_h_step.premises == (
    hopf_step,
  )


def test_phase32_6_transitivity_rejects_mismatched_suspended_smash_middle():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  d = HomotopyElement(
    name="d",
    dimension=1,
  )

  first_middle = Composition(
    left=Suspension(
      expression=SmashProduct(
        left=c,
        right=c,
      ),
    ),
    right=beta,
  )

  second_middle = Composition(
    left=Suspension(
      expression=SmashProduct(
        left=d,
        right=d,
      ),
    ),
    right=beta,
  )

  first_step = ProofStep(
    conclusion=Relation(
      lhs=MapApplication(
        map=HOPF_MAP,
        expression=Composition(
          left=Suspension(
            expression=c,
          ),
          right=a,
        ),
      ),
      rhs=first_middle,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_step = ProofStep(
    conclusion=Relation(
      lhs=second_middle,
      rhs=Composition(
        left=Suspension(
          expression=SmashProduct(
            left=d,
            right=d,
          ),
        ),
        right=MapApplication(
          map=HOPF_MAP,
          expression=a,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    equality_transitivity_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      first_step,
      second_step,
    ),
  )

  assert match is None


def test_phase32_7_smash_product_typing_remains_unknown():
  c = HomotopyElement(
    name="c",
    dimension=3,
    source=6,
    target=3,
  )

  smash = SmashProduct(
    left=c,
    right=c,
  )

  assert not hasattr(
    smash,
    "source",
  )

  assert not hasattr(
    smash,
    "target",
  )


def test_phase32_7_suspended_smash_product_typing_remains_unknown():
  c = HomotopyElement(
    name="c",
    dimension=3,
    source=6,
    target=3,
  )

  suspended_smash = Suspension(
    expression=SmashProduct(
      left=c,
      right=c,
    ),
  )

  assert suspended_smash.source is None
  assert suspended_smash.target is None


def test_phase32_7_left_composition_law_requires_explicit_c():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  rule = (
    hopf_left_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    hopf_step,
  )

  assert match is None


def test_phase32_7_left_formula_requires_explicit_law_statement():
  a = HomotopyElement(
    name="a",
    dimension=1,
  )

  beta = HomotopyElement(
    name="β",
    dimension=1,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=a,
      value=beta,
    )
  )

  rule = (
    hopf_left_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    hopf_step,
  )

  assert match is None


def test_phase32_7_smash_product_is_not_automatically_simplified():
  c = HomotopyElement(
    name="c",
    dimension=1,
  )

  candidate = HomotopyElement(
    name="candidate",
    dimension=1,
  )

  smash = SmashProduct(
    left=c,
    right=c,
  )

  suspended_smash = Suspension(
    expression=smash,
  )

  candidate_suspension = Suspension(
    expression=candidate,
  )

  assert smash != candidate

  assert suspended_smash != (
    candidate_suspension
  )




