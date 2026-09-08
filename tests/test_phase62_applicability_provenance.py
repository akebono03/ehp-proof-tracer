import pytest

from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase62_nu_family_eta_cube_bridge import (
  build_phase62_4_data,
)
from toda_rules import (
  TodaNuFamilyDefinitionStatement,
  toda_nu_family_definition_statement,
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


def build_phase62_5_data():
  phase62_4 = (
    build_phase62_4_data()
  )

  # Phase 62-4 が実際に provenance で使用した
  # Phase 62-3 fixture を再利用する。
  #
  # build_phase62_3_data() をここでもう一度
  # 呼ぶと、数学的 conclusion は同じでも
  # ProofStep object が別 instance になり、
  # id-based ancestor traversal と一致しない。
  phase62_3 = (
    phase62_4[
      "phase62_3"
    ]
  )

  transport_step = (
    phase62_3[
      "transport_step"
    ]
  )

  lemma54_step = (
    phase62_3[
      "lemma54_step"
    ]
  )

  definition_step = (
    phase62_3[
      "definition_step"
    ]
  )

  n_range_step = (
    phase62_3[
      "n_range_step"
    ]
  )

  triple_eta_step = (
    phase62_4[
      "triple_eta_step"
    ]
  )

  four_to_double_suspended_step = (
    phase62_4[
      "four_to_double_suspended_step"
    ]
  )

  final_step = (
    phase62_4[
      "final_step"
    ]
  )

  final_ancestors = (
    collect_ancestor_steps(
      final_step
    )
  )

  final_ancestor_ids = {
    id(
      step
    )
    for step in final_ancestors
  }

  transport_ancestors = (
    collect_ancestor_steps(
      transport_step
    )
  )

  transport_ancestor_ids = {
    id(
      step
    )
    for step in transport_ancestors
  }

  four_to_double_ancestors = (
    collect_ancestor_steps(
      four_to_double_suspended_step
    )
  )

  four_to_double_ancestor_ids = {
    id(
      step
    )
    for step in four_to_double_ancestors
  }

  return {
    "phase62_3": phase62_3,
    "phase62_4": phase62_4,
    "transport_step": transport_step,
    "lemma54_step": lemma54_step,
    "definition_step": definition_step,
    "n_range_step": n_range_step,
    "triple_eta_step": triple_eta_step,
    "four_to_double_suspended_step": (
      four_to_double_suspended_step
    ),
    "final_step": final_step,
    "final_ancestors": final_ancestors,
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "transport_ancestors": (
      transport_ancestors
    ),
    "transport_ancestor_ids": (
      transport_ancestor_ids
    ),
    "four_to_double_ancestors": (
      four_to_double_ancestors
    ),
    "four_to_double_ancestor_ids": (
      four_to_double_ancestor_ids
    ),
  }


def test_phase62_5_nu_family_definition_starts_at_four():
  definition = (
    toda_nu_family_definition_statement(
      4
    )
  )

  assert isinstance(
    definition,
    TodaNuFamilyDefinitionStatement,
  )

  assert (
    definition.index
    == 4
  )


def test_phase62_5_nu_family_definition_rejects_three():
  with pytest.raises(
    ValueError,
    match=(
      "nu family requires n >= 4"
    ),
  ):
    toda_nu_family_definition_statement(
      3
    )


def test_phase62_5_toda55_range_is_explicit_n_at_least_five():
  data = build_phase62_5_data()

  phase62_3 = data[
    "phase62_3"
  ]

  assert (
    data[
      "n_range_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "n_range_step"
    ].conclusion.left
    == phase62_3[
      "n"
    ]
  )

  assert (
    data[
      "n_range_step"
    ].conclusion.right
    == 5
  )


def test_phase62_5_n4_definition_does_not_match_toda55_transport():
  data = build_phase62_5_data()

  nu4_definition = (
    toda_nu_family_definition_statement(
      4
    )
  )

  nu4_definition_step = ProofStep(
    conclusion=nu4_definition,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "phase62_3"
    ][
      "rule"
    ],
    (
      data[
        "lemma54_step"
      ],
      nu4_definition_step,
      data[
        "n_range_step"
      ],
    ),
  ) is None


def test_phase62_5_symbolic_definition_and_range_use_same_index():
  data = build_phase62_5_data()

  assert (
    data[
      "definition_step"
    ].conclusion.index
    == data[
      "n_range_step"
    ].conclusion.left
  )


def test_phase62_5_phase62_3_result_is_derived():
  data = build_phase62_5_data()

  assert (
    data[
      "transport_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "transport_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase62_5_lemma54_dependency_remains_derived():
  data = build_phase62_5_data()

  assert (
    data[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_5_phase60_triple_eta_dependency_is_derived():
  data = build_phase62_5_data()

  assert (
    data[
      "triple_eta_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_5_phase62_4_final_result_is_derived():
  data = build_phase62_5_data()

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


def test_phase62_5_phase62_4_uses_same_symbolic_index():
  data = build_phase62_5_data()

  phase62_3 = data[
    "phase62_3"
  ]

  phase60_3 = (
    data[
      "phase62_4"
    ][
      "phase60_3"
    ]
  )

  assert (
    phase62_3[
      "n"
    ]
    == phase60_3[
      "n"
    ]
  )


def test_phase62_5_final_provenance_reaches_phase62_3():
  data = build_phase62_5_data()

  assert (
    id(
      data[
        "transport_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase62_5_final_provenance_reaches_phase60_triple_eta():
  data = build_phase62_5_data()

  assert (
    id(
      data[
        "triple_eta_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase62_5_transport_provenance_reaches_lemma54():
  data = build_phase62_5_data()

  assert (
    id(
      data[
        "lemma54_step"
      ]
    )
    in data[
      "transport_ancestor_ids"
    ]
  )


def test_phase62_5_transport_preserves_explicit_definition_and_range():
  data = build_phase62_5_data()

  assert (
    data[
      "transport_step"
    ].premises
    == (
      data[
        "lemma54_step"
      ],
      data[
        "definition_step"
      ],
      data[
        "n_range_step"
      ],
    )
  )

  assert (
    data[
      "definition_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    data[
      "n_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase62_5_four_nu_bridge_reaches_phase62_3_transport():
  data = build_phase62_5_data()

  assert (
    id(
      data[
        "transport_step"
      ]
    )
    in data[
      "four_to_double_ancestor_ids"
    ]
  )


def test_phase62_5_final_provenance_graph_is_acyclic():
  data = build_phase62_5_data()

  assert (
    id(
      data[
        "final_step"
      ]
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase62_5_final_conclusion_does_not_appear_in_ancestors():
  data = build_phase62_5_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor in data[
      "final_ancestors"
    ]
  )


