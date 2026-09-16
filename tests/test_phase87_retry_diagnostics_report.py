from repository_inference import (
  BoundedProducerSearchStatus,
  FiniteProducerRetryPolicy,
  build_depth_two_producer_search_report,
  diagnose_depth_two_producer_search_failure,
  repository_available_steps,
)

from test_phase87_selection_side_finite_retry import (
  build_phase87_3_data,
)


def test_phase87_4_without_retry_policy_preserves_ambiguous_diagnostic():
  data = build_phase87_3_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data["repository"],
      data["catalog"],
      data["goal"],
      max_depth=2,
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )

  assert diagnostic.producer_candidates == (
    data["first_a_rule"],
    data["second_a_rule"],
  )


def test_phase87_4_one_attempt_reports_retry_exhausted():
  data = build_phase87_3_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data["repository"],
      data["catalog"],
      data["goal"],
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=1,
      ),
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .PRODUCER_RETRY_EXHAUSTED
  )

  assert diagnostic.producer_candidates == (
    data["first_a_rule"],
  )


def test_phase87_4_two_attempts_clear_search_diagnostic():
  data = build_phase87_3_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data["repository"],
      data["catalog"],
      data["goal"],
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=2,
      ),
    )
  )

  assert diagnostic is None


def test_phase87_4_without_retry_policy_report_preserves_ambiguity():
  data = build_phase87_3_data()

  report = build_depth_two_producer_search_report(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .AMBIGUOUS_PRODUCER
  )
  assert report.search_result is None
  assert report.diagnostic is not None


def test_phase87_4_one_attempt_report_is_retry_exhausted():
  data = build_phase87_3_data()

  report = build_depth_two_producer_search_report(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=1,
    ),
  )

  assert report.status is (
    BoundedProducerSearchStatus
    .PRODUCER_RETRY_EXHAUSTED
  )
  assert report.search_result is None
  assert report.diagnostic is not None

  assert report.diagnostic.producer_candidates == (
    data["first_a_rule"],
  )


def test_phase87_4_two_attempt_report_succeeds_with_second_candidate():
  data = build_phase87_3_data()

  report = build_depth_two_producer_search_report(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )
  assert report.diagnostic is None
  assert report.search_result is not None

  assert tuple(
    node.producer_rule
    for node in report.search_result.producer_nodes
  ) == (
    data["second_a_rule"],
  )


def test_phase87_4_retry_diagnostics_and_report_preserve_repository():
  data = build_phase87_3_data()

  initial_steps = repository_available_steps(
    data["repository"]
  )

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data["repository"],
      data["catalog"],
      data["goal"],
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=2,
      ),
    )
  )

  report = build_depth_two_producer_search_report(
    data["repository"],
    data["catalog"],
    data["goal"],
    max_depth=2,
    retry_policy=FiniteProducerRetryPolicy(
      max_attempts=2,
    ),
  )

  assert diagnostic is None
  assert report.status is (
    BoundedProducerSearchStatus.SUCCESS
  )

  assert repository_available_steps(
    data["repository"]
  ) == initial_steps


def test_phase87_4_retry_exhausted_preserves_ambiguity_context():
  data = build_phase87_3_data()

  diagnostic = (
    diagnose_depth_two_producer_search_failure(
      data["repository"],
      data["catalog"],
      data["goal"],
      max_depth=2,
      retry_policy=FiniteProducerRetryPolicy(
        max_attempts=1,
      ),
    )
  )

  assert diagnostic is not None
  assert diagnostic.final_rule is data[
    "final_rule"
  ]
  assert diagnostic.requesting_rule is data[
    "final_rule"
  ]
  assert diagnostic.current_depth == 0
  assert diagnostic.required_next_depth == 1
  assert diagnostic.ancestor_rules == (
    data["final_rule"],
  )
