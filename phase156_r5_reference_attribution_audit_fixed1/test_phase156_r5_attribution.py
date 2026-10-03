from phase156_r5_reference_attribution_audit.audit_phase156_r5_attribution import (
  CLASS_COMPOSITE_CONSUMER_OVERLAP,
  CLASS_COMPOSITE_CONSUMER_RULE_OVERLAP,
  CLASS_COMPOSITE_REFERENCE,
  CLASS_SINGLE_SOURCE,
  classify_reference_attribution,
  split_reference_components,
)


def test_phase156_r5_splits_composite_reference_locator():
  assert split_reference_components(
    "(5.3) / Lemma 5.2"
  ) == (
    "(5.3)",
    "Lemma 5.2",
  )


def test_phase156_r5_single_source_reference_is_not_suspicious():
  assert classify_reference_attribution(
    reference_title="Proposition 5.3",
    consumer_reference_titles=(
      "Lemma 5.4",
    ),
    consumer_rule_names=(
      "Toda Lemma 5.4 specialization",
    ),
  ) == CLASS_SINGLE_SOURCE


def test_phase156_r5_composite_reference_without_overlap_is_review_candidate():
  assert classify_reference_attribution(
    reference_title="(5.3) / Lemma 5.2",
    consumer_reference_titles=(),
    consumer_rule_names=(),
  ) == CLASS_COMPOSITE_REFERENCE


def test_phase156_r5_composite_reference_detects_consumer_reference_overlap():
  assert classify_reference_attribution(
    reference_title="(5.3) / Lemma 5.2",
    consumer_reference_titles=(
      "Lemma 5.2",
    ),
    consumer_rule_names=(),
  ) == CLASS_COMPOSITE_CONSUMER_OVERLAP


def test_phase156_r5_pi6_pattern_detects_consumer_rule_overlap():
  assert classify_reference_attribution(
    reference_title="(5.3) / Lemma 5.2",
    consumer_reference_titles=(
      "(5.3)",
    ),
    consumer_rule_names=(
      "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization",
    ),
  ) == CLASS_COMPOSITE_CONSUMER_OVERLAP


def test_phase156_r5_consumer_rule_overlap_is_detected_without_reference_overlap():
  assert classify_reference_attribution(
    reference_title="(5.3) / Lemma 5.2",
    consumer_reference_titles=(
      "Proposition 5.3",
    ),
    consumer_rule_names=(
      "Toda 5.3 nu-prime Lemma 5.2 Hopf specialization",
    ),
  ) == CLASS_COMPOSITE_CONSUMER_RULE_OVERLAP
