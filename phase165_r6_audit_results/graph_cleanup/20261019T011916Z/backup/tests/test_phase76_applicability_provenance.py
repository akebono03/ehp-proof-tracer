from functools import (
  lru_cache,
)

from proof import (
  ProofRule,
)
from test_phase76_delta_iota17 import (
  build_phase76_4_data,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


def collect_ancestor_steps(
  step,
):
  stack = list(
    step.premises
  )

  seen_ids = set()
  ancestors = []

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if current_id in seen_ids:
      continue

    seen_ids.add(
      current_id
    )

    ancestors.append(
      current
    )

    stack.extend(
      current.premises
    )

  return tuple(
    ancestors
  )


@lru_cache(maxsize=1)
def build_phase76_5_data():
  phase76_4 = (
    build_phase76_4_data()
  )

  phase76_3 = (
    phase76_4[
      "phase76_3"
    ]
  )

  phase76_2 = (
    phase76_3[
      "phase76_2"
    ]
  )

  phase75_8c = (
    phase76_2[
      "phase75_8c"
    ]
  )

  phase75_9 = (
    phase76_2[
      "phase75_9"
    ]
  )

  final_step = (
    phase76_4[
      "final_step"
    ]
  )

  pi17_17_step = (
    phase76_4[
      "pi17_17_step"
    ]
  )

  delta_image_step = (
    phase76_4[
      "delta_image_step"
    ]
  )

  exactness_step = (
    phase76_3[
      "exactness_step"
    ]
  )

  window_step = (
    phase76_3[
      "window_step"
    ]
  )

  kernel_step = (
    phase76_3[
      "kernel_step"
    ]
  )

  sigma8_step = (
    phase76_2[
      "sigma8_step"
    ]
  )

  sigma9_definition_step = (
    phase76_2[
      "sigma9_definition_step"
    ]
  )

  pi15_8_step = (
    phase76_2[
      "pi15_8_step"
    ]
  )

  pi16_9_step = (
    phase76_2[
      "pi16_9_step"
    ]
  )

  phase75_aggregate_step = (
    phase75_9[
      "aggregate_step"
    ]
  )

  ancestor_steps = (
    collect_ancestor_steps(
      final_step
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestor_steps
  }

  ancestor_conclusions = tuple(
    step.conclusion
    for step in ancestor_steps
  )

  return {
    "phase76_4": phase76_4,
    "phase76_3": phase76_3,
    "phase76_2": phase76_2,
    "phase75_8c": phase75_8c,
    "phase75_9": phase75_9,
    "final_step": final_step,
    "pi17_17_step": pi17_17_step,
    "delta_image_step": (
      delta_image_step
    ),
    "exactness_step": (
      exactness_step
    ),
    "window_step": window_step,
    "kernel_step": kernel_step,
    "sigma8_step": sigma8_step,
    "sigma9_definition_step": (
      sigma9_definition_step
    ),
    "pi15_8_step": pi15_8_step,
    "pi16_9_step": pi16_9_step,
    "phase75_aggregate_step": (
      phase75_aggregate_step
    ),
    "ancestor_steps": ancestor_steps,
    "ancestor_ids": ancestor_ids,
    "ancestor_conclusions": (
      ancestor_conclusions
    ),
  }


def test_phase76_5_final_is_inference():
  data = build_phase76_5_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )


def test_phase76_5_final_has_exact_phase76_4_direct_premises():
  data = build_phase76_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "pi17_17_step"
      ],
      data[
        "delta_image_step"
      ],
    )
  )


