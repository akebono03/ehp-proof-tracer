from functools import lru_cache

import pytest

from proof import (
  InferenceRule,
  PremisePattern,
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepositoryEntry,
)
from repository_generator_production_application_recovery import (
  RepositoryGeneratorProductionApplicationRecoveryStatus,
  recover_repository_generator_production_application,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  build_repository_proof_scope,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
  build_inference_rule_premise_pattern_index,
  find_indexed_inference_rule_applicability_candidates,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from standard_production_applicability_catalog import (
  _inference_rule_factory_name,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


_TARGET_FACTORY = (
  "toda_lemma57_pi6_2_eta2_nu_prime_inference_rule"
)


@lru_cache(maxsize=1)
def build_phase107_5_actual_data():
  repository = (
    build_standard_production_proof_repository()
  )
  scope = build_repository_proof_scope(
    repository
  )

  target_nodes = tuple(
    node
    for node in scope.nodes
    if (
      node.root_entry.key
      == "standard.toda.prop58"
      and node.proof_step.inference_rule
      is not None
      and _inference_rule_factory_name(
        node.proof_step.inference_rule
      )
      == _TARGET_FACTORY
    )
  )

  assert len(
    target_nodes
  ) == 1

  target_node = target_nodes[
    0
  ]
  target_step = (
    target_node.proof_step
  )

  assert len(
    target_step.premises
  ) == 2
  assert (
    target_step.inference_rule
    is not None
  )

  discovery_entry = (
    InferenceRuleCatalogEntry(
      key=(
        "phase107.5.discovery."
        "pi6-2-eta2-nu-prime"
      ),
      rule=target_step.inference_rule,
      conclusion_type=type(
        target_step.conclusion
      ),
      fixed_point_safe=False,
    )
  )

  catalog = InferenceRuleCatalog()
  catalog.register(
    discovery_entry
  )

  index = (
    build_inference_rule_premise_pattern_index(
      catalog
    )
  )

  candidates = []

  for (
    premise_index,
    source_step,
  ) in enumerate(
    target_step.premises
  ):
    source_scope_node = next(
      node
      for node in scope.nodes
      if (
        node.root_entry
        is target_node.root_entry
        and node.proof_step
        is source_step
      )
    )

    raw_candidates = (
      find_indexed_inference_rule_applicability_candidates(
        index,
        source_step,
      )
    )

    raw_candidate = next(
      candidate
      for candidate in raw_candidates
      if (
        candidate.premise_index
        == premise_index
        and candidate.inference_rule
        is target_step.inference_rule
      )
    )

    candidates.append(
      RepositoryProofScopeApplicabilityCandidate(
        scope_node=source_scope_node,
        candidate=raw_candidate,
      )
    )

  return {
    "repository": repository,
    "scope": scope,
    "target_node": target_node,
    "target_step": target_step,
    "goal": target_step.conclusion,
    "candidates": tuple(
      candidates
    ),
  }


def test_phase107_5_recovery_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    recover_repository_generator_production_application(
      object(),
      object(),
    )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_5_actual_two_premise_candidates_recover_same_unique_application(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  result = (
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

  assert result.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.UNIQUE
  )
  assert (
    result.unique_application
    is data[
      "target_step"
    ]
  )


@pytest.mark.parametrize(
  "candidate_index",
  (
    0,
    1,
  ),
)
def test_phase107_5_actual_recovery_preserves_exact_premise_tuple_identity(
  candidate_index,
):
  data = build_phase107_5_actual_data()

  result = (
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

  premise_tuple = (
    result.premise_tuple
  )

  assert premise_tuple == (
    data[
      "target_step"
    ].premises
  )
  assert premise_tuple is (
    data[
      "target_step"
    ].premises
  )
  assert all(
    recovered is expected
    for recovered, expected
    in zip(
      premise_tuple,
      data[
        "target_step"
      ].premises,
    )
  )


def test_phase107_5_actual_recovery_requires_explicit_goal_match():
  data = build_phase107_5_actual_data()

  result = (
    recover_repository_generator_production_application(
      data[
        "candidates"
      ][
        0
      ],
      object(),
    )
  )

  assert result.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.NONE
  )
  assert result.unique_application is None
  assert result.premise_tuple is None


def test_phase107_5_actual_recovery_stays_within_candidate_root():
  data = build_phase107_5_actual_data()

  candidate = data[
    "candidates"
  ][
    0
  ]

  foreign_root = next(
    entry
    for entry in data[
      "repository"
    ].entries()
    if entry.key
    == "standard.toda.prop56"
  )

  foreign_scope_node = (
    RepositoryProofScopeNode(
      root_entry=foreign_root,
      proof_step=(
        candidate.candidate.source_step
      ),
      shortest_depth=1,
    )
  )

  foreign_candidate = (
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=foreign_scope_node,
      candidate=candidate.candidate,
    )
  )

  result = (
    recover_repository_generator_production_application(
      foreign_candidate,
      data[
        "goal"
      ],
    )
  )

  assert result.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.NONE
  )


def test_phase107_5_ambiguous_recovery_does_not_select_by_order():
  seed_statement = object()
  goal_statement = object()
  root_statement = object()

  source_step = ProofStep(
    conclusion=seed_statement,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  rule = InferenceRule(
    name="phase107 5 ambiguous rule",
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
    key="phase107.5.ambiguous.root",
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
      key="phase107.5.ambiguous.discovery",
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

  result = (
    recover_repository_generator_production_application(
      candidate,
      goal_statement,
    )
  )

  assert result.status is (
    RepositoryGeneratorProductionApplicationRecoveryStatus.AMBIGUOUS
  )
  assert result.applications == (
    first_application,
    second_application,
  )
  assert result.unique_application is None
  assert result.premise_tuple is None
