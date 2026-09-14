from dataclasses import replace
from functools import lru_cache

from expression import (
  IteratedSuspension,
)
from proof import (
  ProofRule,
  ProofStep,
  find_inference_match,
)
from test_phase77_lemma516_scaled_bracket_sum import (
  build_phase77_5c_data,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda36Lemma516BracketSumContainmentStatement,
  Toda36Lemma516FirstBracketTermStatement,
  Toda36Lemma516SecondBracketTermStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
  TodaLemma514Sigma8Statement,
  TodaLemma516BracketSumContainmentStatement,
  TodaLemma516ScaledCompositionBridgeStatement,
  TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
  TodaLemma516SigmaTPlus8DefinitionStatement,
  TodaLemma516TypedSetupStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


def _collect_ancestors(
  step,
):
  ancestors = []
  seen = set()
  stack = list(
    step.premises
  )

  while stack:
    current = stack.pop()

    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
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

    if current_id in visiting:
      return False

    if current_id in visited:
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
def build_phase77_6_data():
  data = (
    build_phase77_5c_data()
  )

  final_step = (
    data[
      "final_step"
    ]
  )

  ancestors = (
    _collect_ancestors(
      final_step
    )
  )

  phase77_5a = (
    data[
      "phase77_5a"
    ]
  )

  phase77_5b = (
    data[
      "phase77_5b"
    ]
  )

  phase77_4 = (
    phase77_5a[
      "phase77_4"
    ]
  )

  return {
    "data": data,
    "final_step": final_step,
    "ancestors": ancestors,
    "ancestor_conclusions": tuple(
      step.conclusion
      for step in ancestors
    ),
    "bracket_sum_step": (
      data[
        "bracket_sum_step"
      ]
    ),
    "suspension_bridge_step": (
      data[
        "suspension_bridge_step"
      ]
    ),
    "sigma_definition_step": (
      data[
        "sigma_definition_step"
      ]
    ),
    "composition_step": (
      data[
        "composition_step"
      ]
    ),
    "first_term_step": (
      phase77_5a[
        "first_term_step"
      ]
    ),
    "second_term_step": (
      phase77_5a[
        "second_term_step"
      ]
    ),
    "phase75_theorem36_bridge_step": (
      phase77_4[
        "bridge_step"
      ]
    ),
    "phase75_sigma8_step": (
      phase77_5b[
        "sigma8_step"
      ]
    ),
    "typed_setup_step": (
      phase77_5b[
        "setup_step"
      ]
    ),
  }


def test_phase77_6_final_statement_is_derived():
  data = build_phase77_6_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaLemma516BracketSumContainmentStatement,
  )

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


def test_phase77_6_typed_setup_remains_given():
  data = build_phase77_6_data()

  step = (
    data[
      "typed_setup_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma516TypedSetupStatement,
  )

  assert (
    step.rule
    == ProofRule.GIVEN
  )


def test_phase77_6_phase75_theorem36_bridge_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "phase75_theorem36_bridge_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_phase75_sigma8_statement_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "phase75_sigma8_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma514Sigma8Statement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_first_branch_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "first_term_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    Toda36Lemma516FirstBracketTermStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_second_branch_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "second_term_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    Toda36Lemma516SecondBracketTermStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_theorem36_bracket_sum_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "bracket_sum_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    Toda36Lemma516BracketSumContainmentStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_sigma8_iterated_bridge_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "suspension_bridge_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma516Sigma8IteratedSuspensionBridgeStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_sigma_t_plus_8_definition_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "sigma_definition_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma516SigmaTPlus8DefinitionStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_scaled_composition_bridge_is_derived():
  data = build_phase77_6_data()

  step = (
    data[
      "composition_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma516ScaledCompositionBridgeStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase77_6_final_direct_premises_are_exact():
  data = build_phase77_6_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "bracket_sum_step"
      ],
      data[
        "composition_step"
      ],
    )
  )


