from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase65_prop56_integration import (
  build_phase65_9_data,
)


def collect_ancestors(
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
def build_phase65_provenance_data():
  data = build_phase65_9_data()

  integration_step = (
    data[
      "integration_step"
    ]
  )

  integration_ancestors = (
    collect_ancestors(
      integration_step
    )
  )

  branch_steps = (
    data[
      "pi5_2_step"
    ],
    data[
      "pi6_3_step"
    ],
    data[
      "pi7_4_step"
    ],
    data[
      "pi8_5_step"
    ],
    data[
      "higher_step"
    ],
  )

  branch_ancestors = {
    id(step): collect_ancestors(
      step
    )
    for step in branch_steps
  }

  return {
    "data": data,
    "integration_step": (
      integration_step
    ),
    "integration_ancestors": (
      integration_ancestors
    ),
    "integration_ancestor_ids": {
      id(
        ancestor
      )
      for ancestor
      in integration_ancestors
    },
    "branch_steps": branch_steps,
    "branch_ancestors": (
      branch_ancestors
    ),
  }


def test_phase65_10_final_graph_is_acyclic():
  data = build_phase65_provenance_data()

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


def test_phase65_10_final_conclusion_not_in_ancestors():
  data = build_phase65_provenance_data()

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


def test_phase65_10_final_reaches_all_direct_results():
  data = build_phase65_provenance_data()

  phase65 = data[
    "data"
  ]

  expected_steps = (
    phase65[
      "pi5_2_step"
    ],
    phase65[
      "pi6_3_step"
    ],
    phase65[
      "pi7_4_step"
    ],
    phase65[
      "pi8_5_step"
    ],
    phase65[
      "higher_step"
    ],
    phase65[
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


def test_phase65_10_direct_theorem_results_are_inference():
  data = build_phase65_provenance_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase65_10_scope_is_given():
  data = build_phase65_provenance_data()

  assert (
    data[
      "data"
    ][
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase65_10_pi5_2_branch_does_not_depend_on_final():
  data = build_phase65_provenance_data()

  step = (
    data[
      "data"
    ][
      "pi5_2_step"
    ]
  )

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        step
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor in ancestors
  )


def test_phase65_10_pi6_3_branch_does_not_depend_on_final():
  data = build_phase65_provenance_data()

  step = (
    data[
      "data"
    ][
      "pi6_3_step"
    ]
  )

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        step
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor in ancestors
  )


def test_phase65_10_pi7_4_branch_does_not_depend_on_final():
  data = build_phase65_provenance_data()

  step = (
    data[
      "data"
    ][
      "pi7_4_step"
    ]
  )

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        step
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor in ancestors
  )


def test_phase65_10_pi8_5_branch_does_not_depend_on_final():
  data = build_phase65_provenance_data()

  step = (
    data[
      "data"
    ][
      "pi8_5_step"
    ]
  )

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        step
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor in ancestors
  )


def test_phase65_10_higher_branch_does_not_depend_on_final():
  data = build_phase65_provenance_data()

  step = (
    data[
      "data"
    ][
      "higher_step"
    ]
  )

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        step
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "integration_step"
    ]
    for ancestor in ancestors
  )


def test_phase65_10_final_aggregate_is_inference():
  data = build_phase65_provenance_data()

  assert (
    data[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase65_10_final_aggregate_is_not_given():
  data = build_phase65_provenance_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


