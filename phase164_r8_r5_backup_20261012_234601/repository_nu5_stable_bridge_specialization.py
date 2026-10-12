from expression import (
  GeneratorSymbol,
  IteratedSuspension,
  ScalarProduct,
  ScalarSum,
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
  toda_nu_family_definition_statement,
)


def is_nu5_stable_bridge_operation_query(
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
      family="ν",
      index=5,
    )
  )


def _symbolic_nu5_stable_bridge_relation(
) -> Relation:
  n = ScalarSymbol(
    name="n",
  )

  nu_5 = (
    toda_nu_family_definition_statement(
      5
    ).element
  )

  nu_n = (
    toda_nu_family_definition_statement(
      n
    ).element
  )

  return Relation(
    lhs=IteratedSuspension(
      expression=nu_5,
      exponent=ScalarSum(
        left=n,
        right=ScalarProduct(
          left=-1,
          right=5,
        ),
      ),
    ),
    rhs=nu_n,
    relation_type=RelationType.EQUALITY,
  )


def specialize_nu5_stable_bridge_step(
  symbolic_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    symbolic_step.conclusion
    != _symbolic_nu5_stable_bridge_relation()
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "nu_5 stable-family bridge"
    )

  nu_5 = (
    toda_nu_family_definition_statement(
      5
    ).element
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  return ProofStep(
    conclusion=Relation(
      lhs=Suspension(
        expression=nu_5,
      ),
      rhs=nu_6,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 114-3 theorem-specific concrete "
      "specialization of the Toda Proposition 5.6 "
      "nu_5 stable-family bridge at n=6"
    ),
  )


def query_nu5_stable_bridge_handoff(
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

  if not is_nu5_stable_bridge_operation_query(
    query
  ):
    return RepositoryOperationQueryResult(
      query=query,
      matches=(),
    )

  scope = build_repository_proof_scope(
    repository
  )

  expected_symbolic_relation = (
    _symbolic_nu5_stable_bridge_relation()
  )

  matches = []

  for node in scope.nodes:
    if (
      node.proof_step.conclusion
      != expected_symbolic_relation
    ):
      continue

    specialized_step = (
      specialize_nu5_stable_bridge_step(
        node.proof_step
      )
    )

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
