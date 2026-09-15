from dataclasses import dataclass
from enum import Enum

import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
)
from repository_inference import (
  BoundedProducerSearchDiagnostic,
  BoundedProducerSearchReport,
  BoundedProducerSearchStatus,
)
from test_phase84_unique_depth_two_producer_chain import (
  build_phase84_4_data,
)


@dataclass(frozen=True)
class Phase85DiagnosticPremiseStatement:
  pass


@dataclass(frozen=True)
class Phase85DiagnosticConclusionStatement:
  pass


def _requesting_rule():
  return InferenceRule(
    name="phase85 diagnostic requesting rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase85DiagnosticPremiseStatement
        ),
      ),
    ),
    conclusion_builder=(
      lambda premises: (
        Phase85DiagnosticConclusionStatement()
      )
    ),
  )


def _producer_rule(name):
  return InferenceRule(
    name=name,
    premise_patterns=(),
    conclusion_builder=(
      lambda premises: (
        Phase85DiagnosticPremiseStatement()
      )
    ),
  )


def test_phase85_2_status_is_enum():
  assert issubclass(
    BoundedProducerSearchStatus,
    Enum,
  )


@pytest.mark.parametrize(
  "status",
  tuple(
    BoundedProducerSearchStatus
  ),
)
def test_phase85_2_status_values_are_unique(status):
  assert isinstance(
    status.value,
    str,
  )
  assert status.value

  assert sum(
    candidate.value == status.value
    for candidate
    in BoundedProducerSearchStatus
  ) == 1


def test_phase85_2_diagnostic_preserves_failure_context():
  requesting_rule = _requesting_rule()
  producer_rule = _producer_rule(
    "phase85 safe producer"
  )
  unsafe_producer_rule = _producer_rule(
    "phase85 unsafe producer"
  )
  premise_pattern = (
    requesting_rule.premise_patterns[0]
  )
  goal = Phase85DiagnosticConclusionStatement()

  diagnostic = (
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .DEPTH_LIMIT
      ),
      goal=goal,
      final_rule=requesting_rule,
      final_rule_candidates=(
        requesting_rule,
      ),
      requesting_rule=requesting_rule,
      premise_index=0,
      premise_pattern=premise_pattern,
      current_depth=2,
      required_next_depth=3,
      producer_candidates=(
        producer_rule,
      ),
      unsafe_producer_candidates=(
        unsafe_producer_rule,
      ),
      ancestor_rules=(
        requesting_rule,
      ),
    )
  )

  assert diagnostic.goal == goal
  assert diagnostic.final_rule is requesting_rule
  assert diagnostic.final_rule_candidates == (
    requesting_rule,
  )
  assert diagnostic.requesting_rule is requesting_rule
  assert diagnostic.premise_index == 0
  assert diagnostic.premise_pattern == premise_pattern
  assert diagnostic.current_depth == 2
  assert diagnostic.required_next_depth == 3
  assert diagnostic.producer_candidates == (
    producer_rule,
  )
  assert diagnostic.unsafe_producer_candidates == (
    unsafe_producer_rule,
  )
  assert diagnostic.ancestor_rules == (
    requesting_rule,
  )


def test_phase85_2_success_report_preserves_phase84_result():
  data = build_phase84_4_data()
  phase84_result = data[
    "result"
  ]

  report = BoundedProducerSearchReport(
    status=BoundedProducerSearchStatus.SUCCESS,
    goal=phase84_result.goal,
    search_result=phase84_result,
  )

  assert report.search_result is phase84_result
  assert report.diagnostic is None


def test_phase85_2_failure_report_preserves_diagnostic():
  goal = Phase85DiagnosticConclusionStatement()
  diagnostic = (
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .NO_PRODUCER
      ),
      goal=goal,
    )
  )

  report = BoundedProducerSearchReport(
    status=(
      BoundedProducerSearchStatus
      .NO_PRODUCER
    ),
    goal=goal,
    diagnostic=diagnostic,
  )

  assert report.search_result is None
  assert report.diagnostic is diagnostic


