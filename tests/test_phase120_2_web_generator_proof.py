import pytest

from web_generator_proof import (
  build_standard_web_generator_proof_view,
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
