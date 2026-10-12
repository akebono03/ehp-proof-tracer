from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  GeneratorSymbol,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
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


def is_nu_prime_suspension_membership_operation_query(
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
      decoration="′",
    )
  )


def _is_prop56_pi7_4_decomposition_step(
  step: ProofStep,
) -> bool:
  if not isinstance(
    step,
    ProofStep,
  ):
    return False

  statement = step.conclusion

  if not isinstance(
    statement,
    Relation,
  ):
    return False

  if (
    statement.relation_type
    is not RelationType.EQUALITY
  ):
    return False

  if (
    statement.lhs
    != TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=4,
    )
  ):
    return False

  if not isinstance(
    statement.rhs,
    DirectSumGroup,
  ):
    return False

  if len(
    statement.rhs.summands
  ) != 2:
    return False

  first, second = (
    statement.rhs.summands
  )

  if not isinstance(
    first,
    FreeCyclicGroup,
  ):
    return False

  if (
    getattr(
      first.generator,
      "generator",
      None,
    )
    != GeneratorSymbol(
      family="ν",
      index=4,
    )
  ):
    return False

  if not isinstance(
    second,
    FiniteCyclicGroup,
  ):
    return False

  if second.order != 4:
    return False

  if not isinstance(
    second.generator,
    Suspension,
  ):
    return False

  return (
    getattr(
      second.generator.expression,
      "generator",
      None,
    )
    == GeneratorSymbol(
      family="ν",
      decoration="′",
    )
  )


def specialize_nu_prime_suspension_membership_step(
  group_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    group_step,
    ProofStep,
  ):
    raise TypeError(
      "group_step must be a ProofStep"
    )

  if not _is_prop56_pi7_4_decomposition_step(
    group_step
  ):
    raise ValueError(
      "group_step must prove the Toda Proposition 5.6 "
      "pi_7^4 decomposition with E(nu_prime) as the "
      "order-four generator"
    )

  e_nu_prime = (
    group_step
    .conclusion
    .rhs
    .summands[
      1
    ]
    .generator
  )

  return ProofStep(
    conclusion=HomotopyGroupMembershipStatement(
      element=e_nu_prime,
      group_dimension=7,
      sphere_dimension=4,
    ),
    premises=(
      group_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 129-4 theorem-specific membership handoff "
      "from the Toda Proposition 5.6 pi_7^4 decomposition"
    ),
  )


def query_nu_prime_suspension_membership_handoff(
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

  if not is_nu_prime_suspension_membership_operation_query(
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
    if not _is_prop56_pi7_4_decomposition_step(
      node.proof_step
    ):
      continue

    specialized_step = (
      specialize_nu_prime_suspension_membership_step(
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
          .GROUP_MEMBERSHIP
        ),
      )
    )

  return RepositoryOperationQueryResult(
    query=query,
    matches=tuple(
      matches
    ),
  )
