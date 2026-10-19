from homotopy_groups import (
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase49_capabilities import (
  build_phase49_representative_result,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaPi32Eta2DefinitionStatement,
  TodaSuspensionInjectiveStatement,
)


def test_phase49_probe_has_six_initial_given_premises():
  representative = (
    build_phase49_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 6

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase49_probe_derives_h_injectivity():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "hopf_injective_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaHopfInvariantInjectiveStatement,
  )


def test_phase49_probe_h_injectivity_has_expected_instance():
  representative = (
    build_phase49_representative_result()
  )

  statement = (
    representative[
      "hopf_injective_steps"
    ][
      0
    ].conclusion
  )

  assert statement.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )
  )

  assert statement.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )
  )


def test_phase49_probe_derives_e_injectivity():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "suspension_injective_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaSuspensionInjectiveStatement,
  )


def test_phase49_probe_derives_delta_zero():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "delta_zero_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaDeltaZeroStatement,
  )


def test_phase49_probe_delta_zero_has_expected_instance():
  representative = (
    build_phase49_representative_result()
  )

  statement = (
    representative[
      "delta_zero_steps"
    ][
      0
    ].conclusion
  )

  assert statement.map.source_group == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=3,
    )
  )

  assert statement.map.target_group == (
    TodaPrimaryGroup(
      group_dimension=1,
      sphere_dimension=1,
    )
  )


def test_phase49_probe_derives_h_surjectivity():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "hopf_surjective_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )


def test_phase49_probe_derives_h_isomorphism():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "hopf_isomorphism_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaHopfInvariantIsomorphismStatement,
  )


def test_phase49_probe_h_isomorphism_has_expected_instance():
  representative = (
    build_phase49_representative_result()
  )

  statement = (
    representative[
      "hopf_isomorphism_steps"
    ][
      0
    ].conclusion
  )

  assert statement.map.source_group == (
    representative[
      "pi_3_2"
    ]
  )

  assert statement.map.target_group == (
    representative[
      "pi_3_3"
    ]
  )


def test_phase49_probe_derives_eta_2_definition():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "eta_2_definition_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaPi32Eta2DefinitionStatement,
  )


def test_phase49_probe_eta_2_is_not_given():
  representative = (
    build_phase49_representative_result()
  )

  definition = (
    representative[
      "eta_2_definition_steps"
    ][
      0
    ]
  )

  assert definition.rule == (
    ProofRule.INFERENCE
  )

  assert definition.conclusion.element.name == (
    "η₂"
  )

  assert definition.conclusion.image.name == (
    "ι_3"
  )


def test_phase49_probe_derives_h_eta_2_equals_iota_3():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "hopf_relation_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = steps[
    0
  ].conclusion

  assert relation.lhs.expression.name == (
    "η₂"
  )

  assert relation.rhs.name == (
    "ι_3"
  )


def test_phase49_probe_derives_final_pi_3_2_group():
  representative = (
    build_phase49_representative_result()
  )

  steps = representative[
    "final_group_steps"
  ]

  assert len(
    steps
  ) == 1

  relation = steps[
    0
  ].conclusion

  assert relation.lhs == (
    TodaPrimaryGroup(
      group_dimension=3,
      sphere_dimension=2,
    )
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )

  assert relation.rhs.generator.name == (
    "η₂"
  )


def test_phase49_probe_all_eight_expected_steps_are_derived():
  representative = (
    build_phase49_representative_result()
  )

  derived = tuple(
    step
    for step in representative[
      "result"
    ].steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert len(
    derived
  ) == 8


def test_phase49_probe_all_derived_steps_preserve_inference_rule():
  representative = (
    build_phase49_representative_result()
  )

  derived = tuple(
    step
    for step in representative[
      "result"
    ].steps
    if step.rule
    == ProofRule.INFERENCE
  )

  assert all(
    step.inference_rule
    is not None
    for step in derived
  )


def test_phase49_probe_reaches_fixed_point():
  representative = (
    build_phase49_representative_result()
  )

  assert (
    representative[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )


def test_phase49_probe_reaches_fixed_point_in_six_rounds():
  representative = (
    build_phase49_representative_result()
  )

  assert representative[
    "result"
  ].round_count == 6


def test_phase49_probe_round_one_derives_two_steps():
  representative = (
    build_phase49_representative_result()
  )

  assert len(
    representative[
      "result"
    ].round_results[
      0
    ].new_steps
  ) == 2


def test_phase49_probe_round_two_derives_delta_zero():
  representative = (
    build_phase49_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      1
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaDeltaZeroStatement,
  )


def test_phase49_probe_round_three_derives_h_surjectivity():
  representative = (
    build_phase49_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      2
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaHopfInvariantSurjectiveStatement,
  )


def test_phase49_probe_round_four_derives_h_isomorphism():
  representative = (
    build_phase49_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      3
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaHopfInvariantIsomorphismStatement,
  )


def test_phase49_probe_round_five_derives_eta_2_definition():
  representative = (
    build_phase49_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      4
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaPi32Eta2DefinitionStatement,
  )


def test_phase49_probe_round_six_derives_two_final_consequences():
  representative = (
    build_phase49_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      5
    ].new_steps
  )

  assert len(
    new_steps
  ) == 2

  assert any(
    step
    in representative[
      "hopf_relation_steps"
    ]
    for step in new_steps
  )

  assert any(
    step
    in representative[
      "final_group_steps"
    ]
    for step in new_steps
  )