def test_phase76_5_foundational_pi17_17_remains_given():
  data = build_phase76_5_data()

  assert (
    data[
      "pi17_17_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase76_5_phase76_3_delta_image_is_derived():
  data = build_phase76_5_data()

  assert (
    data[
      "delta_image_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "delta_image_step"
    ].conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )


def test_phase76_5_phase76_2_kernel_is_derived():
  data = build_phase76_5_data()

  assert (
    data[
      "kernel_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "kernel_step"
    ].conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )


def test_phase76_5_exactness_is_derived_from_given_window():
  data = build_phase76_5_data()

  assert (
    data[
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert isinstance(
    data[
      "exactness_step"
    ].conclusion,
    TodaProp42ExactnessStatement,
  )

  assert (
    data[
      "exactness_step"
    ].premises
    == (
      data[
        "window_step"
      ],
    )
  )


def test_phase76_5_final_reaches_phase76_3_delta_image():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "delta_image_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_phase76_2_kernel():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "kernel_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_concrete_exactness():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "exactness_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )

  assert (
    id(
      data[
        "window_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_pi17_17_foundational_fact():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "pi17_17_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_phase75_sigma8_statement():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "sigma8_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_phase75_sigma9_definition():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "sigma9_definition_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_phase75_pi15_8_relation():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "pi15_8_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_reaches_phase75_pi16_9_relation():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "pi16_9_step"
      ]
    )
    in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_phase75_upstream_steps_remain_derived():
  data = build_phase76_5_data()

  upstream_steps = (
    data[
      "sigma8_step"
    ],
    data[
      "sigma9_definition_step"
    ],
    data[
      "pi15_8_step"
    ],
    data[
      "pi16_9_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in upstream_steps
  )


def test_phase76_5_does_not_depend_on_phase75_final_aggregate():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "phase75_aggregate_step"
      ]
    )
    not in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_provenance_graph_is_acyclic():
  data = build_phase76_5_data()

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in data[
      "ancestor_ids"
    ]
  )


def test_phase76_5_final_conclusion_does_not_appear_in_ancestors():
  data = build_phase76_5_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    final_conclusion
    not in data[
      "ancestor_conclusions"
    ]
  )


def test_phase76_5_kernel_branch_does_not_depend_on_final():
  data = build_phase76_5_data()

  ancestors = (
    collect_ancestor_steps(
      data[
        "kernel_step"
      ]
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestors
  }

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase76_5_exactness_branch_does_not_depend_on_final():
  data = build_phase76_5_data()

  ancestors = (
    collect_ancestor_steps(
      data[
        "exactness_step"
      ]
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestors
  }

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase76_5_delta_image_branch_does_not_depend_on_final():
  data = build_phase76_5_data()

  ancestors = (
    collect_ancestor_steps(
      data[
        "delta_image_step"
      ]
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestors
  }

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase76_5_pi17_17_branch_does_not_depend_on_final():
  data = build_phase76_5_data()

  ancestors = (
    collect_ancestor_steps(
      data[
        "pi17_17_step"
      ]
    )
  )

  ancestor_ids = {
    id(
      step
    )
    for step in ancestors
  }

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase76_5_kernel_precedes_delta_image_in_provenance():
  data = build_phase76_5_data()

  delta_image_ancestors = (
    collect_ancestor_steps(
      data[
        "delta_image_step"
      ]
    )
  )

  delta_image_ancestor_ids = {
    id(
      step
    )
    for step in delta_image_ancestors
  }

  assert (
    id(
      data[
        "kernel_step"
      ]
    )
    in delta_image_ancestor_ids
  )


def test_phase76_5_exactness_precedes_delta_image_in_provenance():
  data = build_phase76_5_data()

  delta_image_ancestors = (
    collect_ancestor_steps(
      data[
        "delta_image_step"
      ]
    )
  )

  delta_image_ancestor_ids = {
    id(
      step
    )
    for step in delta_image_ancestors
  }

  assert (
    id(
      data[
        "exactness_step"
      ]
    )
    in delta_image_ancestor_ids
  )


def test_phase76_5_pi17_17_is_not_used_to_derive_kernel():
  data = build_phase76_5_data()

  kernel_ancestors = (
    collect_ancestor_steps(
      data[
        "kernel_step"
      ]
    )
  )

  kernel_ancestor_ids = {
    id(
      step
    )
    for step in kernel_ancestors
  }

  assert (
    id(
      data[
        "pi17_17_step"
      ]
    )
    not in kernel_ancestor_ids
  )


def test_phase76_5_pi17_17_is_not_used_to_derive_exactness():
  data = build_phase76_5_data()

  exactness_ancestors = (
    collect_ancestor_steps(
      data[
        "exactness_step"
      ]
    )
  )

  exactness_ancestor_ids = {
    id(
      step
    )
    for step in exactness_ancestors
  }

  assert (
    id(
      data[
        "pi17_17_step"
      ]
    )
    not in exactness_ancestor_ids
  )


