from expression import (
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
from toda_rules import (
  TodaSigmaFamilyDefinitionStatement,
  toda_sigma_family_definition_statement,
)


def is_toda_prop515_generic_sigma_specialization_generator(
  generator: GeneratorSymbol,
) -> bool:
  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    return False

  if (
    generator.family
    != "σ"
  ):
    return False

  if (
    generator.decoration
    is not None
  ):
    return False

  if (
    isinstance(
      generator.index,
      bool,
    )
    or not isinstance(
      generator.index,
      int,
    )
  ):
    return False

  return (
    generator.index
    >= 10
  )


def _is_symbolic_prop515_sigma_group_step(
  step: ProofStep,
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
        right=7,
      ),
      sphere_dimension=n,
    )
  ):
    return False

  if not isinstance(
    conclusion.rhs,
    FiniteCyclicGroup,
  ):
    return False

  if (
    conclusion.rhs.order
    != 16
  ):
    return False

  generator = getattr(
    conclusion.rhs.generator,
    "generator",
    None,
  )

  return (
    generator
    == GeneratorSymbol(
      family="σ",
      index=n,
    )
  )


def specialize_toda_prop515_sigma_index_step(
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

  if index < 10:
    raise ValueError(
      "index must be at least 10"
    )

  if not _is_symbolic_prop515_sigma_group_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the symbolic "
      "Toda Proposition 5.15 sigma-family group"
    )

  n = ScalarSymbol(
    name="n",
  )

  sigma_family_steps = tuple(
    premise
    for premise in symbolic_step.premises
    if (
      isinstance(
        premise,
        ProofStep,
      )
      and isinstance(
        premise.conclusion,
        TodaSigmaFamilyDefinitionStatement,
      )
      and premise.conclusion.index
      == n
    )
  )

  if len(
    sigma_family_steps
  ) != 1:
    raise ValueError(
      "symbolic_step must have exactly one "
      "symbolic sigma-family definition premise"
    )

  sigma_family_statement = (
    sigma_family_steps[
      0
    ].conclusion
  )

  sigma_definition = (
    toda_sigma_family_definition_statement(
      index,
      sigma_family_statement
      .sigma8_statement,
    )
  )

  conclusion = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=(
        index
        + 7
      ),
      sphere_dimension=index,
    ),
    rhs=FiniteCyclicGroup(
      order=16,
      generator=(
        sigma_definition.element
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  return ProofStep(
    conclusion=conclusion,
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 109-22 theorem-specific concrete "
      "specialization of Toda Proposition 5.15 "
      f"at n={index}"
    ),
  )


def specialize_toda_prop515_sigma10_step(
  symbolic_step: ProofStep,
) -> ProofStep:
  return (
    specialize_toda_prop515_sigma_index_step(
      symbolic_step,
      10,
    )
  )


def specialize_repository_proof_scope_for_generator(
  scope: RepositoryProofScopeResult,
  generator: GeneratorSymbol,
) -> RepositoryProofScopeResult:
  if not isinstance(
    scope,
    RepositoryProofScopeResult,
  ):
    raise TypeError(
      "scope must be a RepositoryProofScopeResult"
    )

  if not isinstance(
    generator,
    GeneratorSymbol,
  ):
    raise TypeError(
      "generator must be a GeneratorSymbol"
    )

  if not (
    is_toda_prop515_generic_sigma_specialization_generator(
      generator
    )
  ):
    return scope

  specialized_nodes = []

  for node in scope.nodes:
    if not _is_symbolic_prop515_sigma_group_step(
      node.proof_step
    ):
      continue

    specialized_step = (
      specialize_toda_prop515_sigma_index_step(
        node.proof_step,
        generator.index,
      )
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
