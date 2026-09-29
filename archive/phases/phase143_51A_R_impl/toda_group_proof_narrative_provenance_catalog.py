from homotopy_groups import (
  TodaProp44DecompositionMap,
)
from toda_group_proof_narrative_catalog import (
  REFERENCE_STATEMENT_TYPES,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp58FiniteDimensionalStatement,
)


TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES = (
  *REFERENCE_STATEMENT_TYPES,
  TodaProp44DecompositionMap,
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp58FiniteDimensionalStatement,
)


def is_toda_group_proof_narrative_provenance_only_statement(
  statement,
) -> bool:
  return isinstance(
    statement,
    TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES,
  )
