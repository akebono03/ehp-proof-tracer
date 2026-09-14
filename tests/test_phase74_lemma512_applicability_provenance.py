from dataclasses import replace
from functools import lru_cache

from expression import (
  Composition,
  Zero,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from test_phase74_lemma512_bracket_singleton_mod2 import (
  build_phase74_5_data,
)
from test_phase74_lemma512_coefficient_stability import (
  build_phase74_6_data,
)
from test_phase74_lemma512_final_integration import (
  build_phase74_8_data,
)
from test_phase74_lemma512_nonzero_anchor import (
  build_phase74_7_data,
)
from toda_rules import (
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaLemma55BracketContainsUpToSignStatement,
  TodaLemma512BracketSingletonMod2Statement,
  TodaLemma512CoefficientStabilityStatement,
  TodaLemma512NonzeroAnchorStatement,
  TodaLemma512Statement,
  TodaProp511FiniteDimensionalStatement,
  toda_eta_family_definition_statement,
  toda_nu_family_definition_statement,
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


def _ancestor_ids(
  step,
):
  return {
    id(
      ancestor
    )
    for ancestor
    in _collect_ancestors(
      step
    )
  }


def _graph_is_acyclic(
  step,
):
  visited = set()
  active = set()

  def visit(
    current,
  ):
    current_id = id(
      current
    )

    if (
      current_id
      in active
    ):
      return False

    if (
      current_id
      in visited
    ):
      return True

    active.add(
      current_id
    )

    for premise in current.premises:
      if not visit(
        premise
      ):
        return False

    active.remove(
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
def build_phase74_9_data():
  phase74_5 = (
    build_phase74_5_data()
  )

  phase74_6 = (
    build_phase74_6_data()
  )

  phase74_7 = (
    build_phase74_7_data()
  )

  phase74_8 = (
    build_phase74_8_data()
  )

  singleton_step = (
    phase74_5[
      "final_step"
    ]
  )

  stability_step = (
    phase74_6[
      "final_step"
    ]
  )

  anchor_step = (
    phase74_7[
      "final_step"
    ]
  )

  final_step = (
    phase74_8[
      "final_step"
    ]
  )

  final_ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  singleton_ancestors = (
    _collect_ancestors(
      singleton_step
    )
  )

  stability_ancestors = (
    _collect_ancestors(
      stability_step
    )
  )

  anchor_ancestors = (
    _collect_ancestors(
      anchor_step
    )
  )

  prop511_step = next(
    step
    for step
    in final_ancestors
    if isinstance(
      step.conclusion,
      TodaProp511FiniteDimensionalStatement,
    )
  )

  nu_family_step = next(
    step
    for step
    in final_ancestors
    if isinstance(
      step.conclusion,
      Toda55NuFamilyFiniteDimensionalStatement,
    )
  )

  lemma55_inclusion_step = next(
    step
    for step
    in final_ancestors
    if isinstance(
      step.conclusion,
      TodaLemma55BracketContainsUpToSignStatement,
    )
    and step.conclusion.bracket.index == 3
  )

  nu_6 = (
    toda_nu_family_definition_statement(
      6
    ).element
  )

  eta_9 = (
    toda_eta_family_definition_statement(
      9
    ).element
  )

  nu6_eta9_zero = Relation(
    lhs=Composition(
      left=nu_6,
      right=eta_9,
    ),
    rhs=Zero(),
    relation_type=RelationType.ZERO,
  )

  nu6_eta9_zero_step = next(
    step
    for step
    in final_ancestors
    if (
      step.conclusion
      == nu6_eta9_zero
    )
  )

  return {
    "phase74_5": phase74_5,
    "phase74_6": phase74_6,
    "phase74_7": phase74_7,
    "phase74_8": phase74_8,
    "singleton_step": (
      singleton_step
    ),
    "stability_step": (
      stability_step
    ),
    "anchor_step": (
      anchor_step
    ),
    "final_step": (
      final_step
    ),
    "final_rule": (
      phase74_8[
        "rule"
      ]
    ),
    "final_ancestors": (
      final_ancestors
    ),
    "final_ancestor_ids": (
      _ancestor_ids(
        final_step
      )
    ),
    "singleton_ancestors": (
      singleton_ancestors
    ),
    "singleton_ancestor_ids": (
      _ancestor_ids(
        singleton_step
      )
    ),
    "stability_ancestors": (
      stability_ancestors
    ),
    "stability_ancestor_ids": (
      _ancestor_ids(
        stability_step
      )
    ),
    "anchor_ancestors": (
      anchor_ancestors
    ),
    "anchor_ancestor_ids": (
      _ancestor_ids(
        anchor_step
      )
    ),
    "prop511_step": (
      prop511_step
    ),
    "nu_family_step": (
      nu_family_step
    ),
    "lemma55_inclusion_step": (
      lemma55_inclusion_step
    ),
    "nu6_eta9_zero": (
      nu6_eta9_zero
    ),
    "nu6_eta9_zero_step": (
      nu6_eta9_zero_step
    ),
  }


def test_phase74_9_final_is_inference():
  data = build_phase74_9_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_9_final_is_lemma512_statement():
  data = build_phase74_9_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma512Statement,
  )


def test_phase74_9_final_has_exact_three_direct_premises():
  data = build_phase74_9_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    )
  )


