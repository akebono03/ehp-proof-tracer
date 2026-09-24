from toda_rules import (
  Toda52CompositionIsomorphismStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaProp44IsomorphismStatement,
)


DEFINITION_STATEMENT_TYPES = (
  TodaNuFamilyDefinitionStatement,
  TodaSigmaFamilyDefinitionStatement,
)


REFERENCE_CANDIDATE_STATEMENT_TYPES = (
  Toda52CompositionIsomorphismStatement,
  TodaProp51FiniteDimensionalStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaProp44IsomorphismStatement,
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
