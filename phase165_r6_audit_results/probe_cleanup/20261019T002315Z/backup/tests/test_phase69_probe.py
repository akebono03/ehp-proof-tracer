from functools import lru_cache

from expression import (
  MapApplication,
)
from map_facts import (
  EHP_DELTA_MAP,
)
from proof import (
  ProofRule,
)
from probes.probe_phase69_capabilities import (
  build_phase69_representative_result,
  main,
)


@lru_cache(maxsize=1)
def build_phase69_probe_data():
  return (
    build_phase69_representative_result()
  )


def test_phase69_probe_final_is_inference():
  data = build_phase69_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_probe_final_is_not_given():
  data = build_phase69_probe_data()

  assert (
    data[
      "final_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase69_probe_reuses_delta_surjective():
  data = build_phase69_probe_data()

  assert (
    data[
      "delta_surjective_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_probe_reuses_derived_pi9_5():
  data = build_phase69_probe_data()

  assert (
    data[
      "pi9_5_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase69_probe_source_group_remains_given():
  data = build_phase69_probe_data()

  assert (
    data[
      "pi11_11_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase69_probe_final_is_delta_iota11():
  data = build_phase69_probe_data()

  assert (
    data[
      "final_step"
    ].conclusion.lhs
    == MapApplication(
      map=EHP_DELTA_MAP,
      expression=data[
        "iota_11"
      ],
    )
  )


def test_phase69_probe_final_value_is_pi9_5_generator():
  data = build_phase69_probe_data()

  assert (
    data[
      "final_step"
    ].conclusion.rhs
    is data[
      "pi9_5_step"
    ].conclusion.rhs.generator
  )


def test_phase69_probe_final_has_exact_three_premises():
  data = build_phase69_probe_data()

  assert (
    data[
      "final_step"
    ].premises
    == (
      data[
        "delta_surjective_step"
      ],
      data[
        "pi11_11_step"
      ],
      data[
        "pi9_5_step"
      ],
    )
  )


def test_phase69_probe_output_contains_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda Equation (5.10) result"
    in output
  )

  assert (
    "Δ(ι₁₁) = ν₅η₈"
    in output
  )


def test_phase69_probe_output_contains_exact_sequence(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_11^11 "
    "─Δ→ "
    "π_9^5 "
    "─E→ "
    "π_10^6"
    in output
  )

  assert (
    "π_10^6 = 0"
    in output
  )
  

def test_phase69_probe_output_contains_delta_surjectivity_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "ker(E) = π_9^5"
    in output
  )

  assert (
    "Im(Δ) = π_9^5"
    in output
  )

  assert (
    "Δ: π_11^11 → π_9^5 "
    "is surjective"
    in output
  )


def test_phase69_probe_output_contains_group_generators(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_11^11 = Z{ι₁₁}"
    in output
  )

  assert (
    "π_9^5 = Z/2{ν₅η₈}"
    in output
  )


def test_phase69_probe_output_explains_order_two_sign(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Since π_9^5 has order two,"
    in output
  )

  assert (
    "the possible sign is immaterial."
    in output
  )


def test_phase69_probe_output_contains_provenance(
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
    "π_10^6=0 derived = True"
    in output
  )

  assert (
    "Delta surjective derived = True"
    in output
  )

  assert (
    "π_9^5 result derived = True"
    in output
  )

  assert (
    "Toda (5.10) derived = True"
    in output
  )

  assert (
    "Toda (5.10) is GIVEN = False"
    in output
  )


def test_phase69_probe_output_contains_given_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "structural exactness window "
    "remains GIVEN = True"
    in output
  )

  assert (
    "π_11^11 source group "
    "remains foundational GIVEN = True"
    in output
  )


def test_phase69_probe_output_contains_fixed_point(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "fixed point = True"
    in output
  )


def test_phase69_probe_output_contains_literature(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Literature / source"
    in output
  )

  assert (
    "[Toda Equation (5.10)]"
    in output
  )

  assert (
    "Locator: Equation (5.10)"
    in output
  )

  assert (
    "Author: H. Toda"
    in output
  )

  assert (
    "Composition Methods in "
    "Homotopy Groups of Spheres"
    in output
  )

  assert (
    "Year: 1962"
    in output
  )


def test_phase69_probe_output_mentions_existing_511(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda Equation (5.11):"
    in output
  )

  assert (
    "Δ(η₉) = Eν′η₇"
    in output
  )

  assert (
    "already derived "
    "in Phase 68"
    in output
  )


def test_phase69_probe_output_does_not_claim_511_reimplementation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 69 does not reimplement "
    "Equation (5.11)."
    in output
  )


def test_phase69_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 69 representative probe boundary"
    in output
  )

  assert (
    "Not added in Phase 69-5:"
    in output
  )

  assert (
    "new mathematical inference rules"
    in output
  )

  assert (
    "stable (G_4;2)=0"
    in output
  )


def test_phase69_probe_does_not_claim_automatic_narrative(
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


def test_phase69_probe_builder_reuses_phase69_3_result():
  data = build_phase69_probe_data()

  phase69_3 = data

  assert (
    data[
      "final_step"
    ]
    is phase69_3[
      "final_step"
    ]
  )


