from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
)


DEFINITION_STATEMENT_TYPES = (
  TodaNuFamilyDefinitionStatement,
  TodaSigmaFamilyDefinitionStatement,
)


REFERENCE_CANDIDATE_STATEMENT_TYPES = (
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
)


REFERENCE_STATEMENT_TYPES = (
  REFERENCE_CANDIDATE_STATEMENT_TYPES
)


REFERENCE_STATEMENT_TYPES_BY_ROOT = {
  (6, 3): (
    Toda52CompositionIsomorphismStatement,
    TodaProp51FiniteDimensionalStatement,
  ),
  (8, 5): (
    Toda55NuFamilyFiniteDimensionalStatement,
    Toda56Nu4DecompositionStatement,
  ),
  (15, 8): (
    TodaProp44IsomorphismStatement,
  ),
}
