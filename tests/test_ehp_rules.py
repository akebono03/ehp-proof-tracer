from pathlib import Path

from ehp import EHPSegment
from ehp_rules import (
  EHPZeroCompositionStatement,
  ehp_exactness_image_implies_kernel_inference_rule,
  ehp_exactness_implies_zero_composition_inference_rule,
  ehp_exactness_inference_rule,
  ehp_exactness_kernel_implies_image_inference_rule,
  ehp_zero_composition_implies_zero_relation_inference_rule,
)
from expression import (
  Composition,
  Multiple,
  Suspension,
  Zero,
  eta,
  nu,
  sigma,
)
from proof import (
  ExactnessStatement,
  ImageStatement,
  InferenceTerminationReason,
  KernelStatement,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  apply_inference_match,
  derive_inference_round_result,
  find_inference_match,
  image_proof_step,
  kernel_proof_step,
  order_relation,
  relation_proof_step,
  run_inference_round,
  run_inference_until_stable_with_history,
)
from relation_rules import (
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  order_implies_zero_multiple_inference_rule,
  suspension_preserves_zero_inference_rule,
  suspension_preserves_zero_multiple_inference_rule,
  zero_composition_equality_implies_zero_inference_rule,
  zero_composition_reverse_equality_implies_zero_inference_rule,
  zero_equality_implies_zero_inference_rule,
)
from repository import SphereRepository


BASE_DIR = Path(__file__).resolve().parent.parent


def make_sphere_repository():
  return SphereRepository(
    BASE_DIR / "data" / "sphere.csv"
  )


def test_ehp_exactness_inference_rule_derives_exactness():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )
  exact_step = segment.exact_step_at_sphere()
  image_step = image_proof_step(
    exact_step.first_map
  )
  kernel_step = kernel_proof_step(
    exact_step.second_map
  )
  rule = ehp_exactness_inference_rule(
    exact_step
  )

  match = find_inference_match(
    rule,
    (image_step, kernel_step),
  )

  assert match is not None
  result = run_inference_until_stable_with_history(
    rule,
    (image_step, kernel_step),
  )

  assert len(result.steps) == 3
  derived_step = result.steps[-1]
  assert isinstance(
    derived_step.conclusion,
    ExactnessStatement,
  )
  assert derived_step.conclusion.is_exact
  assert derived_step.rule == ProofRule.INFERENCE
  assert derived_step.premises == (
    image_step,
    kernel_step,
  )
  assert derived_step.inference_rule == rule
  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )
  assert result.round_count == 1

  duplicate_round = derive_inference_round_result(
    rule,
    result.steps,
  )

  assert duplicate_round.new_steps == ()
  assert len(
    duplicate_round.duplicate_rejected_steps
  ) == 1
  assert duplicate_round.application_results[0].rejection_reason.value == (
    "already_known"
  )


def test_ehp_exactness_argument_free_rule_uses_conclusion_pattern():
  rule = ehp_exactness_inference_rule()

  assert rule.conclusion_builder is None

  assert isinstance(
    rule.conclusion_pattern,
    ExactnessStatement,
  )


def test_ehp_exactness_argument_free_rule_substitutes_maps_into_conclusion():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  rule = ehp_exactness_inference_rule()

  match = find_inference_match(
    rule,
    (
      image_step,
      kernel_step,
    ),
  )

  assert match is not None

  result = apply_inference_match(
    match
  )

  assert result.conclusion == ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  )

  assert result.rule == ProofRule.INFERENCE
  assert result.inference_rule == rule
  assert result.premises == (
    image_step,
    kernel_step,
  )


def test_ehp_exactness_image_implies_kernel_structure():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  rule = (
    ehp_exactness_image_implies_kernel_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      exactness_step,
      image_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    KernelStatement(
      group_map=exact_step.second_map,
      structure=(
        image_step.conclusion.structure
      ),
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    exactness_step,
    image_step,
  )


def test_ehp_exactness_image_implies_kernel_rejects_nonexact_pair():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  nonexact_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=False,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  rule = (
    ehp_exactness_image_implies_kernel_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      nonexact_step,
      image_step,
    ),
  )

  assert match is None


