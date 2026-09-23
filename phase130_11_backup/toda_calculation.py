from expression import (
  Composition,
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_foundational_group_specialization import (
  find_foundational_toda_group_results,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_symbolic_sigma_specialization import (
  specialize_repository_proof_scope_for_generator,
)
from repository_symbolic_stable_group_specialization import (
  specialize_repository_proof_scope_for_toda_group_query,
)
from toda_calculation_goal_discovery import (
  discover_concrete_toda_calculation_goal_candidates,
)
from toda_calculation_goal_normalization import (
  normalize_recovered_toda_calculation_goal_candidate,
)
from toda_calculation_result import (
  TodaCalculationCandidate,
  TodaCalculationResult,
)
from toda_explanation import (
  build_toda_representative_explanation,
)
from toda_group_lookup import (
  find_normalized_toda_group_results,
  is_toda_group_result_for_target,
)
from toda_group_query import TodaGroupQuery
from toda_group_result import (
  normalize_toda_group_result,
)
from toda_rules import (
  TodaProp59FiniteDimensionalStatement,
)


_LOW_DIMENSIONAL_TODA_GROUP_SOURCES = {
  (
    2,
    1,
  ): (
    "pi3_2",
    "55",
    "Toda Proposition 5.1",
  ),
  (
    3,
    1,
  ): (
    "pi4_3",
    "55",
    "Toda Proposition 5.1",
  ),
  (
    2,
    2,
  ): (
    "pi4_2",
    "59",
    "Toda Proposition 5.3",
  ),
  (
    3,
    2,
  ): (
    "pi5_3",
    "59",
    "Toda Proposition 5.3",
  ),
  (
    4,
    2,
  ): (
    "pi6_4",
    "59",
    "Toda Proposition 5.3",
  ),
}


_STABLE_TODA_GROUP_SOURCES = {
  1: (
    "eta",
    "55",
    "Toda Proposition 5.1",
  ),
  2: (
    "eta_squared",
    "59",
    "Toda Proposition 5.3",
  ),
  3: (
    "nu",
    "65",
    "Toda Proposition 5.6",
  ),
  4: (
    "four_stem_zero",
    "68",
    "Toda Proposition 5.8",
  ),
  5: (
    "five_stem_zero",
    "70",
    "Toda Proposition 5.9",
  ),
  6: (
    "nu_squared",
    "73",
    "Toda Proposition 5.11",
  ),
}


def _generator_family_and_index(
  expression,
) -> tuple[
  object,
  object,
]:
  generator = getattr(
    expression,
    "generator",
    None,
  )

  return (
    getattr(
      generator,
      "family",
      None,
    ),
    getattr(
      generator,
      "index",
      None,
    ),
  )


def _is_canonical_low_dimensional_group_result(
  query: TodaGroupQuery,
  conclusion,
) -> bool:
  if not is_toda_group_result_for_target(
    conclusion,
    query.target,
  ):
    return False

  group_structure = getattr(
    conclusion,
    "rhs",
    None,
  )

  if (
    query.n,
    query.k,
  ) == (
    2,
    1,
  ):
    return (
      isinstance(
        group_structure,
        FreeCyclicGroup,
      )
      and _generator_family_and_index(
        group_structure.generator
      )
      == (
        "η",
        2,
      )
    )

  if (
    query.n,
    query.k,
  ) == (
    3,
    1,
  ):
    return (
      isinstance(
        group_structure,
        FiniteCyclicGroup,
      )
      and group_structure.order == 2
      and _generator_family_and_index(
        group_structure.generator
      )
      == (
        "η",
        3,
      )
    )

  if (
    query.k != 2
    or query.n not in (
      2,
      3,
      4,
    )
  ):
    return False

  if (
    not isinstance(
      group_structure,
      FiniteCyclicGroup,
    )
    or group_structure.order != 2
    or not isinstance(
      group_structure.generator,
      Composition,
    )
  ):
    return False

  expected_indices = (
    query.n,
    query.n + 1,
  )

  return (
    _generator_family_and_index(
      group_structure.generator.left
    )
    == (
      "η",
      expected_indices[
        0
      ],
    )
    and _generator_family_and_index(
      group_structure.generator.right
    )
    == (
      "η",
      expected_indices[
        1
      ],
    )
  )


def _find_low_dimensional_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  source_metadata = (
    _LOW_DIMENSIONAL_TODA_GROUP_SOURCES.get(
      (
        query.n,
        query.k,
      )
    )
  )

  if source_metadata is None:
    return ()

  scope = build_repository_proof_scope(
    repository
  )

  (
    key_suffix,
    phase,
    theorem,
  ) = source_metadata

  for node in scope.nodes:
    if (
      node.root_entry.key
      != "standard.toda.prop56"
    ):
      continue

    if not _is_canonical_low_dimensional_group_result(
      query,
      node.proof_step.conclusion,
    ):
      continue

    low_dimensional_entry = (
      ProofRepositoryEntry(
        key=(
          "standard.toda."
          "low-dimensional::"
          f"{key_suffix}"
        ),
        step=node.proof_step,
        phase=phase,
        theorem=theorem,
      )
    )

    return (
      normalize_toda_group_result(
        low_dimensional_entry
      ),
    )

  return ()


_PROP59_CONCRETE_BRANCHES = {
  2: "pi7_2_group_relation",
  3: "pi8_3_group_relation",
  4: "pi9_4_group_relation",
  5: "pi10_5_group_relation",
  6: "pi11_6_group_relation",
}


def _find_prop59_concrete_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  if query.k != 5:
    return ()

  branch_name = (
    _PROP59_CONCRETE_BRANCHES.get(
      query.n
    )
  )

  if branch_name is None:
    return ()

  scope = build_repository_proof_scope(
    repository
  )

  prop59_nodes = tuple(
    node
    for node in scope.nodes
    if (
      node.root_entry.key
      == "standard.toda.prop511"
      and isinstance(
        node.proof_step.conclusion,
        TodaProp59FiniteDimensionalStatement,
      )
    )
  )

  if len(
    prop59_nodes
  ) != 1:
    return ()

  prop59_statement = (
    prop59_nodes[
      0
    ].proof_step.conclusion
  )

  target_conclusion = getattr(
    prop59_statement,
    branch_name,
  )

  matching_nodes = tuple(
    node
    for node in scope.nodes
    if (
      node.root_entry.key
      == "standard.toda.prop511"
      and node.proof_step.conclusion
      == target_conclusion
    )
  )

  if not matching_nodes:
    return ()

  source_step = min(
    matching_nodes,
    key=lambda node: (
      node.shortest_depth
    ),
  ).proof_step

  if not is_toda_group_result_for_target(
    source_step.conclusion,
    query.target,
  ):
    return ()

  source_entry = ProofRepositoryEntry(
    key=(
      "standard.toda.prop59::"
      f"{branch_name}"
    ),
    step=source_step,
    phase="70",
    theorem="Toda Proposition 5.9",
  )

  return (
    normalize_toda_group_result(
      source_entry
    ),
  )


def _find_specialized_stable_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  source_metadata = (
    _STABLE_TODA_GROUP_SOURCES.get(
      query.k
    )
  )

  if source_metadata is None:
    return ()

  scope = build_repository_proof_scope(
    repository
  )

  specialized_scope = (
    specialize_repository_proof_scope_for_toda_group_query(
      scope,
      query,
    )
  )

  if specialized_scope is scope:
    return ()

  added_nodes = (
    specialized_scope.nodes[
      len(
        scope.nodes
      ):
    ]
  )

  (
    key_suffix,
    phase,
    theorem,
  ) = source_metadata

  results = []

  for node in added_nodes:
    if not is_toda_group_result_for_target(
      node.proof_step.conclusion,
      query.target,
    ):
      continue

    specialized_entry = (
      ProofRepositoryEntry(
        key=(
          "standard.toda.stable::"
          f"{key_suffix}_{query.n}_specialization"
        ),
        step=node.proof_step,
        phase=phase,
        theorem=theorem,
      )
    )

    results.append(
      normalize_toda_group_result(
        specialized_entry
      )
    )

  return tuple(
    results
  )


def _find_specialized_sigma_toda_group_results(
  repository: ProofRepository,
  query: TodaGroupQuery,
):
  if query.k != 7:
    return ()

  if query.n < 10:
    return ()

  scope = build_repository_proof_scope(
    repository
  )

  specialized_scope = (
    specialize_repository_proof_scope_for_generator(
      scope,
      GeneratorSymbol(
        family="σ",
        index=query.n,
      ),
    )
  )

  if specialized_scope is scope:
    return ()

  added_nodes = (
    specialized_scope.nodes[
      len(
        scope.nodes
      ):
    ]
  )

  results = []

  for node in added_nodes:
    if not is_toda_group_result_for_target(
      node.proof_step.conclusion,
      query.target,
    ):
      continue

    source_entry = node.root_entry

    specialized_entry = ProofRepositoryEntry(
      key=(
        f"{source_entry.key}::"
        f"sigma_{query.n}_specialization"
      ),
      step=node.proof_step,
      phase=source_entry.phase,
      theorem=source_entry.theorem,
    )

    results.append(
      normalize_toda_group_result(
        specialized_entry
      )
    )

  return tuple(
    results
  )


def build_known_toda_calculation_result(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> TodaCalculationResult:
  group_results = (
    find_foundational_toda_group_results(
      repository,
      query,
    )
  )

  if not group_results:
    group_results = (
      find_normalized_toda_group_results(
        repository,
        query,
      )
    )

  if not group_results:
    group_results = (
      _find_low_dimensional_toda_group_results(
        repository,
        query,
      )
    )

  if not group_results:
    group_results = (
      _find_prop59_concrete_toda_group_results(
        repository,
        query,
      )
    )

  if not group_results:
    group_results = (
      _find_specialized_stable_toda_group_results(
        repository,
        query,
      )
    )

  if not group_results:
    group_results = (
      _find_specialized_sigma_toda_group_results(
        repository,
        query,
      )
    )

  candidates = tuple(
    TodaCalculationCandidate(
      group_result=group_result,
      explanation=(
        build_toda_representative_explanation(
          group_result
        )
      ),
    )
    for group_result in group_results
  )

  return TodaCalculationResult(
    query=query,
    candidates=candidates,
  )


def build_toda_calculation_result(
  repository: ProofRepository,
  query: TodaGroupQuery,
) -> TodaCalculationResult:
  known_result = (
    build_known_toda_calculation_result(
      repository,
      query,
    )
  )

  if known_result.candidates:
    return known_result

  discovery_result = (
    discover_concrete_toda_calculation_goal_candidates(
      repository,
      query,
    )
  )

  candidates = []

  for goal_candidate in (
    discovery_result.candidates
  ):
    group_results = (
      normalize_recovered_toda_calculation_goal_candidate(
        goal_candidate
      )
    )

    for group_result in group_results:
      candidates.append(
        TodaCalculationCandidate(
          group_result=group_result,
          explanation=(
            build_toda_representative_explanation(
              group_result
            )
          ),
          goal_source=(
            goal_candidate.source
          ),
        )
      )

  return TodaCalculationResult(
    query=query,
    candidates=tuple(
      candidates
    ),
  )
