from expression import (
  Composition,
)
from homotopy_groups import (
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase56_capabilities import (
  build_phase56_representative_result,
  main,
)
from toda_rules import (
  Toda52CompositionIsomorphismStatement,
)


def test_phase56_probe_uses_only_base_given_premises():
  representative = (
    build_phase56_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 8

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase56_probe_derives_phase49_eta2_dependencies():
  representative = (
    build_phase56_representative_result()
  )

  assert len(
    representative[
      "eta_2_definition_steps"
    ]
  ) == 1

  assert len(
    representative[
      "hopf_relation_steps"
    ]
  ) == 1

  assert (
    representative[
      "eta_2_definition_steps"
    ][
      0
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    representative[
      "hopf_relation_steps"
    ][
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase56_probe_derives_all_phase56_intermediate_results():
  representative = (
    build_phase56_representative_result()
  )

  intermediate_steps = (
    representative[
      "zero_steps"
    ],
    representative[
      "isomorphism_steps"
    ],
    representative[
      "restriction_steps"
    ],
  )

  assert all(
    len(
      steps
    ) == 1
    for steps in intermediate_steps
  )

  assert all(
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
    for steps in intermediate_steps
  )


def test_phase56_probe_derives_final_toda52_statement():
  representative = (
    build_phase56_representative_result()
  )

  steps = representative[
    "composition_isomorphism_steps"
  ]

  assert len(
    steps
  ) == 1

  step = steps[
    0
  ]

  assert isinstance(
    step.conclusion,
    Toda52CompositionIsomorphismStatement,
  )

  assert step.rule == (
    ProofRule.INFERENCE
  )


def test_phase56_probe_final_statement_has_expected_map():
  representative = (
    build_phase56_representative_result()
  )

  statement = (
    representative[
      "composition_isomorphism_steps"
    ][
      0
    ].conclusion
  )

  assert (
    statement.source_group
    == TodaPrimaryGroup(
      group_dimension=(
        representative[
          "i"
        ]
      ),
      sphere_dimension=3,
    )
  )

  assert (
    statement.target_group
    == TodaPrimaryGroup(
      group_dimension=(
        representative[
          "i"
        ]
      ),
      sphere_dimension=2,
    )
  )

  assert isinstance(
    statement.composition,
    Composition,
  )

  assert (
    statement.composition.left
    == representative[
      "eta_2"
    ]
  )

  assert (
    statement.composition.right
    == representative[
      "gamma"
    ]
  )


def test_phase56_probe_final_statement_preserves_three_derived_premises():
  representative = (
    build_phase56_representative_result()
  )

  step = (
    representative[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  expected_premises = (
    representative[
      "zero_steps"
    ][
      0
    ],
    representative[
      "isomorphism_steps"
    ][
      0
    ],
    representative[
      "restriction_steps"
    ][
      0
    ],
  )

  assert (
    step.premises
    == expected_premises
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase56_probe_does_not_reintroduce_derived_results_as_given():
  representative = (
    build_phase56_representative_result()
  )

  initial_conclusions = tuple(
    step.conclusion
    for step in representative[
      "premise_steps"
    ]
  )

  derived_conclusions = (
    representative[
      "expected_zero"
    ],
    representative[
      "expected_isomorphism"
    ],
    representative[
      "expected_restriction"
    ],
    representative[
      "expected_statement"
    ],
  )

  assert all(
    conclusion
    not in initial_conclusions
    for conclusion in derived_conclusions
  )


def test_phase56_probe_reaches_fixed_point():
  representative = (
    build_phase56_representative_result()
  )

  assert (
    representative[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase56_probe_final_result_occurs_in_last_round():
  representative = (
    build_phase56_representative_result()
  )

  final_step = (
    representative[
      "composition_isomorphism_steps"
    ][
      0
    ]
  )

  assert final_step in (
    representative[
      "result"
    ]
    .round_results[
      -1
    ]
    .new_steps
  )


def test_phase56_probe_output_contains_result_provenance_and_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 56 capability demonstration"
    in output
  )

  assert (
    "π_(i-1)^1 = 0"
    in output
  )

  assert (
    "π_(i-1)^1 ⊕ π_i^3 ≅ π_i^2"
    in output
  )

  assert (
    "Φ|_(π_i^3)(γ) = η₂∘γ"
    in output
  )

  assert (
    "η₂∘- : π_i^3 ≅ π_i^2"
    in output
  )

  assert (
    "Toda (5.2) result is derived = True"
    in output
  )

  assert (
    "final premise count = 3"
    in output
  )

  assert (
    "final premises are derived = True"
    in output
  )

  assert (
    "pi_(i-1)^1=0 is GIVEN premise = False"
    in output
  )

  assert (
    "Prop.4.4 specialization is GIVEN premise = False"
    in output
  )

  assert (
    "second-summand restriction is GIVEN premise = False"
    in output
  )

  assert (
    "Toda (5.2) result is GIVEN premise = False"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )

  assert (
    "Toda Lemma 5.2 proof integration"
    in output
  )


