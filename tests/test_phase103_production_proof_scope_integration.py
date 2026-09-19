from dataclasses import dataclass

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
from repository_proof_scope import (
  build_repository_proof_scope,
)
from repository_proof_scope_applicability import (
  RepositoryProofScopeApplicabilityCandidate,
  find_repository_proof_scope_applicability_candidates,
)
from rule_applicability import (
  InferenceRuleApplicabilityCandidate,
)
from rule_catalog import (
  InferenceRuleCatalog,
  InferenceRuleCatalogEntry,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


@dataclass(frozen=True)
class Phase103ScopeStatement:
  value: str


@dataclass(frozen=True)
class Phase103ScopeConclusion:
  value: str


def make_step(
  value,
  premises=(),
):
  return ProofStep(
    conclusion=(
      Phase103ScopeStatement(
        value=value,
      )
    ),
    premises=premises,
    rule=ProofRule.GIVEN,
  )


def make_catalog(
  *,
  fixed_point_safe=False,
):
  pattern = PremisePattern(
    proof_rule=ProofRule.GIVEN,
    statement_type=(
      Phase103ScopeStatement
    ),
  )

  rule = InferenceRule(
    name=(
      "phase103 proof-scope "
      "applicability rule"
    ),
    premise_patterns=(
      pattern,
    ),
  )

  entry = InferenceRuleCatalogEntry(
    key=(
      "phase103.proof-scope."
      "applicability"
    ),
    rule=rule,
    conclusion_type=(
      Phase103ScopeConclusion
    ),
    fixed_point_safe=(
      fixed_point_safe
    ),
  )

  catalog = InferenceRuleCatalog()
  catalog.register(
    entry
  )

  return {
    "catalog": catalog,
    "entry": entry,
    "rule": rule,
    "pattern": pattern,
  }


def test_phase103_4_wraps_scope_node_and_candidate():
  leaf = make_step(
    "leaf"
  )

  root = make_step(
    "root",
    premises=(
      leaf,
    ),
  )

  repository = ProofRepository()
  root_entry = ProofRepositoryEntry(
    key="phase103.root",
    step=root,
  )
  repository.register(
    root_entry
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  results = (
    find_repository_proof_scope_applicability_candidates(
      scope,
      data[
        "catalog"
      ],
    )
  )

  assert len(
    results
  ) == 2

  assert all(
    isinstance(
      result,
      RepositoryProofScopeApplicabilityCandidate,
    )
    for result in results
  )

  assert all(
    isinstance(
      result.candidate,
      InferenceRuleApplicabilityCandidate,
    )
    for result in results
  )


def test_phase103_4_preserves_scope_provenance_and_identity():
  leaf = make_step(
    "leaf"
  )

  root = make_step(
    "root",
    premises=(
      leaf,
    ),
  )

  repository = ProofRepository()
  root_entry = ProofRepositoryEntry(
    key="phase103.root",
    step=root,
  )
  repository.register(
    root_entry
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  results = (
    find_repository_proof_scope_applicability_candidates(
      scope,
      data[
        "catalog"
      ],
    )
  )

  assert tuple(
    result.root_entry
    for result in results
  ) == (
    root_entry,
    root_entry,
  )

  assert tuple(
    result.shortest_depth
    for result in results
  ) == (
    0,
    1,
  )

  assert (
    results[
      0
    ].candidate.source_step
    is root
  )

  assert (
    results[
      1
    ].candidate.source_step
    is leaf
  )

  assert (
    results[
      0
    ].scope_node.proof_step
    is root
  )

  assert (
    results[
      1
    ].scope_node.proof_step
    is leaf
  )


def test_phase103_4_preserves_scope_node_order():
  left = make_step(
    "left"
  )

  right = make_step(
    "right"
  )

  root = make_step(
    "root",
    premises=(
      left,
      right,
    ),
  )

  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase103.order",
      step=root,
    )
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  results = (
    find_repository_proof_scope_applicability_candidates(
      scope,
      data[
        "catalog"
      ],
    )
  )

  assert tuple(
    result.scope_node.proof_step
    for result in results
  ) == (
    root,
    left,
    right,
  )


def test_phase103_4_same_step_under_two_roots_remains_two_candidates():
  shared = make_step(
    "shared"
  )

  first_root = ProofStep(
    conclusion="first-root",
    premises=(
      shared,
    ),
    rule=ProofRule.GIVEN,
  )

  second_root = ProofStep(
    conclusion="second-root",
    premises=(
      shared,
    ),
    rule=ProofRule.GIVEN,
  )

  first_entry = ProofRepositoryEntry(
    key="phase103.first",
    step=first_root,
  )

  second_entry = ProofRepositoryEntry(
    key="phase103.second",
    step=second_root,
  )

  repository = ProofRepository()
  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  results = (
    find_repository_proof_scope_applicability_candidates(
      scope,
      data[
        "catalog"
      ],
    )
  )

  shared_results = tuple(
    result
    for result in results
    if (
      result.candidate.source_step
      is shared
    )
  )

  assert len(
    shared_results
  ) == 2

  assert tuple(
    result.root_entry
    for result in shared_results
  ) == (
    first_entry,
    second_entry,
  )

  assert tuple(
    result.shortest_depth
    for result in shared_results
  ) == (
    1,
    1,
  )


def test_phase103_4_preserves_unsafe_candidate_metadata():
  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase103.unsafe",
      step=make_step(
        "known"
      ),
    )
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog(
    fixed_point_safe=False,
  )

  results = (
    find_repository_proof_scope_applicability_candidates(
      scope,
      data[
        "catalog"
      ],
    )
  )

  assert len(
    results
  ) == 1

  assert (
    results[
      0
    ].candidate.fixed_point_safe
    is False
  )


def test_phase103_4_non_matching_scope_nodes_produce_no_result():
  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase103.unrelated",
      step=ProofStep(
        conclusion="unrelated",
        premises=(),
        rule=ProofRule.GIVEN,
      ),
    )
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  assert (
    find_repository_proof_scope_applicability_candidates(
      scope,
      data[
        "catalog"
      ],
    )
    == ()
  )


