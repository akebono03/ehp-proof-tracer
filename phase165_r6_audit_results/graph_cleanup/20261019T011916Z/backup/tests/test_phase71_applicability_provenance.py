from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase71_toda512_integration import (
  build_phase71_5_data,
)
from toda_rules import (
  Toda512DeltaInjectivityStatement,
  TodaDeltaInjectiveStatement,
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
def build_phase71_6_data():
  phase71_5 = (
    build_phase71_5_data()
  )

  phase71_2 = (
    phase71_5[
      "phase71_2"
    ]
  )

  phase71_3 = (
    phase71_5[
      "phase71_3"
    ]
  )

  phase71_4 = (
    phase71_5[
      "phase71_4"
    ]
  )

  integration_step = (
    phase71_5[
      "integration_step"
    ]
  )

  n4_step = (
    phase71_5[
      "n4_step"
    ]
  )

  n5_step = (
    phase71_5[
      "n5_step"
    ]
  )

  n6_step = (
    phase71_5[
      "n6_step"
    ]
  )

  n4_delta_eta9_squared_step = (
    phase71_2[
      "delta_eta9_squared_step"
    ]
  )

  n4_pi9_4_step = (
    phase71_2[
      "pi9_4_step"
    ]
  )

  n4_prop53_step = (
    phase71_2[
      "prop53_step"
    ]
  )

  n5_delta_eta11_step = (
    phase71_3[
      "delta_eta11_step"
    ]
  )

  n5_pi10_5_step = (
    phase71_3[
      "pi10_5_step"
    ]
  )

  n5_prop51_step = (
    phase71_3[
      "prop51_step"
    ]
  )

  n6_pi13_13_step = (
    phase71_4[
      "pi13_13_step"
    ]
  )

  n6_pi11_6_step = (
    phase71_4[
      "pi11_6_step"
    ]
  )

  branch_steps = (
    n4_step,
    n5_step,
    n6_step,
  )

  n4_direct_dependencies = (
    n4_delta_eta9_squared_step,
    n4_pi9_4_step,
    n4_prop53_step,
  )

  n5_direct_dependencies = (
    n5_delta_eta11_step,
    n5_pi10_5_step,
    n5_prop51_step,
  )

  n6_direct_dependencies = (
    n6_pi13_13_step,
    n6_pi11_6_step,
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

  return {
    "phase71_5": phase71_5,
    "phase71_2": phase71_2,
    "phase71_3": phase71_3,
    "phase71_4": phase71_4,
    "integration_step": (
      integration_step
    ),
    "n4_step": n4_step,
    "n5_step": n5_step,
    "n6_step": n6_step,
    "branch_steps": branch_steps,
    "n4_delta_eta9_squared_step": (
      n4_delta_eta9_squared_step
    ),
    "n4_pi9_4_step": (
      n4_pi9_4_step
    ),
    "n4_prop53_step": (
      n4_prop53_step
    ),
    "n5_delta_eta11_step": (
      n5_delta_eta11_step
    ),
    "n5_pi10_5_step": (
      n5_pi10_5_step
    ),
    "n5_prop51_step": (
      n5_prop51_step
    ),
    "n6_pi13_13_step": (
      n6_pi13_13_step
    ),
    "n6_pi11_6_step": (
      n6_pi11_6_step
    ),
    "n4_direct_dependencies": (
      n4_direct_dependencies
    ),
    "n5_direct_dependencies": (
      n5_direct_dependencies
    ),
    "n6_direct_dependencies": (
      n6_direct_dependencies
    ),
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
  }


def test_phase71_6_final_is_toda512_aggregate():
  data = build_phase71_6_data()

  assert isinstance(
    data[
      "integration_step"
    ].conclusion,
    Toda512DeltaInjectivityStatement,
  )


def test_phase71_6_final_aggregate_is_inference():
  data = build_phase71_6_data()

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_6_final_aggregate_is_not_given():
  data = build_phase71_6_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase71_6_all_three_cases_are_inference():
  data = build_phase71_6_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase71_6_all_three_cases_are_delta_injectivity():
  data = build_phase71_6_data()

  assert all(
    isinstance(
      step.conclusion,
      TodaDeltaInjectiveStatement,
    )
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase71_6_final_direct_premises_are_exactly_three_cases():
  data = build_phase71_6_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "n4_step"
      ],
      data[
        "n5_step"
      ],
      data[
        "n6_step"
      ],
    )
  )


def test_phase71_6_final_reaches_all_three_cases():
  data = build_phase71_6_data()

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
    in data[
      "branch_steps"
    ]
  )