def test_phase74_9_all_direct_final_dependencies_are_inference():
  data = build_phase74_9_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in data[
      "final_step"
    ].premises
  )


def test_phase74_9_final_rule_matches_exact_dependencies():
  data = build_phase74_9_data()

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    ),
  ) is not None


def test_phase74_9_final_range_is_n_at_least_6():
  data = build_phase74_9_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  n = (
    statement
    .bracket
    .first
    .dimension
  )

  assert (
    statement.n_range
    == ScalarGreaterEqualStatement(
      left=n,
      right=6,
    )
  )


def test_phase74_9_singleton_range_is_n_at_least_6():
  data = build_phase74_9_data()

  singleton = (
    data[
      "singleton_step"
    ].conclusion
  )

  n = (
    singleton
    .bracket
    .first
    .dimension
  )

  assert (
    singleton.n_range
    == ScalarGreaterEqualStatement(
      left=n,
      right=6,
    )
  )


def test_phase74_9_stability_range_is_n_at_least_6():
  data = build_phase74_9_data()

  stability = (
    data[
      "stability_step"
    ].conclusion
  )

  n = (
    stability
    .source_bracket
    .first
    .dimension
  )

  assert (
    stability.n_range
    == ScalarGreaterEqualStatement(
      left=n,
      right=6,
    )
  )


