from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase70_prop59_integration import (
  build_phase70_10_data,
)
from toda_rules import (
  TodaProp59FiniteDimensionalStatement,
)


def collect_ancestor_steps(
  step,
):
  ancestors = []
  seen_ids = set()

  def visit(
    current,
  ):
    for premise in current.premises:
      premise_id = id(
        premise
      )

      if (
        premise_id
        in seen_ids
      ):
        continue

      seen_ids.add(
        premise_id
      )

      ancestors.append(
        premise
      )

      visit(
        premise
      )

  visit(
    step
  )

  return tuple(
    ancestors
  )


@lru_cache(maxsize=1)
def build_phase70_11_data():
  phase70_10 = (
    build_phase70_10_data()
  )

  phase70_9 = (
    phase70_10[
      "phase70_9"
    ]
  )

  phase70_8 = (
    phase70_10[
      "phase70_8"
    ]
  )

  phase70_7 = (
    phase70_10[
      "phase70_7"
    ]
  )

  phase70_6 = (
    phase70_10[
      "phase70_6"
    ]
  )

  phase70_5 = (
    phase70_10[
      "phase70_5"
    ]
  )

  phase70_4 = (
    phase70_10[
      "phase70_4"
    ]
  )

  phase70_3 = (
    phase70_10[
      "phase70_3"
    ]
  )

  phase70_2 = (
    phase70_10[
      "phase70_2"
    ]
  )

  integration_step = (
    phase70_10[
      "integration_step"
    ]
  )

  pi7_2_step = (
    phase70_10[
      "pi7_2_step"
    ]
  )

  pi8_3_step = (
    phase70_10[
      "pi8_3_step"
    ]
  )

  pi9_4_step = (
    phase70_10[
      "pi9_4_step"
    ]
  )

  pi10_5_step = (
    phase70_10[
      "pi10_5_step"
    ]
  )

  pi11_6_step = (
    phase70_10[
      "pi11_6_step"
    ]
  )

  higher_zero_step = (
    phase70_10[
      "higher_zero_step"
    ]
  )

  higher_range_step = (
    phase70_10[
      "higher_range_step"
    ]
  )

  branch_steps = (
    pi7_2_step,
    pi8_3_step,
    pi9_4_step,
    pi10_5_step,
    pi11_6_step,
    higher_zero_step,
  )

  integration_ancestors = (
    collect_ancestor_steps(
      integration_step
    )
  )

  integration_ancestor_ids = {
    id(
      ancestor
    )
    for ancestor
    in integration_ancestors
  }

  branch_ancestors = {
    id(
      step
    ): collect_ancestor_steps(
      step
    )
    for step
    in branch_steps
  }

  branch_ancestor_ids = {
    id(
      step
    ): {
      id(
        ancestor
      )
      for ancestor
      in branch_ancestors[
        id(
          step
        )
      ]
    }
    for step
    in branch_steps
  }

  phase70_5_suspension_surjective_step = (
    phase70_5[
      "suspension_surjective_step"
    ]
  )

  phase70_5_delta_eta9_squared_step = (
    phase70_5[
      "delta_eta9_squared_step"
    ]
  )

  phase70_7_suspension_zero_step = (
    phase70_7[
      "suspension_zero_step"
    ]
  )

  phase70_7_delta_eta11_step = (
    phase70_7[
      "delta_eta11_step"
    ]
  )

  phase69_delta_iota11_step = (
    phase70_7[
      "delta_iota11_step"
    ]
  )

  pi12_7_zero_step = (
    phase70_9[
      "pi12_7_zero_step"
    ]
  )

  return {
    "phase70_10": phase70_10,
    "phase70_9": phase70_9,
    "phase70_8": phase70_8,
    "phase70_7": phase70_7,
    "phase70_6": phase70_6,
    "phase70_5": phase70_5,
    "phase70_4": phase70_4,
    "phase70_3": phase70_3,
    "phase70_2": phase70_2,
    "integration_step": (
      integration_step
    ),
    "pi7_2_step": pi7_2_step,
    "pi8_3_step": pi8_3_step,
    "pi9_4_step": pi9_4_step,
    "pi10_5_step": pi10_5_step,
    "pi11_6_step": pi11_6_step,
    "higher_zero_step": (
      higher_zero_step
    ),
    "higher_range_step": (
      higher_range_step
    ),
    "branch_steps": branch_steps,
    "integration_ancestors": (
      integration_ancestors
    ),
    "integration_ancestor_ids": (
      integration_ancestor_ids
    ),
    "branch_ancestors": (
      branch_ancestors
    ),
    "branch_ancestor_ids": (
      branch_ancestor_ids
    ),
    "phase70_5_suspension_surjective_step": (
      phase70_5_suspension_surjective_step
    ),
    "phase70_5_delta_eta9_squared_step": (
      phase70_5_delta_eta9_squared_step
    ),
    "phase70_7_suspension_zero_step": (
      phase70_7_suspension_zero_step
    ),
    "phase70_7_delta_eta11_step": (
      phase70_7_delta_eta11_step
    ),
    "phase69_delta_iota11_step": (
      phase69_delta_iota11_step
    ),
    "pi12_7_zero_step": (
      pi12_7_zero_step
    ),
  }


