from functools import lru_cache

from proof import (
  InferenceTerminationReason,
  ProofRule,
  run_inference_until_stable_with_history,
)
from test_phase78_g0_stable_ordinary_transport import (
  build_phase78_10_data,
)
from test_phase78_g1_stable_eta_transport import (
  build_phase78_8a_data,
)
from test_phase78_g2_stable_eta_squared_transport import (
  build_phase78_8b_data,
)
from test_phase78_g3_stable_nu_transport import (
  build_phase78_8c_data,
)
from test_phase78_g4_g5_stable_zero_transport import (
  build_phase78_9_data,
)
from test_phase78_g6_stable_nu_squared_transport import (
  build_phase78_8d_data,
)
from test_phase78_g7_stable_sigma_transport import (
  build_phase78_6_data,
)
from toda_rules import (
  TodaStableG0ToG7Statement,
  toda_stable_g0_to_g7_integration_inference_rule,
)


def _collect_ancestors(
  step,
):
  ancestors = []
  visited = set()

  def visit(
    current,
  ):
    for premise in current.premises:
      premise_id = id(
        premise
      )

      if (
        premise_id
        in visited
      ):
        continue

      visited.add(
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


def _proof_graph_is_acyclic(
  step,
):
  visiting = set()
  visited = set()

  def visit(
    current,
  ):
    current_id = id(
      current
    )

    if (
      current_id
      in visiting
    ):
      return False

    if (
      current_id
      in visited
    ):
      return True

    visiting.add(
      current_id
    )

    for premise in current.premises:
      if not visit(
        premise
      ):
        return False

    visiting.remove(
      current_id
    )
    visited.add(
      current_id
    )

    return True

  return visit(
    step
  )


@lru_cache(maxsize=1)
def build_phase78_11_data():
  phase78_10 = (
    build_phase78_10_data()
  )

  phase78_8a = (
    build_phase78_8a_data()
  )

  phase78_8b = (
    build_phase78_8b_data()
  )

  phase78_8c = (
    build_phase78_8c_data()
  )

  phase78_9 = (
    build_phase78_9_data()
  )

  phase78_8d = (
    build_phase78_8d_data()
  )

  phase78_6 = (
    build_phase78_6_data()
  )

  g0_step = (
    phase78_10[
      "final_step"
    ]
  )

  g1_step = (
    phase78_8a[
      "final_step"
    ]
  )

  g2_step = (
    phase78_8b[
      "final_step"
    ]
  )

  g3_step = (
    phase78_8c[
      "final_step"
    ]
  )

  g4_step = (
    phase78_9[
      "g4_zero_step"
    ]
  )

  g5_step = (
    phase78_9[
      "g5_zero_step"
    ]
  )

  g6_step = (
    phase78_8d[
      "final_step"
    ]
  )

  g7_step = (
    phase78_6[
      "final_step"
    ]
  )

  integration_rule = (
    toda_stable_g0_to_g7_integration_inference_rule()
  )

  premise_steps = (
    g0_step,
    g1_step,
    g2_step,
    g3_step,
    g4_step,
    g5_step,
    g6_step,
    g7_step,
  )

  result = (
    run_inference_until_stable_with_history(
      (
        integration_rule,
      ),
      premise_steps,
    )
  )

  aggregate_step = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      TodaStableG0ToG7Statement,
    )
  )

  ancestors = (
    _collect_ancestors(
      aggregate_step
    )
  )

  return {
    "phase78_10": phase78_10,
    "phase78_8a": phase78_8a,
    "phase78_8b": phase78_8b,
    "phase78_8c": phase78_8c,
    "phase78_9": phase78_9,
    "phase78_8d": phase78_8d,
    "phase78_6": phase78_6,
    "g0_step": g0_step,
    "g1_step": g1_step,
    "g2_step": g2_step,
    "g3_step": g3_step,
    "g4_step": g4_step,
    "g5_step": g5_step,
    "g6_step": g6_step,
    "g7_step": g7_step,
    "integration_rule": (
      integration_rule
    ),
    "premise_steps": (
      premise_steps
    ),
    "result": result,
    "aggregate_step": (
      aggregate_step
    ),
    "ancestors": ancestors,
  }