def test_ehp_exactness_kernel_implies_image_structure():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  rule = (
    ehp_exactness_kernel_implies_image_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      exactness_step,
      kernel_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    ImageStatement(
      group_map=exact_step.first_map,
      structure=(
        kernel_step.conclusion.structure
      ),
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    exactness_step,
    kernel_step,
  )


def test_ehp_exactness_kernel_implies_image_rejects_nonexact_pair():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  nonexact_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=False,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  rule = (
    ehp_exactness_kernel_implies_image_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      nonexact_step,
      kernel_step,
    ),
  )

  assert match is None


def test_ehp_exactness_rules_reach_fixed_point_together():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  image_implies_kernel_rule = (
    ehp_exactness_image_implies_kernel_inference_rule()
  )

  kernel_implies_image_rule = (
    ehp_exactness_kernel_implies_image_inference_rule()
  )

  rules = (
    exactness_rule,
    image_implies_kernel_rule,
    kernel_implies_image_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(result.steps) == 3

  assert len(
    result.round_results
  ) == 1

  assert len(
    result.round_results[0].new_steps
  ) == 1

  exactness_step = (
    result.round_results[0]
    .new_steps[0]
  )

  assert exactness_step.conclusion == (
    ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    )
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    exactness_step.inference_rule
    == exactness_rule
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()

  assert len(
    terminal_round.matches
  ) == 3

  assert len(
    terminal_round.candidate_steps
  ) == 3

  assert len(
    terminal_round.duplicate_rejected_steps
  ) == 3

  assert len(
    terminal_round.application_results
  ) == 3

  assert tuple(
    application_result
    .candidate_step
    .conclusion
    for application_result
    in terminal_round.application_results
  ) == (
    ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    ),
    KernelStatement(
      group_map=exact_step.second_map,
      structure=(
        image_step.conclusion.structure
      ),
    ),
    ImageStatement(
      group_map=exact_step.first_map,
      structure=(
        kernel_step.conclusion.structure
      ),
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
      application_result
      .rejection_reason
      .value
      == "already_known"
    )
    for application_result
    in terminal_round.application_results
  )


def test_ehp_exactness_implies_zero_composition():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  exactness_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      exactness_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  assert derived_step.rule == (
    ProofRule.INFERENCE
  )

  assert derived_step.inference_rule == rule

  assert derived_step.premises == (
    exactness_step,
  )


def test_ehp_exactness_zero_composition_rejects_nonexact_pair():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  nonexact_step = ProofStep(
    conclusion=ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=False,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      nonexact_step,
    ),
  )

  assert match is None


