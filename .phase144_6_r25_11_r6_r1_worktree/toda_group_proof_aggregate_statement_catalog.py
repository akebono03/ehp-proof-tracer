from toda_rules import (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda514SecondShortExactStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp56Pi8_5QuotientStatement,
)


TODA_GROUP_PROOF_AGGREGATE_STATEMENT_TYPES = (
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda514SecondShortExactStatement,
  Toda515Sigma8TransportedDecompositionStatement,
  TodaProp56Pi8_5QuotientStatement,
)


def is_toda_group_proof_aggregate_statement(
  statement,
) -> bool:
  return isinstance(
    statement,
    TODA_GROUP_PROOF_AGGREGATE_STATEMENT_TYPES,
  )
