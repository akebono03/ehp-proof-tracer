from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
)
from probes.probe_phase61_capabilities import (
  build_phase61_representative_result,
  main,
)


def test_phase61_probe_derives_lemma55_aggregate():
  representative = (
    build_phase61_representative_result()
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  assert (
    integration_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    integration_step.conclusion
    == representative[
      "expected_statement"
    ]
  )


def test_phase61_probe_derives_final_nu4_inclusion():
  representative = (
    build_phase61_representative_result()
  )

  final_step = (
    representative[
      "final_inclusion_step"
    ]
  )

  assert (
    final_step.rule
    == ProofRule.INFERENCE
  )

  assert (
    final_step.conclusion
    == representative[
      "expected_statement"
    ].bracket_inclusion
  )


def test_phase61_probe_final_aggregate_is_not_given():
  representative = (
    build_phase61_representative_result()
  )

  assert (
    representative[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase61_probe_theorem_dependencies_are_derived():
  representative = (
    build_phase61_representative_result()
  )

  assert (
    representative[
      "lemma54_step"
    ].rule
    == ProofRule.INFERENCE
  )

  assert (
    representative[
      "final_inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase61_probe_hypotheses_remain_given():
  representative = (
    build_phase61_representative_result()
  )

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in (
      representative[
        "beta_membership_step"
      ],
      representative[
        "beta_eta_zero_step"
      ],
      representative[
        "t_range_step"
      ],
    )
  )


def test_phase61_probe_reaches_fixed_point():
  representative = (
    build_phase61_representative_result()
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


def test_phase61_probe_contains_direct_literature_statements():
  representative = (
    build_phase61_representative_result()
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
    == 2
  )

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in statements
  )

  locators = {
    statement.reference.locator
    for statement in statements
  }

  assert (
    "Lemma 5.5"
    in locators
  )

  assert (
    "Lemma 5.5 proof"
    in locators
  )


def test_phase61_probe_preserves_phase60_literature():
  representative = (
    build_phase61_representative_result()
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


def test_phase61_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 61 capability demonstration"
    in output
  )

  assert (
    "Toda Lemma 5.5"
    in output
  )

  assert (
    "β ∈ π_(t+2)(S^m)"
    in output
  )

  assert (
    "β∘η_(t+2) = 0"
    in output
  )

  assert (
    "t > 0"
    in output
  )

  assert (
    "{η_(m+2), E³β, η_(t+5)}_3"
    in output
  )

  assert (
    "±(E²β∘E^tν₄)"
    in output
  )


def test_phase61_probe_output_contains_provenance(
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
    "Lemma 5.4 aggregate derived = True"
    in output
  )

  assert (
    "alpha-star bracket inclusion derived = True"
    in output
  )

  assert (
    "E^tν₄=±E^tα* derived = True"
    in output
  )

  assert (
    "final ν₄ bracket inclusion derived = True"
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
    "theorem dependencies are INFERENCE = True"
    in output
  )

  assert (
    "Lemma 5.5 hypotheses remain GIVEN = True"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase61_probe_output_contains_derivation_chain(
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
    "Phase 61-3: "
    "alpha-star bracket inclusion"
    in output
  )

  assert (
    "Phase 61-4: "
    "nu_4 suspension correction"
    in output
  )

  assert (
    "Phase 61-5: "
    "alpha-star to nu_4 composition bridge"
    in output
  )

  assert (
    "Phase 61-6: "
    "Toda Lemma 5.5 integration"
    in output
  )


def test_phase61_probe_output_contains_full_proof_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "±(E²β∘E^tα*)"
    in output
  )

  assert (
    "E[ι₄,ι₄] = 0"
    in output
  )

  assert (
    "E^tν₄ = ±E^tα*"
    in output
  )

  assert (
    "±(E²β∘E^tν₄)"
    in output
  )

  assert (
    "Toda Lemma 5.5 aggregate"
    in output
  )


def test_phase61_probe_output_contains_literature(
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
    "Phase 61 direct literature"
    in output
  )

  assert (
    "[Toda Lemma 5.5]"
    in output
  )

  assert (
    "[Toda Lemma 5.5 proof]"
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


def test_phase61_probe_output_contains_literature_usage(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 61-3"
    in output
  )

  assert (
    "Phase 61-4"
    in output
  )

  assert (
    "Phase 61-5"
    in output
  )

  assert (
    "Phase 61-6"
    in output
  )


def test_phase61_probe_output_contains_literature_statement_content(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "β∈π_(t+2)(S^m)"
    in output
  )

  assert (
    "E^2β∘E^tν₄"
    in output
  )

  assert (
    "E^2β∘E^tα*"
    in output
  )

  assert (
    "E[ι₄,ι₄]=0"
    in output
  )

  assert (
    "E^tν₄=±E^tα*"
    in output
  )


def test_phase61_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 61 completion boundary"
    in output
  )

  assert (
    "Toda Lemma 5.5 aggregate"
    in output
  )

  assert (
    "proof-style derivation display"
    in output
  )

  assert (
    "generic up-to-sign transitivity"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )

  assert (
    "Toda (5.5) ν-family calculation"
    in output
  )