def test_phase78_11_all_eight_branches_are_inference():
  data = build_phase78_11_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "premise_steps"
    ]
  )


def test_phase78_11_aggregate_is_derived():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "aggregate_step"
    ].conclusion,
    TodaStableG0ToG7Statement,
  )


def test_phase78_11_aggregate_uses_exact_direct_premises():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase78_11_g0_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g0_group_relation
    is data[
      "g0_step"
    ].conclusion
  )


def test_phase78_11_g1_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g1_group_relation
    is data[
      "g1_step"
    ].conclusion
  )


def test_phase78_11_g2_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g2_group_relation
    is data[
      "g2_step"
    ].conclusion
  )


def test_phase78_11_g3_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g3_group_relation
    is data[
      "g3_step"
    ].conclusion
  )


def test_phase78_11_g4_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g4_zero
    is data[
      "g4_step"
    ].conclusion
  )


def test_phase78_11_g5_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g5_zero
    is data[
      "g5_step"
    ].conclusion
  )


def test_phase78_11_g6_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g6_group_relation
    is data[
      "g6_step"
    ].conclusion
  )


def test_phase78_11_g7_is_exact_branch_object():
  data = build_phase78_11_data()

  assert (
    data[
      "aggregate_step"
    ].conclusion
    .g7_group_relation
    is data[
      "g7_step"
    ].conclusion
  )


def test_phase78_11_aggregate_reaches_all_eight_branches():
  data = build_phase78_11_data()

  ancestors = (
    data[
      "ancestors"
    ]
  )

  for key in (
    "g0_step",
    "g1_step",
    "g2_step",
    "g3_step",
    "g4_step",
    "g5_step",
    "g6_step",
    "g7_step",
  ):
    assert any(
      ancestor
      is data[
        key
      ]
      for ancestor
      in ancestors
    )


def test_phase78_11_final_is_not_self_ancestor():
  data = build_phase78_11_data()

  assert not any(
    ancestor
    is data[
      "aggregate_step"
    ]
    for ancestor
    in data[
      "ancestors"
    ]
  )


def test_phase78_11_final_conclusion_is_absent_from_ancestors():
  data = build_phase78_11_data()

  final_conclusion = (
    data[
      "aggregate_step"
    ].conclusion
  )

  assert not any(
    ancestor.conclusion
    == final_conclusion
    for ancestor
    in data[
      "ancestors"
    ]
  )


def test_phase78_11_upstream_branches_do_not_depend_on_aggregate():
  data = build_phase78_11_data()

  aggregate_step = (
    data[
      "aggregate_step"
    ]
  )

  for branch_step in (
    data[
      "g0_step"
    ],
    data[
      "g1_step"
    ],
    data[
      "g2_step"
    ],
    data[
      "g3_step"
    ],
    data[
      "g4_step"
    ],
    data[
      "g5_step"
    ],
    data[
      "g6_step"
    ],
    data[
      "g7_step"
    ],
  ):
    branch_ancestors = (
      _collect_ancestors(
        branch_step
      )
    )

    assert not any(
      ancestor
      is aggregate_step
      for ancestor
      in branch_ancestors
    )


def test_phase78_11_proof_graph_is_acyclic():
  data = build_phase78_11_data()

  assert (
    _proof_graph_is_acyclic(
      data[
        "aggregate_step"
      ]
    )
  )


def test_phase78_11_aggregate_not_present_initially():
  data = build_phase78_11_data()

  assert not any(
    isinstance(
      step.conclusion,
      TodaStableG0ToG7Statement,
    )
    for step
    in data[
      "premise_steps"
    ]
  )


def test_phase78_11_reaches_fixed_point():
  data = build_phase78_11_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


