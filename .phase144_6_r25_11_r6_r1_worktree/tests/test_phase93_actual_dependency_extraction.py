from functools import lru_cache

import pytest

from proof import (
  ProofRule,
  ProofStep,
)
from proof_repository import ProofRepositoryEntry
from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_group_result import TodaGroupResult
from toda_proof_dependency import (
  TodaProofDependencyResult,
  extract_toda_proof_dependencies,
)


@lru_cache(maxsize=1)
def build_phase93_3_data():
  phase92_3 = (
    build_phase92_3_data()
  )

  dependency_result = (
    extract_toda_proof_dependencies(
      phase92_3[
        "group_result"
      ]
    )
  )

  return {
    "phase92_3": phase92_3,
    "phase68": phase92_3[
      "phase68"
    ],
    "group_result": phase92_3[
      "group_result"
    ],
    "dependency_result": (
      dependency_result
    ),
  }


def build_synthetic_group_result(
  root_step,
  key,
):
  phase92_3 = (
    build_phase92_3_data()
  )

  source_group_result = (
    phase92_3[
      "group_result"
    ]
  )

  source_entry = (
    ProofRepositoryEntry(
      key=key,
      step=root_step,
      phase="93",
      theorem=None,
    )
  )

  return TodaGroupResult(
    target=source_group_result.target,
    group_structure=(
      source_group_result
      .group_structure
    ),
    generators=(
      source_group_result
      .generators
    ),
    generator_orders=(
      source_group_result
      .generator_orders
    ),
    source_entry=source_entry,
    proof_step=root_step,
  )


def test_phase93_3_returns_dependency_result():
  data = build_phase93_3_data()

  assert isinstance(
    data[
      "dependency_result"
    ],
    TodaProofDependencyResult,
  )


def test_phase93_3_preserves_actual_root_identity():
  data = build_phase93_3_data()

  assert (
    data[
      "dependency_result"
    ].root_step
    is data[
      "group_result"
    ].proof_step
  )


def test_phase93_3_root_is_actual_phase68_final_step():
  data = build_phase93_3_data()

  assert (
    data[
      "dependency_result"
    ].root_step
    is data[
      "phase68"
    ][
      "final_step"
    ]
  )


def test_phase93_3_actual_dependencies_are_nonempty():
  data = build_phase93_3_data()

  assert (
    data[
      "dependency_result"
    ].dependencies
  )


def test_phase93_3_direct_dependencies_match_root_proof_premises():
  data = build_phase93_3_data()

  root_step = (
    data[
      "dependency_result"
    ].root_step
  )

  expected_direct_steps = tuple(
    premise
    for premise in (
      root_step.premises
    )
    if isinstance(
      premise,
      ProofStep,
    )
  )

  actual_direct_steps = tuple(
    dependency.proof_step
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
    if dependency.is_direct
  )

  assert len(
    actual_direct_steps
  ) == len(
    expected_direct_steps
  )

  assert all(
    actual is expected
    for actual, expected in zip(
      actual_direct_steps,
      expected_direct_steps,
    )
  )


def test_phase93_3_direct_dependencies_have_depth_one():
  data = build_phase93_3_data()

  direct_dependencies = tuple(
    dependency
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
    if dependency.is_direct
  )

  assert direct_dependencies

  assert all(
    dependency.depth == 1
    for dependency in (
      direct_dependencies
    )
  )


def test_phase93_3_contains_actual_ehp_exactness_steps():
  data = build_phase93_3_data()

  phase68 = data[
    "phase68"
  ]

  dependency_steps = tuple(
    dependency.proof_step
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
  )

  expected_exactness_steps = (
    phase68[
      "delta_e_exactness_step"
    ],
    phase68[
      "e_h_exactness_step"
    ],
    phase68[
      "h_delta_exactness_step"
    ],
  )

  assert all(
    any(
      actual is expected
      for actual in (
        dependency_steps
      )
    )
    for expected in (
      expected_exactness_steps
    )
  )


