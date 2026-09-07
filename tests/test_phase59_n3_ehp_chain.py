from expression import (
  GeneratorSymbol,
  HomotopyElement,
  MapApplication,
)
from homotopy_groups import (
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from probes.probe_phase55_capabilities import (
  build_phase55_representative_result,
)
from probes.probe_phase58_capabilities import (
  build_phase58_representative_result,
)
from toda_rules import (
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
  toda_53_n3_delta_injective_hopf_zero_inference_rule,
  toda_53_n3_delta_zero_suspension_injective_inference_rule,
  toda_53_n3_hopf_eta5_surjective_inference_rule,
  toda_53_n3_hopf_surjective_delta_zero_inference_rule,
  toda_53_n3_hopf_zero_suspension_surjective_inference_rule,
  toda_53_n3_prop51_delta_injective_inference_rule,
  toda_53_n3_suspension_isomorphism_inference_rule,
)


def build_phase59_3_data():
  phase55 = (
    build_phase55_representative_result()
  )

  phase58 = (
    build_phase58_representative_result()
  )

  prop51_step = (
    phase55[
      "prop51_steps"
    ][
      0
    ]
  )

  hopf_eta5_step = (
    phase58[
      "final_hopf_step"
    ]
  )

  pi_4_2 = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=2,
  )

  pi_5_3 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=3,
  )

  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )

  pi_6_3 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )

  pi_6_5 = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=5,
  )

  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )

  h_delta_5 = TodaProp42ExactnessStatement(
    window=TodaEHPExactnessWindow(
      source_term=pi_5_3,
      middle_term=pi_5_5,
      target_term=pi_3_2,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
  )

  e_h_5 = TodaProp42ExactnessStatement(
    window=TodaEHPExactnessWindow(
      source_term=pi_4_2,
      middle_term=pi_5_3,
      target_term=pi_5_5,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
  )

  h_delta_6 = TodaProp42ExactnessStatement(
    window=TodaEHPExactnessWindow(
      source_term=pi_6_3,
      middle_term=pi_6_5,
      target_term=pi_4_2,
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
    ),
  )

  delta_e_6 = TodaProp42ExactnessStatement(
    window=TodaEHPExactnessWindow(
      source_term=pi_6_5,
      middle_term=pi_4_2,
      target_term=pi_5_3,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    ),
  )

  h_delta_5_step = ProofStep(
    conclusion=h_delta_5,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  e_h_5_step = ProofStep(
    conclusion=e_h_5,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  h_delta_6_step = ProofStep(
    conclusion=h_delta_6,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  delta_e_6_step = ProofStep(
    conclusion=delta_e_6,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  delta_injective_rule = (
    toda_53_n3_prop51_delta_injective_inference_rule()
  )

  hopf_zero_rule = (
    toda_53_n3_delta_injective_hopf_zero_inference_rule()
  )

  suspension_surjective_rule = (
    toda_53_n3_hopf_zero_suspension_surjective_inference_rule()
  )

  hopf_surjective_rule = (
    toda_53_n3_hopf_eta5_surjective_inference_rule()
  )

  delta_zero_rule = (
    toda_53_n3_hopf_surjective_delta_zero_inference_rule()
  )

  suspension_injective_rule = (
    toda_53_n3_delta_zero_suspension_injective_inference_rule()
  )

  suspension_isomorphism_rule = (
    toda_53_n3_suspension_isomorphism_inference_rule()
  )

  rules = (
    delta_injective_rule,
    hopf_zero_rule,
    suspension_surjective_rule,
    hopf_surjective_rule,
    delta_zero_rule,
    suspension_injective_rule,
    suspension_isomorphism_rule,
  )

  premise_steps = (
    prop51_step,
    hopf_eta5_step,
    h_delta_5_step,
    e_h_5_step,
    h_delta_6_step,
    delta_e_6_step,
  )

  result = (
    run_inference_until_stable_with_history(
      rules,
      premise_steps,
    )
  )

  expected_delta_injective = (
    TodaDeltaInjectiveStatement(
      map=TodaDeltaMap(
        source_group=pi_5_5,
        target_group=pi_3_2,
      ),
    )
  )

  expected_hopf_zero = (
    TodaHopfInvariantZeroStatement(
      map=TodaHopfInvariantMap(
        source_group=pi_5_3,
        target_group=pi_5_5,
      ),
    )
  )

  expected_suspension_surjective = (
    TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=pi_4_2,
        target_group=pi_5_3,
      ),
    )
  )

  expected_hopf_surjective = (
    TodaHopfInvariantSurjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=pi_6_3,
        target_group=pi_6_5,
      ),
    )
  )

  expected_delta_zero = (
    TodaDeltaZeroStatement(
      map=TodaDeltaMap(
        source_group=pi_6_5,
        target_group=pi_4_2,
      ),
    )
  )

  expected_suspension_injective = (
    TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=pi_4_2,
        target_group=pi_5_3,
      ),
    )
  )

  expected_suspension_isomorphism = (
    TodaSuspensionIsomorphismStatement(
      map=TodaSuspensionMap(
        source_group=pi_4_2,
        target_group=pi_5_3,
      ),
    )
  )

  return {
    "phase55": phase55,
    "phase58": phase58,
    "prop51_step": prop51_step,
    "hopf_eta5_step": hopf_eta5_step,
    "h_delta_5_step": h_delta_5_step,
    "e_h_5_step": e_h_5_step,
    "h_delta_6_step": h_delta_6_step,
    "delta_e_6_step": delta_e_6_step,
    "rules": rules,
    "premise_steps": premise_steps,
    "result": result,
    "expected_delta_injective": (
      expected_delta_injective
    ),
    "expected_hopf_zero": (
      expected_hopf_zero
    ),
    "expected_suspension_surjective": (
      expected_suspension_surjective
    ),
    "expected_hopf_surjective": (
      expected_hopf_surjective
    ),
    "expected_delta_zero": (
      expected_delta_zero
    ),
    "expected_suspension_injective": (
      expected_suspension_injective
    ),
    "expected_suspension_isomorphism": (
      expected_suspension_isomorphism
    ),
  }


