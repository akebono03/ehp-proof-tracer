from functools import lru_cache

import pytest

from test_phase92_actual_ehp_extraction import (
  build_phase92_3_data,
)
from toda_ehp_exactness_provenance import (
  TodaEHPExactnessUseProvenanceResult,
)
from toda_ehp_result import (
  TodaEHPSequenceResult,
)
from toda_explanation import (
  TodaRepresentativeExplanationResult,
  build_toda_representative_explanation,
)
from toda_group_result import TodaGroupResult
from toda_proof_dependency import (
  TodaProofDependencyResult,
  TodaProofDependencyRole,
)


@lru_cache(maxsize=1)
def build_phase93_5_data():
  phase92_3 = (
    build_phase92_3_data()
  )

  explanation = (
    build_toda_representative_explanation(
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
    "explanation": explanation,
  }


def test_phase93_5_returns_representative_explanation_result():
  data = build_phase93_5_data()

  assert isinstance(
    data[
      "explanation"
    ],
    TodaRepresentativeExplanationResult,
  )


def test_phase93_5_preserves_group_result_identity():
  data = build_phase93_5_data()

  assert (
    data[
      "explanation"
    ].group_result
    is data[
      "group_result"
    ]
  )


def test_phase93_5_preserves_actual_target():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  assert (
    explanation.target
    is explanation
    .group_result
    .target
  )


def test_phase93_5_integrates_actual_ehp_result():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  assert isinstance(
    explanation.ehp_result,
    TodaEHPSequenceResult,
  )

  assert (
    explanation.ehp_result.target
    == explanation.target
  )


def test_phase93_5_integrates_actual_exactness_provenance():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  assert isinstance(
    explanation.exactness_provenance,
    TodaEHPExactnessUseProvenanceResult,
  )

  assert (
    explanation
    .exactness_provenance
    .ehp_result
    is explanation.ehp_result
  )


def test_phase93_5_integrates_actual_dependency_result():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  assert isinstance(
    explanation.dependency_result,
    TodaProofDependencyResult,
  )

  assert (
    explanation
    .dependency_result
    .root_step
    is explanation
    .group_result
    .proof_step
  )


def test_phase93_5_preserves_actual_phase68_final_step_identity():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  assert (
    explanation
    .dependency_result
    .root_step
    is data[
      "phase68"
    ][
      "final_step"
    ]
  )


def test_phase93_5_exposes_actual_ehp_exactness_dependencies():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  dependencies = (
    explanation
    .dependencies_for_role(
      TodaProofDependencyRole
      .EHP_EXACTNESS
    )
  )

  assert dependencies

  expected_steps = tuple(
    use.exactness_step
    for use in (
      explanation
      .exactness_provenance
      .uses
    )
  )

  actual_steps = tuple(
    dependency.proof_step
    for dependency in (
      dependencies
    )
  )

  assert all(
    any(
      actual is expected
      for actual in actual_steps
    )
    for expected in expected_steps
  )


def test_phase93_5_exposes_actual_group_structure_dependency():
  data = build_phase93_5_data()

  dependencies = (
    data[
      "explanation"
    ].dependencies_for_role(
      TodaProofDependencyRole
      .GROUP_STRUCTURE
    )
  )

  assert any(
    dependency.proof_step
    is data[
      "phase68"
    ][
      "pi8_4_step"
    ]
    for dependency in dependencies
  )


def test_phase93_5_exposes_actual_map_property_dependencies():
  data = build_phase93_5_data()

  dependencies = (
    data[
      "explanation"
    ].dependencies_for_role(
      TodaProofDependencyRole
      .MAP_PROPERTY
    )
  )

  expected_steps = (
    data[
      "phase68"
    ][
      "delta_injective_step"
    ],
    data[
      "phase68"
    ][
      "hopf_zero_step"
    ],
    data[
      "phase68"
    ][
      "suspension_surjective_step"
    ],
  )

  assert all(
    any(
      dependency.proof_step
      is expected_step
      for dependency in dependencies
    )
    for expected_step in expected_steps
  )


def test_phase93_5_exposes_actual_relation_dependencies():
  data = build_phase93_5_data()

  dependencies = (
    data[
      "explanation"
    ].dependencies_for_role(
      TodaProofDependencyRole
      .RELATION
    )
  )

  expected_steps = (
    data[
      "phase68"
    ][
      "delta_eta9_step"
    ],
    data[
      "phase68"
    ][
      "generator_bridge_step"
    ],
  )

  assert all(
    any(
      dependency.proof_step
      is expected_step
      for dependency in dependencies
    )
    for expected_step in expected_steps
  )


def test_phase93_5_exposes_actual_definition_dependency():
  data = build_phase93_5_data()

  dependencies = (
    data[
      "explanation"
    ].dependencies_for_role(
      TodaProofDependencyRole
      .DEFINITION
    )
  )

  assert any(
    dependency.proof_step
    is data[
      "phase68"
    ][
      "nu5_definition_step"
    ]
    for dependency in dependencies
  )


def test_phase93_5_dependency_role_filter_preserves_order():
  data = build_phase93_5_data()

  explanation = data[
    "explanation"
  ]

  role = (
    TodaProofDependencyRole
    .MAP_PROPERTY
  )

  expected = tuple(
    dependency
    for dependency in (
      explanation
      .dependency_result
      .dependencies
    )
    if dependency.role == role
  )

  assert (
    explanation
    .dependencies_for_role(
      role
    )
    == expected
  )


def test_phase93_5_dependency_role_filter_rejects_invalid_role():
  data = build_phase93_5_data()

  with pytest.raises(
    TypeError,
    match=(
      "role must be a "
      "TodaProofDependencyRole"
    ),
  ):
    data[
      "explanation"
    ].dependencies_for_role(
      "map_property"
    )


def test_phase93_5_does_not_replace_group_proof_step():
  data = build_phase93_5_data()

  assert (
    data[
      "explanation"
    ].group_result.proof_step
    is data[
      "phase92_3"
    ][
      "entry"
    ].step
  )


def test_phase93_5_builder_rejects_non_group_result():
  with pytest.raises(
    TypeError,
    match=(
      "group_result must be "
      "a TodaGroupResult"
    ),
  ):
    build_toda_representative_explanation(
      "not a group result"
    )


def test_phase93_5_group_result_type_is_preserved():
  data = build_phase93_5_data()

  assert isinstance(
    data[
      "explanation"
    ].group_result,
    TodaGroupResult,
  )
