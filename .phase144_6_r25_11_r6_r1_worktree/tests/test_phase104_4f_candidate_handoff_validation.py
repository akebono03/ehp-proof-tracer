from dataclasses import dataclass

import pytest

from proof import (
  InferenceRule,
)
from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
  RepositoryGeneratorApplicabilityHandoffValidationStatus,
  validate_repository_generator_applicability_handoff,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


@dataclass(frozen=True)
class Phase1044FGoal:
  value: str


def _handoff(
  goal=None,
):
  data = build_grouped_fixture()

  if goal is None:
    goal = Phase1044FGoal(
      value="wanted",
    )

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=data[
        "candidates"
      ][0],
      goal=goal,
    )
  )

  return handoff, data


def _entry(
  data,
  *,
  key,
  fixed_point_safe,
  conclusion_type=Phase1044FGoal,
  goal_compatibility=None,
  rule=None,
):
  if rule is None:
    rule = (
      data[
        "candidates"
      ][0]
      .candidate
      .inference_rule
    )

  return InferenceRuleCatalogEntry(
    key=key,
    rule=rule,
    conclusion_type=conclusion_type,
    fixed_point_safe=fixed_point_safe,
    goal_compatibility=goal_compatibility,
  )


def test_phase104_4f_ready_uses_same_rule_identity_safe_goal_compatible_entry():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()
  execution_entry = _entry(
    data,
    key="phase104.4f.ready",
    fixed_point_safe=True,
    goal_compatibility=(
      lambda goal:
      goal
      == Phase1044FGoal(
        value="wanted",
      )
    ),
  )
  catalog.register(
    execution_entry
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .READY
  )
  assert validation.handoff is handoff
  assert validation.execution_entry is execution_entry


def test_phase104_4f_same_rule_name_different_identity_is_not_execution_rule():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  different_rule = InferenceRule(
    name=(
      handoff
      .candidate
      .candidate
      .inference_rule
      .name
    ),
  )

  catalog.register(
    _entry(
      data,
      key="phase104.4f.same-name",
      fixed_point_safe=True,
      rule=different_rule,
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .RULE_NOT_IN_EXECUTION_CATALOG
  )
  assert validation.execution_entry is None


def test_phase104_4f_same_rule_without_safe_entry_reports_not_fixed_point_safe():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  catalog.register(
    _entry(
      data,
      key="phase104.4f.unsafe",
      fixed_point_safe=False,
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .RULE_NOT_FIXED_POINT_SAFE
  )
  assert validation.execution_entry is None


def test_phase104_4f_safe_same_rule_wrong_goal_type_is_goal_incompatible():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  catalog.register(
    _entry(
      data,
      key="phase104.4f.wrong-type",
      fixed_point_safe=True,
      conclusion_type=str,
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .GOAL_INCOMPATIBLE
  )
  assert validation.execution_entry is None


def test_phase104_4f_safe_same_rule_false_goal_guard_is_goal_incompatible():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  catalog.register(
    _entry(
      data,
      key="phase104.4f.false-guard",
      fixed_point_safe=True,
      goal_compatibility=(
        lambda goal: False
      ),
    )
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .GOAL_INCOMPATIBLE
  )
  assert validation.execution_entry is None


def test_phase104_4f_multiple_ready_entries_preserve_catalog_registration_order():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  first_entry = _entry(
    data,
    key="phase104.4f.first-ready",
    fixed_point_safe=True,
  )
  second_entry = _entry(
    data,
    key="phase104.4f.second-ready",
    fixed_point_safe=True,
  )

  catalog.register(
    first_entry
  )
  catalog.register(
    second_entry
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .READY
  )
  assert validation.execution_entry is first_entry


def test_phase104_4f_unrelated_invalid_goal_guard_does_not_affect_validation():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  unrelated_rule = InferenceRule(
    name="phase104 unrelated rule",
  )

  catalog.register(
    _entry(
      data,
      key="phase104.4f.unrelated-invalid",
      fixed_point_safe=True,
      goal_compatibility=(
        lambda goal: "invalid"
      ),
      rule=unrelated_rule,
    )
  )

  execution_entry = _entry(
    data,
    key="phase104.4f.ready-after-unrelated",
    fixed_point_safe=True,
  )
  catalog.register(
    execution_entry
  )

  validation = (
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )
  )

  assert validation.status is (
    RepositoryGeneratorApplicabilityHandoffValidationStatus
    .READY
  )
  assert validation.execution_entry is execution_entry


def test_phase104_4f_same_rule_invalid_goal_guard_preserves_existing_type_error():
  handoff, data = _handoff()
  catalog = InferenceRuleCatalog()

  catalog.register(
    _entry(
      data,
      key="phase104.4f.invalid-guard-result",
      fixed_point_safe=True,
      goal_compatibility=(
        lambda goal: "invalid"
      ),
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "goal_compatibility must return a bool"
    ),
  ):
    validate_repository_generator_applicability_handoff(
      handoff,
      catalog,
    )


def test_phase104_4f_rejects_non_handoff():
  with pytest.raises(
    TypeError,
    match=(
      "handoff must be a "
      "RepositoryGeneratorApplicabilityCandidateHandoff"
    ),
  ):
    validate_repository_generator_applicability_handoff(
      object(),
      InferenceRuleCatalog(),
    )


def test_phase104_4f_rejects_non_execution_catalog():
  handoff, _ = _handoff()

  with pytest.raises(
    TypeError,
    match=(
      "execution_catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    validate_repository_generator_applicability_handoff(
      handoff,
      object(),
    )
