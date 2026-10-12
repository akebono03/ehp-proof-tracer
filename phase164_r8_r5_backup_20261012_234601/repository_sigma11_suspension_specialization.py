from expression import (
  GeneratorSymbol,
  ScalarSymbol,
  Suspension,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryGeneratorQuery,
  RepositoryMapOperationQuery,
)
from repository_operation_query_lookup import (
  RepositoryOperationQueryMatch,
  RepositoryOperationQueryMatchKind,
  RepositoryOperationQueryResult,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from toda_rules import (
  TodaSigmaFamilyDefinitionStatement,
  toda_sigma_family_definition_statement,
)


def is_sigma11_suspension_operation_query(
  query,
) -> bool:
  if not isinstance(
    query,
    RepositoryMapOperationQuery,
  ):
    return False

  if query.operation != "E":
    return False

  if not isinstance(
    query.operand,
    RepositoryGeneratorQuery,
  ):
    return False

  return (
    query.operand.generator
    == GeneratorSymbol(
      family="σ",
      index=11,
    )
  )


def _is_symbolic_sigma_family_definition_step(
  step: ProofStep,
) -> bool:
  if not isinstance(
    step,
    ProofStep,
  ):
    return False

  if step.rule is not ProofRule.INFERENCE:
    return False

  statement = step.conclusion

  if not isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return False

  return (
    statement.index
    == ScalarSymbol(
      name="n",
    )
  )


def specialize_sigma11_suspension_step(
  symbolic_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if not _is_symbolic_sigma_family_definition_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda sigma-family definition"
    )

  sigma_family_statement = (
    symbolic_step.conclusion
  )

  sigma_11_definition = (
    toda_sigma_family_definition_statement(
      11,
      sigma_family_statement.sigma8_statement,
    )
  )

  sigma_12_definition = (
    toda_sigma_family_definition_statement(
      12,
      sigma_family_statement.sigma8_statement,
    )
  )

  return ProofStep(
    conclusion=Relation(
      lhs=Suspension(
        expression=sigma_11_definition.element,
      ),
      rhs=sigma_12_definition.element,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 115-4 theorem-specific concrete "
      "specialization of the Toda sigma-family "
      "definition from sigma_11 to sigma_12"
    ),
  )


def query_sigma11_suspension_handoff(
  repository: ProofRepository,
  query,
) -> RepositoryOperationQueryResult:
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not is_sigma11_suspension_operation_query(
    query
  ):
    return RepositoryOperationQueryResult(
      query=query,
      matches=(),
    )

  scope = build_repository_proof_scope(
    repository
  )

  matches = []

  for node in scope.nodes:
    if not _is_symbolic_sigma_family_definition_step(
      node.proof_step
    ):
      continue

    specialized_step = (
      specialize_sigma11_suspension_step(
        node.proof_step
      )
    )

    if any(
      match.statement
      == specialized_step.conclusion
      for match in matches
    ):
      continue

    specialized_node = (
      RepositoryProofScopeNode(
        root_entry=node.root_entry,
        proof_step=specialized_step,
        shortest_depth=(
          node.shortest_depth
          + 1
        ),
      )
    )

    matches.append(
      RepositoryOperationQueryMatch(
        scope_node=specialized_node,
        statement=specialized_step.conclusion,
        match_kind=(
          RepositoryOperationQueryMatchKind
          .SUSPENSION_RELATION
        ),
      )
    )

  return RepositoryOperationQueryResult(
    query=query,
    matches=tuple(
      matches
    ),
  )
