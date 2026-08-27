import pytest

from ehp_rules import (
  EHPZeroCompositionStatement,
  ehp_exactness_implies_zero_composition_inference_rule,
)
from expression import (
  Composition,
  Multiple,
  Suspension,
  Zero,
  eta,
  nu,
)
from hopf_rules import (
  HopfCompositionLawStatement,
  HopfInvariantStatement,
  ehp_zero_composition_implies_suspended_hopf_zero_inference_rule,
  hopf_composition_formula_inference_rule,
  hopf_composition_law_inference_rule,
  hopf_invariant_proof_step,
  hopf_invariant_value_zero_inference_rule,
)
from proof import (
  ExactnessStatement,
  InferenceTerminationReason,
  LiteratureReference,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
  relation_proof_step,
  run_inference_round,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  composition_equality_to_zero_inference_rule,
  equality_symmetry_inference_rule,
  suspension_composition_functoriality_inference_rule,
  suspension_preserves_zero_inference_rule,
  zero_equality_implies_zero_inference_rule,
)


def test_hopf_invariant_statement():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  assert statement.expression == nu(4)
  assert statement.value == eta(7)


def test_hopf_invariant_statement_has_structural_equality():
  first = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  second = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  assert first == second


def test_hopf_invariant_statement_distinguishes_expression():
  first = HopfInvariantStatement(
    expression=eta(4),
    value=eta(7),
  )

  different_expression = (
    HopfInvariantStatement(
      expression=nu(4),
      value=eta(7),
    )
  )

  assert first != different_expression


def test_hopf_invariant_statement_distinguishes_value():
  first = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  different_value = (
    HopfInvariantStatement(
      expression=nu(4),
      value=Zero(),
    )
  )

  assert first != different_value


def test_hopf_invariant_statement_supports_zero_value():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=Zero(),
  )

  assert statement.value == Zero()


def test_hopf_invariant_statement_supports_multiple_value():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=Multiple(
      coefficient=2,
      expression=eta(7),
    ),
  )

  assert statement.value == Multiple(
    coefficient=2,
    expression=eta(7),
  )


def test_hopf_invariant_statement_preserves_provenance():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Hopf invariant fact",
  )

  statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
    source=reference,
    note="known generalized Hopf invariant fact",
  )

  assert statement.source == reference

  assert (
    statement.note
    == "known generalized Hopf invariant fact"
  )


def test_hopf_invariant_proof_step():
  statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  step = hopf_invariant_proof_step(
    statement
  )

  assert step.conclusion == statement
  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None


def test_hopf_invariant_proof_step_preserves_provenance():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Hopf invariant fact",
  )

  statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
    source=reference,
    note="known generalized Hopf invariant fact",
  )

  step = hopf_invariant_proof_step(
    statement
  )

  assert step.conclusion == statement

  assert (
    step.conclusion.source
    == reference
  )

  assert (
    step.conclusion.note
    == "known generalized Hopf invariant fact"
  )

  assert step.premises == ()
  assert step.rule == ProofRule.GIVEN
  assert step.inference_rule is None


def test_hopf_invariant_proof_step_rejects_non_hopf_statement():
  with pytest.raises(
    TypeError
  ):
    hopf_invariant_proof_step(
      eta(2)
    )


def test_hopf_composition_law_statement():
  statement = HopfCompositionLawStatement(
    alpha=nu(4),
    beta=eta(7),
  )

  assert statement.alpha == nu(4)
  assert statement.beta == eta(7)


def test_hopf_invariant_implies_hopf_composition_law_statement():
  hopf_statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  premise = hopf_invariant_proof_step(
    hopf_statement
  )

  rule = (
    hopf_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise,
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfCompositionLawStatement(
      alpha=nu(4),
      beta=eta(7),
    )
  )

  assert step.premises == (
    premise,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_hopf_composition_law_inference_preserves_hopf_fact_provenance():
  reference = LiteratureReference(
    label="Toda",
    author="H. Toda",
    title=(
      "Composition Methods in "
      "Homotopy Groups of Spheres"
    ),
    year=1962,
    locator="Hopf invariant fact",
  )

  hopf_statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
    source=reference,
    note=(
      "known generalized "
      "Hopf invariant fact"
    ),
  )

  premise = hopf_invariant_proof_step(
    hopf_statement
  )

  rule = (
    hopf_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise,
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfCompositionLawStatement(
      alpha=nu(4),
      beta=eta(7),
    )
  )

  assert step.premises == (
    premise,
  )

  assert (
    step.premises[0].conclusion.source
    == reference
  )

  assert (
    step.premises[0].conclusion.note
    == (
      "known generalized "
      "Hopf invariant fact"
    )
  )

  assert step.inference_rule == rule


