from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
)
from probes.probe_phase62_capabilities import (
  build_phase62_representative_result,
  main,
)


def test_phase62_probe_derives_toda55_aggregate():
  representative = (
    build_phase62_representative_result()
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


def test_phase62_probe_derives_double_nu_relation():
  representative = (
    build_phase62_representative_result()
  )

  assert (
    representative[
      "double_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_probe_derives_quadruple_nu_relation():
  representative = (
    build_phase62_representative_result()
  )

  assert (
    representative[
      "quadruple_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase62_probe_final_aggregate_is_not_given():
  representative = (
    build_phase62_representative_result()
  )

  assert (
    representative[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase62_probe_theorem_dependencies_are_derived():
  representative = (
    build_phase62_representative_result()
  )

  phase62_4 = (
    representative[
      "phase62_4"
    ]
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in (
      representative[
        "lemma54_step"
      ],
      representative[
        "double_nu_step"
      ],
      phase62_4[
        "triple_eta_step"
      ],
      representative[
        "quadruple_nu_step"
      ],
    )
  )


def test_phase62_probe_definition_and_range_remain_given():
  representative = (
    build_phase62_representative_result()
  )

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in (
      representative[
        "definition_step"
      ],
      representative[
        "n_range_step"
      ],
    )
  )


def test_phase62_probe_reaches_fixed_point():
  representative = (
    build_phase62_representative_result()
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


def test_phase62_probe_contains_direct_literature():
  representative = (
    build_phase62_representative_result()
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
    == "Equation (5.5)"
  )


def test_phase62_probe_preserves_phase60_literature():
  representative = (
    build_phase62_representative_result()
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


def test_phase62_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 62 capability demonstration"
    in output
  )

  assert (
    "Toda (5.5) finite-dimensional "
    "nu-family calculation"
    in output
  )

  assert (
    "ν_n := E^(n-4)ν₄"
    in output
  )

  assert (
    "n ≥ 4"
    in output
  )

  assert (
    "For n ≥ 5:"
    in output
  )

  assert (
    "2ν_n = E^(n-3)ν′"
    in output
  )

  assert (
    "4ν_n = η_n³"
    in output
  )


def test_phase62_probe_output_contains_eta_cube_definition(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "η_n³"
    in output
  )

  assert (
    "η_n∘η_(n+1)∘η_(n+2)"
    in output
  )


def test_phase62_probe_output_contains_derivation_chain(
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
    "Phase 62-2: "
    "nu-family definition"
    in output
  )

  assert (
    "Phase 62-3: "
    "double-value suspension transport"
    in output
  )

  assert (
    "Phase 62-4: "
    "eta-cube bridge"
    in output
  )

  assert (
    "Phase 62-6: "
    "Toda (5.5) finite-dimensional integration"
    in output
  )


def test_phase62_probe_output_contains_full_proof_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "2Eν₄ = E²ν′"
    in output
  )

  assert (
    "↓ suspend by E^(n-5)"
    in output
  )

  assert (
    "2ν_n = E^(n-3)ν′"
    in output
  )

  assert (
    "↓ multiply by 2"
    in output
  )

  assert (
    "4ν_n = 2E^(n-3)ν′"
    in output
  )

  assert (
    "2ν′ = η₃∘η₄∘η₅"
    in output
  )

  assert (
    "2E^(n-3)ν′"
    in output
  )

  assert (
    "= η_n∘η_(n+1)∘η_(n+2)"
    in output
  )


def test_phase62_probe_output_contains_provenance(
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
    "nu-family definition is GIVEN = True"
    in output
  )

  assert (
    "n>=5 applicability is GIVEN = True"
    in output
  )

  assert (
    "2ν_n=E^(n-3)ν′ derived = True"
    in output
  )

  assert (
    "Phase 60 triple-eta transport derived = True"
    in output
  )

  assert (
    "4ν_n=η_n³ derived = True"
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
    "definition / applicability remain GIVEN = True"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase62_probe_output_contains_literature(
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
    "Phase 62 direct literature"
    in output
  )

  assert (
    "[Toda (5.5)]"
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


def test_phase62_probe_output_contains_literature_usage(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 62-2"
    in output
  )

  assert (
    "Phase 62-3"
    in output
  )

  assert (
    "Phase 62-4"
    in output
  )

  assert (
    "Phase 62-6"
    in output
  )


def test_phase62_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 62 completion boundary"
    in output
  )

  assert (
    "Toda (5.5) "
    "finite-dimensional aggregate"
    in output
  )

  assert (
    "stable ν := E^∞ν₄"
    in output
  )

  assert (
    "stable 4ν = η³"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )

  assert (
    "Toda (5.6) "
    "ν₄ decomposition isomorphism"
    in output
  )


def test_phase62_probe_output_excludes_stable_result_from_result_section(
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
    "4ν = η³"
    not in result_section
  )


