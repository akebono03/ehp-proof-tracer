import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import (
  ProofRepository,
  ProofRepositoryEntry,
)
from repository_proof_scope import (
  RepositoryProofScopeNode,
  RepositoryProofScopeResult,
  build_repository_entry_proof_scope,
  build_repository_proof_scope,
)
from standard_production_repository import (
  build_standard_production_proof_repository,
)


def make_step(
  conclusion,
  premises=(),
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.GIVEN,
  )


def test_phase102_5a_entry_scope_contains_root_at_depth_zero():
  root = make_step(
    "root"
  )

  entry = ProofRepositoryEntry(
    key="phase102.root",
    step=root,
  )

  result = (
    build_repository_entry_proof_scope(
      entry
    )
  )

  assert len(
    result
  ) == 1

  assert isinstance(
    result[
      0
    ],
    RepositoryProofScopeNode,
  )

  assert (
    result[
      0
    ].root_entry
    is entry
  )

  assert (
    result[
      0
    ].proof_step
    is root
  )

  assert (
    result[
      0
    ].shortest_depth
    == 0
  )


def test_phase102_5a_entry_scope_traverses_premises_breadth_first():
  leaf = make_step(
    "leaf"
  )

  left = make_step(
    "left",
    premises=(
      leaf,
    ),
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

  entry = ProofRepositoryEntry(
    key="phase102.bfs",
    step=root,
  )

  result = (
    build_repository_entry_proof_scope(
      entry
    )
  )

  assert tuple(
    node.proof_step
    for node in result
  ) == (
    root,
    left,
    right,
    leaf,
  )

  assert tuple(
    node.shortest_depth
    for node in result
  ) == (
    0,
    1,
    1,
    2,
  )


def test_phase102_5a_shared_dependency_is_reported_once_per_root():
  shared = make_step(
    "shared"
  )

  left = make_step(
    "left",
    premises=(
      shared,
    ),
  )

  right = make_step(
    "right",
    premises=(
      shared,
    ),
  )

  root = make_step(
    "root",
    premises=(
      left,
      right,
    ),
  )

  entry = ProofRepositoryEntry(
    key="phase102.shared",
    step=root,
  )

  result = (
    build_repository_entry_proof_scope(
      entry
    )
  )

  assert sum(
    node.proof_step is shared
    for node in result
  ) == 1

  shared_node = next(
    node
    for node in result
    if node.proof_step is shared
  )

  assert (
    shared_node.shortest_depth
    == 2
  )


def test_phase102_5a_cycle_is_safe():
  root = make_step(
    "root"
  )

  child = make_step(
    "child",
    premises=(
      root,
    ),
  )

  object.__setattr__(
    root,
    "premises",
    (
      child,
    ),
  )

  entry = ProofRepositoryEntry(
    key="phase102.cycle",
    step=root,
  )

  result = (
    build_repository_entry_proof_scope(
      entry
    )
  )

  assert tuple(
    node.proof_step
    for node in result
  ) == (
    root,
    child,
  )


def test_phase102_5a_non_proofstep_premises_are_ignored():
  child = make_step(
    "child"
  )

  root = make_step(
    "root",
    premises=(
      "not-a-proof-step",
      child,
      123,
    ),
  )

  entry = ProofRepositoryEntry(
    key="phase102.non-step",
    step=root,
  )

  result = (
    build_repository_entry_proof_scope(
      entry
    )
  )

  assert tuple(
    node.proof_step
    for node in result
  ) == (
    root,
    child,
  )


def test_phase102_5a_repository_scope_preserves_registration_order():
  first_root = make_step(
    "first"
  )

  second_root = make_step(
    "second"
  )

  first_entry = ProofRepositoryEntry(
    key="phase102.first",
    step=first_root,
  )

  second_entry = ProofRepositoryEntry(
    key="phase102.second",
    step=second_root,
  )

  repository = ProofRepository()
  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    build_repository_proof_scope(
      repository
    )
  )

  assert isinstance(
    result,
    RepositoryProofScopeResult,
  )

  assert (
    result.repository
    is repository
  )

  assert tuple(
    node.root_entry
    for node in result.nodes
  ) == (
    first_entry,
    second_entry,
  )

  assert tuple(
    node.proof_step
    for node in result.nodes
  ) == (
    first_root,
    second_root,
  )


def test_phase102_5a_same_proof_step_under_two_roots_remains_two_scope_nodes():
  shared = make_step(
    "shared"
  )

  first_entry = ProofRepositoryEntry(
    key="phase102.first",
    step=make_step(
      "first",
      premises=(
        shared,
      ),
    ),
  )

  second_entry = ProofRepositoryEntry(
    key="phase102.second",
    step=make_step(
      "second",
      premises=(
        shared,
      ),
    ),
  )

  repository = ProofRepository()
  repository.register(
    first_entry
  )
  repository.register(
    second_entry
  )

  result = (
    build_repository_proof_scope(
      repository
    )
  )

  shared_nodes = tuple(
    node
    for node in result.nodes
    if node.proof_step is shared
  )

  assert len(
    shared_nodes
  ) == 2

  assert tuple(
    node.root_entry
    for node in shared_nodes
  ) == (
    first_entry,
    second_entry,
  )


def test_phase102_5a_standard_production_scope_reaches_unregistered_ancestry():
  repository = (
    build_standard_production_proof_repository()
  )

  result = (
    build_repository_proof_scope(
      repository
    )
  )

  assert (
    len(
      result.nodes
    )
    > len(
      repository.entries()
    )
  )

  assert all(
    any(
      node.root_entry is entry
      and node.proof_step is entry.step
      and node.shortest_depth == 0
      for node in result.nodes
    )
    for entry in repository.entries()
  )

  assert any(
    node.shortest_depth > 0
    for node in result.nodes
  )


def test_phase102_5a_repository_is_not_mutated():
  repository = (
    build_standard_production_proof_repository()
  )

  before = (
    repository.entries()
  )

  build_repository_proof_scope(
    repository
  )

  after = (
    repository.entries()
  )

  assert after == before

  assert all(
    actual is expected
    for actual, expected in zip(
      after,
      before,
    )
  )


def test_phase102_5a_entry_scope_rejects_non_entry():
  with pytest.raises(
    TypeError,
    match=(
      "entry must be a ProofRepositoryEntry"
    ),
  ):
    build_repository_entry_proof_scope(
      "not-an-entry"
    )


def test_phase102_5a_repository_scope_rejects_non_repository():
  with pytest.raises(
    TypeError,
    match=(
      "repository must be a ProofRepository"
    ),
  ):
    build_repository_proof_scope(
      "not-a-repository"
    )
