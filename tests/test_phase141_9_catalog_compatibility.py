from toda_group_proof_narrative_catalog import (
  REFERENCE_CANDIDATE_STATEMENT_TYPES,
  REFERENCE_STATEMENT_TYPES,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
)


def test_phase141_9_reference_candidate_catalog_remains_backward_compatible(
):
  assert REFERENCE_CANDIDATE_STATEMENT_TYPES == (
    Toda52CompositionIsomorphismStatement,
    TodaProp51FiniteDimensionalStatement,
    Toda55NuFamilyFiniteDimensionalStatement,
    Toda56Nu4DecompositionStatement,
    TodaProp44IsomorphismStatement,
  )


def test_phase141_9_general_reference_catalog_extends_without_mutating_candidates(
):
  assert REFERENCE_STATEMENT_TYPES == (
    Toda52CompositionIsomorphismStatement,
    Toda53NuPrimeBracketSpecializationStatement,
    TodaProp44IsomorphismStatement,
    TodaProp44SecondSummandRestrictionStatement,
    TodaProp51FiniteDimensionalStatement,
    Toda55NuFamilyFiniteDimensionalStatement,
    Toda56Nu4DecompositionStatement,
  )
