from typing import (
  get_type_hints,
)

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
  Suspension,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaSuspensionKernelFreeCyclicStatement,
  TodaSuspensionSurjectiveStatement,
)


def build_phase50_4d_data():
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  pi_4_3 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )

  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )

  source_group_relation = Relation(
    lhs=pi_3_2,
    rhs=FreeCyclicGroup(
      generator=eta_2,
    ),
    relation_type=RelationType.EQUALITY,
  )

  suspension_map = TodaSuspensionMap(
    source_group=pi_3_2,
    target_group=pi_4_3,
  )

  kernel_statement = (
    TodaSuspensionKernelFreeCyclicStatement(
      map=suspension_map,
      kernel_group=FreeCyclicGroup(
        generator=Multiple(
          coefficient=2,
          expression=eta_2,
        ),
      ),
    )
  )

  surjectivity = (
    TodaSuspensionSurjectiveStatement(
      map=suspension_map,
    )
  )

  final_relation = Relation(
    lhs=pi_4_3,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Suspension(
        expression=eta_2,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  return {
    "pi_3_2": pi_3_2,
    "pi_4_3": pi_4_3,
    "eta_2": eta_2,
    "source_group_relation": (
      source_group_relation
    ),
    "suspension_map": (
      suspension_map
    ),
    "kernel_statement": (
      kernel_statement
    ),
    "surjectivity": (
      surjectivity
    ),
    "final_relation": (
      final_relation
    ),
  }


def build_phase50_4d_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "source_group_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "kernel_statement"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "surjectivity"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase50_4d_finite_cyclic_order_type():
  type_hints = get_type_hints(
    FiniteCyclicGroup
  )

  assert type_hints[
    "order"
  ] is int


def test_phase50_4d_finite_cyclic_generator_uses_expression():
  type_hints = get_type_hints(
    FiniteCyclicGroup
  )

  assert (
    type_hints[
      "generator"
    ].__name__
    == "Expression"
  )


def test_phase50_4d_expected_group_has_order_two():
  data = build_phase50_4d_data()

  assert data[
    "final_relation"
  ].rhs.order == 2


def test_phase50_4d_expected_generator_is_suspension_eta_2():
  data = build_phase50_4d_data()

  assert data[
    "final_relation"
  ].rhs.generator == (
    Suspension(
      expression=data[
        "eta_2"
      ],
    )
  )








def test_phase50_4d_final_group_is_pi_4_3():
  data = build_phase50_4d_data()

  relation = data[
    "final_relation"
  ]

  assert relation.lhs == (
    TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=3,
    )
  )


def test_phase50_4d_final_group_is_finite_cyclic():
  data = build_phase50_4d_data()

  assert isinstance(
    data[
      "final_relation"
    ].rhs,
    FiniteCyclicGroup,
  )



















