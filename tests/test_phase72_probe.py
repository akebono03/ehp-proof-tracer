from functools import lru_cache

from homotopy_groups import (
  HomotopyGroup,
)
from proof import (
  ProofRule,
)
from probes.probe_phase72_capabilities import (
  build_phase72_representative_result,
  main,
)
from toda_rules import (
  TodaLemma510BracketModuloStatement,
  TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  TodaLemma510OrdinarySuspensionImageInDoubleStatement,
)


@lru_cache(maxsize=1)
def build_phase72_probe_data():
  return (
    build_phase72_representative_result()
  )


def test_phase72_probe_derives_corrected_final_statement():
  data = build_phase72_probe_data()

  step = (
    data[
      "final_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510BracketModuloStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )

  assert (
    step.conclusion.ambient_group
    == HomotopyGroup(
      group_dimension=11,
      sphere_dimension=6,
    )
  )


def test_phase72_probe_final_is_not_given():
  data = build_phase72_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase72_probe_core_is_corrected_and_derived():
  data = build_phase72_probe_data()

  step = (
    data[
      "core_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_indeterminacy_is_corrected_and_derived():
  data = build_phase72_probe_data()

  step = (
    data[
      "indeterminacy_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_image_containment_is_corrected_and_derived():
  data = build_phase72_probe_data()

  step = (
    data[
      "image_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaLemma510OrdinarySuspensionImageInDoubleStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase72_probe_final_premises_are_corrected_three_branches():
  data = build_phase72_probe_data()

  premises = (
    data[
      "final_step"
    ].premises
  )

  assert (
    len(
      premises
    )
    == 3
  )

  assert (
    premises[
      0
    ]
    is data[
      "core_step"
    ]
  )

  assert (
    premises[
      1
    ]
    is data[
      "indeterminacy_step"
    ]
  )

  assert (
    premises[
      2
    ]
    is data[
      "image_step"
    ]
  )


def test_phase72_probe_builder_reuses_corrected_representative_graph():
  data = build_phase72_probe_data()

  direct = (
    build_phase72_representative_result()
  )

  assert (
    data[
      "final_step"
    ]
    is direct[
      "final_step"
    ]
  )


def test_phase72_probe_output_contains_corrected_heading(
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
    "Phase 72R corrected capability demonstration"
    in output
  )

  assert (
    "Toda Lemma 5.10 corrected result"
    in output
  )


def test_phase72_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Δ(ι₁₃)"
    in output
  )

  assert (
    "{ν₆, η₉, 2ι₁₀}"
    in output
  )

  assert (
    "mod 2π₁₁(S⁶)"
    in output
  )

  assert (
    "ambient group = ordinary π₁₁(S⁶)"
    in output
  )

  assert (
    "derived = True"
    in output
  )


def test_phase72_probe_output_contains_ordinary_exactness(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[1] Ordinary EHP exactness"
    in output
  )

  assert (
    "Toda (2.11), m=5, i=10:"
    in output
  )

  assert (
    "π₁₀(S⁵) --E--> π₁₁(S⁶) --H--> π₁₁(S¹¹)"
    in output
  )

  assert (
    "ordinary exactness window"
    in output
  )


def test_phase72_probe_output_contains_prop26_and_toda115(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[2] Proposition 2.6 and Toda (1.15)"
    in output
  )

  assert (
    "H{ν₆,η₉,2ι₁₀}_1 contains 2ι₁₁"
    in output
  )

  assert (
    "Toda (1.15), n=1, m=0:"
    in output
  )

  assert (
    "{ν₆,η₉,2ι₁₀}_1 ⊂ {ν₆,η₉,2ι₁₀}"
    in output
  )


def test_phase72_probe_output_contains_corrected_indeterminacy(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] Corrected ordinary indeterminacy"
    in output
  )

  assert (
    "ν₆∘π₁₁(S⁹) = ν₆∘π₁₁⁹"
    in output
  )

  assert (
    "ν₆∘π₁₁(S⁹) = 0"
    in output
  )

  assert (
    "Indeterminacy = 2π₁₁(S⁶)"
    in output
  )


def test_phase72_probe_output_contains_corrected_image_containment(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[5] Corrected ordinary suspension image"
    in output
  )

  assert (
    "Eπ₁₀(S⁵) is finite."
    in output
  )

  assert (
    "the 2-primary part of Eπ₁₀(S⁵) is zero"
    in output
  )

  assert (
    "Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)"
    in output
  )


def test_phase72_probe_output_contains_final_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[6] Toda Lemma 5.10"
    in output
  )

  assert (
    "Indeterminacy = 2π₁₁(S⁶)"
    in output
  )

  assert (
    "Eπ₁₀(S⁵) ⊂ 2π₁₁(S⁶)"
    in output
  )

  assert (
    "mod 2π₁₁(S⁶)"
    in output
  )


def test_phase72_probe_output_contains_corrected_source_reuse(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Corrected representative source objects"
    in output
  )

  assert (
    "ordinary Toda (2.11) exactness reachable = True"
    in output
  )

  assert (
    "Prop.2.6 indexed bracket reachable = True"
    in output
  )

  assert (
    "Toda (1.15) split reachable = True"
    in output
  )

  assert (
    "composition-level primary reduction reachable = True"
    in output
  )

  assert (
    "ordinary finite E-image reachable = True"
    in output
  )

  assert (
    "ordinary E-image 2-primary zero reachable = True"
    in output
  )


def test_phase72_probe_output_contains_corrected_provenance(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Corrected provenance / retirement audit"
    in output
  )

  assert (
    "final modulo statement derived = True"
    in output
  )

  assert (
    "final modulo statement is GIVEN = False"
    in output
  )

  assert (
    "final ambient group is ordinary = True"
    in output
  )

  assert (
    "exact three direct premises = True"
    in output
  )

  assert (
    "final graph acyclic = True"
    in output
  )


def test_phase72_probe_output_contains_retirement_audit(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "legacy Phase 72 core step absent = True"
    in output
  )

  assert (
    "legacy Phase 72 indeterminacy step absent = True"
    in output
  )

  assert (
    "legacy Phase 72 image step absent = True"
    in output
  )

  assert (
    "Phase 71 n=6 Delta injectivity absent = True"
    in output
  )


def test_phase72_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 72R corrected representative probe boundary"
    in output
  )

  assert (
    "Historical only:"
    in output
  )

  assert (
    "generic primary-decomposition solver"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )


def test_phase72_probe_output_marks_hand_authored_presentation(
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

