from audit_phase144_6_r5_17d_r1 import (
  OtherSemanticResolution,
  audit_other_providers,
)


def test_phase144_6_r5_17d_r1_recovers_all_nine_other_provider_occurrences():
  occurrences = audit_other_providers()

  assert len(occurrences) == 9


def test_phase144_6_r5_17d_r1_has_no_unresolved_other_provider():
  occurrences = audit_other_providers()

  assert all(
    item.resolution is not OtherSemanticResolution.UNRESOLVED
    for item in occurrences
  )


def test_phase144_6_r5_17d_r1_separates_aggregate_and_provenance_semantics():
  occurrences = audit_other_providers()

  resolutions = {
    item.resolution
    for item in occurrences
  }

  assert resolutions == {
    OtherSemanticResolution.AGGREGATE_STATEMENT,
    OtherSemanticResolution.PROVENANCE_ONLY_STATEMENT,
  }


def test_phase144_6_r5_17d_r1_does_not_double_classify_existing_catalogs():
  occurrences = audit_other_providers()

  assert all(
    not (item.aggregate and item.provenance_only)
    for item in occurrences
  )


def test_phase144_6_r5_17d_r1_identifies_known_aggregate_statement_types():
  occurrences = audit_other_providers()

  aggregate_types = {
    item.statement_type
    for item in occurrences
    if item.resolution is OtherSemanticResolution.AGGREGATE_STATEMENT
  }

  assert aggregate_types == {
    "TodaProp56Pi8_5QuotientStatement",
    "Toda515Sigma8TransportedDecompositionStatement",
    "Toda48Pi16_9OrderAndE4InjectiveStatement",
  }


def test_phase144_6_r5_17d_r1_identifies_known_provenance_only_statement_types():
  occurrences = audit_other_providers()

  provenance_types = {
    item.statement_type
    for item in occurrences
    if item.resolution is OtherSemanticResolution.PROVENANCE_ONLY_STATEMENT
  }

  assert provenance_types == {
    "TodaProp515Pi12_5HopfIsomorphismStatement",
    "TodaLemma514Sigma8Statement",
  }