def test_ehp_exactness_derives_zero_composition_over_two_rounds():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      (
        exactness_rule,
        zero_composition_rule,
      ),
      (
        image_step,
        kernel_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2

  assert len(result.round_results) == 2

  assert len(result.steps) == 4

  first_round = result.round_results[0]

  assert len(first_round.new_steps) == 1

  exactness_step = (
    first_round.new_steps[0]
  )

  assert exactness_step.conclusion == (
    ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    )
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    exactness_step.inference_rule
    == exactness_rule
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  second_round = result.round_results[1]

  assert len(second_round.new_steps) == 1

  zero_composition_step = (
    second_round.new_steps[0]
  )

  assert zero_composition_step.conclusion == (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  assert zero_composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    zero_composition_step.inference_rule
    == zero_composition_rule
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  assert result.steps == (
    image_step,
    kernel_step,
    exactness_step,
    zero_composition_step,
  )


def test_ehp_zero_composition_implies_zero_relation():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  zero_composition_step = ProofStep(
    conclusion=(
      EHPZeroCompositionStatement(
        first_map=exact_step.first_map,
        second_map=exact_step.second_map,
      )
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      zero_composition_step,
    ),
  )

  assert match is not None

  derived_step = apply_inference_match(
    match
  )

  assert derived_step.conclusion == (
    Relation(
      lhs=Composition(
        left=exact_step.second_map,
        right=exact_step.first_map,
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
    zero_composition_step,
  )


def test_ehp_exactness_derives_zero_relation_over_three_rounds():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_composition_rule,
    zero_relation_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 3

  assert len(result.round_results) == 3

  assert len(result.steps) == 5

  first_round = (
    result.round_results[0]
  )

  assert len(
    first_round.new_steps
  ) == 1

  exactness_step = (
    first_round.new_steps[0]
  )

  assert exactness_step.conclusion == (
    ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    )
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    exactness_step.inference_rule
    == exactness_rule
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  second_round = (
    result.round_results[1]
  )

  assert len(
    second_round.new_steps
  ) == 1

  zero_composition_step = (
    second_round.new_steps[0]
  )

  assert zero_composition_step.conclusion == (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  assert zero_composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    zero_composition_step.inference_rule
    == zero_composition_rule
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  third_round = (
    result.round_results[2]
  )

  assert len(
    third_round.new_steps
  ) == 1

  zero_relation_step = (
    third_round.new_steps[0]
  )

  assert zero_relation_step.conclusion == (
    Relation(
      lhs=Composition(
        left=exact_step.second_map,
        right=exact_step.first_map,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert zero_relation_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    zero_relation_step.inference_rule
    == zero_relation_rule
  )

  assert zero_relation_step.premises == (
    zero_composition_step,
  )

  assert result.steps == (
    image_step,
    kernel_step,
    exactness_step,
    zero_composition_step,
    zero_relation_step,
  )


def test_ehp_inference_reaches_generic_zero_relation_over_four_rounds():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  equivalent_expression = eta(4)

  equality_step = relation_proof_step(
    Relation(
      lhs=equivalent_expression,
      rhs=composition,
      relation_type=RelationType.EQUALITY,
    )
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  zero_propagation_rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_composition_rule,
    zero_relation_rule,
    zero_propagation_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
        equality_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 4

  assert len(result.round_results) == 4

  assert len(result.steps) == 7

  first_round = (
    result.round_results[0]
  )

  assert len(
    first_round.new_steps
  ) == 1

  exactness_step = (
    first_round.new_steps[0]
  )

  assert exactness_step.conclusion == (
    ExactnessStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
      is_exact=True,
    )
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    exactness_step.inference_rule
    == exactness_rule
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  second_round = (
    result.round_results[1]
  )

  assert len(
    second_round.new_steps
  ) == 1

  zero_composition_step = (
    second_round.new_steps[0]
  )

  assert zero_composition_step.conclusion == (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  assert zero_composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    zero_composition_step.inference_rule
    == zero_composition_rule
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  third_round = (
    result.round_results[2]
  )

  assert len(
    third_round.new_steps
  ) == 1

  zero_relation_step = (
    third_round.new_steps[0]
  )

  assert zero_relation_step.conclusion == (
    Relation(
      lhs=composition,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert zero_relation_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    zero_relation_step.inference_rule
    == zero_relation_rule
  )

  assert zero_relation_step.premises == (
    zero_composition_step,
  )

  fourth_round = (
    result.round_results[3]
  )

  assert len(
    fourth_round.new_steps
  ) == 1

  propagated_zero_step = (
    fourth_round.new_steps[0]
  )

  assert propagated_zero_step.conclusion == (
    Relation(
      lhs=equivalent_expression,
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    )
  )

  assert propagated_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    propagated_zero_step.inference_rule
    == zero_propagation_rule
  )

  assert propagated_zero_step.premises == (
    zero_relation_step,
    equality_step,
  )

  assert result.steps == (
    image_step,
    kernel_step,
    equality_step,
    exactness_step,
    zero_composition_step,
    zero_relation_step,
    propagated_zero_step,
  )


def test_ehp_inference_reaches_zero_through_equality_closure():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  target_expression = eta(4)
  intermediate_expression = eta(5)

  first_equality_step = relation_proof_step(
    Relation(
      lhs=target_expression,
      rhs=intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=composition,
      rhs=intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  zero_propagation_rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_composition_rule,
    zero_relation_rule,
    symmetry_rule,
    transitivity_rule,
    zero_propagation_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
        first_equality_step,
        second_equality_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 4

  assert len(result.round_results) == 4

  first_round_conclusions = tuple(
    step.conclusion
    for step
    in result.round_results[0].new_steps
  )

  assert ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  ) in first_round_conclusions

  assert Relation(
    lhs=intermediate_expression,
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  ) in first_round_conclusions

  second_round_conclusions = tuple(
    step.conclusion
    for step
    in result.round_results[1].new_steps
  )

  assert EHPZeroCompositionStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
  ) in second_round_conclusions

  target_composition_relation = Relation(
    lhs=target_expression,
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )

  assert target_composition_relation in (
    second_round_conclusions
  )

  third_round_conclusions = tuple(
    step.conclusion
    for step
    in result.round_results[2].new_steps
  )

  zero_composition_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert zero_composition_relation in (
    third_round_conclusions
  )

  fourth_round_conclusions = tuple(
    step.conclusion
    for step
    in result.round_results[3].new_steps
  )

  target_zero_relation = Relation(
    lhs=target_expression,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  assert target_zero_relation in (
    fourth_round_conclusions
  )

  final_conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert target_composition_relation in (
    final_conclusions
  )

  assert zero_composition_relation in (
    final_conclusions
  )

  assert target_zero_relation in (
    final_conclusions
  )


def test_phase6_representative_end_to_end_scenario_reaches_fixed_point():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  target_expression = eta(4)
  intermediate_expression = eta(5)

  first_equality_step = relation_proof_step(
    Relation(
      lhs=target_expression,
      rhs=intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  second_equality_step = relation_proof_step(
    Relation(
      lhs=composition,
      rhs=intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  image_implies_kernel_rule = (
    ehp_exactness_image_implies_kernel_inference_rule()
  )

  kernel_implies_image_rule = (
    ehp_exactness_kernel_implies_image_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  zero_propagation_rule = (
    zero_composition_equality_implies_zero_inference_rule()
  )

  reverse_zero_propagation_rule = (
    zero_composition_reverse_equality_implies_zero_inference_rule()
  )

  rules = (
    exactness_rule,
    image_implies_kernel_rule,
    kernel_implies_image_rule,
    zero_composition_rule,
    zero_relation_rule,
    symmetry_rule,
    transitivity_rule,
    zero_propagation_rule,
    reverse_zero_propagation_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
        first_equality_step,
        second_equality_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 4

  exactness_relation = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  )

  zero_composition_statement = (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  zero_composition_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  target_composition_relation = Relation(
    lhs=target_expression,
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )

  reverse_target_composition_relation = Relation(
    lhs=composition,
    rhs=target_expression,
    relation_type=RelationType.EQUALITY,
  )

  target_zero_relation = Relation(
    lhs=target_expression,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  final_conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert exactness_relation in (
    final_conclusions
  )

  assert zero_composition_statement in (
    final_conclusions
  )

  assert zero_composition_relation in (
    final_conclusions
  )

  assert target_composition_relation in (
    final_conclusions
  )

  assert reverse_target_composition_relation in (
    final_conclusions
  )

  assert target_zero_relation in (
    final_conclusions
  )

  application_results = tuple(
    application_result
    for round_result in result.round_results
    for application_result
    in round_result.application_results
  )

  for rule in rules:
    assert any(
      (
        application_result
        .match
        .inference_rule
        is rule
      )
      for application_result
      in application_results
    )

  accepted_rules = tuple(
    application_result
    .match
    .inference_rule
    for application_result
    in application_results
    if application_result.accepted
  )

  assert exactness_rule in (
    accepted_rules
  )

  assert zero_composition_rule in (
    accepted_rules
  )

  assert zero_relation_rule in (
    accepted_rules
  )

  assert symmetry_rule in (
    accepted_rules
  )

  assert transitivity_rule in (
    accepted_rules
  )

  assert zero_propagation_rule in (
    accepted_rules
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_ehp_and_order_derived_zero_coexist_in_same_fixed_point_run():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  element = eta(3)

  order_step = relation_proof_step(
    order_relation(
      element,
      2,
    )
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  order_multiple = Multiple(
    coefficient=2,
    expression=element,
  )

  ehp_zero_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  order_zero_relation = Relation(
    lhs=order_multiple,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  ehp_zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  order_zero_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_composition_rule,
    ehp_zero_relation_rule,
    order_zero_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
        order_step,
      ),
    )
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert ehp_zero_relation in conclusions
  assert order_zero_relation in conclusions

  ehp_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == ehp_zero_relation
  )

  order_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == order_zero_relation
  )

  assert ehp_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert ehp_zero_step.inference_rule == (
    ehp_zero_relation_rule
  )

  assert order_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert order_zero_step.inference_rule == (
    order_zero_rule
  )

  assert order_zero_step.premises == (
    order_step,
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_ehp_and_order_branches_preserve_provenance_end_to_end():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  element = eta(3)

  order_step = relation_proof_step(
    order_relation(
      element,
      2,
    )
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  order_multiple = Multiple(
    coefficient=2,
    expression=element,
  )

  exactness_statement = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  )

  zero_composition_statement = (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  ehp_zero_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  order_zero_relation = Relation(
    lhs=order_multiple,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  ehp_zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  order_zero_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_composition_rule,
    ehp_zero_relation_rule,
    order_zero_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
        order_step,
      ),
    )
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  exactness_step = next(
    step
    for step in result.steps
    if step.conclusion
    == exactness_statement
  )

  zero_composition_step = next(
    step
    for step in result.steps
    if step.conclusion
    == zero_composition_statement
  )

  ehp_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == ehp_zero_relation
  )

  order_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == order_zero_relation
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert exactness_step.inference_rule == (
    exactness_rule
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  assert zero_composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    zero_composition_step.inference_rule
    == zero_composition_rule
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  assert ehp_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert ehp_zero_step.inference_rule == (
    ehp_zero_relation_rule
  )

  assert ehp_zero_step.premises == (
    zero_composition_step,
  )

  assert order_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert order_zero_step.inference_rule == (
    order_zero_rule
  )

  assert order_zero_step.premises == (
    order_step,
  )

  assert exactness_step not in (
    order_zero_step.premises
  )

  assert zero_composition_step not in (
    order_zero_step.premises
  )

  assert order_step not in (
    ehp_zero_step.premises
  )


def test_phase7_representative_end_to_end_scenario_reaches_fixed_point():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  ehp_intermediate_expression = eta(5)
  ehp_target_expression = eta(4)

  ehp_first_equality_step = relation_proof_step(
    Relation(
      lhs=composition,
      rhs=ehp_intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  ehp_second_equality_step = relation_proof_step(
    Relation(
      lhs=ehp_target_expression,
      rhs=ehp_intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  order_element = eta(3)

  order_multiple = Multiple(
    coefficient=2,
    expression=order_element,
  )

  order_step = relation_proof_step(
    order_relation(
      order_element,
      2,
    )
  )

  order_intermediate_expression = nu(4)
  order_target_expression = sigma(5)

  order_first_equality_step = relation_proof_step(
    Relation(
      lhs=order_multiple,
      rhs=order_intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  order_second_equality_step = relation_proof_step(
    Relation(
      lhs=order_target_expression,
      rhs=order_intermediate_expression,
      relation_type=RelationType.EQUALITY,
    )
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  image_implies_kernel_rule = (
    ehp_exactness_image_implies_kernel_inference_rule()
  )

  kernel_implies_image_rule = (
    ehp_exactness_kernel_implies_image_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  ehp_zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  order_zero_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  zero_propagation_rule = (
    zero_equality_implies_zero_inference_rule()
  )

  rules = (
    exactness_rule,
    image_implies_kernel_rule,
    kernel_implies_image_rule,
    zero_composition_rule,
    ehp_zero_relation_rule,
    order_zero_rule,
    symmetry_rule,
    transitivity_rule,
    zero_propagation_rule,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      (
        image_step,
        kernel_step,
        order_step,
        ehp_first_equality_step,
        ehp_second_equality_step,
        order_first_equality_step,
        order_second_equality_step,
      ),
    )
  )

  ehp_zero_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  order_zero_relation = Relation(
    lhs=order_multiple,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  ehp_target_equality = Relation(
    lhs=ehp_target_expression,
    rhs=composition,
    relation_type=RelationType.EQUALITY,
  )

  order_target_equality = Relation(
    lhs=order_target_expression,
    rhs=order_multiple,
    relation_type=RelationType.EQUALITY,
  )

  ehp_target_zero = Relation(
    lhs=ehp_target_expression,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  order_target_zero = Relation(
    lhs=order_target_expression,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert result.termination_reason == (
    InferenceTerminationReason.FIXED_POINT
  )

  assert ehp_zero_relation in conclusions
  assert order_zero_relation in conclusions

  assert ehp_target_equality in conclusions
  assert order_target_equality in conclusions

  assert ehp_target_zero in conclusions
  assert order_target_zero in conclusions

  ehp_target_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == ehp_target_zero
  )

  order_target_zero_step = next(
    step
    for step in result.steps
    if step.conclusion
    == order_target_zero
  )

  assert ehp_target_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert ehp_target_zero_step.inference_rule == (
    zero_propagation_rule
  )

  assert order_target_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert order_target_zero_step.inference_rule == (
    zero_propagation_rule
  )

  assert any(
    isinstance(
      premise.conclusion,
      Relation,
    )
    and premise.conclusion.relation_type
    == RelationType.ZERO
    for premise in ehp_target_zero_step.premises
  )

  assert any(
    isinstance(
      premise.conclusion,
      Relation,
    )
    and premise.conclusion.relation_type
    == RelationType.EQUALITY
    for premise in ehp_target_zero_step.premises
  )

  assert any(
    isinstance(
      premise.conclusion,
      Relation,
    )
    and premise.conclusion.relation_type
    == RelationType.ZERO
    for premise in order_target_zero_step.premises
  )

  assert any(
    isinstance(
      premise.conclusion,
      Relation,
    )
    and premise.conclusion.relation_type
    == RelationType.EQUALITY
    for premise in order_target_zero_step.premises
  )

  terminal_round = (
    derive_inference_round_result(
      rules,
      result.steps,
    )
  )

  assert terminal_round.new_steps == ()


def test_ehp_derived_zero_suspends_over_four_rounds():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  zero_relation_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  suspension_rule = (
    suspension_preserves_zero_inference_rule()
  )

  rules = (
    exactness_rule,
    zero_composition_rule,
    zero_relation_rule,
    suspension_rule,
  )

  first_round_steps = run_inference_round(
    rules,
    (
      image_step,
      kernel_step,
    ),
  )

  exactness_relation = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  )

  exactness_step = next(
    step
    for step in first_round_steps
    if step.conclusion == exactness_relation
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  assert (
    exactness_step.inference_rule
    is exactness_rule
  )

  assert (
    exactness_step.rule
    == ProofRule.INFERENCE
  )

  second_round_steps = run_inference_round(
    rules,
    first_round_steps,
  )

  zero_composition_statement = (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  zero_composition_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == zero_composition_statement
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  assert (
    zero_composition_step.inference_rule
    is zero_composition_rule
  )

  assert (
    zero_composition_step.rule
    == ProofRule.INFERENCE
  )

  third_round_steps = run_inference_round(
    rules,
    second_round_steps,
  )

  ehp_zero_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  ehp_zero_step = next(
    step
    for step in third_round_steps
    if step.conclusion == ehp_zero_relation
  )

  assert ehp_zero_step.premises == (
    zero_composition_step,
  )

  assert (
    ehp_zero_step.inference_rule
    is zero_relation_rule
  )

  assert (
    ehp_zero_step.rule
    == ProofRule.INFERENCE
  )

  fourth_round_steps = run_inference_round(
    rules,
    third_round_steps,
  )

  suspended_zero_relation = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  suspended_zero_step = next(
    step
    for step in fourth_round_steps
    if step.conclusion
    == suspended_zero_relation
  )

  assert suspended_zero_step.premises == (
    ehp_zero_step,
  )

  assert (
    suspended_zero_step.inference_rule
    is suspension_rule
  )

  assert (
    suspended_zero_step.rule
    == ProofRule.INFERENCE
  )


def test_phase8_representative_ehp_order_suspension_scenario():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  order_element = eta(3)

  order_step = relation_proof_step(
    order_relation(
      order_element,
      2,
    )
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  ehp_zero_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  order_zero_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  suspension_zero_rule = (
    suspension_preserves_zero_inference_rule()
  )

  suspension_multiple_rule = (
    suspension_preserves_zero_multiple_inference_rule()
  )

  first_round_steps = run_inference_round(
    (
      exactness_rule,
      order_zero_rule,
    ),
    (
      image_step,
      kernel_step,
      order_step,
    ),
  )

  exactness_relation = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  )

  order_zero_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=order_element,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  exactness_step = next(
    step
    for step in first_round_steps
    if step.conclusion
    == exactness_relation
  )

  order_zero_step = next(
    step
    for step in first_round_steps
    if step.conclusion
    == order_zero_relation
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  assert (
    exactness_step.inference_rule
    is exactness_rule
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert order_zero_step.premises == (
    order_step,
  )

  assert (
    order_zero_step.inference_rule
    is order_zero_rule
  )

  assert order_zero_step.rule == (
    ProofRule.INFERENCE
  )

  second_round_steps = run_inference_round(
    (
      zero_composition_rule,
      suspension_multiple_rule,
    ),
    first_round_steps,
  )

  zero_composition_statement = (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  suspended_order_zero_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=Suspension(
        expression=order_element,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  zero_composition_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == zero_composition_statement
  )

  suspended_order_zero_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == suspended_order_zero_relation
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  assert (
    zero_composition_step.inference_rule
    is zero_composition_rule
  )

  assert zero_composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert suspended_order_zero_step.premises == (
    order_zero_step,
  )

  assert (
    suspended_order_zero_step.inference_rule
    is suspension_multiple_rule
  )

  assert suspended_order_zero_step.rule == (
    ProofRule.INFERENCE
  )

  third_round_steps = run_inference_round(
    ehp_zero_rule,
    second_round_steps,
  )

  ehp_zero_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  ehp_zero_step = next(
    step
    for step in third_round_steps
    if step.conclusion
    == ehp_zero_relation
  )

  assert ehp_zero_step.premises == (
    zero_composition_step,
  )

  assert (
    ehp_zero_step.inference_rule
    is ehp_zero_rule
  )

  assert ehp_zero_step.rule == (
    ProofRule.INFERENCE
  )

  fourth_round_steps = run_inference_round(
    suspension_zero_rule,
    third_round_steps,
  )

  suspended_ehp_zero_relation = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  suspended_ehp_zero_step = next(
    step
    for step in fourth_round_steps
    if step.conclusion
    == suspended_ehp_zero_relation
  )

  assert suspended_ehp_zero_step.premises == (
    ehp_zero_step,
  )

  assert (
    suspended_ehp_zero_step.inference_rule
    is suspension_zero_rule
  )

  assert suspended_ehp_zero_step.rule == (
    ProofRule.INFERENCE
  )

  conclusions = tuple(
    step.conclusion
    for step in fourth_round_steps
  )

  assert ehp_zero_relation in conclusions

  assert order_zero_relation in conclusions

  assert suspended_ehp_zero_relation in (
    conclusions
  )

  assert suspended_order_zero_relation in (
    conclusions
  )

  assert order_step not in (
    suspended_ehp_zero_step.premises
  )

  assert exactness_step not in (
    suspended_order_zero_step.premises
  )

  assert ehp_zero_step not in (
    suspended_order_zero_step.premises
  )


def test_phase8_representative_provenance_chain_is_preserved():
  segment = EHPSegment(
    make_sphere_repository(),
    n=3,
    k=5,
  )

  exact_step = (
    segment.exact_step_at_sphere()
  )

  image_step = image_proof_step(
    exact_step.first_map
  )

  kernel_step = kernel_proof_step(
    exact_step.second_map
  )

  order_element = eta(3)

  order_step = relation_proof_step(
    order_relation(
      order_element,
      2,
    )
  )

  composition = Composition(
    left=exact_step.second_map,
    right=exact_step.first_map,
  )

  exactness_rule = (
    ehp_exactness_inference_rule()
  )

  zero_composition_rule = (
    ehp_exactness_implies_zero_composition_inference_rule()
  )

  ehp_zero_rule = (
    ehp_zero_composition_implies_zero_relation_inference_rule()
  )

  order_zero_rule = (
    order_implies_zero_multiple_inference_rule()
  )

  suspension_zero_rule = (
    suspension_preserves_zero_inference_rule()
  )

  suspension_multiple_rule = (
    suspension_preserves_zero_multiple_inference_rule()
  )

  first_round_steps = run_inference_round(
    (
      exactness_rule,
      order_zero_rule,
    ),
    (
      image_step,
      kernel_step,
      order_step,
    ),
  )

  exactness_relation = ExactnessStatement(
    first_map=exact_step.first_map,
    second_map=exact_step.second_map,
    is_exact=True,
  )

  order_zero_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=order_element,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  exactness_step = next(
    step
    for step in first_round_steps
    if step.conclusion
    == exactness_relation
  )

  order_zero_step = next(
    step
    for step in first_round_steps
    if step.conclusion
    == order_zero_relation
  )

  second_round_steps = run_inference_round(
    (
      zero_composition_rule,
      suspension_multiple_rule,
    ),
    first_round_steps,
  )

  zero_composition_statement = (
    EHPZeroCompositionStatement(
      first_map=exact_step.first_map,
      second_map=exact_step.second_map,
    )
  )

  suspended_order_zero_relation = Relation(
    lhs=Multiple(
      coefficient=2,
      expression=Suspension(
        expression=order_element,
      ),
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  zero_composition_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == zero_composition_statement
  )

  suspended_order_zero_step = next(
    step
    for step in second_round_steps
    if step.conclusion
    == suspended_order_zero_relation
  )

  third_round_steps = run_inference_round(
    ehp_zero_rule,
    second_round_steps,
  )

  ehp_zero_relation = Relation(
    lhs=composition,
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  ehp_zero_step = next(
    step
    for step in third_round_steps
    if step.conclusion
    == ehp_zero_relation
  )

  fourth_round_steps = run_inference_round(
    suspension_zero_rule,
    third_round_steps,
  )

  suspended_ehp_zero_relation = Relation(
    lhs=Suspension(
      expression=composition,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  suspended_ehp_zero_step = next(
    step
    for step in fourth_round_steps
    if step.conclusion
    == suspended_ehp_zero_relation
  )

  assert exactness_step.premises == (
    image_step,
    kernel_step,
  )

  assert exactness_step.inference_rule is (
    exactness_rule
  )

  assert exactness_step.rule == (
    ProofRule.INFERENCE
  )

  assert zero_composition_step.premises == (
    exactness_step,
  )

  assert (
    zero_composition_step.inference_rule
    is zero_composition_rule
  )

  assert zero_composition_step.rule == (
    ProofRule.INFERENCE
  )

  assert ehp_zero_step.premises == (
    zero_composition_step,
  )

  assert ehp_zero_step.inference_rule is (
    ehp_zero_rule
  )

  assert ehp_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert suspended_ehp_zero_step.premises == (
    ehp_zero_step,
  )

  assert (
    suspended_ehp_zero_step.inference_rule
    is suspension_zero_rule
  )

  assert suspended_ehp_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert order_zero_step.premises == (
    order_step,
  )

  assert order_zero_step.inference_rule is (
    order_zero_rule
  )

  assert order_zero_step.rule == (
    ProofRule.INFERENCE
  )

  assert suspended_order_zero_step.premises == (
    order_zero_step,
  )

  assert (
    suspended_order_zero_step.inference_rule
    is suspension_multiple_rule
  )

  assert suspended_order_zero_step.rule == (
    ProofRule.INFERENCE
  )

  ehp_branch_steps = (
    exactness_step,
    zero_composition_step,
    ehp_zero_step,
    suspended_ehp_zero_step,
  )

  order_branch_steps = (
    order_zero_step,
    suspended_order_zero_step,
  )

  assert all(
    order_step not in step.premises
    for step in ehp_branch_steps
  )

  assert all(
    image_step not in step.premises
    for step in order_branch_steps
  )

  assert all(
    kernel_step not in step.premises
    for step in order_branch_steps
  )

  assert exactness_step not in (
    suspended_order_zero_step.premises
  )

  assert zero_composition_step not in (
    suspended_order_zero_step.premises
  )

  assert ehp_zero_step not in (
    suspended_order_zero_step.premises
  )

  assert order_zero_step not in (
    suspended_ehp_zero_step.premises
  )

  assert suspended_order_zero_step not in (
    suspended_ehp_zero_step.premises
  )













