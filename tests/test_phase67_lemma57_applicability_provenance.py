from functools import lru_cache

from proof import (
  ProofRule,
)
from test_phase67_lemma57_delta_generator import (
  build_phase67_7_data,
)
from toda_rules import (
  Toda58EquationStatement,
  TodaDeltaImageUpToSignStatement,
  TodaDeltaSurjectiveStatement,
  TodaLemma57TwoIota5ImageMembershipStatement,
  TodaProp42ExactnessStatement,
  TodaProp56FiniteDimensionalStatement,
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
def build_phase67_8_data():
  phase67_7 = (
    build_phase67_7_data()
  )

  final_step = (
    phase67_7[
      "final_step"
    ]
  )

  final_ancestors = (
    collect_ancestors(
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

  phase67_5 = (
    phase67_7[
      "phase67_5"
    ]
  )

  phase67_6 = (
    phase67_7[
      "phase67_6"
    ]
  )

  hypothesis_step = (
    phase67_5[
      "hypothesis_step"
    ]
  )

  eta2_nu_prime_zero_step = (
    phase67_7[
      "eta2_nu_prime_zero_step"
    ]
  )

  pi6_2_step = (
    phase67_7[
      "pi6_2_step"
    ]
  )

  exactness_step = (
    phase67_7[
      "exactness_step"
    ]
  )

  delta_surjective_step = (
    phase67_7[
      "delta_surjective_step"
    ]
  )

  prop56_step = (
    phase67_7[
      "prop56_step"
    ]
  )

  branch_steps = (
    hypothesis_step,
    eta2_nu_prime_zero_step,
    pi6_2_step,
    exactness_step,
    delta_surjective_step,
    prop56_step,
  )

  branch_ancestors = {
    id(step): collect_ancestors(
      step
    )
    for step
    in branch_steps
  }

  return {
    "phase67_7": phase67_7,
    "phase67_5": phase67_5,
    "phase67_6": phase67_6,
    "final_step": final_step,
    "final_ancestors": final_ancestors,
    "final_ancestor_ids": (
      final_ancestor_ids
    ),
    "hypothesis_step": hypothesis_step,
    "eta2_nu_prime_zero_step": (
      eta2_nu_prime_zero_step
    ),
    "pi6_2_step": pi6_2_step,
    "exactness_step": exactness_step,
    "delta_surjective_step": (
      delta_surjective_step
    ),
    "prop56_step": prop56_step,
    "branch_steps": branch_steps,
    "branch_ancestors": (
      branch_ancestors
    ),
  }


def test_phase67_8_final_delta_statement_is_inference():
  data = build_phase67_8_data()

  assert isinstance(
    data[
      "final_step"
    ].conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_8_nu_prime_hypothesis_is_derived():
  data = build_phase67_8_data()

  assert isinstance(
    data[
      "hypothesis_step"
    ].conclusion,
    TodaLemma57TwoIota5ImageMembershipStatement,
  )

  assert (
    data[
      "hypothesis_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_8_eta2_nu_prime_zero_is_derived():
  data = build_phase67_8_data()

  assert (
    data[
      "eta2_nu_prime_zero_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_8_pi6_2_relation_is_derived():
  data = build_phase67_8_data()

  assert (
    data[
      "pi6_2_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_8_exactness_is_derived_from_structural_window():
  data = build_phase67_8_data()

  assert isinstance(
    data[
      "exactness_step"
    ].conclusion,
    TodaProp42ExactnessStatement,
  )

  assert (
    data[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    data[
      "phase67_7"
    ][
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase67_8_delta_surjectivity_is_derived():
  data = build_phase67_8_data()

  assert isinstance(
    data[
      "delta_surjective_step"
    ].conclusion,
    TodaDeltaSurjectiveStatement,
  )

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_8_prop56_dependency_is_derived():
  data = build_phase67_8_data()

  assert isinstance(
    data[
      "prop56_step"
    ].conclusion,
    TodaProp56FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop56_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase67_8_final_reaches_nu_prime_hypothesis_branch():
  data = build_phase67_8_data()

  assert (
    id(
      data[
        "hypothesis_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase67_8_final_reaches_eta2_nu_prime_zero_branch():
  data = build_phase67_8_data()

  assert (
    id(
      data[
        "eta2_nu_prime_zero_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase67_8_final_reaches_pi6_2_branch():
  data = build_phase67_8_data()

  assert (
    id(
      data[
        "pi6_2_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase67_8_final_reaches_exactness_branch():
  data = build_phase67_8_data()

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


def test_phase67_8_final_reaches_delta_surjectivity():
  data = build_phase67_8_data()

  assert (
    id(
      data[
        "delta_surjective_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase67_8_final_reaches_prop56():
  data = build_phase67_8_data()

  assert (
    id(
      data[
        "prop56_step"
      ]
    )
    in data[
      "final_ancestor_ids"
    ]
  )


def test_phase67_8_final_graph_is_acyclic():
  data = build_phase67_8_data()

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


def test_phase67_8_final_conclusion_not_in_ancestors():
  data = build_phase67_8_data()

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


def test_phase67_8_intermediate_branches_do_not_depend_on_final():
  data = build_phase67_8_data()

  final_step = (
    data[
      "final_step"
    ]
  )

  assert all(
    all(
      ancestor
      is not final_step
      for ancestor
      in data[
        "branch_ancestors"
      ][
        id(
          step
        )
      ]
    )
    for step
    in data[
      "branch_steps"
    ]
  )


def test_phase67_8_phase66_equation_is_not_an_ancestor():
  data = build_phase67_8_data()

  assert all(
    not isinstance(
      ancestor.conclusion,
      Toda58EquationStatement,
    )
    for ancestor
    in data[
      "final_ancestors"
    ]
  )


def test_phase67_8_final_direct_premises_are_all_derived():
  data = build_phase67_8_data()

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise
    in data[
      "final_step"
    ].premises
  )


def test_phase67_8_only_structural_exactness_window_is_given_in_phase67_7_boundary():
  data = build_phase67_8_data()

  phase67_7 = (
    data[
      "phase67_7"
    ]
  )

  assert (
    phase67_7[
      "window_step"
    ].rule
    == ProofRule.GIVEN
  )

  assert (
    phase67_7[
      "exactness_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    phase67_7[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    phase67_7[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


