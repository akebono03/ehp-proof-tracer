from dataclasses import replace
from functools import lru_cache

from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase72_lemma510_modulo_integration import (
  build_phase72_4_data,
)
from toda_rules import (
  Toda54IndeterminacyGeneratorStatement,
  TodaDeltaInjectiveStatement,
  TodaLemma510BracketModuloStatement,
  TodaLemma510BracketPlusSuspensionImageStatement,
  TodaLemma510SuspensionImageInDoubleStatement,
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
def build_phase72_5_data():
  phase72_4 = (
    build_phase72_4_data()
  )

  final_step = (
    phase72_4[
      "final_step"
    ]
  )

  core_step = (
    phase72_4[
      "core_step"
    ]
  )

  indeterminacy_step = (
    phase72_4[
      "indeterminacy_step"
    ]
  )

  image_step = (
    phase72_4[
      "image_step"
    ]
  )

  final_ancestors = (
    collect_ancestor_steps(
      final_step
    )
  )

  final_ancestor_ids = {
    id(
      ancestor
    )
    for ancestor
    in final_ancestors
  }

  branch_steps = (
    core_step,
    indeterminacy_step,
    image_step,
  )

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
    "phase72_4": phase72_4,
    "final_step": final_step,
    "core_step": core_step,
    "indeterminacy_step": (
      indeterminacy_step
    ),
    "image_step": image_step,
    "integration_rule": (
      phase72_4[
        "integration_rule"
      ]
    ),
    "nu6_eta9_zero_step": (
      phase72_4[
        "nu6_eta9_zero_step"
      ]
    ),
    "pi10_5_step": (
      phase72_4[
        "pi10_5_step"
      ]
    ),
    "pi11_6_step": (
      phase72_4[
        "pi11_6_step"
      ]
    ),
    "prop53_step": (
      phase72_4[
        "prop53_step"
      ]
    ),
    "delta_iota11_step": (
      phase72_4[
        "phase72_3"
      ][
        "delta_iota11_step"
      ]
    ),
    "hopf_delta_step": (
      phase72_4[
        "phase72_3"
      ][
        "hopf_delta_step"
      ]
    ),
    "exactness_step": (
      phase72_4[
        "phase72_3"
      ][
        "exactness_step"
      ]
    ),
    "hopf_bracket_step": (
      phase72_4[
        "phase72_3"
      ][
        "hopf_bracket_step"
      ]
    ),
    "final_ancestors": (
      final_ancestors
    ),
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "branch_steps": branch_steps,
    "branch_ancestors": (
      branch_ancestors
    ),
    "branch_ancestor_ids": (
      branch_ancestor_ids
    ),
  }


def test_phase72_5_final_is_modulo_statement():
  data = build_phase72_5_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma510BracketModuloStatement,
  )


def test_phase72_5_final_is_inference():
  data = build_phase72_5_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_5_final_is_not_given():
  data = build_phase72_5_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72_5_final_direct_dependencies_are_exact():
  data = build_phase72_5_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    )
  )