def test_phase77_6_phase75_theorem36_bridge_is_reachable():
  data = build_phase77_6_data()

  assert any(
    ancestor
    is data[
      "phase75_theorem36_bridge_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_phase75_sigma8_statement_is_reachable():
  data = build_phase77_6_data()

  assert any(
    ancestor
    is data[
      "phase75_sigma8_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_typed_setup_is_reachable():
  data = build_phase77_6_data()

  setup = (
    data[
      "typed_setup_step"
    ].conclusion
  )

  assert any(
    ancestor.conclusion
    == setup
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_first_and_second_branches_are_reachable():
  data = build_phase77_6_data()

  assert any(
    ancestor
    is data[
      "first_term_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )

  assert any(
    ancestor
    is data[
      "second_term_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_bracket_sum_branch_is_reachable():
  data = build_phase77_6_data()

  assert any(
    ancestor
    is data[
      "bracket_sum_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_sigma_bridge_branch_is_reachable():
  data = build_phase77_6_data()

  assert any(
    ancestor
    is data[
      "suspension_bridge_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )

  assert any(
    ancestor
    is data[
      "sigma_definition_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )

  assert any(
    ancestor
    is data[
      "composition_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_same_odd_parameter_reaches_final():
  data = build_phase77_6_data()

  sigma8_statement = (
    data[
      "phase75_sigma8_step"
    ].conclusion
  )

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    final_statement.odd_parameter
    is sigma8_statement.odd_parameter
  )

  assert (
    final_statement.odd_parameter_statement
    is (
      sigma8_statement
      .theorem36_bridge
      .odd_parameter_statement
    )
  )


def test_phase77_6_same_alpha_star_is_used_by_both_main_branches():
  data = build_phase77_6_data()

  theorem36_bridge = (
    data[
      "phase75_theorem36_bridge_step"
    ].conclusion
  )

  first_term = (
    data[
      "first_term_step"
    ].conclusion
  )

  second_term = (
    data[
      "second_term_step"
    ].conclusion
  )

  suspension_bridge = (
    data[
      "suspension_bridge_step"
    ].conclusion
  )

  assert (
    first_term.alpha_star
    is theorem36_bridge.alpha_star
  )

  assert (
    second_term.alpha_star
    is theorem36_bridge.alpha_star
  )

  assert (
    suspension_bridge.alpha_star
    is theorem36_bridge.alpha_star
  )


def test_phase77_6_source_typo_correction_is_fixed_to_e7_beta():
  data = build_phase77_6_data()

  first_term = (
    data[
      "first_term_step"
    ].conclusion
  )

  assert isinstance(
    first_term.bracket.second,
    IteratedSuspension,
  )

  assert (
    first_term.bracket.second.exponent
    == 7
  )

  assert (
    first_term.bracket.second.expression
    is first_term.beta
  )


def test_phase77_6_final_reuses_corrected_first_bracket():
  data = build_phase77_6_data()

  first_term = (
    data[
      "first_term_step"
    ].conclusion
  )

  final_statement = (
    data[
      "final_step"
    ].conclusion
  )

  assert (
    final_statement.first_bracket
    is first_term.bracket
  )

  assert (
    final_statement
    .first_bracket
    .second
    .exponent
    == 7
  )


def test_phase77_6_phase76_specific_rules_are_not_in_ancestry():
  data = build_phase77_6_data()

  phase76_steps = tuple(
    ancestor
    for ancestor in data[
      "ancestors"
    ]
    if (
      ancestor.inference_rule
      is not None
      and (
        ancestor
        .inference_rule
        .name
        .startswith(
          "Toda (5.16)"
        )
      )
    )
  )

  assert (
    phase76_steps
    == ()
  )


def test_phase77_6_final_is_not_its_own_ancestor():
  data = build_phase77_6_data()

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_final_conclusion_is_absent_from_ancestors():
  data = build_phase77_6_data()

  final_conclusion = (
    data[
      "final_step"
    ].conclusion
  )

  assert all(
    ancestor.conclusion
    != final_conclusion
    for ancestor in data[
      "ancestors"
    ]
  )


def test_phase77_6_full_proof_graph_is_acyclic():
  data = build_phase77_6_data()

  assert (
    _proof_graph_is_acyclic(
      data[
        "final_step"
      ]
    )
  )


def test_phase77_6_first_branch_does_not_depend_on_final():
  data = build_phase77_6_data()

  ancestors = (
    _collect_ancestors(
      data[
        "first_term_step"
      ]
    )
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in ancestors
  )


def test_phase77_6_second_branch_does_not_depend_on_final():
  data = build_phase77_6_data()

  ancestors = (
    _collect_ancestors(
      data[
        "second_term_step"
      ]
    )
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in ancestors
  )


def test_phase77_6_theorem36_sum_branch_does_not_depend_on_final():
  data = build_phase77_6_data()

  ancestors = (
    _collect_ancestors(
      data[
        "bracket_sum_step"
      ]
    )
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in ancestors
  )


def test_phase77_6_sigma_bridge_branch_does_not_depend_on_final():
  data = build_phase77_6_data()

  ancestors = (
    _collect_ancestors(
      data[
        "suspension_bridge_step"
      ]
    )
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in ancestors
  )


def test_phase77_6_composition_branch_does_not_depend_on_final():
  data = build_phase77_6_data()

  ancestors = (
    _collect_ancestors(
      data[
        "composition_step"
      ]
    )
  )

  assert all(
    ancestor
    is not data[
      "final_step"
    ]
    for ancestor in ancestors
  )


def test_phase77_6_final_rule_rejects_mismatched_beta_instance():
  data = build_phase77_6_data()

  bracket_sum = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  composition_bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  wrong_beta = replace(
    composition_bridge.beta,
    name="γ",
  )

  wrong_bridge = replace(
    composition_bridge,
    beta=wrong_beta,
  )

  wrong_step = ProofStep(
    conclusion=wrong_bridge,
    premises=(
      data[
        "composition_step"
      ].premises
    ),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "data"
    ][
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
      wrong_step,
    ),
  )

  assert match is None

  assert (
    bracket_sum.beta
    != wrong_beta
  )


def test_phase77_6_final_rule_rejects_mismatched_t_instance():
  data = build_phase77_6_data()

  bracket_sum = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  composition_bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  wrong_bridge = replace(
    composition_bridge,
    t=replace(
      composition_bridge.t,
      name="q",
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_bridge,
    premises=(
      data[
        "composition_step"
      ].premises
    ),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "data"
    ][
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
      wrong_step,
    ),
  )

  assert match is None

  assert (
    bracket_sum.t
    != wrong_bridge.t
  )


def test_phase77_6_final_rule_rejects_mismatched_m_instance():
  data = build_phase77_6_data()

  bracket_sum = (
    data[
      "bracket_sum_step"
    ].conclusion
  )

  composition_bridge = (
    data[
      "composition_step"
    ].conclusion
  )

  wrong_bridge = replace(
    composition_bridge,
    m=replace(
      composition_bridge.m,
      name="r",
    ),
  )

  wrong_step = ProofStep(
    conclusion=wrong_bridge,
    premises=(
      data[
        "composition_step"
      ].premises
    ),
    rule=ProofRule.INFERENCE,
  )

  match = find_inference_match(
    data[
      "data"
    ][
      "final_rule"
    ],
    (
      data[
        "bracket_sum_step"
      ],
      wrong_step,
    ),
  )

  assert match is None

  assert (
    bracket_sum.m
    != wrong_bridge.m
  )


