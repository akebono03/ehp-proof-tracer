from expression import (
  Composition,
  Multiple,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
  apply_inference_match,
  find_inference_match,
)
from relation_rules import (
  equality_preserved_under_multiple_inference_rule,
  equality_symmetry_inference_rule,
  equality_transitivity_inference_rule,
  nested_integer_multiple_inference_rule,
)
from test_phase60_toda54_indeterminacy import (
  build_phase60_3_data,
)
from test_phase62_nu_family_double_transport import (
  build_phase62_3_data,
)


def require_match(
  rule,
  premises,
):
  match = find_inference_match(
    rule,
    premises,
  )

  assert match is not None

  return apply_inference_match(
    match
  )


def build_phase62_4_data():
  phase62_3 = (
    build_phase62_3_data()
  )

  phase60_3 = (
    build_phase60_3_data()
  )

  double_nu_step = (
    phase62_3[
      "transport_step"
    ]
  )

  triple_eta_step = (
    phase60_3[
      "transport_step"
    ]
  )

  nu_n = (
    phase62_3[
      "definition"
    ].element
  )

  eta_cube = (
    phase60_3[
      "eta_cube"
    ]
  )

  multiple_rule = (
    equality_preserved_under_multiple_inference_rule(
      coefficient=2,
    )
  )

  doubled_step = require_match(
    multiple_rule,
    (
      double_nu_step,
    ),
  )

  nested_rule = (
    nested_integer_multiple_inference_rule(
      outer_coefficient=2,
      inner_coefficient=2,
      expression=nu_n,
    )
  )

  nested_step = require_match(
    nested_rule,
    (),
  )

  symmetry_rule = (
    equality_symmetry_inference_rule()
  )

  nested_symmetry_step = require_match(
    symmetry_rule,
    (
      nested_step,
    ),
  )

  transitivity_rule = (
    equality_transitivity_inference_rule()
  )

  four_to_double_suspended_step = (
    require_match(
      transitivity_rule,
      (
        nested_symmetry_step,
        doubled_step,
      ),
    )
  )

  final_step = require_match(
    transitivity_rule,
    (
      four_to_double_suspended_step,
      triple_eta_step,
    ),
  )

  expected_four_to_double_suspended = (
    Relation(
      lhs=Multiple(
        coefficient=4,
        expression=nu_n,
      ),
      rhs=(
        triple_eta_step
        .conclusion
        .lhs
      ),
      relation_type=RelationType.EQUALITY,
    )
  )

  expected_final = Relation(
    lhs=Multiple(
      coefficient=4,
      expression=nu_n,
    ),
    rhs=eta_cube,
    relation_type=RelationType.EQUALITY,
  )

  return {
    "phase62_3": phase62_3,
    "phase60_3": phase60_3,
    "double_nu_step": double_nu_step,
    "triple_eta_step": triple_eta_step,
    "nu_n": nu_n,
    "eta_cube": eta_cube,
    "multiple_rule": multiple_rule,
    "doubled_step": doubled_step,
    "nested_rule": nested_rule,
    "nested_step": nested_step,
    "symmetry_rule": symmetry_rule,
    "nested_symmetry_step": (
      nested_symmetry_step
    ),
    "transitivity_rule": (
      transitivity_rule
    ),
    "four_to_double_suspended_step": (
      four_to_double_suspended_step
    ),
    "final_step": final_step,
    "expected_four_to_double_suspended": (
      expected_four_to_double_suspended
    ),
    "expected_final": expected_final,
  }


def test_phase62_4_reuses_derived_phase62_3_relation():
  data = build_phase62_4_data()

  assert (
    data[
      "double_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_4_reuses_derived_phase60_transport():
  data = build_phase62_4_data()

  assert (
    data[
      "triple_eta_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_4_shared_middle_expression_matches():
  data = build_phase62_4_data()

  assert (
    data[
      "doubled_step"
    ].conclusion.rhs
    == data[
      "triple_eta_step"
    ].conclusion.lhs
  )


def test_phase62_4_doubles_phase62_3_relation():
  data = build_phase62_4_data()

  source_relation = (
    data[
      "double_nu_step"
    ].conclusion
  )

  assert (
    data[
      "doubled_step"
    ].conclusion
    == Relation(
      lhs=Multiple(
        coefficient=2,
        expression=source_relation.lhs,
      ),
      rhs=Multiple(
        coefficient=2,
        expression=source_relation.rhs,
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase62_4_nested_multiple_reduces_two_times_two_to_four():
  data = build_phase62_4_data()

  assert (
    data[
      "nested_step"
    ].conclusion
    == Relation(
      lhs=Multiple(
        coefficient=2,
        expression=Multiple(
          coefficient=2,
          expression=data[
            "nu_n"
          ],
        ),
      ),
      rhs=Multiple(
        coefficient=4,
        expression=data[
          "nu_n"
        ],
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase62_4_symmetry_places_four_nu_n_on_left():
  data = build_phase62_4_data()

  assert (
    data[
      "nested_symmetry_step"
    ].conclusion
    == Relation(
      lhs=Multiple(
        coefficient=4,
        expression=data[
          "nu_n"
        ],
      ),
      rhs=Multiple(
        coefficient=2,
        expression=Multiple(
          coefficient=2,
          expression=data[
            "nu_n"
          ],
        ),
      ),
      relation_type=RelationType.EQUALITY,
    )
  )


def test_phase62_4_derives_four_nu_to_double_suspended_nu_prime():
  data = build_phase62_4_data()

  assert (
    data[
      "four_to_double_suspended_step"
    ].conclusion
    == data[
      "expected_four_to_double_suspended"
    ]
  )

  assert (
    data[
      "four_to_double_suspended_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_4_derives_four_nu_equals_eta_cube():
  data = build_phase62_4_data()

  assert (
    data[
      "final_step"
    ].conclusion
    == data[
      "expected_final"
    ]
  )

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_4_final_left_is_four_nu_n():
  data = build_phase62_4_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == Multiple(
      coefficient=4,
      expression=data[
        "nu_n"
      ],
    )
  )


def test_phase62_4_eta_cube_is_right_associated():
  data = build_phase62_4_data()

  phase60_3 = data[
    "phase60_3"
  ]

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    == Composition(
      left=phase60_3[
        "eta_n"
      ],
      right=Composition(
        left=phase60_3[
          "eta_n_plus_one"
        ],
        right=phase60_3[
          "eta_n_plus_two"
        ],
      ),
    )
  )


def test_phase62_4_final_step_uses_two_derived_premises():
  data = build_phase62_4_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "four_to_double_suspended_step"
      ],
      data[
        "triple_eta_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in data[
      "final_step"
    ].premises
  )


def test_phase62_4_final_result_is_not_initial_input():
  data = build_phase62_4_data()

  initial_conclusions = (
    data[
      "double_nu_step"
    ].conclusion,
    data[
      "triple_eta_step"
    ].conclusion,
  )

  assert (
    data[
      "expected_final"
    ]
    not in initial_conclusions
  )


def test_phase62_4_final_result_is_not_given():
  data = build_phase62_4_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