def test_phase93_3_contains_actual_hopf_zero_step():
  data = build_phase93_3_data()

  assert any(
    dependency.proof_step
    is data[
      "phase68"
    ][
      "hopf_zero_step"
    ]
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
  )


def test_phase93_3_contains_actual_suspension_surjective_step():
  data = build_phase93_3_data()

  assert any(
    dependency.proof_step
    is data[
      "phase68"
    ][
      "suspension_surjective_step"
    ]
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
  )


def test_phase93_3_root_is_not_returned_as_dependency():
  data = build_phase93_3_data()

  root_step = (
    data[
      "dependency_result"
    ].root_step
  )

  assert all(
    dependency.proof_step
    is not root_step
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
  )


def test_phase93_3_actual_dependency_identities_are_unique():
  data = build_phase93_3_data()

  step_ids = tuple(
    id(
      dependency.proof_step
    )
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
  )

  assert len(
    step_ids
  ) == len(
    set(
      step_ids
    )
  )


def test_phase93_3_all_dependencies_have_positive_depth():
  data = build_phase93_3_data()

  assert all(
    dependency.depth > 0
    for dependency in (
      data[
        "dependency_result"
      ].dependencies
    )
  )


def test_phase93_3_non_proof_premises_are_not_dependencies():
  premise_step = ProofStep(
    conclusion="premise",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  root_step = ProofStep(
    conclusion="root",
    premises=(
      "non proof premise",
      premise_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  result = (
    extract_toda_proof_dependencies(
      build_synthetic_group_result(
        root_step,
        "phase93.synthetic",
      )
    )
  )

  assert len(
    result.dependencies
  ) == 1

  assert (
    result.dependencies[
      0
    ].proof_step
    is premise_step
  )


def test_phase93_3_shared_dependency_uses_shortest_depth():
  shared_step = ProofStep(
    conclusion="shared",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  deep_step = ProofStep(
    conclusion="deep",
    premises=(
      shared_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  direct_step = ProofStep(
    conclusion="direct",
    premises=(
      shared_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  other_step = ProofStep(
    conclusion="other",
    premises=(
      deep_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  root_step = ProofStep(
    conclusion="root",
    premises=(
      direct_step,
      other_step,
    ),
    rule=ProofRule.INFERENCE,
  )

  result = (
    extract_toda_proof_dependencies(
      build_synthetic_group_result(
        root_step,
        "phase93.shared-depth",
      )
    )
  )

  shared_dependencies = tuple(
    dependency
    for dependency in (
      result.dependencies
    )
    if (
      dependency.proof_step
      is shared_step
    )
  )

  assert len(
    shared_dependencies
  ) == 1

  assert (
    shared_dependencies[
      0
    ].depth
    == 2
  )


def test_phase93_3_breadth_first_order_is_stable():
  first_child = ProofStep(
    conclusion="first child",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  second_child = ProofStep(
    conclusion="second child",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  first_direct = ProofStep(
    conclusion="first direct",
    premises=(
      first_child,
    ),
    rule=ProofRule.INFERENCE,
  )

  second_direct = ProofStep(
    conclusion="second direct",
    premises=(
      second_child,
    ),
    rule=ProofRule.INFERENCE,
  )

  root_step = ProofStep(
    conclusion="root",
    premises=(
      first_direct,
      second_direct,
    ),
    rule=ProofRule.INFERENCE,
  )

  result = (
    extract_toda_proof_dependencies(
      build_synthetic_group_result(
        root_step,
        "phase93.stable-order",
      )
    )
  )

  assert tuple(
    dependency.proof_step
    for dependency in (
      result.dependencies
    )
  ) == (
    first_direct,
    second_direct,
    first_child,
    second_child,
  )


def test_phase93_3_rejects_non_group_result():
  with pytest.raises(
    TypeError,
    match=(
      "group_result must be "
      "a TodaGroupResult"
    ),
  ):
    extract_toda_proof_dependencies(
      "not a group result"
    )
