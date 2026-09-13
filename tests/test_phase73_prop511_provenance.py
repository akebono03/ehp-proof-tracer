from proof import (
  ProofRule,
)
from test_phase73_prop511_finite_dimensional_integration import (
  build_phase73_8e_data,
)
from toda_rules import (
  TodaProp511FiniteDimensionalStatement,
)


def collect_ancestors(
  step,
):
  visited = set()
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if (
      current_id
      in visited
    ):
      continue

    visited.add(
      current_id
    )

    stack.extend(
      current.premises
    )

  return visited


def collect_ancestor_steps(
  step,
):
  visited = set()
  result = []
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if (
      current_id
      in visited
    ):
      continue

    visited.add(
      current_id
    )

    result.append(
      current
    )

    stack.extend(
      current.premises
    )

  return result


def test_phase73_8e_all_four_direct_mathematical_premises_are_inference():
  data = build_phase73_8e_data()

  for step in (
    data[
      "pi8_2_step"
    ],
    data[
      "pi9_3_zero_step"
    ],
    data[
      "pi10_4_step"
    ],
    data[
      "nu_squared_step"
    ],
  ):
    assert (
      step.rule
      == ProofRule.INFERENCE
    )


def test_phase73_8e_final_aggregate_is_not_given():
  data = build_phase73_8e_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase73_8e_final_reaches_all_four_branches():
  data = build_phase73_8e_data()

  ancestor_ids = (
    collect_ancestors(
      data[
        "final_step"
      ]
    )
  )

  for step in (
    data[
      "pi8_2_step"
    ],
    data[
      "pi9_3_zero_step"
    ],
    data[
      "pi10_4_step"
    ],
    data[
      "nu_squared_step"
    ],
  ):
    assert (
      id(
        step
      )
      in ancestor_ids
    )


def test_phase73_8e_final_is_not_its_own_ancestor():
  data = build_phase73_8e_data()

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in collect_ancestors(
      data[
        "final_step"
      ]
    )
  )


def test_phase73_8e_final_conclusion_absent_from_ancestors():
  data = build_phase73_8e_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  ancestor_steps = (
    collect_ancestor_steps(
      data[
        "final_step"
      ]
    )
  )

  assert all(
    step.conclusion
    != final_conclusion
    for step
    in ancestor_steps
  )


def test_phase73_8e_branches_do_not_depend_on_final_aggregate():
  data = build_phase73_8e_data()

  final_id = id(
    data[
      "final_step"
    ]
  )

  for step in (
    data[
      "pi8_2_step"
    ],
    data[
      "pi9_3_zero_step"
    ],
    data[
      "pi10_4_step"
    ],
    data[
      "nu_squared_step"
    ],
  ):
    assert (
      final_id
      not in collect_ancestors(
        step
      )
    )


def test_phase73_8e_no_stable_group_statement_in_final_aggregate():
  data = build_phase73_8e_data()

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert isinstance(
    final_statement,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    not hasattr(
      final_statement,
      "stable_group"
    )
  )

  assert (
    not hasattr(
      final_statement,
      "stable_nu_squared"
    )
  )



