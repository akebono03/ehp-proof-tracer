import pytest

from web_generator_proof import (
  build_standard_web_generator_proof_view,
)


def test_phase120_2_sigma11_generator_proof_uses_existing_known_group_result():
  view = (
    build_standard_web_generator_proof_view(
      "sigma_11"
    )
  )

  assert (
    view.generator_latex
    == r"\sigma_{11}"
  )

  assert (
    view.conclusion_latex
    == (
      r"\pi_{18}^{11} = "
      r"\mathbb{Z}/16\{\sigma_{11}\}"
    )
  )

  assert (
    view.max_depth
    == 1
  )


@pytest.mark.parametrize(
  "depth",
  (
    0,
    1,
    2,
  ),
)
def test_phase120_2_generator_proof_accepts_web_depths(
  depth,
):
  view = (
    build_standard_web_generator_proof_view(
      "sigma_11",
      max_depth=depth,
    )
  )

  assert (
    view.max_depth
    == depth
  )

  assert all(
    step.depth <= depth
    for step in view.steps
  )


def test_phase120_2_depth_zero_contains_only_root_step():
  view = (
    build_standard_web_generator_proof_view(
      "sigma_11",
      max_depth=0,
    )
  )

  assert len(
    view.steps
  ) == 1

  assert (
    view.steps[
      0
    ].depth
    == 0
  )


def test_phase120_2_nu_prime_preserves_existing_known_group_identity():
  view = (
    build_standard_web_generator_proof_view(
      "nu_prime"
    )
  )

  assert (
    view.generator_latex
    == r"\nu'"
  )

  assert (
    view.conclusion_latex
    == (
      r"\pi_{6}^{3} = "
      r"\mathbb{Z}/4\{\nu'\}"
    )
  )


def test_phase120_2_blank_generator_is_rejected():
  with pytest.raises(
    ValueError,
    match="generator is required",
  ):
    build_standard_web_generator_proof_view(
      "  "
    )


def test_phase120_2_negative_depth_is_rejected():
  with pytest.raises(
    ValueError,
    match="max_depth must be nonnegative",
  ):
    build_standard_web_generator_proof_view(
      "sigma_11",
      max_depth=-1,
    )