def test_phase74_9_rejects_singleton_with_range_n_at_least_5():
  data = build_phase74_9_data()

  singleton = (
    data[
      "singleton_step"
    ].conclusion
  )

  n = (
    singleton
    .bracket
    .first
    .dimension
  )

  wrong_singleton = replace(
    singleton,
    n_range=(
      ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_singleton,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      wrong_step,
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_9_rejects_stability_with_range_n_at_least_5():
  data = build_phase74_9_data()

  stability = (
    data[
      "stability_step"
    ].conclusion
  )

  n = (
    stability
    .source_bracket
    .first
    .dimension
  )

  wrong_stability = replace(
    stability,
    n_range=(
      ScalarGreaterEqualStatement(
        left=n,
        right=5,
      )
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_stability,
    premises=(),
    rule=ProofRule.INFERENCE,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "singleton_step"
      ],
      wrong_step,
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_9_final_reaches_singleton_branch():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "singleton_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase74_9_final_reaches_stability_branch():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "stability_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase74_9_final_reaches_anchor_branch():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "anchor_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase74_9_final_reaches_prop511():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "prop511_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_9_final_reaches_nu_family():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "nu_family_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )

  assert (
    data[
      "nu_family_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_9_final_reaches_nu6_eta9_zero():
  data = build_phase74_9_data()

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

  assert (
    data[
      "nu6_eta9_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_9_nu6_eta9_zero_is_exact_expected_relation():
  data = build_phase74_9_data()

  assert (
    data[
      "nu6_eta9_zero_step"
    ].conclusion
    == data[
      "nu6_eta9_zero"
    ]
  )


def test_phase74_9_final_reaches_lemma55_inclusion():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "lemma55_inclusion_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )

  assert (
    data[
      "lemma55_inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_9_lemma55_anchor_is_index_three():
  data = build_phase74_9_data()

  assert (
    data[
      "lemma55_inclusion_step"
    ].conclusion
    .bracket
    .index
    == 3
  )


def test_phase74_9_anchor_dimension_remains_eight():
  data = build_phase74_9_data()

  assert (
    data[
      "anchor_step"
    ].conclusion
    .anchor_dimension
    == 8
  )


def test_phase74_9_anchor_is_not_symbolic_all_n_statement():
  data = build_phase74_9_data()

  assert isinstance(
    data[
      "anchor_step"
    ].conclusion,
    TodaLemma512NonzeroAnchorStatement,
  )

  assert (
    data[
      "anchor_step"
    ].conclusion
    .anchor_dimension
    == 8
  )


def test_phase74_9_stability_does_not_depend_on_anchor():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "anchor_step"
      ]
    )
    not in data[
      "stability_ancestor_ids"
    ]
  )

  assert all(
    not isinstance(
      ancestor.conclusion,
      TodaLemma512NonzeroAnchorStatement,
    )
    for ancestor
    in data[
      "stability_ancestors"
    ]
  )


def test_phase74_9_anchor_does_not_depend_on_stability():
  data = build_phase74_9_data()

  assert (
    id(
      data[
        "stability_step"
      ]
    )
    not in data[
      "anchor_ancestor_ids"
    ]
  )

  assert all(
    not isinstance(
      ancestor.conclusion,
      TodaLemma512CoefficientStabilityStatement,
    )
    for ancestor
    in data[
      "anchor_ancestors"
    ]
  )


def test_phase74_9_singleton_does_not_depend_on_later_phase74_branches():
  data = build_phase74_9_data()

  assert all(
    not isinstance(
      ancestor.conclusion,
      (
        TodaLemma512CoefficientStabilityStatement,
        TodaLemma512NonzeroAnchorStatement,
        TodaLemma512Statement,
      ),
    )
    for ancestor
    in data[
      "singleton_ancestors"
    ]
  )


def test_phase74_9_final_graph_is_acyclic():
  data = build_phase74_9_data()

  assert _graph_is_acyclic(
    data[
      "final_step"
    ]
  )


def test_phase74_9_singleton_graph_is_acyclic():
  data = build_phase74_9_data()

  assert _graph_is_acyclic(
    data[
      "singleton_step"
    ]
  )


def test_phase74_9_stability_graph_is_acyclic():
  data = build_phase74_9_data()

  assert _graph_is_acyclic(
    data[
      "stability_step"
    ]
  )


def test_phase74_9_anchor_graph_is_acyclic():
  data = build_phase74_9_data()

  assert _graph_is_acyclic(
    data[
      "anchor_step"
    ]
  )


def test_phase74_9_final_is_not_own_ancestor():
  data = build_phase74_9_data()

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


def test_phase74_9_final_conclusion_not_in_ancestors():
  data = build_phase74_9_data()

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


def test_phase74_9_no_branch_depends_on_final():
  data = build_phase74_9_data()

  final_id = id(
    data[
      "final_step"
    ]
  )

  assert (
    final_id
    not in data[
      "singleton_ancestor_ids"
    ]
  )

  assert (
    final_id
    not in data[
      "stability_ancestor_ids"
    ]
  )

  assert (
    final_id
    not in data[
      "anchor_ancestor_ids"
    ]
  )


def test_phase74_9_given_singleton_shortcut_is_rejected():
  data = build_phase74_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "singleton_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      given,
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_9_given_stability_shortcut_is_rejected():
  data = build_phase74_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "stability_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "singleton_step"
      ],
      given,
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_9_given_anchor_shortcut_is_rejected():
  data = build_phase74_9_data()

  given = ProofStep(
    conclusion=(
      data[
        "anchor_step"
      ].conclusion
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      given,
    ),
  ) is None


def test_phase74_9_missing_singleton_does_not_match():
  data = build_phase74_9_data()

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_9_missing_stability_does_not_match():
  data = build_phase74_9_data()

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "anchor_step"
      ],
    ),
  ) is None


def test_phase74_9_missing_anchor_does_not_match():
  data = build_phase74_9_data()

  assert find_inference_match(
    data[
      "final_rule"
    ],
    (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
    ),
  ) is None


def test_phase74_9_final_generator_remains_composition():
  data = build_phase74_9_data()

  assert type(
    data[
      "final_step"
    ].conclusion
    .generator
  ) is Composition


def test_phase74_9_no_explicit_coefficient_field():
  data = build_phase74_9_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert not hasattr(
    statement,
    "coefficient",
  )

  assert not hasattr(
    statement,
    "x",
  )


def test_phase74_9_no_stable_branch_field():
  data = build_phase74_9_data()

  statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert not hasattr(
    statement,
    "stable_group",
  )

  assert not hasattr(
    statement,
    "stable_generator",
  )


