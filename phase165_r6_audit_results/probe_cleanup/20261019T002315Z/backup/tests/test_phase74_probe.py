from functools import lru_cache

from expression import (
  Composition,
)
from proof import (
  ProofRule,
)
from probes.probe_phase74_capabilities import (
  build_phase74_representative_result,
  main,
)
from toda_rules import (
  TodaLemma55BracketContainsUpToSignStatement,
  TodaLemma512BracketSingletonMod2Statement,
  TodaLemma512CoefficientStabilityStatement,
  TodaLemma512NonzeroAnchorStatement,
  TodaLemma512Statement,
  TodaProp511FiniteDimensionalStatement,
)


@lru_cache(maxsize=1)
def build_phase74_probe_data():
  return (
    build_phase74_representative_result()
  )


def test_phase74_probe_derives_final_statement():
  data = build_phase74_probe_data()

  step = (
    data[
      "final_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma512Statement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase74_probe_final_is_not_given():
  data = build_phase74_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase74_probe_reuses_singleton_branch():
  data = build_phase74_probe_data()

  assert isinstance(
    data[
      "singleton_step"
    ].conclusion,
    TodaLemma512BracketSingletonMod2Statement,
  )

  assert (
    data[
      "singleton_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_probe_reuses_stability_branch():
  data = build_phase74_probe_data()

  assert isinstance(
    data[
      "stability_step"
    ].conclusion,
    TodaLemma512CoefficientStabilityStatement,
  )

  assert (
    data[
      "stability_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_probe_reuses_anchor_branch():
  data = build_phase74_probe_data()

  assert isinstance(
    data[
      "anchor_step"
    ].conclusion,
    TodaLemma512NonzeroAnchorStatement,
  )

  assert (
    data[
      "anchor_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_probe_final_uses_exact_three_branches():
  data = build_phase74_probe_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "singleton_step"
      ],
      data[
        "stability_step"
      ],
      data[
        "anchor_step"
      ],
    )
  )


def test_phase74_probe_reuses_phase74_9_graph():
  data = build_phase74_probe_data()

  direct = (
    build_phase74_representative_result()
  )

  assert (
    data[
      "final_step"
    ]
    is direct[
      "final_step"
    ]
  )


def test_phase74_probe_reaches_prop511():
  data = build_phase74_probe_data()

  assert isinstance(
    data[
      "prop511_step"
    ].conclusion,
    TodaProp511FiniteDimensionalStatement,
  )

  assert (
    data[
      "prop511_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_probe_reaches_lemma55_inclusion():
  data = build_phase74_probe_data()

  assert isinstance(
    data[
      "lemma55_inclusion_step"
    ].conclusion,
    TodaLemma55BracketContainsUpToSignStatement,
  )

  assert (
    data[
      "lemma55_inclusion_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase74_probe_anchor_is_n8():
  data = build_phase74_probe_data()

  assert (
    data[
      "anchor_step"
    ].conclusion
    .anchor_dimension
    == 8
  )


def test_phase74_probe_final_generator_is_composition():
  data = build_phase74_probe_data()

  assert type(
    data[
      "final_step"
    ].conclusion
    .generator
  ) is Composition


def test_phase74_probe_output_contains_heading(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "EHP Proof Tracer"
    in output
  )

  assert (
    "Phase 74 capability demonstration"
    in output
  )

  assert (
    "Toda Lemma 5.12 result"
    in output
  )


def test_phase74_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "{η_n, ν_(n+1), η_(n+4)}"
    in output
  )

  assert (
    "{ν_n²}"
    in output
  )

  assert (
    "for n >= 6"
    in output
  )

  assert (
    "TodaLemma512Statement"
    in output
  )

  assert (
    "derived = True"
    in output
  )


def test_phase74_probe_output_contains_bracket_definedness(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[1] Bracket defined"
    in output
  )

  assert (
    "η_n ν_(n+1) = 0"
    in output
  )

  assert (
    "ν_(n+1) η_(n+4) = 0"
    in output
  )

  assert (
    "is defined"
    in output
  )


def test_phase74_probe_output_contains_first_indeterminacy(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[2] First indeterminacy"
    in output
  )

  assert (
    "π_(n+6)(S^(n+1))"
    in output
  )

  assert (
    "first indeterminacy = 0"
    in output
  )


def test_phase74_probe_output_contains_second_indeterminacy(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[3] Second indeterminacy"
    in output
  )

  assert (
    "π_(n+5)(S^n)"
    in output
  )

  assert (
    "π_11^6 = Z{Δι₁₃}"
    in output
  )

  assert (
    "Δ(η₁₃) = 0"
    in output
  )

  assert (
    "second indeterminacy = 0"
    in output
  )


def test_phase74_probe_output_contains_singleton_mod_two(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] Singleton mod two"
    in output
  )

  assert (
    "π_(n+6)^n = Z/2{ν_n²}"
    in output
  )

  assert (
    "= {x_n ν_n²}"
    in output
  )

  assert (
    "x_n in {0,1}"
    in output
  )


def test_phase74_probe_output_contains_coefficient_stability(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[5] Coefficient stability"
    in output
  )

  assert (
    "Toda Proposition 1.3 "
    "+ Toda (1.15)"
    in output
  )

  assert (
    "E(ν_n²) = ν_(n+1)²"
    in output
  )

  assert (
    "x_n = x_(n+1)"
    in output
  )


def test_phase74_probe_output_contains_nonzero_anchor(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[6] Nonzero anchor"
    in output
  )

  assert (
    "m=6, t=7, β=ν₆"
    in output
  )

  assert (
    "{η₈, ν₉, η₁₂}_3"
    in output
  )

  assert (
    "contains ±ν₈²"
    in output
  )

  assert (
    "x_8 = 1"
    in output
  )


def test_phase74_probe_output_contains_final_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[7] Toda Lemma 5.12"
    in output
  )

  assert (
    "x_n = 1 for every n >= 6"
    in output
  )

  assert (
    "{η_n, ν_(n+1), η_(n+4)}"
    in output
  )

  assert (
    "= {ν_n²}"
    in output
  )


def test_phase74_probe_output_contains_provenance(
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
    "singleton-mod-two branch derived = True"
    in output
  )

  assert (
    "coefficient-stability branch derived = True"
    in output
  )

  assert (
    "nonzero-anchor branch derived = True"
    in output
  )

  assert (
    "final Lemma 5.12 derived = True"
    in output
  )

  assert (
    "final Lemma 5.12 is GIVEN = False"
    in output
  )


def test_phase74_probe_output_contains_dependency_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Proposition 5.11 reachable = True"
    in output
  )

  assert (
    "nu-family reachable = True"
    in output
  )

  assert (
    "ν₆η₉=0 reachable = True"
    in output
  )

  assert (
    "Lemma 5.5 indexed inclusion reachable = True"
    in output
  )


def test_phase74_probe_output_contains_applicability(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Applicability / non-circularity"
    in output
  )

  assert (
    "range lower bound = 6"
    in output
  )

  assert (
    "range is n>=6 = True"
    in output
  )

  assert (
    "anchor dimension is exactly 8 = True"
    in output
  )


def test_phase74_probe_output_contains_non_circularity(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "stability does not depend on anchor = True"
    in output
  )

  assert (
    "anchor does not depend on stability = True"
    in output
  )


def test_phase74_probe_output_contains_representation_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "ν_n² remains Composition = True"
    in output
  )

  assert (
    "explicit coefficient field present = False"
    in output
  )

  assert (
    "stable branch field present = False"
    in output
  )


def test_phase74_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 74 representative probe boundary"
    in output
  )

  assert (
    "new mathematical inference rules"
    in output
  )

  assert (
    "generic Toda-bracket coset algebra"
    in output
  )

  assert (
    "generic induction engine"
    in output
  )

  assert (
    "stable (G_6;2) result"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )


def test_phase74_probe_output_marks_hand_authored_presentation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "hand-authored presentation code"
    in output
  )

  assert (
    "not yet generated "
    "automatically from the ProofStep graph"
    in output
  )


