from toda_group_proof_narrative_catalog import (
  DEFINITION_STATEMENT_TYPES,
  REFERENCE_CANDIDATE_STATEMENT_TYPES,
  REFERENCE_STATEMENT_TYPES_BY_ROOT,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
)


def test_phase134_16_definition_catalog_contains_nu_and_sigma(
):
  assert DEFINITION_STATEMENT_TYPES == (
    TodaNuFamilyDefinitionStatement,
    TodaSigmaFamilyDefinitionStatement,
  )


def test_phase134_16_reference_candidate_catalog_contains_existing_types(
):
  assert REFERENCE_CANDIDATE_STATEMENT_TYPES == (
    Toda52CompositionIsomorphismStatement,
    TodaProp51FiniteDimensionalStatement,
    Toda55NuFamilyFiniteDimensionalStatement,
    Toda56Nu4DecompositionStatement,
  )


def test_phase134_16_pi6_3_reference_scope_is_unchanged(
):
  assert REFERENCE_STATEMENT_TYPES_BY_ROOT[
    (6, 3)
  ] == (
    Toda52CompositionIsomorphismStatement,
    TodaProp51FiniteDimensionalStatement,
  )


def test_phase134_16_pi8_5_reference_scope_is_unchanged(
):
  assert REFERENCE_STATEMENT_TYPES_BY_ROOT[
    (8, 5)
  ] == (
    Toda55NuFamilyFiniteDimensionalStatement,
    Toda56Nu4DecompositionStatement,
  )


def test_phase134_16_scoped_reference_types_are_candidates(
):
  candidate_types = set(
    REFERENCE_CANDIDATE_STATEMENT_TYPES
  )

  for scoped_types in (
    REFERENCE_STATEMENT_TYPES_BY_ROOT.values()
  ):
    assert set(
      scoped_types
    ).issubset(
      candidate_types
    )
