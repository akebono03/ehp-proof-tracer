from expression import (
  GeneratorSymbol,
  HomotopyElement,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import (
  normalize_toda_group_result,
)


def _build_identity_group_step(
  n: int,
) -> ProofStep:
  iota_n = HomotopyElement(
    name=f"ι_{n}",
    dimension=n,
    generator=GeneratorSymbol(
      family="ι",
      index=n,
    ),
  )

  return ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=n,
        sphere_dimension=n,
      ),
      rhs=FreeCyclicGroup(
        generator=iota_n,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
    note=(
      "Phase 130-10 foundational identity group "
      "pi_n(S^n) = Z{iota_n}"
    ),
  )


def _build_connectivity_zero_step(
  query: TodaGroupQuery,
) -> ProofStep:
  return ProofStep(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=query.target,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
    note=(
      "Phase 130-10 foundational sphere "
      "connectivity: pi_m(S^n)=0 for 1 <= m < n"
    ),
  )


def _is_symbolic_circle_higher_zero_step(
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
    TodaPrimaryGroupZeroStatement,
  ):
    return False

  i = ScalarSymbol(
    name="i",
  )

  return (
    conclusion.group
    == TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=i,
        right=-1,
      ),
      sphere_dimension=1,
    )
  )


def _find_circle_higher_zero_step(
  repository: ProofRepository,
) -> ProofStep | None:
  scope = build_repository_proof_scope(
    repository
  )

  matches = tuple(
    node.proof_step
    for node in scope.nodes
    if _is_symbolic_circle_higher_zero_step(
      node.proof_step
    )
  )

  if not matches:
    return None

  return matches[
    0
  ]


def _specialize_circle_higher_zero_step(
  symbolic_step: ProofStep,
  query: TodaGroupQuery,
) -> ProofStep:
  if query.n != 1 or query.k < 1:
    raise ValueError(
      "query must have n=1 and k>=1"
    )

  if not _is_symbolic_circle_higher_zero_step(
    symbolic_step
  ):
    raise ValueError(
      "symbolic_step must prove the Phase 56 "
      "symbolic circle higher-homotopy zero"
    )

  return ProofStep(
    conclusion=TodaPrimaryGroupZeroStatement(
      group=query.target,
    ),
    premises=(
      symbolic_step,
    ),
    rule=ProofRule.INFERENCE,
    note=(
      "Phase 130-10 concrete specialization of "
      "Phase 56 pi_(i-1)^1 zero"
    ),
  )


def find_foundational_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  if not isinstance(
    repository,
    ProofRepository,
  ):
    raise TypeError(
      "repository must be a ProofRepository"
    )

  if not isinstance(
    query,
    TodaGroupQuery,
  ):
    raise TypeError(
      "query must be a TodaGroupQuery"
    )

  group_dimension = (
    query.n
    + query.k
  )

  if group_dimension <= 0:
    return ()

  if query.k == 0:
    step = _build_identity_group_step(
      query.n
    )
    entry = ProofRepositoryEntry(
      key=(
        "standard.toda.foundational::"
        f"identity_{query.n}"
      ),
      step=step,
      phase="130",
      theorem="Sphere identity group",
    )
    return (
      normalize_toda_group_result(
        entry
      ),
    )

  if (
    query.n == 1
    and query.k >= 1
  ):
    symbolic_step = (
      _find_circle_higher_zero_step(
        repository
      )
    )

    if symbolic_step is None:
      return ()

    step = (
      _specialize_circle_higher_zero_step(
        symbolic_step,
        query,
      )
    )
    entry = ProofRepositoryEntry(
      key=(
        "standard.toda.foundational::"
        f"circle_zero_{query.k}"
      ),
      step=step,
      phase="56",
      theorem=(
        "Toda pi_(i-1)^1 zero "
        "for i at least 3"
      ),
    )
    return (
      normalize_toda_group_result(
        entry
      ),
    )

  if (
    query.k < 0
    and group_dimension >= 1
    and group_dimension < query.n
  ):
    step = (
      _build_connectivity_zero_step(
        query
      )
    )
    entry = ProofRepositoryEntry(
      key=(
        "standard.toda.foundational::"
        f"connectivity_{group_dimension}_{query.n}"
      ),
      step=step,
      phase="130",
      theorem="Sphere connectivity",
    )
    return (
      normalize_toda_group_result(
        entry
      ),
    )

  return ()
