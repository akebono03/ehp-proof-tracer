from dataclasses import FrozenInstanceError

import pytest

from repository_generator_applicability_handoff import (
  RepositoryGeneratorApplicabilityCandidateHandoff,
)
from test_phase103_grouped_applicability_presentation import (
  build_grouped_fixture,
)


def test_phase104_4c_handoff_preserves_candidate_identity_and_goal():
  data = build_grouped_fixture()
  candidate = data[
    "candidates"
  ][0]
  goal = object()

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=candidate,
      goal=goal,
    )
  )

  assert handoff.candidate is candidate
  assert handoff.goal is goal


def test_phase104_4c_handoff_preserves_candidate_provenance_indirectly():
  data = build_grouped_fixture()
  candidate = data[
    "candidates"
  ][2]

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=candidate,
      goal="phase104 goal",
    )
  )

  assert (
    handoff.candidate.scope_node
    is candidate.scope_node
  )
  assert (
    handoff.candidate.candidate
    is candidate.candidate
  )
  assert (
    handoff.candidate.candidate.catalog_entry
    is candidate.candidate.catalog_entry
  )
  assert (
    handoff.candidate.candidate.source_step
    is candidate.candidate.source_step
  )


def test_phase104_4c_handoff_does_not_restrict_goal_type():
  data = build_grouped_fixture()
  candidate = data[
    "candidates"
  ][0]

  goals = (
    None,
    "goal",
    42,
    object(),
  )

  for goal in goals:
    handoff = (
      RepositoryGeneratorApplicabilityCandidateHandoff(
        candidate=candidate,
        goal=goal,
      )
    )

    assert handoff.goal is goal


def test_phase104_4c_handoff_is_frozen():
  data = build_grouped_fixture()

  handoff = (
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=data[
        "candidates"
      ][0],
      goal="goal",
    )
  )

  with pytest.raises(
    FrozenInstanceError,
  ):
    handoff.goal = "changed"


def test_phase104_4c_handoff_rejects_non_candidate():
  with pytest.raises(
    TypeError,
    match=(
      "candidate must be a "
      "RepositoryProofScopeApplicabilityCandidate"
    ),
  ):
    RepositoryGeneratorApplicabilityCandidateHandoff(
      candidate=object(),
      goal="goal",
    )
