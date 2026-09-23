from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
  Suspension,
  Zero,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepository
from repository_operation_query import (
  RepositoryCompositionQuery,
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


def is_nu5_eta8_suspension_zero_operation_query(
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
    RepositoryCompositionQuery,
  ):
    return False

  return (
    query.operand.left.generator
    == GeneratorSymbol(
      family="ν",
      index=5,
    )
    and query.operand.right.generator
    == GeneratorSymbol(
      family="η",
      index=8,
    )
  )


def _matches_generator(
  value,
  expected: GeneratorSymbol,
) -> bool:
  return (
    isinstance(
      value,
      HomotopyElement,
    )
    and value.generator
    == expected
  )


def _is_pi9_5_nu5_eta8_group_relation(
  statement,
) -> bool:
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
      group_dimension=9,
      sphere_dimension=5,
    )
  ):
    return False

  if not isinstance(
    statement.rhs,
    FiniteCyclicGroup,
  ):
    return False

  if statement.rhs.order != 2:
    return False

  generator = statement.rhs.generator

  if not isinstance(
    generator,
    Composition,
  ):
    return False

  return (
    _matches_generator(
      generator.left,
      GeneratorSymbol(
        family="ν",
        index=5,
      ),
    )
    and _matches_generator(
      generator.right,
      GeneratorSymbol(
        family="η",
        index=8,
      ),
    )
  )


def _find_pi9_5_nu5_eta8_premise(
  pi10_6_zero_step: ProofStep,
) -> ProofStep | None:
  matches = tuple(
    premise
    for premise in pi10_6_zero_step.premises
    if (
      isinstance(
        premise,
        ProofStep,
      )
      and _is_pi9_5_nu5_eta8_group_relation(
        premise.conclusion
      )
    )
  )

  if len(matches) != 1:
    return None

  return matches[0]


def _is_derived_pi10_6_zero_step(
  step: ProofStep,
) -> bool:
  if not isinstance(
    step,
    ProofStep,
  ):
    return False

  if step.rule is not ProofRule.INFERENCE:
    return False

  if (
    step.conclusion
    != TodaPrimaryGroupZeroStatement(
      group=TodaPrimaryGroup(
        group_dimension=10,
        sphere_dimension=6,
      )
    )
  ):
    return False

  return (
    _find_pi9_5_nu5_eta8_premise(
      step
    )
    is not None
  )


def specialize_nu5_eta8_suspension_zero_step(
  pi10_6_zero_step: ProofStep,
) -> ProofStep:
  if not isinstance(
    pi10_6_zero_step,
    ProofStep,
  ):
    raise TypeError(
      "pi10_6_zero_step must be a ProofStep"
    )

  if not _is_derived_pi10_6_zero_step(
    pi10_6_zero_step
  ):
    raise ValueError(
      "pi10_6_zero_step must be the derived "
      "Toda Proposition 5.8 pi_10^6 zero step "
      "with pi_9^5 = Z/2{nu_5 eta_8} provenance"
    )

  pi9_5_step = (
    _find_pi9_5_nu5_eta8_premise(
      pi10_6_zero_step
    )
  )

  if pi9_5_step is None:
    raise RuntimeError(
      "validated pi_10^6 zero step lost "
      "its pi_9^5 provenance"
    )

  nu5_eta8 = (
    pi9_5_step
    .conclusion
    .rhs
    .generator
  )

  return ProofStep(
    conclusion=Relation(
      lhs=Suspension(
        expression=nu5_eta8,
      ),
      rhs=Zero(),
      relation_type=RelationType.ZERO,
    ),
    premises=(
      pi10_6_zero_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 128-2 theorem-specific handoff: "
      "E(nu_5 eta_8)=0 from the derived "
      "Toda Proposition 5.8 target group pi_10^6=0"
    ),
  )


def query_nu5_eta8_suspension_zero_handoff(
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

  if not is_nu5_eta8_suspension_zero_operation_query(
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
    if (
      node.root_entry.key
      != "standard.toda.prop58"
    ):
      continue

    if not _is_derived_pi10_6_zero_step(
      node.proof_step
    ):
      continue

    specialized_step = (
      specialize_nu5_eta8_suspension_zero_step(
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
