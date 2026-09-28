from dataclasses import replace
from functools import lru_cache

from homotopy_groups import (
  HomotopyGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase72_lemma510_modulo_integration import (
  build_phase72_4_data,
)
from test_phase72r8_corrected_lemma510_integration import (
  build_phase72r8_data,
)
from toda_rules import (
  Toda211OrdinaryEHPExactnessStatement,
  Toda54IndeterminacyGeneratorStatement,
  TodaDeltaInjectiveStatement,
  TodaLemma510BracketPlusSuspensionImageStatement,
  TodaLemma510IndexedHopfBracketContainsStatement,
  TodaLemma510Nu6OrdinaryCompositionReductionStatement,
  TodaLemma510Nu6OrdinaryCompositionZeroStatement,
  TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  TodaLemma510OrdinarySuspensionImageFiniteStatement,
  TodaLemma510OrdinarySuspensionImageInDoubleStatement,
  TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,
  TodaLemma510Split115Statement,
  TodaLemma510SuspensionImageInDoubleStatement,
  TodaProp42ExactnessStatement,
)


def collect_ancestor_steps(
  step,
):
  ancestors = []
  seen = set()
  stack = list(
    step.premises
  )

  while stack:
    ancestor = (
      stack.pop()
    )

    ancestor_id = id(
      ancestor
    )

    if (
      ancestor_id
      in seen
    ):
      continue

    seen.add(
      ancestor_id
    )

    ancestors.append(
      ancestor
    )

    stack.extend(
      ancestor.premises
    )

  return tuple(
    ancestors
  )


@lru_cache(maxsize=1)
def build_phase72r9_data():
  corrected = (
    build_phase72r8_data()
  )

  legacy = (
    build_phase72_4_data()
  )

  final_step = (
    corrected[
      "final_step"
    ]
  )

  core_step = (
    corrected[
      "core_step"
    ]
  )

  indeterminacy_step = (
    corrected[
      "phase72r7"
    ][
      "final_step"
    ]
  )

  image_step = (
    corrected[
      "phase72r6"
    ][
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
    "corrected": corrected,
    "legacy": legacy,
    "final_step": final_step,
    "core_step": core_step,
    "indeterminacy_step": (
      indeterminacy_step
    ),
    "image_step": image_step,
    "branch_steps": branch_steps,
    "final_ancestors": (
      final_ancestors
    ),
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "branch_ancestors": (
      branch_ancestors
    ),
    "branch_ancestor_ids": (
      branch_ancestor_ids
    ),
    "integration_rule": (
      corrected[
        "integration_rule"
      ]
    ),
    "core_rule": (
      corrected[
        "core_rule"
      ]
    ),
  }


def test_phase72r9_final_is_inference_not_given():
  data = build_phase72r9_data()

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


def test_phase72r9_final_has_exact_corrected_three_direct_branches():
  data = build_phase72r9_data()

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


def test_phase72r9_final_direct_branches_are_corrected_statement_types():
  data = build_phase72r9_data()

  assert isinstance(
    data[
      "core_step"
    ].conclusion,
    TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  )

  assert isinstance(
    data[
      "indeterminacy_step"
    ].conclusion,
    TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  )

  assert isinstance(
    data[
      "image_step"
    ].conclusion,
    TodaLemma510OrdinarySuspensionImageInDoubleStatement,
  )


def test_phase72r9_final_ambient_group_is_ordinary():
  data = build_phase72r9_data()

  assert (
    data[
      "final_step"
    ].conclusion
    .ambient_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase72r9_final_graph_is_acyclic():
  data = build_phase72r9_data()

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


def test_phase72r9_final_conclusion_absent_from_ancestors():
  data = build_phase72r9_data()

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


def test_phase72r9_all_three_corrected_branches_are_acyclic():
  data = build_phase72r9_data()

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


def test_phase72r9_no_corrected_branch_depends_on_final():
  data = build_phase72r9_data()

  assert all(
    id(
      data[
        "final_step"
      ]
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


def test_phase72r9_corrected_core_reaches_ordinary_ehp_exactness():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      Toda211OrdinaryEHPExactnessStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_core_reaches_indexed_prop26_consequence():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      TodaLemma510IndexedHopfBracketContainsStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_core_reaches_split_115():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      TodaLemma510Split115Statement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_image_reaches_finite_image_statement():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      TodaLemma510OrdinarySuspensionImageFiniteStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_image_reaches_two_primary_zero_statement():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      TodaLemma510OrdinarySuspensionImageTwoPrimaryZeroStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_indeterminacy_reaches_composition_reduction():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      TodaLemma510Nu6OrdinaryCompositionReductionStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_indeterminacy_reaches_ordinary_composition_zero():
  data = build_phase72r9_data()

  assert any(
    isinstance(
      ancestor.conclusion,
      TodaLemma510Nu6OrdinaryCompositionZeroStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase72r9_corrected_final_does_not_reuse_legacy_core_step():
  data = build_phase72r9_data()

  legacy_core_step = (
    data[
      "legacy"
    ][
      "core_step"
    ]
  )

  assert (
    id(
      legacy_core_step
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72r9_corrected_final_does_not_reuse_legacy_indeterminacy_step():
  data = build_phase72r9_data()

  legacy_indeterminacy_step = (
    data[
      "legacy"
    ][
      "indeterminacy_step"
    ]
  )

  assert (
    id(
      legacy_indeterminacy_step
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72r9_corrected_final_does_not_reuse_legacy_image_step():
  data = build_phase72r9_data()

  legacy_image_step = (
    data[
      "legacy"
    ][
      "image_step"
    ]
  )

  assert (
    id(
      legacy_image_step
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72r9_corrected_final_does_not_reuse_legacy_phase72_exactness_step():
  data = build_phase72r9_data()

  legacy_exactness_step = (
    data[
      "legacy"
    ][
      "phase72_3"
    ][
      "exactness_step"
    ]
  )

  assert (
    id(
      legacy_exactness_step
    )
    not in data[
      "final_ancestor_ids"
    ]
  )


def test_phase72r9_corrected_final_has_no_phase71_n6_delta_injectivity():
  data = build_phase72r9_data()

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


def test_phase72r9_legacy_graph_still_exists_for_regression_only():
  data = build_phase72r9_data()

  assert isinstance(
    data[
      "legacy"
    ][
      "core_step"
    ].conclusion,
    TodaLemma510BracketPlusSuspensionImageStatement,
  )

  assert isinstance(
    data[
      "legacy"
    ][
      "indeterminacy_step"
    ].conclusion,
    Toda54IndeterminacyGeneratorStatement,
  )

  assert isinstance(
    data[
      "legacy"
    ][
      "image_step"
    ].conclusion,
    TodaLemma510SuspensionImageInDoubleStatement,
  )


def test_phase72r9_corrected_integration_rejects_legacy_core():
  data = build_phase72r9_data()

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "legacy"
      ][
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72r9_corrected_integration_rejects_legacy_indeterminacy():
  data = build_phase72r9_data()

  assert find_inference_match(
    data[
      "integration_rule"
    ],
    (
      data[
        "core_step"
      ],
      data[
        "legacy"
      ][
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72r9_corrected_integration_rejects_legacy_image():
  data = build_phase72r9_data()

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
      data[
        "legacy"
      ][
        "image_step"
      ],
    ),
  ) is None


def test_phase72r9_corrected_integration_rejects_given_core():
  data = build_phase72r9_data()

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


def test_phase72r9_corrected_integration_rejects_given_indeterminacy():
  data = build_phase72r9_data()

  given = ProofStep(
    conclusion=(
      data[
        "indeterminacy_step"
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
      data[
        "core_step"
      ],
      given,
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72r9_corrected_integration_rejects_given_image():
  data = build_phase72r9_data()

  given = ProofStep(
    conclusion=(
      data[
        "image_step"
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
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      given,
    ),
  ) is None


def test_phase72r9_corrected_integration_rejects_wrong_indeterminacy_modulus():
  data = build_phase72r9_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "indeterminacy_step"
      ].conclusion,
      modulus=4,
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


def test_phase72r9_corrected_integration_rejects_wrong_image_modulus():
  data = build_phase72r9_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "image_step"
      ].conclusion,
      modulus=4,
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


def test_phase72r9_corrected_integration_rejects_wrong_ordinary_ambient_group():
  data = build_phase72r9_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "indeterminacy_step"
      ].conclusion,
      ambient_group=HomotopyGroup(
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
      wrong,
      data[
        "image_step"
      ],
    ),
  ) is None


def test_phase72r9_corrected_integration_rejects_wrong_image_target():
  data = build_phase72r9_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "image_step"
      ].conclusion,
      target_group=HomotopyGroup(
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


def test_phase72r9_corrected_integration_rejects_wrong_image_map():
  data = build_phase72r9_data()

  wrong = ProofStep(
    conclusion=replace(
      data[
        "image_step"
      ].conclusion,
      suspension_map=EHP_H_MAP,
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


def test_phase72r9_corrected_core_rejects_given_ordinary_exactness():
  data = build_phase72r9_data()

  exactness_step = (
    data[
      "corrected"
    ][
      "phase72r5"
    ][
      "exactness_step"
    ]
  )

  given = ProofStep(
    conclusion=(
      exactness_step
      .conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "core_rule"
    ],
    (
      data[
        "corrected"
      ][
        "ordinary_hopf_step"
      ],
      data[
        "corrected"
      ][
        "hopf_delta_step"
      ],
      given,
    ),
  ) is None


