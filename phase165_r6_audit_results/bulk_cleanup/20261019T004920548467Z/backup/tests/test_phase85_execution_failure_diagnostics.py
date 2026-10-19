from dataclasses import dataclass

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_inference import (
  BoundedProducerSearchStatus,
  diagnose_depth_two_producer_execution_failure,
  repository_available_steps,
  select_unique_depth_two_producer_chain,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)


@dataclass(frozen=True)
class Phase85ExecutionSeedStatement:
  name: str


@dataclass(frozen=True)
class Phase85ExecutionPremiseStatement:
  name: str


@dataclass(frozen=True)
class Phase85ExecutionWrongStatement:
  name: str


@dataclass(frozen=True)
class Phase85ExecutionGoalStatement:
  name: str


def _repository():
  seed_step = ProofStep(
    conclusion=Phase85ExecutionSeedStatement(
      name="seed",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  repository = ProofRepository()

  repository.register(
    ProofRepositoryEntry(
      key="phase85.execution.seed",
      step=seed_step,
      phase="85",
      theorem=(
        "execution failure diagnostics"
      ),
    )
  )

  return repository


def _producer_rule(
  *,
  applicable=True,
  usable=True,
):
  def guard(
    premises,
    bindings,
  ):
    return applicable

  def build_conclusion(
    premises,
  ):
    if usable:
      return Phase85ExecutionPremiseStatement(
        name="produced",
      )

    return Phase85ExecutionWrongStatement(
      name="wrong",
    )

  return InferenceRule(
    name="phase85 execution producer",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
        statement_type=(
          Phase85ExecutionSeedStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def _final_rule(
  *,
  applicable=True,
  derive_requested_goal=True,
):
  def guard(
    premises,
    bindings,
  ):
    return applicable

  def build_conclusion(
    premises,
  ):
    if derive_requested_goal:
      return Phase85ExecutionGoalStatement(
        name="requested",
      )

    return Phase85ExecutionGoalStatement(
      name="different",
    )

  return InferenceRule(
    name="phase85 execution final",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.INFERENCE,
        statement_type=(
          Phase85ExecutionPremiseStatement
        ),
      ),
    ),
    conclusion_builder=build_conclusion,
    match_guard=guard,
  )


def _catalog(
  producer_rule,
  final_rule,
):
  catalog = InferenceRuleCatalog()

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase85.execution.producer",
      rule=producer_rule,
      conclusion_type=(
        Phase85ExecutionPremiseStatement
      ),
      fixed_point_safe=True,
    )
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key="phase85.execution.final",
      rule=final_rule,
      conclusion_type=(
        Phase85ExecutionGoalStatement
      ),
      fixed_point_safe=True,
    )
  )

  return catalog


def _search_result(
  *,
  producer_applicable=True,
  producer_usable=True,
  final_applicable=True,
  derive_requested_goal=True,
):
  repository = _repository()

  producer_rule = _producer_rule(
    applicable=producer_applicable,
    usable=producer_usable,
  )

  final_rule = _final_rule(
    applicable=final_applicable,
    derive_requested_goal=(
      derive_requested_goal
    ),
  )

  catalog = _catalog(
    producer_rule,
    final_rule,
  )

  goal = Phase85ExecutionGoalStatement(
    name="requested",
  )

  search_result = (
    select_unique_depth_two_producer_chain(
      repository,
      catalog,
      goal,
    )
  )

  assert search_result is not None

  return {
    "repository": repository,
    "catalog": catalog,
    "goal": goal,
    "producer_rule": producer_rule,
    "final_rule": final_rule,
    "search_result": search_result,
  }


def test_phase85_5_classifies_producer_not_applicable():
  data = _search_result(
    producer_applicable=False,
  )

  diagnostic = (
    diagnose_depth_two_producer_execution_failure(
      data[
        "repository"
      ],
      data[
        "search_result"
      ],
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .PRODUCER_NOT_APPLICABLE
  )
  assert diagnostic.final_rule is data[
    "final_rule"
  ]
  assert diagnostic.requesting_rule is data[
    "final_rule"
  ]
  assert diagnostic.premise_index == 0
  assert diagnostic.current_depth == 0
  assert diagnostic.required_next_depth == 1
  assert diagnostic.producer_candidates == (
    data[
      "producer_rule"
    ],
  )


def test_phase85_5_classifies_unusable_producer_output():
  data = _search_result(
    producer_usable=False,
  )

  diagnostic = (
    diagnose_depth_two_producer_execution_failure(
      data[
        "repository"
      ],
      data[
        "search_result"
      ],
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .PRODUCER_OUTPUT_NOT_USABLE
  )
  assert diagnostic.final_rule is data[
    "final_rule"
  ]
  assert diagnostic.producer_candidates == (
    data[
      "producer_rule"
    ],
  )


def test_phase85_5_classifies_final_rule_not_applicable():
  data = _search_result(
    final_applicable=False,
  )

  diagnostic = (
    diagnose_depth_two_producer_execution_failure(
      data[
        "repository"
      ],
      data[
        "search_result"
      ],
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .FINAL_RULE_NOT_APPLICABLE
  )
  assert diagnostic.final_rule is data[
    "final_rule"
  ]


def test_phase85_5_classifies_goal_not_derived():
  data = _search_result(
    derive_requested_goal=False,
  )

  diagnostic = (
    diagnose_depth_two_producer_execution_failure(
      data[
        "repository"
      ],
      data[
        "search_result"
      ],
    )
  )

  assert diagnostic is not None
  assert diagnostic.status is (
    BoundedProducerSearchStatus
    .GOAL_NOT_DERIVED
  )
  assert diagnostic.final_rule is data[
    "final_rule"
  ]


def test_phase85_5_returns_none_when_execution_succeeds():
  data = _search_result()

  diagnostic = (
    diagnose_depth_two_producer_execution_failure(
      data[
        "repository"
      ],
      data[
        "search_result"
      ],
    )
  )

  assert diagnostic is None


def test_phase85_5_diagnostic_does_not_mutate_repository():
  data = _search_result(
    producer_applicable=False,
  )

  initial_steps = repository_available_steps(
    data[
      "repository"
    ]
  )

  diagnose_depth_two_producer_execution_failure(
    data[
      "repository"
    ],
    data[
      "search_result"
    ],
  )

  assert repository_available_steps(
    data[
      "repository"
    ]
  ) == initial_steps


