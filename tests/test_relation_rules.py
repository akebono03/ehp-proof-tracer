from expression import (
  Composition,
  Multiple,
  Zero,
  eta,
  nu,
  sigma,
)
from proof import (
  InferenceRejectionReason,
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  derive_inference_round_result,
  find_inference_match,
  order_relation,
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  order_implies_zero_multiple_inference_rule,
  zero_composition_equality_implies_zero_inference_rule,
  zero_composition_reverse_equality_implies_zero_inference_rule,
  zero_equality_implies_zero_inference_rule,
)


def test_order_implies_zero_multiple():
  order_step = relation_proof_step(
    order_relation(
      eta(3),
      2,
    )
  )

  rule = (
    order_implies_zero_multiple_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      order_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=Multiple(
        coefficient=2,
        expression=eta(3),
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    order_step,
  )


def test_order_implies_zero_multiple_rejects_non_order_relation():
  equality_step = relation_proof_step(
    Relation(
      lhs=eta(3),
      rhs=2,
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    order_implies_zero_multiple_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      equality_step,
    ),
  )

  assert match is None


def test_order_implies_zero_multiple_rejects_invalid_order():
  invalid_order_step = relation_proof_step(
    Relation(
      lhs=eta(3),
      rhs=0,
      relation_type=RelationType.ORDER,
    )
  )

  rule = (
    order_implies_zero_multiple_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      invalid_order_step,
    ),
  )

  assert match is None


def test_order_derived_zero_propagates_through_equality():
  element = eta(3)
  equivalent_expression = nu(4)

  order_step = relation_proof_step(
    order_relation(
      element,
      2,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=equivalent_expression,
      rhs=Multiple(
        coefficient=2,
        expression=element,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )

  order_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  zero_propagation_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        order_rule,
        zero_propagation_rule,
      ),
      (
        order_step,
        equality_step,
      ),
    )
  )

  order_derived_zero = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=element,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  propagated_zero = Relation(
    lhs=equivalent_expression,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert order_derived_zero in tuple(
    step.conclusion
    for step in result.steps
  )

  assert propagated_zero in tuple(
    step.conclusion
    for step in result.steps
  )

  order_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == order_derived_zero
  )

  propagated_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == propagated_zero
  )

  assert order_zero_step.premises == (
    order_step,
  )

  assert order_zero_step.inference_rule == (
    order_rule
  )

  assert propagated_zero_step.premises == (
    order_zero_step,
    equality_step,
  )

  assert (
    propagated_zero_step.inference_rule
    == zero_propagation_rule
  )


