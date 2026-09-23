from expression import (
  Composition,
  GeneratorSymbol,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
)
from toda_group_query import TodaGroupQuery
from toda_rules import (
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
)


def _is_symbolic_group_relation(
  step: ProofStep,
  *,
  stem: int,
  order: int,
) -> bool:
  if not isinstance(
    step,
    ProofStep,
  ):
    return False

  if (
    step.rule
    is not ProofRule.INFERENCE
  ):
    return False

  conclusion = step.conclusion

  if not isinstance(
    conclusion,
    Relation,
  ):
    return False

  if (
    conclusion.relation_type
    is not RelationType.EQUALITY
  ):
    return False

  n = ScalarSymbol(
    name="n",
  )

  if (
    conclusion.lhs
    != TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=stem,
      ),
      sphere_dimension=n,
    )
  ):
    return False

  return (
    isinstance(
      conclusion.rhs,
      FiniteCyclicGroup,
    )
    and conclusion.rhs.order
    == order
  )


def _is_symbolic_prop51_eta_group_step(
  step: ProofStep,
) -> bool:
  if not _is_symbolic_group_relation(
    step,
    stem=1,
    order=2,
  ):
    return False

  n = ScalarSymbol(
    name="n",
  )

  generator = getattr(
    step.conclusion.rhs.generator,
    "generator",
    None,
  )

  return (
    generator
    == GeneratorSymbol(
      family="η",
      index=n,
    )
  )


def _is_symbolic_prop53_eta_squared_group_step(
  step: ProofStep,
) -> bool:
  if not _is_symbolic_group_relation(
    step,
    stem=2,
    order=2,
  ):
    return False

  generator = (
    step.conclusion.rhs.generator
  )

  if not isinstance(
    generator,
    Composition,
  ):
    return False

  n = ScalarSymbol(
    name="n",
  )

  return (
    getattr(
      generator.left,
      "generator",
      None,
    )
    == GeneratorSymbol(
      family="η",
      index=n,
    )
    and getattr(
      generator.right,
      "generator",
      None,
    )
    == GeneratorSymbol(
      family="η",
      index=ScalarSum(
        left=n,
        right=1,
      ),
    )
  )


def _is_symbolic_prop56_nu_group_step(
  step: ProofStep,
) -> bool:
  if not _is_symbolic_group_relation(
    step,
    stem=3,
    order=8,
  ):
    return False

  n = ScalarSymbol(
    name="n",
  )

  generator = getattr(
    step.conclusion.rhs.generator,
    "generator",
    None,
  )

  return (
    generator
    == GeneratorSymbol(
      family="ν",
      index=n,
    )
  )


def specialize_toda_prop51_eta_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 3:
    raise ValueError(
      "index must be at least 3"
    )

  if not _is_symbolic_prop51_eta_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.1 eta-family group"
    )

  eta_definition = (
    toda_eta_family_definition_statement(
      index
    )
  )

  return ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 1,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_definition.element,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-6 theorem-specific concrete "
      "specialization of Toda Proposition 5.1 "
      f"at n={index}"
    ),
  )


def specialize_toda_prop53_eta_squared_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 5:
    raise ValueError(
      "index must be at least 5"
    )

  if not _is_symbolic_prop53_eta_squared_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.3 eta-squared group"
    )

  eta_n = (
    toda_eta_family_definition_statement(
      index
    ).element
  )
  eta_n_plus_one = (
    toda_eta_family_definition_statement(
      index + 1
    ).element
  )

  return ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 2,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=Composition(
          left=eta_n,
          right=eta_n_plus_one,
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-6 theorem-specific concrete "
      "specialization of Toda Proposition 5.3 "
      f"at n={index}"
    ),
  )


def specialize_toda_prop56_nu_index_step(
  symbolic_step: ProofStep,
  index: int,
) -> ProofStep:
  if not isinstance(
    symbolic_step,
    ProofStep,
  ):
    raise TypeError(
      "symbolic_step must be a ProofStep"
    )

  if (
    isinstance(
      index,
      bool,
    )
    or not isinstance(
      index,
      int,
    )
  ):
    raise TypeError(
      "index must be an int"
    )

  if index < 6:
    raise ValueError(
      "index must be at least 6"
    )

  if not _is_symbolic_prop56_nu_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.6 nu-family group"
    )

  nu_definition = (
    toda_nu_family_definition_statement(
      index
    )
  )

  return ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=index + 3,
        sphere_dimension=index,
      ),
      rhs=FiniteCyclicGroup(
        order=8,
        generator=nu_definition.element,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-6 theorem-specific concrete "
      "specialization of Toda Proposition 5.6 "
      f"at n={index}"
    ),
  )


def specialize_repository_proof_scope_for_toda_group_query(
  scope: RepositoryProofScopeResult,
  query: TodaGroupQuery,
) -> RepositoryProofScopeResult:
  if not isinstance(
    scope,
    RepositoryProofScopeResult,
  ):
    raise TypeError(
      "scope must be a RepositoryProofScopeResult"
    )

  if not isinstance(
    query,
    TodaGroupQuery,
  ):
    raise TypeError(
      "query must be a TodaGroupQuery"
    )

  if (
    query.k == 1
    and query.n >= 3
  ):
    predicate = (
      _is_symbolic_prop51_eta_group_step
    )
    specialize = (
      specialize_toda_prop51_eta_index_step
    )
  elif (
    query.k == 2
    and query.n >= 5
  ):
    predicate = (
      _is_symbolic_prop53_eta_squared_group_step
    )
    specialize = (
      specialize_toda_prop53_eta_squared_index_step
    )
  elif (
    query.k == 3
    and query.n >= 6
  ):
    predicate = (
      _is_symbolic_prop56_nu_group_step
    )
    specialize = (
      specialize_toda_prop56_nu_index_step
    )
  else:
    return scope

  specialized_nodes = []

  for node in scope.nodes:
    if not predicate(
      node.proof_step
    ):
      continue

    specialized_step = specialize(
      node.proof_step,
      query.n,
    )

    if any(
      existing.proof_step.conclusion
      == specialized_step.conclusion
      for existing in specialized_nodes
    ):
      continue

    specialized_nodes.append(
      RepositoryProofScopeNode(
        root_entry=node.root_entry,
        proof_step=specialized_step,
        shortest_depth=(
          node.shortest_depth
          + 1
        ),
      )
    )

  if not specialized_nodes:
    return scope

  return RepositoryProofScopeResult(
    repository=scope.repository,
    nodes=(
      scope.nodes
      + tuple(
        specialized_nodes
      )
    ),
  )