def test_hopf_composition_law_inference_rejects_non_hopf_statement():
  premise = ProofStep(
    conclusion=eta(2),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_composition_law_inference_rule()
  )

  match = find_inference_match(
    rule,
    premise,
  )

  assert match is None


def test_hopf_composition_formula():
  law_statement = (
    HopfCompositionLawStatement(
      alpha=nu(4),
      beta=eta(7),
    )
  )

  law_step = ProofStep(
    conclusion=law_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  gamma = eta(8)

  gamma_step = ProofStep(
    conclusion=gamma,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      law_step,
      gamma_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfInvariantStatement(
      expression=Composition(
        left=nu(4),
        right=Suspension(
          expression=eta(8),
        ),
      ),
      value=Composition(
        left=eta(7),
        right=Suspension(
          expression=eta(8),
        ),
      ),
    )
  )

  assert step.premises == (
    law_step,
    gamma_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_hopf_invariant_reaches_hopf_composition_formula():
  hopf_statement = HopfInvariantStatement(
    expression=nu(4),
    value=eta(7),
  )

  hopf_step = hopf_invariant_proof_step(
    hopf_statement
  )

  law_rule = (
    hopf_composition_law_inference_rule()
  )

  law_match = find_inference_match(
    law_rule,
    hopf_step,
  )

  assert law_match is not None

  law_step = apply_inference_match(
    law_match
  )

  gamma = eta(8)

  gamma_step = ProofStep(
    conclusion=gamma,
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
      gamma_step,
    ),
  )

  assert formula_match is not None

  formula_step = apply_inference_match(
    formula_match
  )

  assert formula_step.conclusion == (
    HopfInvariantStatement(
      expression=Composition(
        left=nu(4),
        right=Suspension(
          expression=eta(8),
        ),
      ),
      value=Composition(
        left=eta(7),
        right=Suspension(
          expression=eta(8),
        ),
      ),
    )
  )

  assert formula_step.premises == (
    law_step,
    gamma_step,
  )

  assert law_step.premises == (
    hopf_step,
  )


def test_hopf_composition_formula_rejects_missing_law_statement():
  unrelated_step = ProofStep(
    conclusion=nu(4),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  gamma_step = ProofStep(
    conclusion=eta(8),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_composition_formula_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      unrelated_step,
      gamma_step,
    ),
  )

  assert match is None


def test_hopf_invariant_value_zero():
  value = Composition(
    left=eta(7),
    right=Suspension(
      expression=eta(8),
    ),
  )

  hopf_step = ProofStep(
    conclusion=HopfInvariantStatement(
      expression=nu(4),
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=value,
      rhs=Zero(),
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
      zero_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfInvariantStatement(
      expression=nu(4),
      value=Zero(),
    )
  )

  assert step.premises == (
    hopf_step,
    zero_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_hopf_invariant_value_zero_rejects_unrelated_zero():
  value = Composition(
    left=eta(7),
    right=Suspension(
      expression=eta(8),
    ),
  )

  unrelated_value = Composition(
    left=nu(7),
    right=Suspension(
      expression=eta(8),
    ),
  )

  hopf_step = ProofStep(
    conclusion=HopfInvariantStatement(
      expression=nu(4),
      value=value,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_step = ProofStep(
    conclusion=Relation(
      lhs=unrelated_value,
      rhs=Zero(),
      relation_type=(
        RelationType.ZERO
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      hopf_step,
      zero_step,
    ),
  )

  assert match is None


def test_hopf_invariant_zero_does_not_mean_expression_zero():
  hopf_step = ProofStep(
    conclusion=HopfInvariantStatement(
      expression=nu(4),
      value=Zero(),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    hopf_step,
  )

  assert match is None


def test_hopf_reasoning_connects_to_suspension_composition_functoriality():
  alpha = nu(4)
  delta = eta(7)
  gamma = eta(8)

  beta = Suspension(
    expression=delta,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=alpha,
      value=beta,
    )
  )

  gamma_step = ProofStep(
    conclusion=gamma,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  composition = Composition(
    left=delta,
    right=gamma,
  )

  zero_composition_fact = (
    relation_proof_step(
      Relation(
        lhs=composition,
        rhs=Zero(),
        relation_type=RelationType.EQUALITY,
        source="Toda",
        note=(
          "known zero composition "
          "for Phase 11-6"
        ),
      )
    )
  )

  hopf_law_rule = (
    hopf_composition_law_inference_rule()
  )

  composition_zero_rule = (
    composition_equality_to_zero_inference_rule()
  )

  functoriality_rule = (
    suspension_composition_functoriality_inference_rule()
  )

  first_round_steps = run_inference_round(
    (
      hopf_law_rule,
      composition_zero_rule,
      functoriality_rule,
    ),
    (
      hopf_step,
      gamma_step,
      zero_composition_fact,
    ),
  )

  hopf_law = HopfCompositionLawStatement(
    alpha=alpha,
    beta=beta,
  )

  zero_composition = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  functoriality_equality = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Composition(
      left=Suspension(
        expression=delta,
      ),
      right=Suspension(
        expression=gamma,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert hopf_law in tuple(
    step.conclusion
    for step in first_round_steps
  )

  assert zero_composition in tuple(
    step.conclusion
    for step in first_round_steps
  )

  assert functoriality_equality in tuple(
    step.conclusion
    for step in first_round_steps
  )

  hopf_formula_rule = (
    hopf_composition_formula_inference_rule()
  )

  suspension_zero_rule = (
    suspension_preserves_zero_inference_rule()
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  second_round_steps = run_inference_round(
    (
      hopf_formula_rule,
      suspension_zero_rule,
      symmetry_rule,
    ),
    first_round_steps,
  )

  hopf_formula = HopfInvariantStatement(
    expression=Composition(
      left=alpha,
      right=Suspension(
        expression=gamma,
      ),
    ),
    value=Composition(
      left=Suspension(
        expression=delta,
      ),
      right=Suspension(
        expression=gamma,
      ),
    ),
  )

  suspended_composition_zero = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  reversed_functoriality = Relation(
    lhs=Composition(
      left=Suspension(
        expression=delta,
      ),
      right=Suspension(
        expression=gamma,
      ),
    ),
    rhs=Suspension(
      expression=composition,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert hopf_formula in tuple(
    step.conclusion
    for step in second_round_steps
  )

  assert suspended_composition_zero in tuple(
    step.conclusion
    for step in second_round_steps
  )

  assert reversed_functoriality in tuple(
    step.conclusion
    for step in second_round_steps
  )

  zero_propagation_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  hopf_zero_rule = (
    hopf_invariant_value_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        zero_propagation_rule,
        hopf_zero_rule,
      ),
      second_round_steps,
    )
  )

  hopf_value = Composition(
    left=Suspension(
      expression=delta,
    ),
    right=Suspension(
      expression=gamma,
    ),
  )

  hopf_value_zero = Relation(
    lhs=hopf_value,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  final_hopf_zero = HopfInvariantStatement(
    expression=Composition(
      left=alpha,
      right=Suspension(
        expression=gamma,
      ),
    ),
    value=Zero(),
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert hopf_value_zero in conclusions
  assert final_hopf_zero in conclusions

  hopf_value_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == hopf_value_zero
  )

  final_hopf_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == final_hopf_zero
  )

  suspended_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == suspended_composition_zero
  )

  reversed_functoriality_step = next(
    step
    for step in result.steps
    if step.conclusion
    == reversed_functoriality
  )

  hopf_formula_step = next(
    step
    for step in result.steps
    if step.conclusion
    == hopf_formula
  )

  assert hopf_value_zero_step.premises == (
    suspended_zero_step,
    reversed_functoriality_step,
  )

  assert (
    hopf_value_zero_step.inference_rule
    == zero_propagation_rule
  )

  assert final_hopf_zero_step.premises == (
    hopf_formula_step,
    hopf_value_zero_step,
  )

  assert (
    final_hopf_zero_step.inference_rule
    == hopf_zero_rule
  )

  assert (
    final_hopf_zero_step.rule
    == ProofRule.INFERENCE
  )


def test_ehp_eh_zero_composition_implies_suspended_hopf_zero():
  e_map = type(
    "EMap",
    (),
    {
      "name": "E",
    },
  )()

  h_map = type(
    "HMap",
    (),
    {
      "name": "H",
    },
  )()

  ehp_step = ProofStep(
    conclusion=EHPZeroCompositionStatement(
      first_map=e_map,
      second_map=h_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  alpha = eta(7)

  alpha_step = ProofStep(
    conclusion=alpha,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    ehp_zero_composition_implies_suspended_hopf_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      ehp_step,
      alpha_step,
    ),
  )

  assert match is not None

  step = apply_inference_match(
    match
  )

  assert step.conclusion == (
    HopfInvariantStatement(
      expression=Suspension(
        expression=alpha,
      ),
      value=Zero(),
    )
  )

  assert step.premises == (
    ehp_step,
    alpha_step,
  )

  assert step.rule == ProofRule.INFERENCE
  assert step.inference_rule == rule


def test_ehp_h_p_zero_composition_does_not_imply_suspended_hopf_zero():
  h_map = type(
    "HMap",
    (),
    {
      "name": "H",
    },
  )()

  p_map = type(
    "PMap",
    (),
    {
      "name": "P",
    },
  )()

  ehp_step = ProofStep(
    conclusion=EHPZeroCompositionStatement(
      first_map=h_map,
      second_map=p_map,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  alpha_step = ProofStep(
    conclusion=eta(7),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    ehp_zero_composition_implies_suspended_hopf_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      ehp_step,
      alpha_step,
    ),
  )

  assert match is None


def test_ehp_exactness_reaches_suspended_hopf_zero():
  e_map = type(
    "EMap",
    (),
    {
      "name": "E",
    },
  )()

  h_map = type(
    "HMap",
    (),
    {
      "name": "H",
    },
  )()

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=e_map,
      second_map=h_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  alpha = eta(7)

  alpha_step = ProofStep(
    conclusion=alpha,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  first_round_steps = run_inference_round(
    zero_composition_rule,
    (
      exactness_step,
      alpha_step,
    ),
  )

  ehp_zero_composition = (
    EHPZeroCompositionStatement(
      first_map=e_map,
      second_map=h_map,
    )
  )

  assert ehp_zero_composition in tuple(
    step.conclusion
    for step in first_round_steps
  )

  hopf_zero_rule = (
    ehp_zero_composition_implies_suspended_hopf_zero_inference_rule()
  )

  second_round_steps = run_inference_round(
    hopf_zero_rule,
    first_round_steps,
  )

  hopf_zero = HopfInvariantStatement(
    expression=Suspension(
      expression=alpha,
    ),
    value=Zero(),
  )

  assert hopf_zero in tuple(
    step.conclusion
    for step in second_round_steps
  )

  ehp_zero_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == ehp_zero_composition
  )

  hopf_zero_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == hopf_zero
  )

  assert ehp_zero_step.premises == (
    exactness_step,
  )

  assert (
    ehp_zero_step.inference_rule
    == zero_composition_rule
  )

  assert hopf_zero_step.premises == (
    ehp_zero_step,
    alpha_step,
  )

  assert (
    hopf_zero_step.inference_rule
    == hopf_zero_rule
  )

  assert (
    hopf_zero_step.rule
    == ProofRule.INFERENCE
  )


def test_phase11_representative_hopf_and_ehp_scenario_reaches_fixed_point():
  alpha = nu(4)
  delta = eta(7)
  gamma = eta(8)

  beta = Suspension(
    expression=delta,
  )

  hopf_step = hopf_invariant_proof_step(
    HopfInvariantStatement(
      expression=alpha,
      value=beta,
      source=LiteratureReference(
        label="Phase 11 representative",
        author="Toda",
        title="Composition methods",
        year=1962,
        locator="representative Hopf fact",
      ),
    )
  )

  gamma_step = ProofStep(
    conclusion=gamma,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  composition = Composition(
    left=delta,
    right=gamma,
  )

  zero_composition_fact = (
    relation_proof_step(
      Relation(
        lhs=composition,
        rhs=Zero(),
        relation_type=RelationType.EQUALITY,
        source="Toda",
        note=(
          "known zero composition "
          "for Phase 11 representative "
          "scenario"
        ),
      )
    )
  )

  e_map = type(
    "EMap",
    (),
    {
      "name": "E",
    },
  )()

  h_map = type(
    "HMap",
    (),
    {
      "name": "H",
    },
  )()

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=e_map,
      second_map=h_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_round_steps = run_inference_round(
    (
      hopf_composition_law_inference_rule(),
      composition_equality_to_zero_inference_rule(),
      suspension_composition_functoriality_inference_rule(),
      ehp_exactness_implies_zero_composition_inference_rule(),
    ),
    (
      hopf_step,
      gamma_step,
      zero_composition_fact,
      exactness_step,
    ),
  )

  hopf_law = HopfCompositionLawStatement(
    alpha=alpha,
    beta=beta,
  )

  composition_zero = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  functoriality_equality = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Composition(
      left=Suspension(
        expression=delta,
      ),
      right=Suspension(
        expression=gamma,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  ehp_zero_composition = (
    EHPZeroCompositionStatement(
      first_map=e_map,
      second_map=h_map,
    )
  )

  first_round_conclusions = tuple(
    step.conclusion
    for step in first_round_steps
  )

  assert hopf_law in first_round_conclusions
  assert composition_zero in first_round_conclusions
  assert (
    functoriality_equality
    in first_round_conclusions
  )
  assert (
    ehp_zero_composition
    in first_round_conclusions
  )

  second_round_steps = run_inference_round(
    (
      hopf_composition_formula_inference_rule(),
      suspension_preserves_zero_inference_rule(),
      equality_symmetry_inference_rule(),
      ehp_zero_composition_implies_suspended_hopf_zero_inference_rule(),
    ),
    first_round_steps,
  )

  hopf_value = Composition(
    left=Suspension(
      expression=delta,
    ),
    right=Suspension(
      expression=gamma,
    ),
  )

  hopf_formula = HopfInvariantStatement(
    expression=Composition(
      left=alpha,
      right=Suspension(
        expression=gamma,
      ),
    ),
    value=hopf_value,
  )

  suspended_composition_zero = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  reversed_functoriality = Relation(
    lhs=hopf_value,
    rhs=Suspension(
      expression=composition,
    ),
    relation_type=RelationType.EQUALITY,
  )

  ehp_hopf_zero = HopfInvariantStatement(
    expression=Suspension(
      expression=gamma,
    ),
    value=Zero(),
  )

  second_round_conclusions = tuple(
    step.conclusion
    for step in second_round_steps
  )

  assert hopf_formula in second_round_conclusions
  assert (
    suspended_composition_zero
    in second_round_conclusions
  )
  assert (
    reversed_functoriality
    in second_round_conclusions
  )
  assert ehp_hopf_zero in second_round_conclusions

  result = (
    run_inference_until_stable_with_history(
      (
        zero_equality_implies_zero_inference_rule(),
        hopf_invariant_value_zero_inference_rule(),
      ),
      second_round_steps,
    )
  )

  hopf_value_zero = Relation(
    lhs=hopf_value,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  composition_hopf_zero = (
    HopfInvariantStatement(
      expression=Composition(
        left=alpha,
        right=Suspension(
          expression=gamma,
        ),
      ),
      value=Zero(),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert hopf_value_zero in conclusions
  assert composition_hopf_zero in conclusions
  assert ehp_hopf_zero in conclusions