def test_phase71_6_n4_direct_dependencies_are_exact():
  data = build_phase71_6_data()

  assert (
    data[
      "n4_step"
    ].premises
    == data[
      "n4_direct_dependencies"
    ]
  )


def test_phase71_6_n5_direct_dependencies_are_exact():
  data = build_phase71_6_data()

  assert (
    data[
      "n5_step"
    ].premises
    == data[
      "n5_direct_dependencies"
    ]
  )


def test_phase71_6_n6_direct_dependencies_are_exact():
  data = build_phase71_6_data()

  assert (
    data[
      "n6_step"
    ].premises
    == data[
      "n6_direct_dependencies"
    ]
  )


def test_phase71_6_final_reaches_n4_upstream_dependencies():
  data = build_phase71_6_data()

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
    in data[
      "n4_direct_dependencies"
    ]
  )


def test_phase71_6_final_reaches_n5_upstream_dependencies():
  data = build_phase71_6_data()

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
    in data[
      "n5_direct_dependencies"
    ]
  )


def test_phase71_6_final_reaches_n6_upstream_dependencies():
  data = build_phase71_6_data()

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
    in data[
      "n6_direct_dependencies"
    ]
  )


def test_phase71_6_final_graph_is_acyclic():
  data = build_phase71_6_data()

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


def test_phase71_6_final_conclusion_not_in_ancestors():
  data = build_phase71_6_data()

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


def test_phase71_6_n4_branch_is_acyclic():
  data = build_phase71_6_data()

  assert (
    id(
      data[
        "n4_step"
      ]
    )
    not in data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "n4_step"
        ]
      )
    ]
  )


def test_phase71_6_n5_branch_is_acyclic():
  data = build_phase71_6_data()

  assert (
    id(
      data[
        "n5_step"
      ]
    )
    not in data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "n5_step"
        ]
      )
    ]
  )


def test_phase71_6_n6_branch_is_acyclic():
  data = build_phase71_6_data()

  assert (
    id(
      data[
        "n6_step"
      ]
    )
    not in data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "n6_step"
        ]
      )
    ]
  )


def test_phase71_6_n4_branch_does_not_depend_on_final():
  data = build_phase71_6_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "n4_step"
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


def test_phase71_6_n5_branch_does_not_depend_on_final():
  data = build_phase71_6_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "n5_step"
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


def test_phase71_6_n6_branch_does_not_depend_on_final():
  data = build_phase71_6_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "n6_step"
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


def test_phase71_6_n4_conclusion_not_in_own_ancestors():
  data = build_phase71_6_data()

  conclusion = (
    data[
      "n4_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != conclusion
    for ancestor
    in data[
      "branch_ancestors"
    ][
      id(
        data[
          "n4_step"
        ]
      )
    ]
  )


def test_phase71_6_n5_conclusion_not_in_own_ancestors():
  data = build_phase71_6_data()

  conclusion = (
    data[
      "n5_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != conclusion
    for ancestor
    in data[
      "branch_ancestors"
    ][
      id(
        data[
          "n5_step"
        ]
      )
    ]
  )


def test_phase71_6_n6_conclusion_not_in_own_ancestors():
  data = build_phase71_6_data()

  conclusion = (
    data[
      "n6_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != conclusion
    for ancestor
    in data[
      "branch_ancestors"
    ][
      id(
        data[
          "n6_step"
        ]
      )
    ]
  )


def test_phase71_6_n4_upstream_results_are_inference():
  data = build_phase71_6_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "n4_direct_dependencies"
    ]
  )


def test_phase71_6_n5_upstream_results_are_inference():
  data = build_phase71_6_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "n5_direct_dependencies"
    ]
  )


def test_phase71_6_n6_preserves_given_inference_boundary():
  data = build_phase71_6_data()

  assert (
    data[
      "n6_pi13_13_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "n6_pi11_6_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase71_6_n4_does_not_depend_on_other_phase71_cases():
  data = build_phase71_6_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "n4_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "n5_step"
      ]
    )
    not in ancestor_ids
  )

  assert (
    id(
      data[
        "n6_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase71_6_n5_does_not_depend_on_other_phase71_cases():
  data = build_phase71_6_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "n5_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "n4_step"
      ]
    )
    not in ancestor_ids
  )

  assert (
    id(
      data[
        "n6_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase71_6_n6_does_not_depend_on_other_phase71_cases():
  data = build_phase71_6_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "n6_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "n4_step"
      ]
    )
    not in ancestor_ids
  )

  assert (
    id(
      data[
        "n5_step"
      ]
    )
    not in ancestor_ids
  )