def test_phase59_3_reuses_derived_prop51():
  data = build_phase59_3_data()

  assert (
    data[
      "prop51_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_3_reuses_phase58_hopf_eta5():
  data = build_phase59_3_data()

  step = data[
    "hopf_eta5_step"
  ]

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  eta_5 = HomotopyElement(
    name="η₅",
    dimension=5,
    source=6,
    target=5,
    generator=GeneratorSymbol(
      family="η",
      index=5,
    ),
  )

  assert (
    step.conclusion.rhs
    == eta_5
  )


def test_phase59_3_derives_delta_pi5_5_injective():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_delta_injective"
      ]
    )
  )

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_3_derives_h_pi5_3_zero():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_zero"
      ]
    )
  )

  assert len(
    steps
  ) == 1


def test_phase59_3_derives_e_pi4_2_surjective():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_suspension_surjective"
      ]
    )
  )

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_3_derives_h_pi6_3_surjective():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_hopf_surjective"
      ]
    )
  )

  assert len(
    steps
  ) == 1


def test_phase59_3_derives_delta_pi6_5_zero():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_delta_zero"
      ]
    )
  )

  assert len(
    steps
  ) == 1


def test_phase59_3_derives_e_pi4_2_injective():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_suspension_injective"
      ]
    )
  )

  assert len(
    steps
  ) == 1


def test_phase59_3_derives_e_pi4_2_isomorphism():
  data = build_phase59_3_data()

  steps = tuple(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_suspension_isomorphism"
      ]
    )
  )

  assert len(
    steps
  ) == 1

  assert (
    steps[
      0
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase59_3_final_isomorphism_preserves_two_derived_properties():
  data = build_phase59_3_data()

  final_step = next(
    step
    for step in data[
      "result"
    ].steps
    if (
      step.conclusion
      == data[
        "expected_suspension_isomorphism"
      ]
    )
  )

  assert len(
    final_step.premises
  ) == 2

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in final_step.premises
  )


def test_phase59_3_final_map_is_pi4_2_to_pi5_3():
  data = build_phase59_3_data()

  map_instance = (
    data[
      "expected_suspension_isomorphism"
    ].map
  )

  assert (
    map_instance.source_group
    == TodaPrimaryGroup(
      group_dimension=4,
      sphere_dimension=2,
    )
  )

  assert (
    map_instance.target_group
    == TodaPrimaryGroup(
      group_dimension=5,
      sphere_dimension=3,
    )
  )


def test_phase59_3_final_result_is_not_given():
  data = build_phase59_3_data()

  initial_conclusions = tuple(
    step.conclusion
    for step in data[
      "premise_steps"
    ]
  )

  assert (
    data[
      "expected_suspension_isomorphism"
    ]
    not in initial_conclusions
  )


def test_phase59_3_reaches_fixed_point():
  data = build_phase59_3_data()

  assert (
    data[
      "result"
    ].termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

