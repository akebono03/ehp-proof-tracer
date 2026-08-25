from pathlib import Path

from ehp import EHPSegment
from ehp_rules import ehp_exactness_inference_rule
from proof import (
  ExactnessStatement,
  InferenceTerminationReason,
  ProofRule,
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
