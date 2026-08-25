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
  Zero,
)
from proof import (
  ProofStep,
  ImageStatement,
  KernelStatement,
  ExactnessStatement,
  InferenceTerminationReason,
  ProofRule,
  Relation,
  RelationType,
  apply_inference_match,
  derive_inference_round_result,
  find_inference_match,
  image_proof_step,
  kernel_proof_step,
  run_inference_until_stable_with_history,
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















