import pytest

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
from repository_generator_production_application_execution_seed import (
  build_repository_generator_production_application_execution_seed_repository,
)
from repository_generator_production_application_recovery import (
  RepositoryGeneratorProductionApplicationRecovery,
  RepositoryGeneratorProductionApplicationRecoveryStatus,
  recover_repository_generator_production_application,
)
from repository_inference import (
  repository_available_steps,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalogEntry,
)
from test_phase107_5_exact_production_application_premise_tuple_recovery import (
  build_phase107_5_actual_data,
)


def test_phase107_7_adapter_rejects_non_recovery():
  with pytest.raises(
    TypeError,
    match=(
      "recovery must be a "
      "RepositoryGeneratorProductionApplicationRecovery"
    ),
  ):
    build_repository_generator_production_application_execution_seed_repository(
      object()
    )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_7_actual_unique_recovery_builds_two_premise_seed(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  recovery = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        candidate_index
      ],
      data[
        "goal"
      ],
    )
  )

  assert recovery.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.UNIQUE
  )

  seed_repository = (
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )
  )

  assert isinstance(
    seed_repository,
    ProofRepository,
  )

  entries = (
    seed_repository.entries()
  )

  assert len(
    entries
  ) == 2

  assert tuple(
    entry.key
    for entry in entries
  ) == (
    (
      f"{recovery.candidate.root_entry.key}::"
      "applicability-execution-seed::000"
    ),
    (
      f"{recovery.candidate.root_entry.key}::"
      "applicability-execution-seed::001"
    ),
  )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_7_seed_preserves_exact_premise_order_and_identity(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  recovery = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        candidate_index
      ],
      data[
        "goal"
      ],
    )
  )

  seed_repository = (
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )
  )

  seed_steps = (
    repository_available_steps(
      seed_repository
    )
  )

  assert recovery.premise_tuple is not None

  assert seed_steps == (
    recovery.premise_tuple
  )

  assert all(
    actual is expected
    for actual, expected
    in zip(
      seed_steps,
      recovery.premise_tuple,
    )
  )

  assert all(
    actual is expected
    for actual, expected
    in zip(
      seed_steps,
      data[
        "target_step"
      ].premises,
    )
  )


def test_phase107_7_seed_entries_preserve_root_metadata():
  data = build_phase107_5_actual_data()

  recovery = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        0
      ],
      data[
        "goal"
      ],
    )
  )

  seed_repository = (
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )
  )

  root_entry = (
    recovery.candidate.root_entry
  )

  assert all(
    entry.phase
    == root_entry.phase
    for entry
    in seed_repository.entries()
  )

  assert all(
    entry.theorem
    == root_entry.theorem
    for entry
    in seed_repository.entries()
  )


def test_phase107_7_seed_adapter_does_not_mutate_standard_repository():
  data = build_phase107_5_actual_data()

  before_entries = (
    data[
      "repository"
    ].entries()
  )

  recovery = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        0
      ],
      data[
        "goal"
      ],
    )
  )

  seed_repository = (
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )
  )

  assert (
    data[
      "repository"
    ].entries()
    == before_entries
  )

  assert all(
    seed_entry
    not in before_entries
    for seed_entry
    in seed_repository.entries()
  )


def test_phase107_7_adapter_rejects_none_recovery():
  data = build_phase107_5_actual_data()

  recovery = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        0
      ],
      object(),
    )
  )

  assert recovery.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.NONE
  )

  with pytest.raises(
    ValueError,
    match="recovery must have UNIQUE status",
  ):
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )


def test_phase107_7_adapter_rejects_ambiguous_recovery():
  seed_statement = object()
  goal_statement = object()
  root_statement = object()

  source_step = ProofStep(
    conclusion=seed_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="phase107 7 ambiguous rule",
    premise_patterns=(
      PremisePattern(
        proof_rule=ProofRule.GIVEN,
      ),
    ),
    conclusion_builder=(
      lambda premises:
      goal_statement
    ),
  )

  first_application = ProofStep(
    conclusion=goal_statement,
    premises=(
      source_step,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  second_application = ProofStep(
    conclusion=goal_statement,
    premises=(
      source_step,
    ),
    rule=ProofRule.INFERENCE,
    inference_rule=rule,
  )

  root_step = ProofStep(
    conclusion=root_statement,
    premises=(
      first_application,
      second_application,
    ),
    rule=ProofRule.GIVEN,
  )

  root_entry = ProofRepositoryEntry(
    key="phase107.7.ambiguous.root",
    step=root_step,
  )

  source_scope_node = (
    RepositoryProofScopeNode(
      root_entry=root_entry,
      proof_step=source_step,
      shortest_depth=2,
    )
  )

  discovery_entry = (
    InferenceRuleCatalogEntry(
      key="phase107.7.ambiguous.discovery",
      rule=rule,
      conclusion_type=object,
      fixed_point_safe=False,
    )
  )

  raw_candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=discovery_entry,
      premise_index=0,
      premise_pattern=(
        rule.premise_patterns[
          0
        ]
      ),
      source_step=source_step,
      bindings=(),
    )
  )

  candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=source_scope_node,
      candidate=raw_candidate,
    )
  )

  recovery = (
    recover_repository_generator_production_application(
      candidate,
      goal_statement,
    )
  )

  assert recovery.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.AMBIGUOUS
  )

  with pytest.raises(
    ValueError,
    match="recovery must have UNIQUE status",
  ):
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )


def test_phase107_7_adapter_uses_recovery_premises_without_cloning():
  data = build_phase107_5_actual_data()

  recovery = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        1
      ],
      data[
        "goal"
      ],
    )
  )

  seed_repository = (
    build_repository_generator_production_application_execution_seed_repository(
      recovery
    )
  )

  entries = (
    seed_repository.entries()
  )

  assert recovery.premise_tuple is not None

  assert entries[
    0
  ].step is recovery.premise_tuple[
    0
  ]

  assert entries[
    1
  ].step is recovery.premise_tuple[
    1
  ]

  assert entries[
    0
  ].step is data[
    "target_step"
  ].premises[
    0
  ]

  assert entries[
    1
  ].step is data[
    "target_step"
  ].premises[
    1
  ]
