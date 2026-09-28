from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_narrative_provenance_catalog import (
  TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES,
)
from toda_rules import (
  TodaEtaFamilyDefinitionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
)


def test_phase143_70_finite_dimensional_aggregate_types_are_provenance_only():
  expected_types = (
    TodaProp51FiniteDimensionalStatement,
    TodaProp53FiniteDimensionalStatement,
    TodaProp56FiniteDimensionalStatement,
    TodaProp58FiniteDimensionalStatement,
    TodaProp59FiniteDimensionalStatement,
    TodaProp511FiniteDimensionalStatement,
  )

  for statement_type in expected_types:
    assert (
      statement_type
      in TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES
    )


def test_phase143_70_eta_family_definition_is_not_suppressed():
  assert (
    TodaEtaFamilyDefinitionStatement
    not in TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES
  )


def test_phase143_70_scalar_constraint_is_not_suppressed():
  assert (
    ScalarGreaterEqualStatement
    not in TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES
  )
