from enum import Enum

import pytest

from proof import (
  InferenceRule,
)
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
  RepositoryGeneratorApplicabilityHandoffValidation,
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def _handoff():
  data = build_grouped_fixture()

  return (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=data[
        "candidates"
      ][0],
      goal="phase104 goal",
    ),
    data,
  )


def _execution_entry(data):
  return InferenceRuleCatalogEntry(
    key="phase104.4e.execution",
    rule=(
      data[
        "candidates"
      ][0]
      .candidate
      .inference_rule
    ),
    conclusion_type=str,
    fixed_point_safe=True,
  )


def test_phase104_4e_status_is_enum():
  assert issubclass(
    RepositoryGeneratorApplicabilityHandoffValidationStatus,
    Enum,
  )


@pytest.mark.parametrize(
  "status",
  tuple(
    RepositoryGeneratorApplicabilityHandoffValidationStatus
  ),
)
def test_phase104_4e_status_values_are_unique(status):
  assert isinstance(
    status.value,
    str,
  )
  assert status.value

  assert sum(
    candidate.value == status.value
    for candidate
    in RepositoryGeneratorApplicabilityHandoffValidationStatus
  ) == 1


def test_phase104_4e_ready_preserves_handoff_and_execution_entry_identity():
  handoff, data = _handoff()
  execution_entry = _execution_entry(
    data
  )

  validation = (
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status=(
        RepositoryGeneratorApplicabilityHandoffValidationStatus
        .READY
      ),
      execution_entry=execution_entry,
    )
  )

  assert validation.handoff is handoff
  assert validation.execution_entry is execution_entry


@pytest.mark.parametrize(
  "status",
  (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .RULE_NOT_IN_EXECUTION_CATALOG,
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .RULE_NOT_FIXED_POINT_SAFE,
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .GOAL_INCOMPATIBLE,
  ),
)
def test_phase104_4e_failure_statuses_require_no_execution_entry(
  status,
):
  handoff, _ = _handoff()

  validation = (
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status=status,
    )
  )

  assert validation.handoff is handoff
  assert validation.execution_entry is None


def test_phase104_4e_ready_requires_execution_entry():
  handoff, _ = _handoff()

  with pytest.raises(
    ValueError,
    match=(
      "READY validation requires an "
      "execution_entry"
    ),
  ):
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status=(
        RepositoryGeneratorApplicabilityHandoffValidationStatus
        .READY
      ),
    )


def test_phase104_4e_failure_rejects_execution_entry():
  handoff, data = _handoff()
  execution_entry = _execution_entry(
    data
  )

  with pytest.raises(
    ValueError,
    match=(
      "failed validation must not contain an "
      "execution_entry"
    ),
  ):
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status=(
        RepositoryGeneratorApplicabilityHandoffValidationStatus
        .GOAL_INCOMPATIBLE
      ),
      execution_entry=execution_entry,
    )


def test_phase104_4e_rejects_invalid_handoff():
  with pytest.raises(
    TypeError,
    match=(
      "handoff must be a "
      "RepositoryGeneratorApplicabilityCandidateHandoff"
    ),
  ):
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=object(),
      status=(
        RepositoryGeneratorApplicabilityHandoffValidationStatus
        .RULE_NOT_IN_EXECUTION_CATALOG
      ),
    )


def test_phase104_4e_rejects_invalid_status():
  handoff, _ = _handoff()

  with pytest.raises(
    TypeError,
    match=(
      "status must be a "
      "RepositoryGeneratorApplicabilityHandoffValidationStatus"
    ),
  ):
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status="ready",
    )


def test_phase104_4e_rejects_invalid_execution_entry():
  handoff, _ = _handoff()

  with pytest.raises(
    TypeError,
    match=(
      "execution_entry must be an "
      "InferenceRuleCatalogEntry or None"
    ),
  ):
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status=(
        RepositoryGeneratorApplicabilityHandoffValidationStatus
        .READY
      ),
      execution_entry=object(),
    )


def test_phase104_4e_representation_does_not_validate_goal_or_safety():
  handoff, data = _handoff()

  unsafe_entry = InferenceRuleCatalogEntry(
    key="phase104.4e.unsafe",
    rule=InferenceRule(
      name="phase104 unrelated unsafe rule",
    ),
    conclusion_type=int,
    fixed_point_safe=False,
  )

  validation = (
    RepositoryGeneratorApplicabilityHandoffValidation(
      handoff=handoff,
      status=(
        RepositoryGeneratorApplicabilityHandoffValidationStatus
        .READY
      ),
      execution_entry=unsafe_entry,
    )
  )

  assert validation.handoff is handoff
  assert validation.execution_entry is unsafe_entry
  assert validation.execution_entry.fixed_point_safe is False
  assert validation.execution_entry.conclusion_type is int
