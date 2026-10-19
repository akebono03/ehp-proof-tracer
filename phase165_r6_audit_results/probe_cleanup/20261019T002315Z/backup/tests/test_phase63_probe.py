from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
)
from probes.probe_phase63_capabilities import (
  build_phase63_representative_result,
  main,
)


def test_phase63_probe_derives_final_aggregate():
  representative = (
    build_phase63_representative_result()
  )

  assert (
    representative[
      "integration_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    representative[
      "integration_step"
    ].conclusion
    == representative[
      "expected_statement"
    ]
  )


def test_phase63_probe_derives_toda56_semantics():
  representative = (
    build_phase63_representative_result()
  )

  assert (
    representative[
      "decomposition_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_probe_reuses_derived_lemma54():
  representative = (
    build_phase63_representative_result()
  )

  assert (
    representative[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase63_probe_theorem_dependencies_are_derived():
  representative = (
    build_phase63_representative_result()
  )

  phase63_4 = (
    representative[
      "phase63_4"
    ]
  )

  phase63_3 = (
    representative[
      "phase63_3"
    ]
  )

  phase63_2 = (
    representative[
      "phase63_2"
    ]
  )

  phase60_9 = (
    phase63_2[
      "phase60_9"
    ]
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      phase60_9[
        "membership_step"
      ],
      phase60_9[
        "hopf_step"
      ],
      phase60_9[
        "double_step"
      ],
      representative[
        "lemma54_step"
      ],
      phase63_3[
        "specialization_step"
      ],
      phase63_4[
        "prop44_isomorphism_step"
      ],
      representative[
        "decomposition_step"
      ],
      representative[
        "integration_step"
      ],
    )
  )


def test_phase63_probe_decomposition_map_remains_given():
  representative = (
    build_phase63_representative_result()
  )

  decomposition_map_step = (
    representative[
      "phase63_3"
    ][
      "decomposition_map_step"
    ]
  )

  assert (
    decomposition_map_step.rule
    == ProofRule.GIVEN
  )


def test_phase63_probe_final_aggregate_is_not_given():
  representative = (
    build_phase63_representative_result()
  )

  assert (
    representative[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase63_probe_reaches_fixed_point():
  representative = (
    build_phase63_representative_result()
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
    == 1
  )


def test_phase63_probe_contains_direct_literature():
  representative = (
    build_phase63_representative_result()
  )

  statements = (
    representative[
      "integration_step"
    ]
    .conclusion
    .literature_statements
  )

  assert (
    len(
      statements
    )
    == 1
  )

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in statements
  )

  assert (
    statements[
      0
    ].reference.locator
    == "Equation (5.6)"
  )


def test_phase63_probe_preserves_phase60_literature():
  representative = (
    build_phase63_representative_result()
  )

  statements = (
    representative[
      "integration_step"
    ]
    .conclusion
    .lemma54_statement
    .literature_statements
  )

  assert (
    len(
      statements
    )
    > 0
  )

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in statements
  )


def test_phase63_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 63 capability demonstration"
    in output
  )

  assert (
    "Toda (5.6) nu_4 "
    "decomposition isomorphism"
    in output
  )

  assert (
    "π_(i-1)^3 ⊕ π_i^7"
    in output
  )

  assert (
    "π_i^4"
    in output
  )

  assert (
    "= Eα + ν₄∘β"
    in output
  )

  assert (
    "Φ is an isomorphism."
    in output
  )


def test_phase63_probe_output_contains_derivation_chain(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Proof-style derivation"
    in output
  )

  assert (
    "Phase 60: "
    "Toda Lemma 5.4"
    in output
  )

  assert (
    "Phase 63-2: "
    "nu_4 specialization premises"
    in output
  )

  assert (
    "Phase 63-3: "
    "Proposition 4.4 decomposition "
    "specialization"
    in output
  )

  assert (
    "Phase 63-4: "
    "Toda (5.6) semantics"
    in output
  )

  assert (
    "Phase 63-6: "
    "Toda (5.6) literature-aware "
    "aggregate"
    in output
  )


def test_phase63_probe_output_contains_prop44_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "n = 4"
    in output
  )

  assert (
    "α = ν₄"
    in output
  )

  assert (
    "ν₄ ∈ π_7^4"
    in output
  )

  assert (
    "H(ν₄) = ι₇"
    in output
  )

  assert (
    "↓ Toda Proposition 4.4"
    in output
  )

  assert (
    "(α,β)"
    in output
  )

  assert (
    "Eα + ν₄∘β"
    in output
  )


def test_phase63_probe_output_contains_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Provenance / integration"
    in output
  )

  assert (
    "nu_4 membership derived = True"
    in output
  )

  assert (
    "H(nu_4)=iota_7 derived = True"
    in output
  )

  assert (
    "Lemma 5.4 aggregate derived = True"
    in output
  )

  assert (
    "nu_4 specialization derived = True"
    in output
  )

  assert (
    "decomposition map is GIVEN = True"
    in output
  )

  assert (
    "Prop.4.4 specialization "
    "isomorphism derived = True"
    in output
  )

  assert (
    "Toda (5.6) semantics derived = True"
    in output
  )

  assert (
    "final aggregate derived = True"
    in output
  )

  assert (
    "final aggregate is GIVEN = False"
    in output
  )

  assert (
    "theorem dependencies are "
    "INFERENCE = True"
    in output
  )

  assert (
    "structural decomposition map "
    "remains GIVEN = True"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase63_probe_output_contains_literature(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Literature statements used"
    in output
  )

  assert (
    "Phase 63 direct literature"
    in output
  )

  assert (
    "[Toda (5.6)]"
    in output
  )

  assert (
    "Inherited through "
    "Toda Lemma 5.4"
    in output
  )

  assert (
    "Used in:"
    in output
  )

  assert (
    "Statement:"
    in output
  )


def test_phase63_probe_output_contains_literature_usage(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 63-3"
    in output
  )

  assert (
    "Phase 63-4"
    in output
  )

  assert (
    "Phase 63-6"
    in output
  )


def test_phase63_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 63 completion boundary"
    in output
  )

  assert (
    "Proposition 4.4 concrete "
    "decomposition specialization"
    in output
  )

  assert (
    "Toda (5.6) "
    "isomorphism semantics"
    in output
  )

  assert (
    "Toda (5.6) "
    "literature-aware aggregate"
    in output
  )

  assert (
    "automatic proof narrative "
    "generation"
    in output
  )


def test_phase63_probe_output_excludes_future_frameworks_from_result_section(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  result_section = (
    output.split(
      "Proof-style derivation"
    )[
      0
    ]
  )

  assert (
    "generic Proposition 4.4 "
    "specialization framework"
    not in result_section
  )

  assert (
    "automatic proof narrative "
    "generation"
    not in result_section
  )


