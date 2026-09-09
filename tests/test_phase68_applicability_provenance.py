from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase68_prop58_integration import (
  build_phase68_11_data,
)
from test_phase68_toda59_eta3_nu4 import (
  build_phase68_7_data,
)
from toda_rules import (
  Toda58EquationStatement,
  TodaProp58FiniteDimensionalStatement,
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
def build_phase68_12_data():
  phase68_11 = (
    build_phase68_11_data()
  )

  phase68_7 = (
    build_phase68_7_data()
  )

  integration_step = (
    phase68_11[
      "integration_step"
    ]
  )

  branch_steps = (
    phase68_11[
      "pi6_2_step"
    ],
    phase68_11[
      "pi7_3_step"
    ],
    phase68_11[
      "pi8_4_step"
    ],
    phase68_11[
      "pi9_5_step"
    ],
    phase68_11[
      "higher_zero_step"
    ],
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

  toda58_step = (
    phase68_11[
      "phase68_6"
    ][
      "toda58_step"
    ]
  )

  toda59_step = (
    phase68_7[
      "final_step"
    ]
  )

  pi6_2_step = (
    phase68_11[
      "pi6_2_step"
    ]
  )

  pi7_3_step = (
    phase68_11[
      "pi7_3_step"
    ]
  )

  pi8_4_step = (
    phase68_11[
      "pi8_4_step"
    ]
  )

  pi9_5_step = (
    phase68_11[
      "pi9_5_step"
    ]
  )

  higher_zero_step = (
    phase68_11[
      "higher_zero_step"
    ]
  )

  return {
    "phase68_11": phase68_11,
    "phase68_7": phase68_7,
    "integration_step": (
      integration_step
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
    "toda58_step": toda58_step,
    "toda59_step": toda59_step,
    "pi6_2_step": pi6_2_step,
    "pi7_3_step": pi7_3_step,
    "pi8_4_step": pi8_4_step,
    "pi9_5_step": pi9_5_step,
    "higher_zero_step": (
      higher_zero_step
    ),
    "higher_range_step": (
      phase68_11[
        "higher_range_step"
      ]
    ),
  }


def test_phase68_12_final_is_prop58_aggregate():
  data = build_phase68_12_data()

  assert isinstance(
    data[
      "integration_step"
    ].conclusion,
    TodaProp58FiniteDimensionalStatement,
  )


def test_phase68_12_final_aggregate_is_inference():
  data = build_phase68_12_data()

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_12_final_aggregate_is_not_given():
  data = build_phase68_12_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase68_12_all_five_branches_are_inference():
  data = build_phase68_12_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase68_12_scope_is_given():
  data = build_phase68_12_data()

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
    == 6
  )


def test_phase68_12_final_direct_premises_are_exactly_five_branches_and_scope():
  data = build_phase68_12_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "pi6_2_step"
      ],
      data[
        "pi7_3_step"
      ],
      data[
        "pi8_4_step"
      ],
      data[
        "pi9_5_step"
      ],
      data[
        "higher_zero_step"
      ],
      data[
        "higher_range_step"
      ],
    )
  )


def test_phase68_12_final_reaches_all_direct_dependencies():
  data = build_phase68_12_data()

  expected_steps = (
    data[
      "pi6_2_step"
    ],
    data[
      "pi7_3_step"
    ],
    data[
      "pi8_4_step"
    ],
    data[
      "pi9_5_step"
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


def test_phase68_12_final_graph_is_acyclic():
  data = build_phase68_12_data()

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


def test_phase68_12_final_conclusion_not_in_ancestors():
  data = build_phase68_12_data()

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


def test_phase68_12_pi6_2_branch_does_not_depend_on_final():
  data = build_phase68_12_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi6_2_step"
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


def test_phase68_12_pi7_3_branch_does_not_depend_on_final():
  data = build_phase68_12_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi7_3_step"
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


def test_phase68_12_pi8_4_branch_does_not_depend_on_final():
  data = build_phase68_12_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi8_4_step"
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


def test_phase68_12_pi9_5_branch_does_not_depend_on_final():
  data = build_phase68_12_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "pi9_5_step"
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


def test_phase68_12_higher_branch_does_not_depend_on_final():
  data = build_phase68_12_data()

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


def test_phase68_12_phase66_toda58_is_derived():
  data = build_phase68_12_data()

  assert isinstance(
    data[
      "toda58_step"
    ].conclusion,
    Toda58EquationStatement,
  )

  assert (
    data[
      "toda58_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_12_pi7_3_does_not_depend_on_phase66_toda58():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi7_3_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "toda58_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase68_12_pi8_4_does_not_depend_on_phase66_toda58():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi8_4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "toda58_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase68_12_pi9_5_reaches_phase66_toda58():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi9_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "toda58_step"
      ]
    )
    in ancestor_ids
  )


def test_phase68_12_higher_zero_reaches_phase66_toda58():
  data = build_phase68_12_data()

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
        "toda58_step"
      ]
    )
    in ancestor_ids
  )


def test_phase68_12_toda59_is_derived():
  data = build_phase68_12_data()

  assert (
    data[
      "toda59_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase68_12_pi7_3_does_not_depend_on_toda59():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi7_3_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "toda59_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase68_12_toda59_does_not_depend_on_final_aggregate():
  data = build_phase68_12_data()

  ancestors = collect_ancestor_steps(
    data[
      "toda59_step"
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


def test_phase68_12_toda59_does_not_depend_on_pi9_5():
  data = build_phase68_12_data()

  ancestor_ids = {
    id(
      ancestor
    )
    for ancestor
    in collect_ancestor_steps(
      data[
        "toda59_step"
      ]
    )
  }

  assert (
    id(
      data[
        "pi9_5_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase68_12_pi6_2_is_upstream_of_pi7_3():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi7_3_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi6_2_step"
      ]
    )
    in ancestor_ids
  )


def test_phase68_12_pi7_3_is_upstream_of_pi8_4():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi8_4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi7_3_step"
      ]
    )
    in ancestor_ids
  )


def test_phase68_12_pi8_4_is_upstream_of_pi9_5():
  data = build_phase68_12_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "pi9_5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "pi8_4_step"
      ]
    )
    in ancestor_ids
  )


def test_phase68_12_pi9_5_is_upstream_of_higher_zero():
  data = build_phase68_12_data()

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
        "pi9_5_step"
      ]
    )
    in ancestor_ids
  )


def test_phase68_12_final_aggregate_has_no_stable_g4_literature():
  data = build_phase68_12_data()

  literature = (
    data[
      "integration_step"
    ].conclusion
    .literature_statements
  )

  assert all(
    "(G_4;2)"
    not in statement.statement
    for statement
    in literature
  )


