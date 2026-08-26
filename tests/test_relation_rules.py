from expression import (
  Composition,
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
  relation_proof_step,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  zero_composition_equality_implies_zero_inference_rule,
  zero_composition_reverse_equality_implies_zero_inference_rule,
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















