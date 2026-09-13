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
def build_phase72r10_probe_data():
  return (
    build_phase72_representative_result()
  )


def test_phase72r10_probe_uses_corrected_final_statement():
  data = build_phase72r10_probe_data()

  step = data[
    "final_step"
  ]

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


def test_phase72r10_probe_uses_corrected_three_branches():
  data = build_phase72r10_probe_data()

  assert isinstance(
    data[
      "core_step"
    ].conclusion,
    TodaLemma510OrdinaryBracketPlusSuspensionImageStatement,
  )

  assert isinstance(
    data[
      "indeterminacy_step"
    ].conclusion,
    TodaLemma510OrdinaryIndeterminacyDoubleStatement,
  )

  assert isinstance(
    data[
      "image_step"
    ].conclusion,
    TodaLemma510OrdinarySuspensionImageInDoubleStatement,
  )

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "core_step"
      ],
      data[
        "indeterminacy_step"
      ],
      data[
        "image_step"
      ],
    )
  )


def test_phase72r10_probe_output_contains_corrected_heading(
  capsys,
):
  main()
  output = capsys.readouterr().out

  assert (
    "Phase 72R corrected capability demonstration"
    in output
  )

  assert (
    "Toda Lemma 5.10 corrected result"
    in output
  )


def test_phase72r10_probe_output_contains_ordinary_exactness(
  capsys,
):
  main()
  output = capsys.readouterr().out

  assert (
    "ordinary exactness window"
    in output
  )

  assert (
    "π₁₀(S⁵) --E--> π₁₁(S⁶) --H--> π₁₁(S¹¹)"
    in output
  )


def test_phase72r10_probe_output_contains_prop26_and_split(
  capsys,
):
  main()
  output = capsys.readouterr().out

  assert (
    "H{ν₆,η₉,2ι₁₀}_1 contains 2ι₁₁"
    in output
  )

  assert (
    "Toda (1.15), n=1, m=0:"
    in output
  )


def test_phase72r10_probe_output_contains_composition_level_reduction(
  capsys,
):
  main()
  output = capsys.readouterr().out

  assert (
    "ν₆∘π₁₁(S⁹) = ν₆∘π₁₁⁹"
    in output
  )

  assert (
    "Indeterminacy = 2π₁₁(S⁶)"
    in output
  )


def test_phase72r10_probe_output_contains_corrected_image_bridge(
  capsys,
):
  main()
  output = capsys.readouterr().out

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


def test_phase72r10_probe_output_contains_retirement_audit(
  capsys,
):
  main()
  output = capsys.readouterr().out

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


def test_phase72r10_probe_output_marks_hand_authored_presentation(
  capsys,
):
  main()
  output = capsys.readouterr().out

  assert (
    "hand-authored presentation code"
    in output
  )

  assert (
    "not yet generated "
    "automatically from the ProofStep graph"
    in output
  )
