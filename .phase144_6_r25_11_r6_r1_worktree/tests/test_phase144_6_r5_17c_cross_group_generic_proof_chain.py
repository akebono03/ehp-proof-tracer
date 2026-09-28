from audit_phase144_6_r5_17c import (
  BASELINE_TARGET,
  CROSS_GROUP_TARGETS,
  GenericProofChainType,
  audit_cross_groups,
  baseline_chain_types,
)


def test_phase144_6_r5_17c_keeps_17b_baseline_and_five_cross_group_targets():
  assert BASELINE_TARGET == (3, 3)
  assert CROSS_GROUP_TARGETS == (
    (5, 3),
    (4, 6),
    (5, 7),
    (8, 7),
    (9, 7),
  )


def test_phase144_6_r5_17c_preserves_frozen_17b_type_schema():
  assert tuple(GenericProofChainType.__dataclass_fields__) == (
    "claim_role",
    "provider_kind",
    "provider_role",
  )


def test_phase144_6_r5_17c_preserves_known_pi6_3_chain_types():
  baseline = set(baseline_chain_types())
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
  assert GenericProofChainType(
    "order",
    "supporting_block",
    "calculation",
  ) in baseline


def test_phase144_6_r5_17c_applies_unchanged_extractor_to_all_five_groups():
  audits = audit_cross_groups()
  assert tuple((audit.n, audit.k) for audit in audits) == CROSS_GROUP_TARGETS
  assert all(audit.argument_audits for audit in audits)


def test_phase144_6_r5_17c_represents_every_argument_support_with_frozen_schema():
  audits = audit_cross_groups()
  occurrences = tuple(
    occurrence
    for audit in audits
    for argument in audit.argument_audits
    for occurrence in argument.occurrences
  )
  assert occurrences
  assert all(
    occurrence.chain_type.claim_role
    and occurrence.chain_type.provider_kind
    and occurrence.chain_type.provider_role
    for occurrence in occurrences
  )
  assert all(
    occurrence.direct_presentation_match_count > 0
    or occurrence.direct_semantic_match_count > 0
    for occurrence in occurrences
  )


def test_phase144_6_r5_17c_keeps_new_types_within_same_generic_vocabulary():
  new_types = {
    chain_type
    for audit in audit_cross_groups()
    for chain_type in audit.new_types
  }
  assert all(
    chain_type.provider_kind in {"supporting_block", "child_argument"}
    for chain_type in new_types
  )
  assert all(chain_type.claim_role for chain_type in new_types)
  assert all(chain_type.provider_role for chain_type in new_types)