def test_phase103_4_standard_production_scope_reaches_ancestry():
  repository = (
    build_standard_production_proof_repository()
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  catalog = InferenceRuleCatalog()

  wildcard_rule = InferenceRule(
    name=(
      "phase103 production "
      "wildcard audit rule"
    ),
    premise_patterns=(
      PremisePattern(),
    ),
  )

  catalog.register(
    InferenceRuleCatalogEntry(
      key=(
        "phase103.production."
        "wildcard-audit"
      ),
      rule=wildcard_rule,
      conclusion_type=object,
    )
  )

  results = (
    find_repository_proof_scope_applicability_candidates(
      scope,
      catalog,
    )
  )

  assert len(
    results
  ) == len(
    scope.nodes
  )

  assert any(
    result.shortest_depth > 0
    for result in results
  )

  assert any(
    result.candidate.source_step
    is not result.root_entry.step
    for result in results
  )


def test_phase103_4_search_does_not_mutate_repository_or_catalog():
  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase103.read-only",
      step=make_step(
        "known"
      ),
    )
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  before_repository = (
    repository.entries()
  )

  before_catalog = (
    data[
      "catalog"
    ].entries()
  )

  find_repository_proof_scope_applicability_candidates(
    scope,
    data[
      "catalog"
    ],
  )

  after_repository = (
    repository.entries()
  )

  after_catalog = (
    data[
      "catalog"
    ].entries()
  )

  assert (
    after_repository
    == before_repository
  )

  assert (
    after_catalog
    == before_catalog
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      after_repository,
      before_repository,
    )
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      after_catalog,
      before_catalog,
    )
  )


def test_phase103_4_wrapper_rejects_mismatched_source_step():
  first_step = make_step(
    "first"
  )

  second_step = make_step(
    "second"
  )

  repository = ProofRepository()

  entry = ProofRepositoryEntry(
    key="phase103.wrapper",
    step=first_step,
  )

  repository.register(
    entry
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  data = make_catalog()

  candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "pattern"
      ],
      source_step=second_step,
    )
  )

  with pytest.raises(
    ValueError,
    match=(
      "candidate source_step must be "
      "scope_node.proof_step"
    ),
  ):
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=scope.nodes[
        0
      ],
      candidate=candidate,
    )


def test_phase103_4_wrapper_rejects_invalid_scope_node():
  data = make_catalog()

  source_step = make_step(
    "known"
  )

  candidate = (
    InferenceRuleApplicabilityCandidate(
      catalog_entry=data[
        "entry"
      ],
      premise_index=0,
      premise_pattern=data[
        "pattern"
      ],
      source_step=source_step,
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "scope_node must be a "
      "RepositoryProofScopeNode"
    ),
  ):
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=object(),
      candidate=candidate,
    )


def test_phase103_4_wrapper_rejects_invalid_candidate():
  repository = ProofRepository()

  entry = ProofRepositoryEntry(
    key="phase103.wrapper.invalid",
    step=make_step(
      "known"
    ),
  )

  repository.register(
    entry
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "candidate must be an "
      "InferenceRuleApplicabilityCandidate"
    ),
  ):
    RepositoryProofScopeApplicabilityCandidate(
      scope_node=scope.nodes[
        0
      ],
      candidate=object(),
    )


def test_phase103_4_rejects_invalid_scope():
  data = make_catalog()

  with pytest.raises(
    TypeError,
    match=(
      "scope must be a "
      "RepositoryProofScopeResult"
    ),
  ):
    find_repository_proof_scope_applicability_candidates(
      object(),
      data[
        "catalog"
      ],
    )


def test_phase103_4_rejects_invalid_catalog():
  repository = ProofRepository()
  repository.register(
    ProofRepositoryEntry(
      key="phase103.invalid-catalog",
      step=make_step(
        "known"
      ),
    )
  )

  scope = (
    build_repository_proof_scope(
      repository
    )
  )

  with pytest.raises(
    TypeError,
    match=(
      "catalog must be an "
      "InferenceRuleCatalog"
    ),
  ):
    find_repository_proof_scope_applicability_candidates(
      scope,
      object(),
    )
