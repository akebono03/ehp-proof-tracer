from functools import lru_cache

import pytest

from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  LiteratureReference,
  LiteratureStatement,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  order_relation,
)
from test_phase93_actual_dependency_extraction import (
  build_phase93_3_data,
)
from toda_proof_dependency import (
  TodaProofDependency,
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)


@lru_cache(maxsize=1)
def build_phase93_4_data():
  phase93_3 = (
    build_phase93_3_data()
  )

  return {
    "phase93_3": phase93_3,
    "phase68": phase93_3[
      "phase68"
    ],
    "dependency_result": (
      phase93_3[
        "dependency_result"
      ]
    ),
  }


def find_dependency_for_step(
  dependency_result,
  expected_step,
):
  return next(
    dependency
    for dependency in (
      dependency_result
      .dependencies
    )
    if (
      dependency.proof_step
      is expected_step
    )
  )


def test_phase93_4_role_enum_values_are_stable():
  assert (
    TodaProofDependencyRole
    .EHP_EXACTNESS
    .value
    == "ehp_exactness"
  )

  assert (
    TodaProofDependencyRole
    .EHP_WINDOW
    .value
    == "ehp_window"
  )

  assert (
    TodaProofDependencyRole
    .GROUP_STRUCTURE
    .value
    == "group_structure"
  )

  assert (
    TodaProofDependencyRole
    .RELATION
    .value
    == "relation"
  )

  assert (
    TodaProofDependencyRole
    .ORDER
    .value
    == "order"
  )

  assert (
    TodaProofDependencyRole
    .MAP_PROPERTY
    .value
    == "map_property"
  )

  assert (
    TodaProofDependencyRole
    .DEFINITION
    .value
    == "definition"
  )

  assert (
    TodaProofDependencyRole
    .LITERATURE
    .value
    == "literature"
  )

  assert (
    TodaProofDependencyRole
    .OTHER
    .value
    == "other"
  )


def test_phase93_4_dependency_default_role_preserves_phase93_2_api():
  step = ProofStep(
    conclusion="dependency",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  dependency = (
    TodaProofDependency(
      proof_step=step,
      depth=1,
    )
  )

  assert (
    dependency.role
    == TodaProofDependencyRole.OTHER
  )


def test_phase93_4_dependency_rejects_invalid_role():
  step = ProofStep(
    conclusion="dependency",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  with pytest.raises(
    TypeError,
    match=(
      "role must be a "
      "TodaProofDependencyRole"
    ),
  ):
    TodaProofDependency(
      proof_step=step,
      depth=1,
      role="relation",
    )


def test_phase93_4_actual_exactness_steps_are_classified():
  data = build_phase93_4_data()

  dependency_result = data[
    "dependency_result"
  ]

  phase68 = data[
    "phase68"
  ]

  for key in (
    "delta_e_exactness_step",
    "e_h_exactness_step",
    "h_delta_exactness_step",
  ):
    dependency = (
      find_dependency_for_step(
        dependency_result,
        phase68[
          key
        ],
      )
    )

    assert (
      dependency.role
      == (
        TodaProofDependencyRole
        .EHP_EXACTNESS
      )
    )


def test_phase93_4_actual_ehp_windows_are_classified():
  data = build_phase93_4_data()

  dependency_result = data[
    "dependency_result"
  ]

  phase68 = data[
    "phase68"
  ]

  for key in (
    "delta_e_window_step",
    "e_h_window_step",
    "h_delta_window_step",
  ):
    dependency = (
      find_dependency_for_step(
        dependency_result,
        phase68[
          key
        ],
      )
    )

    assert (
      dependency.role
      == (
        TodaProofDependencyRole
        .EHP_WINDOW
      )
    )


def test_phase93_4_actual_pi8_4_group_is_classified():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "pi8_4_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .GROUP_STRUCTURE
    )
  )


def test_phase93_4_actual_hopf_zero_is_map_property():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "hopf_zero_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .MAP_PROPERTY
    )
  )


def test_phase93_4_actual_suspension_surjective_is_map_property():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "suspension_surjective_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .MAP_PROPERTY
    )
  )


def test_phase93_4_actual_delta_injective_is_map_property():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "delta_injective_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .MAP_PROPERTY
    )
  )


def test_phase93_4_actual_nu5_definition_is_classified():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "nu5_definition_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .DEFINITION
    )
  )


def test_phase93_4_actual_delta_eta9_is_relation():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "delta_eta9_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .RELATION
    )
  )


def test_phase93_4_actual_generator_bridge_is_relation():
  data = build_phase93_4_data()

  dependency = (
    find_dependency_for_step(
      data[
        "dependency_result"
      ],
      data[
        "phase68"
      ][
        "generator_bridge_step"
      ],
    )
  )

  assert (
    dependency.role
    == (
      TodaProofDependencyRole
      .RELATION
    )
  )


def test_phase93_4_order_relation_is_classified_before_generic_relation():
  element = HomotopyElement(
    name="x",
    dimension=1,
    source=2,
    target=1,
    generator=GeneratorSymbol(
      family="x",
    ),
  )

  step = ProofStep(
    conclusion=order_relation(
      element,
      2,
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    classify_toda_proof_step_role(
      step
    )
    == TodaProofDependencyRole.ORDER
  )


def test_phase93_4_group_relation_is_classified_before_generic_relation():
  group = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=5,
  )

  generator = HomotopyElement(
    name="x",
    dimension=5,
    source=9,
    target=5,
    generator=GeneratorSymbol(
      family="x",
    ),
  )

  step = ProofStep(
    conclusion=Relation(
      lhs=group,
      rhs=FiniteCyclicGroup(
        order=2,
        generator=generator,
      ),
      relation_type=(
        RelationType.EQUALITY
      ),
    ),
    premises=(),
    rule=ProofRule.RELATION,
  )

  assert (
    classify_toda_proof_step_role(
      step
    )
    == (
      TodaProofDependencyRole
      .GROUP_STRUCTURE
    )
  )


def test_phase93_4_literature_statement_is_classified():
  step = ProofStep(
    conclusion=LiteratureStatement(
      reference=LiteratureReference(
        label="test reference",
      ),
      statement="test statement",
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    classify_toda_proof_step_role(
      step
    )
    == (
      TodaProofDependencyRole
      .LITERATURE
    )
  )


def test_phase93_4_unknown_statement_remains_other():
  step = ProofStep(
    conclusion="unknown",
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert (
    classify_toda_proof_step_role(
      step
    )
    == TodaProofDependencyRole.OTHER
  )


def test_phase93_4_classifier_rejects_non_proof_step():
  with pytest.raises(
    TypeError,
    match=(
      "proof_step must be a ProofStep"
    ),
  ):
    classify_toda_proof_step_role(
      "not a proof step"
    )
