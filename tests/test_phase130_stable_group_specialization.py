from expression import (
  Composition,
  GeneratorSymbol,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  Relation,
)
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_symbolic_stable_group_specialization import (
  specialize_repository_proof_scope_for_toda_group_query,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)
from toda_calculation import (
  build_known_toda_calculation_result,
  build_toda_calculation_result,
)
from toda_calculation_result import (
  TodaCalculationStatus,
)
from toda_group_query import TodaGroupQuery


def test_phase130_6_pi5_4_standard_query_specializes_eta_family():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=4,
        k=1,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    group_result.group_structure.order
    == 2
  )
  assert (
    group_result.generators[
      0
    ].generator
    == GeneratorSymbol(
      family="η",
      index=4,
    )
  )
  assert (
    group_result.source_entry.phase
    == "55"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.1"
  )
  assert (
    group_result.proof_step.rule
    is ProofRule.INFERENCE
  )
  assert len(
    group_result.proof_step.premises
  ) == 1


def test_phase130_6_pi6_4_standard_query_reuses_existing_concrete_boundary():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=4,
        k=2,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    group_result.group_structure.order
    == 2
  )
  assert isinstance(
    group_result.generators[
      0
    ],
    Composition,
  )
  assert (
    group_result.generators[
      0
    ].left.generator
    == GeneratorSymbol(
      family="η",
      index=4,
    )
  )
  assert (
    group_result.generators[
      0
    ].right.generator
    == GeneratorSymbol(
      family="η",
      index=5,
    )
  )
  assert (
    group_result.source_entry.phase
    == "59"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.3"
  )


def test_phase130_6_pi7_5_standard_query_specializes_eta_squared_family():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=5,
        k=2,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert isinstance(
    group_result.generators[
      0
    ],
    Composition,
  )
  assert (
    group_result.generators[
      0
    ].left.generator
    == GeneratorSymbol(
      family="η",
      index=5,
    )
  )
  assert (
    group_result.generators[
      0
    ].right.generator
    == GeneratorSymbol(
      family="η",
      index=6,
    )
  )
  assert (
    group_result.source_entry.phase
    == "59"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.3"
  )


def test_phase130_6_pi9_6_standard_query_specializes_nu_family():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_known_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=6,
        k=3,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert len(
    result.candidates
  ) == 1

  group_result = (
    result.candidates[
      0
    ].group_result
  )

  assert isinstance(
    group_result.group_structure,
    FiniteCyclicGroup,
  )
  assert (
    group_result.group_structure.order
    == 8
  )
  assert (
    group_result.generators[
      0
    ].generator
    == GeneratorSymbol(
      family="ν",
      index=6,
    )
  )
  assert (
    group_result.source_entry.phase
    == "65"
  )
  assert (
    group_result.source_entry.theorem
    == "Toda Proposition 5.6"
  )


def test_phase130_6_specialized_scope_preserves_symbolic_step_as_premise():
  repository = (
    build_standard_production_proof_repository()
  )
  raw_scope = (
    build_repository_proof_scope(
      repository
    )
  )
  query = TodaGroupQuery(
    n=6,
    k=3,
  )

  specialized_scope = (
    specialize_repository_proof_scope_for_toda_group_query(
      raw_scope,
      query,
    )
  )

  added_nodes = (
    specialized_scope.nodes[
      len(
        raw_scope.nodes
      ):
    ]
  )

  matching_nodes = tuple(
    node
    for node in added_nodes
    if (
      isinstance(
        node.proof_step.conclusion,
        Relation,
      )
      and node.proof_step.conclusion.lhs
      == TodaPrimaryGroup(
        group_dimension=9,
        sphere_dimension=6,
      )
    )
  )

  assert len(
    matching_nodes
  ) == 1

  specialized_step = (
    matching_nodes[
      0
    ].proof_step
  )

  assert (
    specialized_step.rule
    is ProofRule.INFERENCE
  )
  assert len(
    specialized_step.premises
  ) == 1

  symbolic_step = (
    specialized_step.premises[
      0
    ]
  )

  assert isinstance(
    symbolic_step.conclusion,
    Relation,
  )
  assert (
    symbolic_step.conclusion.rhs.order
    == 8
  )
  assert (
    matching_nodes[
      0
    ].shortest_depth
    > 0
  )


def test_phase130_6_eta_squared_specialization_does_not_cross_n4_boundary():
  repository = (
    build_standard_production_proof_repository()
  )
  raw_scope = (
    build_repository_proof_scope(
      repository
    )
  )

  specialized_scope = (
    specialize_repository_proof_scope_for_toda_group_query(
      raw_scope,
      TodaGroupQuery(
        n=4,
        k=2,
      ),
    )
  )

  assert (
    specialized_scope
    is raw_scope
  )


def test_phase130_6_existing_pi8_5_query_remains_aggregate_result():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_toda_calculation_result(
      repository,
      TodaGroupQuery(
        n=5,
        k=3,
      ),
    )
  )

  assert (
    result.status
    is TodaCalculationStatus.FOUND
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.phase
    == "65"
  )
  assert (
    result.candidates[
      0
    ].group_result.source_entry.theorem
    == "Toda Proposition 5.6"
  )


def test_phase130_6_standard_repository_roots_remain_unchanged():
  repository = (
    build_standard_production_proof_repository()
  )

  before = tuple(
    entry.key
    for entry in repository.entries()
  )

  build_known_toda_calculation_result(
    repository,
    TodaGroupQuery(
      n=6,
      k=3,
    ),
  )

  after = tuple(
    entry.key
    for entry in repository.entries()
  )

  assert before == (
    "standard.toda.prop56",
    "standard.toda.prop58",
    "standard.toda.prop511",
    "standard.toda.prop515",
  )
  assert after == before
