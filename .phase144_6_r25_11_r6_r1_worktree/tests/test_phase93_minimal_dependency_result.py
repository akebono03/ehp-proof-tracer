import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from toda_proof_dependency import (
  TodaProofDependency,
  TodaProofDependencyResult,
)


def build_test_step(
  conclusion,
  premises=(),
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.GIVEN,
  )


def test_phase93_2_dependency_preserves_proof_step_identity():
  step = build_test_step(
    "dependency",
  )

  dependency = (
    TodaProofDependency(
      proof_step=step,
      depth=1,
    )
  )

  assert (
    dependency.proof_step
    is step
  )


def test_phase93_2_dependency_preserves_depth():
  step = build_test_step(
    "dependency",
  )

  dependency = (
    TodaProofDependency(
      proof_step=step,
      depth=3,
    )
  )

  assert dependency.depth == 3


def test_phase93_2_depth_one_dependency_is_direct():
  step = build_test_step(
    "dependency",
  )

  dependency = (
    TodaProofDependency(
      proof_step=step,
      depth=1,
    )
  )

  assert (
    dependency.is_direct
    is True
  )


def test_phase93_2_deeper_dependency_is_not_direct():
  step = build_test_step(
    "dependency",
  )

  dependency = (
    TodaProofDependency(
      proof_step=step,
      depth=2,
    )
  )

  assert (
    dependency.is_direct
    is False
  )


def test_phase93_2_dependency_requires_proof_step():
  with pytest.raises(
    TypeError,
    match=(
      "proof_step must be a ProofStep"
    ),
  ):
    TodaProofDependency(
      proof_step="not a proof step",
      depth=1,
    )


def test_phase93_2_dependency_depth_requires_int():
  step = build_test_step(
    "dependency",
  )

  with pytest.raises(
    TypeError,
    match="depth must be an int",
  ):
    TodaProofDependency(
      proof_step=step,
      depth="1",
    )


def test_phase93_2_dependency_depth_rejects_bool():
  step = build_test_step(
    "dependency",
  )

  with pytest.raises(
    TypeError,
    match="depth must be an int",
  ):
    TodaProofDependency(
      proof_step=step,
      depth=True,
    )


def test_phase93_2_dependency_depth_must_be_positive():
  step = build_test_step(
    "dependency",
  )

  with pytest.raises(
    ValueError,
    match="depth must be positive",
  ):
    TodaProofDependency(
      proof_step=step,
      depth=0,
    )


def test_phase93_2_result_preserves_root_step_identity():
  root_step = build_test_step(
    "root",
  )

  result = (
    TodaProofDependencyResult(
      root_step=root_step,
      dependencies=(),
    )
  )

  assert result.root_step is root_step


def test_phase93_2_result_preserves_dependency_order():
  first_step = build_test_step(
    "first",
  )

  second_step = build_test_step(
    "second",
  )

  first_dependency = (
    TodaProofDependency(
      proof_step=first_step,
      depth=1,
    )
  )

  second_dependency = (
    TodaProofDependency(
      proof_step=second_step,
      depth=2,
    )
  )

  result = (
    TodaProofDependencyResult(
      root_step=build_test_step(
        "root",
      ),
      dependencies=(
        first_dependency,
        second_dependency,
      ),
    )
  )

  assert result.dependencies == (
    first_dependency,
    second_dependency,
  )


def test_phase93_2_result_requires_root_proof_step():
  with pytest.raises(
    TypeError,
    match=(
      "root_step must be a ProofStep"
    ),
  ):
    TodaProofDependencyResult(
      root_step="not a proof step",
      dependencies=(),
    )


def test_phase93_2_result_requires_dependency_tuple():
  root_step = build_test_step(
    "root",
  )

  with pytest.raises(
    TypeError,
    match=(
      "dependencies must be a tuple"
    ),
  ):
    TodaProofDependencyResult(
      root_step=root_step,
      dependencies=[],
    )


def test_phase93_2_result_rejects_non_dependency_member():
  root_step = build_test_step(
    "root",
  )

  dependency_step = build_test_step(
    "dependency",
  )

  with pytest.raises(
    TypeError,
    match=(
      "dependencies must contain only "
      "TodaProofDependency objects"
    ),
  ):
    TodaProofDependencyResult(
      root_step=root_step,
      dependencies=(
        dependency_step,
      ),
    )


def test_phase93_2_result_rejects_root_as_dependency():
  root_step = build_test_step(
    "root",
  )

  dependency = (
    TodaProofDependency(
      proof_step=root_step,
      depth=1,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "root_step must not appear "
      "in dependencies"
    ),
  ):
    TodaProofDependencyResult(
      root_step=root_step,
      dependencies=(
        dependency,
      ),
    )


def test_phase93_2_result_rejects_duplicate_proof_step_identity():
  root_step = build_test_step(
    "root",
  )

  shared_step = build_test_step(
    "shared",
  )

  first_dependency = (
    TodaProofDependency(
      proof_step=shared_step,
      depth=1,
    )
  )

  second_dependency = (
    TodaProofDependency(
      proof_step=shared_step,
      depth=2,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "dependencies must not contain "
      "the same ProofStep more than once"
    ),
  ):
    TodaProofDependencyResult(
      root_step=root_step,
      dependencies=(
        first_dependency,
        second_dependency,
      ),
    )


def test_phase93_2_equal_but_distinct_steps_are_not_identity_duplicates():
  root_step = build_test_step(
    "root",
  )

  first_step = build_test_step(
    "same conclusion",
  )

  second_step = build_test_step(
    "same conclusion",
  )

  assert first_step == second_step
  assert first_step is not second_step

  first_dependency = (
    TodaProofDependency(
      proof_step=first_step,
      depth=1,
    )
  )

  second_dependency = (
    TodaProofDependency(
      proof_step=second_step,
      depth=1,
    )
  )

  result = (
    TodaProofDependencyResult(
      root_step=root_step,
      dependencies=(
        first_dependency,
        second_dependency,
      ),
    )
  )

  assert len(
    result.dependencies
  ) == 2