def test_zero_composition_equality_implies_zero():
  composition = Composition(
    left=nu(4),
    right=eta(3),
  )

  zero_composition_step = ProofStep(
    conclusion=Relation(
      lhs=composition,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=composition,
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_composition_step,
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=eta(4),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    zero_composition_step,
    equality_step,
  )


def test_zero_composition_equality_rule_rejects_noncomposition_zero_relation():
  zero_step = relation_proof_step(
    Relation(
      lhs=eta(3),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=eta(3),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
      equality_step,
    ),
  )

  assert match is None


def test_zero_composition_reverse_equality_implies_zero():
  composition = Composition(
    left=nu(4),
    right=eta(3),
  )

  zero_composition_step = ProofStep(
    conclusion=Relation(
      lhs=composition,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=composition,
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_composition_reverse_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_composition_step,
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=eta(4),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    zero_composition_step,
    equality_step,
  )


def test_zero_composition_reverse_equality_rule_rejects_noncomposition_zero_relation():
  zero_step = relation_proof_step(
    Relation(
      lhs=eta(3),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=eta(3),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = (
    zero_composition_reverse_equality_implies_zero_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_step,
      equality_step,
    ),
  )

  assert match is None


def test_equality_symmetry():
  equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = equality_symmetry_inference_rule()

  match = find_inference_match(
    rule,
    (
      equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=nu(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    equality_step,
  )


def test_equality_symmetry_rejects_non_equality_relation():
  zero_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  rule = equality_symmetry_inference_rule()

  match = find_inference_match(
    rule,
    (
      zero_step,
    ),
  )

  assert match is None


def test_equality_symmetry_reaches_fixed_point_after_duplicate_rejection():
  initial_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = equality_symmetry_inference_rule()

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        initial_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(result.round_results) == 1

  assert len(result.steps) == 2

  first_round = (
    result.round_results[0]
  )

  assert len(
    first_round.new_steps
  ) == 1

  reversed_step = (
    first_round.new_steps[0]
  )

  assert reversed_step.conclusion == (
    Relation(
      lhs=nu(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert reversed_step.rule == (
    ProofRule.INFERENCE
  )

  assert reversed_step.inference_rule == rule

  assert reversed_step.premises == (
    initial_step,
  )

  assert result.steps == (
    initial_step,
    reversed_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rule,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()

  assert len(
    terminal_round.matches
  ) == 2

  assert len(
    terminal_round.candidate_steps
  ) == 2

  assert len(
    terminal_round.duplicate_rejected_steps
  ) == 2

  assert tuple(
    candidate_step.conclusion
    for candidate_step
    in terminal_round.candidate_steps
  ) == (
    Relation(
      lhs=nu(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    ),
  )

  assert all(
    (
      application_result.accepted
      is False
    )
    for application_result
    in terminal_round.application_results
  )

  assert all(
    (
      application_result.rejection_reason
      == InferenceRejectionReason.ALREADY_KNOWN
    )
    for application_result
    in terminal_round.application_results
  )

  assert (
    terminal_round
    .application_results[1]
    .candidate_step
    .conclusion
  ) == initial_step.conclusion


def test_equality_transitivity():
  first_equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=nu(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = equality_transitivity_inference_rule()

  match = find_inference_match(
    rule,
    (
      first_equality_step,
      second_equality_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=eta(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    first_equality_step,
    second_equality_step,
  )


def test_equality_transitivity_rejects_mismatched_middle_expression():
  first_equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=sigma(4),
      rhs=eta(3),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = equality_transitivity_inference_rule()

  match = find_inference_match(
    rule,
    (
      first_equality_step,
      second_equality_step,
    ),
  )

  assert match is None


def test_equality_transitivity_rejects_non_equality_relation():
  zero_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  equality_step = relation_proof_step(
    Relation(
      lhs=Zero(),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = equality_transitivity_inference_rule()

  match = find_inference_match(
    rule,
    (
      zero_step,
      equality_step,
    ),
  )

  assert match is None


def test_equality_transitivity_closes_three_link_chain_over_two_rounds():
  first_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  second_step = relation_proof_step(
    Relation(
      lhs=nu(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  third_step = relation_proof_step(
    Relation(
      lhs=sigma(4),
      rhs=eta(5),
      relation_type=RelationType.EQUALITY,
    )
  )

  rule = equality_transitivity_inference_rule()

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        first_step,
        second_step,
        third_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert len(result.round_results) == 2

  assert len(result.steps) == 6

  first_round = (
    result.round_results[0]
  )

  assert len(
    first_round.new_steps
  ) == 2

  eta_sigma_step = (
    first_round.new_steps[0]
  )

  nu_eta_step = (
    first_round.new_steps[1]
  )

  assert eta_sigma_step.conclusion == (
    Relation(
      lhs=eta(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert eta_sigma_step.premises == (
    first_step,
    second_step,
  )

  assert nu_eta_step.conclusion == (
    Relation(
      lhs=nu(4),
      rhs=eta(5),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert nu_eta_step.premises == (
    second_step,
    third_step,
  )

  second_round = (
    result.round_results[1]
  )

  assert len(
    second_round.new_steps
  ) == 1

  eta_eta_step = (
    second_round.new_steps[0]
  )

  assert eta_eta_step.conclusion == (
    Relation(
      lhs=eta(4),
      rhs=eta(5),
      relation_type=RelationType.EQUALITY,
    )
  )

  assert eta_eta_step.rule == (
    ProofRule.INFERENCE
  )

  assert eta_eta_step.inference_rule == rule

  assert eta_eta_step.premises in (
    (
      first_step,
      nu_eta_step,
    ),
    (
      eta_sigma_step,
      third_step,
    ),
  )

  assert result.steps == (
    first_step,
    second_step,
    third_step,
    eta_sigma_step,
    nu_eta_step,
    eta_eta_step,
  )


def test_equality_symmetry_and_transitivity_close_connected_component():
  first_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  second_step = relation_proof_step(
    Relation(
      lhs=nu(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        symmetry_rule,
        transitivity_rule,
      ),
      (
        first_step,
        second_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert len(result.round_results) == 2

  assert len(
    result.round_results[0].new_steps
  ) == 3

  assert len(
    result.round_results[1].new_steps
  ) == 4

  assert len(result.steps) == 9

  expected_conclusions = {
    Relation(
      lhs=eta(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=eta(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=nu(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=nu(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=nu(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=sigma(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=sigma(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=sigma(4),
      rhs=sigma(4),
      relation_type=RelationType.EQUALITY,
    ),
  }

  actual_conclusions = {
    step.conclusion
    for step in result.steps
  }

  assert actual_conclusions == (
    expected_conclusions
  )


def test_equality_closure_propagates_zero_over_multiple_rounds():
  composition = Composition(
    left=sigma(4),
    right=eta(3),
  )

  zero_composition_step = relation_proof_step(
    Relation(
      lhs=composition,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  first_equality_step = relation_proof_step(
    Relation(
      lhs=eta(4),
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=composition,
      rhs=nu(4),
      relation_type=RelationType.EQUALITY,
    )
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  zero_rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  rules = (
    symmetry_rule,
    transitivity_rule,
    zero_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        zero_composition_step,
        first_equality_step,
        second_equality_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert len(result.round_results) == 3

  first_round_conclusions = {
    step.conclusion
    for step
    in result.round_results[0].new_steps
  }

  assert first_round_conclusions == {
    Relation(
      lhs=nu(4),
      rhs=eta(4),
      relation_type=RelationType.EQUALITY,
    ),
    Relation(
      lhs=nu(4),
      rhs=composition,
      relation_type=RelationType.EQUALITY,
    ),
  }

  second_round_conclusions = {
    step.conclusion
    for step
    in result.round_results[1].new_steps
  }

  assert Relation(
    lhs=eta(4),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  ) in second_round_conclusions

  assert Relation(
    lhs=nu(4),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  ) in second_round_conclusions

  third_round_conclusions = {
    step.conclusion
    for step
    in result.round_results[2].new_steps
  }

  expected_zero_relation = Relation(
    lhs=eta(4),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert expected_zero_relation in (
    third_round_conclusions
  )

  final_conclusions = {
    step.conclusion
    for step
    in result.steps
  }

  assert Relation(
    lhs=eta(4),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  ) in final_conclusions

  assert Relation(
    lhs=nu(4),
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  ) in final_conclusions

  assert Relation(
    lhs=nu(4),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  ) in final_conclusions

  assert expected_zero_relation in (
    final_conclusions
  )
