def test_phase72_5_core_is_inference():
  data = build_phase72_5_data()

  assert isinstance(
    data[
      "core_step"
    ].conclusion,
    TodaLemma510BracketPlusSuspensionImageStatement,
  )

  assert (
    data[
      "core_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_5_indeterminacy_is_inference():
  data = build_phase72_5_data()

  assert isinstance(
    data[
      "indeterminacy_step"
    ].conclusion,
    Toda54IndeterminacyGeneratorStatement,
  )

  assert (
    data[
      "indeterminacy_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_5_image_containment_is_inference():
  data = build_phase72_5_data()

  assert isinstance(
    data[
      "image_step"
    ].conclusion,
    TodaLemma510SuspensionImageInDoubleStatement,
  )

  assert (
    data[
      "image_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase72_5_final_reaches_three_direct_branches():
  data = build_phase72_5_data()

  ancestor_ids = (
    data[
      "final_ancestor_ids"
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


def test_phase72_5_final_reaches_phase69_delta_iota11():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "delta_iota11_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_hopf_delta_iota13():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "hopf_delta_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_e_h_exactness():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "exactness_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_hopf_bracket_consequence():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "hopf_bracket_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_nu6_eta9_zero():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "nu6_eta9_zero_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_prop53():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "prop53_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_pi10_5():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "pi10_5_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_reaches_pi11_6():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "pi11_6_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72_5_final_graph_is_acyclic():
  data = build_phase72_5_data()

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


def test_phase72_5_final_conclusion_not_in_ancestors():
  data = build_phase72_5_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72_5_all_three_branch_graphs_are_acyclic():
  data = build_phase72_5_data()

  assert all(
    id(
      step
    )
    not in data[
      "branch_ancestor_ids"
    ][
      id(
        step
      )
    ]
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase72_5_core_does_not_depend_on_final():
  data = build_phase72_5_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "core_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase72_5_indeterminacy_does_not_depend_on_final():
  data = build_phase72_5_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "indeterminacy_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase72_5_image_does_not_depend_on_final():
  data = build_phase72_5_data()

  ancestors = (
    data[
      "branch_ancestors"
    ][
      id(
        data[
          "image_step"
        ]
      )
    ]
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor
    in ancestors
  )


def test_phase72_5_indeterminacy_does_not_depend_on_core():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "core_step"
      ]
    )
    not in data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "indeterminacy_step"
        ]
      )
    ]
  )


def test_phase72_5_image_does_not_depend_on_core():
  data = build_phase72_5_data()

  assert (
    id(
      data[
        "core_step"
      ]
    )
    not in data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "image_step"
        ]
      )
    ]
  )


def test_phase72_5_core_does_not_depend_on_phase72_4_branches():
  data = build_phase72_5_data()

  ancestor_ids = (
    data[
      "branch_ancestor_ids"
    ][
      id(
        data[
          "core_step"
        ]
      )
    ]
  )

  assert (
    id(
      data[
        "indeterminacy_step"
      ]
    )
    not in ancestor_ids
  )

  assert (
    id(
      data[
        "image_step"
      ]
    )
    not in ancestor_ids
  )


def test_phase72_5_does_not_depend_on_phase71_n6_injectivity():
  data = build_phase72_5_data()

  phase71_n6_statement = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=TodaPrimaryGroup(
          group_dimension=13,
          sphere_dimension=13,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=6,
        ),
      )
    )
  )

  assert all(
    ancestor.conclusion
    != phase71_n6_statement
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72_5_rejects_given_core():
  data = build_phase72_5_data()

  given = ProofStep(
    conclusion=(
      data[
        "core_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      given,
      data[
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72_5_rejects_wrong_indeterminacy_generator():
  data = build_phase72_5_data()

  original_generator = (
    data[
      "indeterminacy_step"
    ].conclusion
    .generator
  )

  assert isinstance(
    original_generator,
    Multiple,
  )

  wrong = ProofStep(
    conclusion=replace(
      data[
        "indeterminacy_step"
      ].conclusion,
      generator=Multiple(
        coefficient=4,
        expression=(
          original_generator
          .expression
        ),
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      wrong,
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72_5_rejects_wrong_indeterminacy_bracket():
  data = build_phase72_5_data()

  wrong_eta = HomotopyElement(
    name="η₈",
    dimension=8,
    generator=GeneratorSymbol(
      family="η",
      index=8,
    ),
  )

  wrong_bracket = replace(
    data[
      "indeterminacy_step"
    ].conclusion
    .bracket,
    second=wrong_eta,
  )

  wrong = ProofStep(
    conclusion=replace(
      data[
        "indeterminacy_step"
      ].conclusion,
      bracket=wrong_bracket,
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      wrong,
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72_5_rejects_wrong_image_ambient_group():
  data = build_phase72_5_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "image_step"
      ].conclusion,
      ambient_group=TodaPrimaryGroup(
        group_dimension=11,
        sphere_dimension=7,
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      wrong,
    ),
  ) is None


def test_phase72_5_rejects_wrong_suspension_map():
  data = build_phase72_5_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "image_step"
      ].conclusion,
      suspension_map=TodaSuspensionMap(
        source_group=TodaPrimaryGroup(
          group_dimension=10,
          sphere_dimension=5,
        ),
        target_group=TodaPrimaryGroup(
          group_dimension=11,
          sphere_dimension=7,
        ),
      ),
    ),
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      wrong,
    ),
  ) is None