def test_phase85_2_execution_failure_can_preserve_search_result():
  data = build_phase84_4_data()
  phase84_result = data[
    "result"
  ]
  diagnostic = (
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .PRODUCER_NOT_APPLICABLE
      ),
      goal=phase84_result.goal,
      final_rule=phase84_result.final_rule,
    )
  )

  report = BoundedProducerSearchReport(
    status=(
      BoundedProducerSearchStatus
      .PRODUCER_NOT_APPLICABLE
    ),
    goal=phase84_result.goal,
    search_result=phase84_result,
    diagnostic=diagnostic,
  )

  assert report.search_result is phase84_result
  assert report.diagnostic is diagnostic


def test_phase85_2_goal_already_available_has_no_failure_data():
  report = BoundedProducerSearchReport(
    status=(
      BoundedProducerSearchStatus
      .GOAL_ALREADY_AVAILABLE
    ),
    goal=Phase85DiagnosticConclusionStatement(),
  )

  assert report.search_result is None
  assert report.diagnostic is None


def test_phase85_2_diagnostic_rejects_success_status():
  with pytest.raises(
    ValueError,
    match=(
      "diagnostic status must describe a failure"
    ),
  ):
    BoundedProducerSearchDiagnostic(
      status=BoundedProducerSearchStatus.SUCCESS,
      goal=Phase85DiagnosticConclusionStatement(),
    )


def test_phase85_2_diagnostic_requires_complete_premise_context():
  requesting_rule = _requesting_rule()

  with pytest.raises(
    ValueError,
    match=(
      "requesting_rule, premise_index, and "
      "premise_pattern must be provided "
      "together"
    ),
  ):
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .NO_PRODUCER
      ),
      goal=Phase85DiagnosticConclusionStatement(),
      requesting_rule=requesting_rule,
    )


def test_phase85_2_diagnostic_rejects_wrong_premise_pattern():
  requesting_rule = _requesting_rule()

  with pytest.raises(
    ValueError,
    match=(
      "premise_pattern must match the "
      "requesting_rule premise"
    ),
  ):
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .NO_PRODUCER
      ),
      goal=Phase85DiagnosticConclusionStatement(),
      requesting_rule=requesting_rule,
      premise_index=0,
      premise_pattern=PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase85DiagnosticPremiseStatement
        ),
      ),
    )


def test_phase85_2_diagnostic_rejects_non_increasing_depth():
  with pytest.raises(
    ValueError,
    match=(
      "required_next_depth must be greater "
      "than current_depth"
    ),
  ):
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .DEPTH_LIMIT
      ),
      goal=Phase85DiagnosticConclusionStatement(),
      current_depth=2,
      required_next_depth=2,
    )


def test_phase85_2_success_report_requires_search_result():
  with pytest.raises(
    ValueError,
    match=(
      "successful report requires a "
      "search_result"
    ),
  ):
    BoundedProducerSearchReport(
      status=BoundedProducerSearchStatus.SUCCESS,
      goal=Phase85DiagnosticConclusionStatement(),
    )


def test_phase85_2_failure_report_requires_diagnostic():
  with pytest.raises(
    ValueError,
    match=(
      "failure report requires a diagnostic"
    ),
  ):
    BoundedProducerSearchReport(
      status=(
        BoundedProducerSearchStatus
        .NO_PRODUCER
      ),
      goal=Phase85DiagnosticConclusionStatement(),
    )


def test_phase85_2_report_requires_matching_status():
  goal = Phase85DiagnosticConclusionStatement()
  diagnostic = (
    BoundedProducerSearchDiagnostic(
      status=(
        BoundedProducerSearchStatus
        .NO_PRODUCER
      ),
      goal=goal,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "diagnostic status must match report status"
    ),
  ):
    BoundedProducerSearchReport(
      status=(
        BoundedProducerSearchStatus
        .AMBIGUOUS_PRODUCER
      ),
      goal=goal,
      diagnostic=diagnostic,
    )
