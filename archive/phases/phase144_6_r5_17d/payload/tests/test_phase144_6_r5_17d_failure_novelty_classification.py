from audit_phase144_6_r5_17d import (
  GenericProofChainType,
  NoveltyClassification,
  audit_cross_groups,
  baseline_chain_types,
  classify_chain_type,
  novelty_occurrences,
)


def test_phase144_6_r5_17d_preserves_17b_baseline_type_identity():
  baseline = baseline_chain_types()

  assert GenericProofChainType(
    "target",
    "child_argument",
    "establish_order",
  ) in baseline
  assert GenericProofChainType(
    "definition",
    "supporting_block",
    "precondition",
  ) in baseline


def test_phase144_6_r5_17d_classifies_reference_as_explicit_role_novelty():
  baseline = baseline_chain_types()

  classification = classify_chain_type(
    GenericProofChainType(
      "definition",
      "supporting_block",
      "reference",
    ),
    baseline,
  )

  assert classification is NoveltyClassification.EXPLICIT_ROLE_NOVELTY


def test_phase144_6_r5_17d_classifies_child_definition_as_argument_novelty():
  baseline = baseline_chain_types()

  classification = classify_chain_type(
    GenericProofChainType(
      "order",
      "child_argument",
      "establish_definition",
    ),
    baseline,
  )

  assert classification is NoveltyClassification.CHILD_ARGUMENT_NOVELTY


def test_phase144_6_r5_17d_classifies_other_as_semantic_gap_candidate():
  baseline = baseline_chain_types()

  classification = classify_chain_type(
    GenericProofChainType(
      "target",
      "supporting_block",
      "other",
    ),
    baseline,
  )

  assert (
    classification
    is NoveltyClassification.OTHER_ROLE_SEMANTIC_GAP_CANDIDATE
  )


def test_phase144_6_r5_17d_preserves_all_cross_group_direct_supports():
  occurrences = audit_cross_groups()

  assert len(occurrences) == 127
  assert all(item.direct_statement_types for item in occurrences)
  assert all(item.direct_rule_names for item in occurrences)


def test_phase144_6_r5_17d_recovers_six_novel_chain_types():
  novel_types = {
    item.chain_type
    for item in novelty_occurrences()
  }

  assert len(novel_types) == 6


def test_phase144_6_r5_17d_separates_all_three_novelty_classes():
  classifications = {
    item.classification
    for item in novelty_occurrences()
  }

  assert classifications == {
    NoveltyClassification.EXPLICIT_ROLE_NOVELTY,
    NoveltyClassification.CHILD_ARGUMENT_NOVELTY,
    NoveltyClassification.OTHER_ROLE_SEMANTIC_GAP_CANDIDATE,
  }
