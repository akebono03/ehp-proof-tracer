from ehp_rules import (
  EHPZeroCompositionStatement,
)
from expression import (
  ScalarSymbol,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from probes.probe_phase45_capabilities import (
  build_phase45_representative_result,
  exactness_text,
  window_text,
  zero_composition_text,
)
from proof import (
  ExactnessStatement,
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  toda_prop42_exactness_to_generic_inference_rule,
)


def test_phase45_6_bridge_rule_requires_toda_prop42_exactness_statement():
  rule = (
    toda_prop42_exactness_to_generic_inference_rule()
  )

  assert len(
    rule.premise_patterns
  ) == 1

  assert (
    rule.premise_patterns[
      0
    ].statement_type
    is TodaProp42ExactnessStatement
  )


def test_phase45_6_bridge_matches_toda_exactness_statement():
  representative = (
    build_phase45_representative_result()
  )

  theorem_step = (
    representative[
      "theorem_steps"
    ][
      0
    ]
  )

  rule = (
    toda_prop42_exactness_to_generic_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      theorem_step,
    ),
  )

  assert match is not None

  assert match.premises == (
    theorem_step,
  )


def test_phase45_6_bridge_derives_generic_e_h_exactness():
  representative = (
    build_phase45_representative_result()
  )

  theorem_step = (
    representative[
      "theorem_steps"
    ][
      0
    ]
  )

  rule = (
    toda_prop42_exactness_to_generic_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      (
        theorem_step,
      ),
    )
  )

  expected = ExactnessStatement(
    first_map=EHP_E_MAP,
    second_map=EHP_H_MAP,
    is_exact=True,
  )

  conclusions = tuple(
    step.conclusion
    for step in result.steps
  )

  assert expected in conclusions


def test_phase45_6_all_three_toda_exactness_results_bridge_to_generic_exactness():
  representative = (
    build_phase45_representative_result()
  )

  generic_steps = representative[
    "generic_exactness_steps"
  ]

  assert len(
    generic_steps
  ) == 3

  assert tuple(
    step.conclusion
    for step in generic_steps
  ) == (
    ExactnessStatement(
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
      is_exact=True,
    ),
    ExactnessStatement(
      first_map=EHP_H_MAP,
      second_map=EHP_DELTA_MAP,
      is_exact=True,
    ),
    ExactnessStatement(
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
      is_exact=True,
    ),
  )


def test_phase45_6_bridge_preserves_theorem_step_as_provenance():
  representative = (
    build_phase45_representative_result()
  )

  theorem_steps = representative[
    "theorem_steps"
  ]

  generic_steps = representative[
    "generic_exactness_steps"
  ]

  for theorem_step, generic_step in zip(
    theorem_steps,
    generic_steps,
  ):
    assert generic_step.premises == (
      theorem_step,
    )

    assert (
      generic_step.rule
      == ProofRule.INFERENCE
    )

    assert (
      generic_step.inference_rule
      == representative[
        "bridge_rule"
      ]
    )


def test_phase45_6_bridge_does_not_match_raw_window():
  representative = (
    build_phase45_representative_result()
  )

  raw_window_step = (
    representative[
      "premise_steps"
    ][
      0
    ]
  )

  rule = (
    toda_prop42_exactness_to_generic_inference_rule()
  )

  match = find_inference_match(
    rule,
    (
      raw_window_step,
    ),
  )

  assert match is None


