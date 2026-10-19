from probes.probe_phase87_capabilities import (
  build_phase87_representative_result,
)
from repository_inference import (
  BoundedProducerSearchStatus,
)


def test_phase87_probe_preserves_no_policy_ambiguity():
  result = (
    build_phase87_representative_result()
  )

  assert result[
    "no_policy_status"
  ] is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )


def test_phase87_probe_reports_retry_exhaustion_at_one_attempt():
  result = (
    build_phase87_representative_result()
  )

  assert result[
    "one_attempt_status"
  ] is (
    BoundedProducerSearchStatus
    .PRODUCER_RETRY_EXHAUSTED
  )


def test_phase87_probe_succeeds_at_two_attempts():
  result = (
    build_phase87_representative_result()
  )

  assert result[
    "two_attempt_status"
  ] is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert result[
    "selected_second_candidate"
  ]
  assert result[
    "goal_derived"
  ]


def test_phase87_probe_preserves_selected_path_provenance():
  result = (
    build_phase87_representative_result()
  )

  assert result[
    "selected_rule_reused"
  ]
  assert result[
    "final_uses_selected_step"
  ]
  assert result[
    "final_rule_reused"
  ]


def test_phase87_probe_excludes_failed_branch_from_execution():
  result = (
    build_phase87_representative_result()
  )

  assert not result[
    "failed_first_candidate_executed"
  ]
  assert not result[
    "failed_b_branch_executed"
  ]
  assert not result[
    "failed_c_branch_executed"
  ]


def test_phase87_probe_preserves_repository():
  result = (
    build_phase87_representative_result()
  )

  assert not result[
    "repository_mutated"
  ]
