import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
)
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import (
  TodaGroupResultProofReplayResult,
  build_toda_group_result_proof_replay,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
)


def build_phase131_3_fixture():
  target = TodaPrimaryGroup(
    group_dimension=16,
    sphere_dimension=9,
  )

  generator = HomotopyElement(
    name="sigma_9",
    dimension=16,
    generator=GeneratorSymbol(
      family="σ",
      index=9,
    ),
  )

  leaf_step = ProofStep(
    conclusion=Relation(
      lhs="leaf lhs",
      rhs="leaf rhs",
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  middle_step = ProofStep(
    conclusion=Relation(
      lhs="middle lhs",
      rhs="middle rhs",
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      leaf_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  sibling_step = ProofStep(
    conclusion=Relation(
      lhs="sibling lhs",
      rhs="sibling rhs",
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  group_structure = FiniteCyclicGroup(
    order=16,
    generator=generator,
  )

  root_step = ProofStep(
    conclusion=Relation(
      lhs=target,
      rhs=group_structure,
      relation_type=RelationType.EQUALITY,
    ),
    premises=(
      middle_step,
      sibling_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  source_entry = ProofRepositoryEntry(
    key="phase131.fixture.pi16_9",
    step=root_step,
    phase="131-3",
    theorem="Phase 131-3 group-result replay fixture",
  )

  group_result = TodaGroupResult(
    target=target,
    group_structure=group_structure,
    generators=(
      generator,
    ),
    generator_orders=(
      16,
    ),
    source_entry=source_entry,
    proof_step=root_step,
  )

  return {
    "target": target,
    "generator": generator,
    "leaf_step": leaf_step,
    "middle_step": middle_step,
    "sibling_step": sibling_step,
    "root_step": root_step,
    "source_entry": source_entry,
    "group_result": group_result,
  }


def build_phase131_3_zero_group_fixture():
  target = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=2,
  )

  premise_step = ProofStep(
    conclusion=Relation(
      lhs="zero premise lhs",
      rhs="zero premise rhs",
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  root_step = ProofStep(
    conclusion=(
      TodaPrimaryGroupZeroStatement(
        group=target,
      )
    ),
    premises=(
      premise_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  source_entry = ProofRepositoryEntry(
    key="phase131.fixture.pi9_2",
    step=root_step,
    phase="131-3",
    theorem="Phase 131-3 zero-group replay fixture",
  )

  group_result = TodaGroupResult(
    target=target,
    group_structure=None,
    generators=(),
    generator_orders=(),
    source_entry=source_entry,
    proof_step=root_step,
  )

  return {
    "target": target,
    "premise_step": premise_step,
    "root_step": root_step,
    "source_entry": source_entry,
    "group_result": group_result,
  }


def test_phase131_3_default_replay_preserves_group_result_source_and_root_identity():
  data = build_phase131_3_fixture()

  replay = build_toda_group_result_proof_replay(
    data[
      "group_result"
    ]
  )

  assert isinstance(
    replay,
    TodaGroupResultProofReplayResult,
  )
  assert (
    replay.group_result
    is data[
      "group_result"
    ]
  )
  assert (
    replay.source_entry
    is data[
      "source_entry"
    ]
  )
  assert (
    replay.root_step
    is data[
      "root_step"
    ]
  )
  assert replay.max_depth == 1


def test_phase131_3_default_replay_contains_result_and_direct_premises_only():
  data = build_phase131_3_fixture()

  replay = build_toda_group_result_proof_replay(
    data[
      "group_result"
    ]
  )

  assert tuple(
    step.depth
    for step in replay.steps
  ) == (
    0,
    1,
    1,
  )

  assert tuple(
    step.proof_step
    for step in replay.steps
  ) == (
    data[
      "root_step"
    ],
    data[
      "middle_step"
    ],
    data[
      "sibling_step"
    ],
  )

  assert all(
    step.proof_step
    is not data[
      "leaf_step"
    ]
    for step in replay.steps
  )


def test_phase131_3_zero_depth_replay_contains_only_group_result_root():
  data = build_phase131_3_fixture()

  replay = build_toda_group_result_proof_replay(
    data[
      "group_result"
    ],
    max_depth=0,
  )

  assert len(
    replay.steps
  ) == 1
  assert replay.steps[
    0
  ].depth == 0
  assert (
    replay.steps[
      0
    ].proof_step
    is data[
      "root_step"
    ]
  )


def test_phase131_3_depth_two_replay_preserves_existing_proofstep_identities():
  data = build_phase131_3_fixture()

  replay = build_toda_group_result_proof_replay(
    data[
      "group_result"
    ],
    max_depth=2,
  )

  assert tuple(
    step.depth
    for step in replay.steps
  ) == (
    0,
    1,
    1,
    2,
  )

  assert tuple(
    step.proof_step
    for step in replay.steps
  ) == (
    data[
      "root_step"
    ],
    data[
      "middle_step"
    ],
    data[
      "sibling_step"
    ],
    data[
      "leaf_step"
    ],
  )

  assert len(
    {
      id(
        step.proof_step
      )
      for step in replay.steps
    }
  ) == len(
    replay.steps
  )


def test_phase131_3_replay_preserves_existing_dependency_roles():
  data = build_phase131_3_fixture()

  replay = build_toda_group_result_proof_replay(
    data[
      "group_result"
    ],
    max_depth=2,
  )

  assert (
    replay.steps[
      0
    ].role
    is TodaProofDependencyRole.GROUP_STRUCTURE
  )
  assert all(
    step.role
    is TodaProofDependencyRole.RELATION
    for step in replay.steps[
      1:
    ]
  )


def test_phase131_3_zero_group_replay_does_not_require_generator_lookup():
  data = build_phase131_3_zero_group_fixture()

  replay = build_toda_group_result_proof_replay(
    data[
      "group_result"
    ],
    max_depth=1,
  )

  assert replay.group_result.generators == ()
  assert replay.group_result.generator_orders == ()
  assert (
    replay.root_step
    is data[
      "root_step"
    ]
  )
  assert tuple(
    step.depth
    for step in replay.steps
  ) == (
    0,
    1,
  )
  assert (
    replay.steps[
      0
    ].role
    is TodaProofDependencyRole.GROUP_STRUCTURE
  )


def test_phase131_3_replay_rejects_invalid_group_result():
  with pytest.raises(
    TypeError,
    match="group_result must be a TodaGroupResult",
  ):
    build_toda_group_result_proof_replay(
      "not-a-group-result"
    )


def test_phase131_3_replay_rejects_invalid_max_depth():
  data = build_phase131_3_fixture()

  with pytest.raises(
    TypeError,
    match="max_depth must be an int",
  ):
    build_toda_group_result_proof_replay(
      data[
        "group_result"
      ],
      max_depth=True,
    )

  with pytest.raises(
    ValueError,
    match="max_depth must be nonnegative",
  ):
    build_toda_group_result_proof_replay(
      data[
        "group_result"
      ],
      max_depth=-1,
    )