def test_phase45_6_toda_exactness_remains_instance_aware_before_bridge():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  j = ScalarSymbol(
    name="j",
  )

  m = ScalarSymbol(
    name="m",
  )

  first = (
    build_phase45_representative_result(
      i=i,
      n=n,
    )
  )

  second = (
    build_phase45_representative_result(
      i=j,
      n=m,
    )
  )

  first_statement = (
    first[
      "theorem_steps"
    ][
      0
    ].conclusion
  )

  second_statement = (
    second[
      "theorem_steps"
    ][
      0
    ].conclusion
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase45_6_generic_exactness_is_intentionally_instance_lossy():
  i = ScalarSymbol(
    name="i",
  )

  n = ScalarSymbol(
    name="n",
  )

  j = ScalarSymbol(
    name="j",
  )

  m = ScalarSymbol(
    name="m",
  )

  first = (
    build_phase45_representative_result(
      i=i,
      n=n,
    )
  )

  second = (
    build_phase45_representative_result(
      i=j,
      n=m,
    )
  )

  first_generic = (
    first[
      "generic_exactness_steps"
    ][
      0
    ].conclusion
  )

  second_generic = (
    second[
      "generic_exactness_steps"
    ][
      0
    ].conclusion
  )

  assert (
    first_generic
    == second_generic
  )


def test_phase45_6_existing_ehp_rule_consumes_generic_exactness():
  representative = (
    build_phase45_representative_result()
  )

  zero_steps = representative[
    "zero_composition_steps"
  ]

  assert len(
    zero_steps
  ) == 3

  assert all(
    isinstance(
      step.conclusion,
      EHPZeroCompositionStatement,
    )
    for step in zero_steps
  )


def test_phase45_6_existing_ehp_rule_derives_expected_zero_compositions():
  representative = (
    build_phase45_representative_result()
  )

  zero_steps = representative[
    "zero_composition_steps"
  ]

  assert tuple(
    (
      step.conclusion.first_map,
      step.conclusion.second_map,
    )
    for step in zero_steps
  ) == (
    (
      EHP_E_MAP,
      EHP_H_MAP,
    ),
    (
      EHP_H_MAP,
      EHP_DELTA_MAP,
    ),
    (
      EHP_DELTA_MAP,
      EHP_E_MAP,
    ),
  )


def test_phase45_6_representative_reaches_fixed_point_in_three_rounds():
  representative = (
    build_phase45_representative_result()
  )

  result = representative[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert (
    result.round_count
    == 3
  )

  assert tuple(
    len(
      round_result.new_steps
    )
    for round_result
    in result.round_results
  ) == (
    3,
    3,
    3,
  )


def test_phase45_6_representative_preserves_three_toda_theorem_steps():
  representative = (
    build_phase45_representative_result()
  )

  theorem_steps = representative[
    "theorem_steps"
  ]

  assert len(
    theorem_steps
  ) == 3

  assert all(
    isinstance(
      step.conclusion,
      TodaProp42ExactnessStatement,
    )
    for step in theorem_steps
  )


def test_phase45_6_probe_formats_three_windows():
  representative = (
    build_phase45_representative_result()
  )

  windows = representative[
    "windows"
  ]

  assert tuple(
    window_text(
      window
    )
    for window in windows
  ) == (
    (
      "π_{i}^{n} -E→ "
      "π_{i+1}^{n+1} -H→ "
      "π_{i+1}^{2n+1}"
    ),
    (
      "π_{i+1}^{n+1} -H→ "
      "π_{i+1}^{2n+1} -Δ→ "
      "π_{i-1}^{n}"
    ),
    (
      "π_{i+1}^{2n+1} -Δ→ "
      "π_{i-1}^{n} -E→ "
      "π_{i}^{n+1}"
    ),
  )


def test_phase45_6_probe_formats_generic_exactness():
  representative = (
    build_phase45_representative_result()
  )

  assert tuple(
    exactness_text(
      step.conclusion
    )
    for step
    in representative[
      "generic_exactness_steps"
    ]
  ) == (
    "E-H exact",
    "H-Δ exact",
    "Δ-E exact",
  )


def test_phase45_6_probe_formats_zero_composition_consequences():
  representative = (
    build_phase45_representative_result()
  )

  assert tuple(
    zero_composition_text(
      step.conclusion
    )
    for step
    in representative[
      "zero_composition_steps"
    ]
  ) == (
    "H∘E = 0",
    "Δ∘H = 0",
    "E∘Δ = 0",
  )


def test_phase45_6_generic_bridge_does_not_replace_toda_theorem_statement():
  representative = (
    build_phase45_representative_result()
  )

  conclusions = tuple(
    step.conclusion
    for step in representative[
      "result"
    ].steps
  )

  for theorem_step in representative[
    "theorem_steps"
  ]:
    assert (
      theorem_step.conclusion
      in conclusions
    )

  for generic_step in representative[
    "generic_exactness_steps"
  ]:
    assert (
      generic_step.conclusion
      in conclusions
    )


