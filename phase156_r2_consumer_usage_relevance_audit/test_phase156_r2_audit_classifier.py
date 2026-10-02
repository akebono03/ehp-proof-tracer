from phase156_r2_consumer_usage_relevance_audit.audit_phase156_r2 import (
  CLASS_AGGREGATE_PARTIAL,
  CLASS_BOUNDARY_DIRECT,
  CLASS_INTERNAL_ONLY,
  CLASS_UNUSED,
  classify_consumer_usage,
)


def test_phase156_r2_boundary_direct_consumer():
  classification, _reason = classify_consumer_usage(
    has_external_consumer=True,
    has_internal_consumer=False,
    aggregate_component_used=False,
  )

  assert classification == CLASS_BOUNDARY_DIRECT


def test_phase156_r2_internal_consumer_only():
  classification, _reason = classify_consumer_usage(
    has_external_consumer=False,
    has_internal_consumer=True,
    aggregate_component_used=False,
  )

  assert classification == CLASS_INTERNAL_ONLY


def test_phase156_r2_no_consumer():
  classification, _reason = classify_consumer_usage(
    has_external_consumer=False,
    has_internal_consumer=False,
    aggregate_component_used=False,
  )

  assert classification == CLASS_UNUSED


def test_phase156_r2_aggregate_component_has_priority():
  classification, _reason = classify_consumer_usage(
    has_external_consumer=True,
    has_internal_consumer=True,
    aggregate_component_used=True,
  )

  assert classification == CLASS_AGGREGATE_PARTIAL
