from proof import (
  InferenceTerminationReason,
  LiteratureStatement,
  ProofRule,
)
from probes.probe_phase60_capabilities import (
  build_phase60_representative_result,
  main,
)


def test_phase60_probe_derives_lemma54_aggregate():
  representative = (
    build_phase60_representative_result()
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


def test_phase60_probe_derives_three_final_conclusions():
  representative = (
    build_phase60_representative_result()
  )

  final_steps = (
    representative[
      "membership_step"
    ],
    representative[
      "hopf_step"
    ],
    representative[
      "double_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in final_steps
  )


def test_phase60_probe_final_aggregate_is_not_given():
  representative = (
    build_phase60_representative_result()
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  assert (
    integration_step.rule
    != ProofRule.GIVEN
  )


def test_phase60_probe_final_provenance_uses_phase60_8_results():
  representative = (
    build_phase60_representative_result()
  )

  integration_step = (
    representative[
      "integration_step"
    ]
  )

  assert (
    integration_step.premises
    == (
      representative[
        "membership_step"
      ],
      representative[
        "hopf_step"
      ],
      representative[
        "double_step"
      ],
    )
  )

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in (
      integration_step
      .premises
    )
  )


def test_phase60_probe_reaches_fixed_point():
  representative = (
    build_phase60_representative_result()
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


def test_phase60_probe_aggregate_contains_literature_statements():
  representative = (
    build_phase60_representative_result()
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
    > 0
  )

  assert all(
    isinstance(
      statement,
      LiteratureStatement,
    )
    for statement in statements
  )

  assert all(
    statement.statement
    for statement in statements
  )


def test_phase60_probe_literature_contains_required_phase60_sources():
  representative = (
    build_phase60_representative_result()
  )

  statements = (
    representative[
      "integration_step"
    ]
    .conclusion
    .literature_statements
  )

  locators = {
    statement.reference.locator
    for statement in statements
  }

  assert (
    "Proposition 1.3"
    in locators
  )

  assert (
    "Equation (1.15)"
    in locators
  )

  assert (
    "Equation (3.2)"
    in locators
  )

  assert (
    "Theorem 3.6"
    in locators
  )

  assert (
    "Equation (4.7)"
    in locators
  )

  assert (
    "Equation (4.8)"
    in locators
  )

  assert (
    "Proposition 5.3"
    in locators
  )

  assert (
    "Equation (5.3)"
    in locators
  )

  assert (
    "Equation (5.4)"
    in locators
  )

  assert (
    "Lemma 5.4 proof"
    in locators
  )


def test_phase60_probe_output_contains_final_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 60 capability demonstration"
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
    "2Eν₄ = E²ν′"
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
    "all final premises are INFERENCE = True"
    in output
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase60_probe_output_contains_literature_statements(
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
    "[Toda Proposition 1.3]"
    in output
  )

  assert (
    "[Toda Theorem 3.6]"
    in output
  )

  assert (
    "[Toda Proposition 5.3]"
    in output
  )

  assert (
    "[Toda (5.4)]"
    in output
  )

  assert (
    "Statement:"
    in output
  )


def test_phase60_probe_output_contains_referenced_statement_content(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "-E{α,E^nβ,E^nγ}_n"
    in output
  )

  assert (
    "α=η₂"
    in output
  )

  assert (
    "α*∈π_7^4"
    in output
  )

  assert (
    "π_(n+2)^n = Z/2{η_n²}"
    in output
  )

  assert (
    "±E^(n-3)ν′"
    in output
  )

  assert (
    "H(α*)=(2s+1)ι₇"
    in output
  )


def test_phase60_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 60 completion boundary"
    in output
  )

  assert (
    "Toda Lemma 5.4 aggregate"
    in output
  )

  assert (
    "literature references with "
    "statement text"
    in output
  )

  assert (
    "generic sign solver"
    in output
  )

  assert (
    "Toda Lemma 5.5"
    in output
  )


def test_phase60_probe_output_contains_literature_usage(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Used in:"
    in output
  )

  assert (
    "Phase 60-3"
    in output
  )

  assert (
    "Phase 60-4"
    in output
  )

  assert (
    "Phase 60-5"
    in output
  )

  assert (
    "Phase 60-6"
    in output
  )

  assert (
    "Phase 60-7"
    in output
  )

  assert (
    "Phase 60-8"
    in output
  )


def test_phase60_probe_usage_distinguishes_phase_locations(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 60-3: "
    "Toda (5.4) bracket の "
    "indeterminacy calculation"
    in output
  )

  assert (
    "Phase 60-5: "
    "E: π_(n+2)^n → π_(n+3)^(n+1) "
    "の surjectivity を使った t=0 bridge"
    in output
  )

  assert (
    "Phase 60-6: "
    "α*∈π_7^4 と "
    "2Eα*∈-{η₅,2ι₆,η₆}_3 の導出"
    in output
  )

  assert (
    "Phase 60-7: "
    "H(α*)=(2s+1)ι₇ の "
    "Hopf invariant / parity consequence"
    in output
  )

  assert (
    "Phase 60-8: "
    "ν₄ の構成と "
    "H(ν₄)=ι₇, 2Eν₄=E²ν′ の導出"
    in output
  )


def test_phase60_probe_output_contains_derivation_chain(
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
    "Phase 60-3: "
    "Toda (5.4) indeterminacy"
    in output
  )

  assert (
    "Phase 60-4: "
    "bracket inclusion"
    in output
  )

  assert (
    "Phase 60-5: "
    "Toda (5.4)"
    in output
  )

  assert (
    "Phase 60-6: "
    "Theorem 3.6 specialization"
    in output
  )

  assert (
    "Phase 60-7: "
    "Hopf invariant parity"
    in output
  )

  assert (
    "Phase 60-8: "
    "Whitehead correction"
    in output
  )


def test_phase60_probe_output_contains_phase60_4_formula_chain(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "ν′ ∈ {η₃, 2ι₄, η₄}_1"
    in output
  )

  assert (
    "E^(n-3)ν′"
    in output
  )

  assert (
    "∈ E^(n-3)"
    "{η₃, 2ι₄, η₄}_1"
    in output
  )

  assert (
    "⊂ (-1)^(n-3)"
    "{η_n, 2ι_(n+1), "
    "η_(n+1)}_(n-2)"
    in output
  )

  assert (
    "[Toda Proposition 1.3]"
    in output
  )

  assert (
    "⊂ (-1)^(n-3)"
    "{η_n, 2ι_(n+1), "
    "η_(n+1)}_t"
    in output
  )

  assert (
    "[Toda (1.15), "
    "1 ≤ t ≤ n-2]"
    in output
  )

  assert (
    "∈ {η_n, 2ι_(n+1), "
    "η_(n+1)}_t"
    in output
  )


def test_phase60_probe_output_contains_full_proof_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Indeterminacy = <2E^(n-3)ν′>"
    in output
  )

  assert (
    "{η_n, 2ι_(n+1), "
    "η_(n+1)}_t"
    in output
  )

  assert (
    "= {±E^(n-3)ν′}"
    in output
  )

  assert (
    "∃ α* ∈ π_7^4"
    in output
  )

  assert (
    "2Eα* = ±E²ν′"
    in output
  )

  assert (
    "H(α*) = (2s+1)ι₇"
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
    "2Eν₄ = E²ν′"
    in output
  )