def test_phase70_11_final_is_prop59_aggregate():
  data = build_phase70_11_data()

  assert isinstance(
    data[
      "integration_step"
    ].conclusion,
    TodaProp59FiniteDimensionalStatement,
  )


def test_phase70_11_final_aggregate_is_inference():
  data = build_phase70_11_data()

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase70_11_final_aggregate_is_not_given():
  data = build_phase70_11_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase70_11_all_six_branches_are_inference():
  data = build_phase70_11_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase70_11_scope_is_given():
  data = build_phase70_11_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "higher_range_step"
    ].conclusion.right
    == 7
  )


def test_phase70_11_final_direct_premises_are_exactly_six_branches_and_scope():
  data = build_phase70_11_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "pi7_2_step"
      ],
      data[
        "pi8_3_step"
      ],
      data[
        "pi9_4_step"
      ],
      data[
        "pi10_5_step"
      ],
      data[
        "pi11_6_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase70_11_final_reaches_all_direct_dependencies():
  data = build_phase70_11_data()

  expected_steps = (
    data[
      "pi7_2_step"
    ],
    data[
      "pi8_3_step"
    ],
    data[
      "pi9_4_step"
    ],
    data[
      "pi10_5_step"
    ],
    data[
      "pi11_6_step"
    ],
    data[
      "higher_zero_step"
    ],
    data[
      "higher_range_step"
    ],
  )

  ancestor_ids = (
    data[
      "integration_ancestor_ids"
    ]
  )

  assert all(
    id(
      step
    )
    in ancestor_ids
    for step
    in expected_steps
  )


def test_phase70_11_final_graph_is_acyclic():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "integration_step"
      ]
    )
    not in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_conclusion_not_in_ancestors():
  data = build_phase70_11_data()

  final_conclusion = (
    data[
      "integration_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor
    in data[
      "integration_ancestors"
    ]
  )


def test_phase70_11_pi7_2_branch_does_not_depend_on_final():
  data = build_phase70_11_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi7_2_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase70_11_pi8_3_branch_does_not_depend_on_final():
  data = build_phase70_11_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi8_3_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase70_11_pi9_4_branch_does_not_depend_on_final():
  data = build_phase70_11_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi9_4_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase70_11_pi10_5_branch_does_not_depend_on_final():
  data = build_phase70_11_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase70_11_pi11_6_branch_does_not_depend_on_final():
  data = build_phase70_11_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi11_6_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase70_11_higher_branch_does_not_depend_on_final():
  data = build_phase70_11_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "higher_zero_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase70_11_pi7_2_is_upstream_of_pi8_3():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi8_3_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi7_2_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_pi8_3_is_upstream_of_pi9_4():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi9_4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi8_3_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_pi9_4_is_upstream_of_pi10_5():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi9_4_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_pi10_5_is_upstream_of_pi11_6():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi11_6_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi10_5_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_pi11_6_is_upstream_of_higher_zero():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "higher_zero_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi11_6_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_pi12_7_zero_is_upstream_of_higher_zero():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "higher_zero_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi12_7_zero_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_phase70_5_surjectivity_is_upstream_of_pi10_5():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_5_suspension_surjective_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_phase70_5_surjectivity_does_not_flow_backward_into_pi9_4():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi9_4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_5_suspension_surjective_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_delta_eta9_squared_is_upstream_of_pi10_5():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_5_delta_eta9_squared_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_delta_eta9_squared_does_not_flow_backward_into_pi9_4():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi9_4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_5_delta_eta9_squared_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_phase70_7_suspension_zero_is_upstream_of_pi11_6():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi11_6_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_7_suspension_zero_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_phase70_7_suspension_zero_does_not_flow_backward_into_pi10_5():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_7_suspension_zero_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_phase69_delta_iota11_is_upstream_of_pi11_6():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi11_6_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase69_delta_iota11_step"
      ]
    )
    in ancestor_ids
  )


def test_phase70_11_phase69_delta_iota11_does_not_flow_backward_into_pi9_4():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi9_4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase69_delta_iota11_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_phase69_delta_iota11_does_not_flow_backward_into_pi10_5():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase69_delta_iota11_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_delta_eta11_is_not_used_to_derive_pi10_5():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi10_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_7_delta_eta11_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_delta_eta11_is_not_used_to_derive_pi11_6():
  data = build_phase70_11_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi11_6_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "phase70_7_delta_eta11_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase70_11_final_aggregate_has_no_stable_g5_literature():
  data = build_phase70_11_data()

  literature = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements
  )

  assert all(
    "(G_5;2)"
    not in statement.statement
    for statement
    in literature
  )


def test_phase70_11_final_aggregate_reaches_pi7_2():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "pi7_2_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_aggregate_reaches_pi8_3():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "pi8_3_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_aggregate_reaches_pi9_4():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "pi9_4_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_aggregate_reaches_pi10_5():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "pi10_5_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_aggregate_reaches_pi11_6():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "pi11_6_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_aggregate_reaches_higher_zero():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "higher_zero_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


def test_phase70_11_final_aggregate_reaches_scope():
  data = build_phase70_11_data()

  assert (
    id(
      data[
        "higher_range_step"
      ]
    )
    in data[
      "integration_ancestor_ids"
    ]
  )


