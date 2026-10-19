from functools import lru_cache

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
)
from proof import (
  ProofRule,
)
from probes.probe_phase75_capabilities import (
  build_phase75_representative_result,
  main,
)
from toda_rules import (
  TodaProp515FiniteDimensionalStatement,
)


@lru_cache(maxsize=1)
def build_phase75_probe_data():
  return (
    build_phase75_representative_result()
  )


def test_phase75_probe_derives_final_aggregate():
  data = build_phase75_probe_data()

  step = (
    data[
      "aggregate_step"
    ]
  )

  assert isinstance(
    step.conclusion,
    TodaProp515FiniteDimensionalStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase75_probe_final_is_not_given():
  data = build_phase75_probe_data()

  assert (
    data[
      "aggregate_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase75_probe_all_mathematical_branches_are_inference():
  data = build_phase75_probe_data()

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step
    in (
      data[
        "pi9_2_step"
      ],
      data[
        "pi10_3_step"
      ],
      data[
        "pi11_4_step"
      ],
      data[
        "pi12_5_step"
      ],
      data[
        "pi13_6_step"
      ],
      data[
        "pi14_7_step"
      ],
      data[
        "pi15_8_step"
      ],
      data[
        "higher_step"
      ],
    )
  )


def test_phase75_probe_higher_range_remains_given():
  data = build_phase75_probe_data()

  assert (
    data[
      "higher_range_step"
    ].rule
    == ProofRule.GIVEN
  )


def test_phase75_probe_uses_exact_aggregate_premises():
  data = build_phase75_probe_data()

  assert (
    data[
      "aggregate_step"
    ].premises
    == data[
      "premise_steps"
    ]
  )


def test_phase75_probe_reuses_phase75_9_graph():
  data = build_phase75_probe_data()

  direct = (
    build_phase75_representative_result()
  )

  assert (
    data[
      "aggregate_step"
    ]
    is direct[
      "aggregate_step"
    ]
  )


def test_phase75_probe_pi15_8_is_mixed_direct_sum():
  data = build_phase75_probe_data()

  relation = (
    data[
      "aggregate_step"
    ].conclusion
    .pi15_8_group_relation
  )

  assert isinstance(
    relation.rhs,
    DirectSumGroup,
  )

  assert isinstance(
    relation.rhs.summands[
      0
    ],
    FreeCyclicGroup,
  )

  assert isinstance(
    relation.rhs.summands[
      1
    ],
    FiniteCyclicGroup,
  )

  assert (
    relation.rhs.summands[
      1
    ].order
    == 8
  )


def test_phase75_probe_stable_branch_is_absent():
  data = build_phase75_probe_data()

  statement = (
    data[
      "aggregate_step"
    ].conclusion
  )

  assert not hasattr(
    statement,
    "stable_group_relation",
  )


def test_phase75_probe_has_literature_metadata():
  data = build_phase75_probe_data()

  literature = (
    data[
      "aggregate_step"
    ].conclusion
    .literature_statements
  )

  assert any(
    item.reference.label
    == "Toda Proposition 5.15"
    for item
    in literature
  )


def test_phase75_probe_output_contains_heading(
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
    "Phase 75 capability demonstration"
    in output
  )

  assert (
    "Toda Proposition 5.15 "
    "finite-dimensional result"
    in output
  )


def test_phase75_probe_output_contains_all_group_results(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "π_9^2 = 0"
    in output
  )

  assert (
    "π_10^3 = 0"
    in output
  )

  assert (
    "π_11^4 = 0"
    in output
  )

  assert (
    "π_12^5 = Z/2{σ'''}"
    in output
  )

  assert (
    "π_13^6 = Z/4{σ''}"
    in output
  )

  assert (
    "π_14^7 = Z/8{σ'}"
    in output
  )

  assert (
    "π_15^8 = Z{σ₈} ⊕ Z/8{Eσ'}"
    in output
  )

  assert (
    "π_(n+7)^n = Z/16{σ_n}"
    in output
  )


def test_phase75_probe_output_contains_low_zero_derivation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[1] Low zero branches"
    in output
  )

  assert (
    "π_9^3 = 0"
    in output
  )

  assert (
    "π_11^4 = 0"
    in output
  )


def test_phase75_probe_output_contains_sigma_low_branches(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[2] σ''' and π_12^5"
    in output
  )

  assert (
    "Toda Lemma 5.13"
    in output
  )

  assert (
    "[3] σ'' and σ'"
    in output
  )

  assert (
    "2σ'' = Eσ'''"
    in output
  )

  assert (
    "2σ' = Eσ''"
    in output
  )


def test_phase75_probe_output_contains_sigma8_branch(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[4] σ₈ and the sigma family"
    in output
  )

  assert (
    "H(σ₈) = ι₁₅"
    in output
  )

  assert (
    "2Eσ₈ = E²σ'"
    in output
  )


def test_phase75_probe_output_contains_n8_prop44_branch(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[5] n=8 critical branch"
    in output
  )

  assert (
    "π_14^7 ⊕ π_15^15 ≅ π_15^8"
    in output
  )

  assert (
    "(α,β) ↦ Eα + σ₈∘β"
    in output
  )

  assert (
    "σ' ↦ Eσ'"
    in output
  )

  assert (
    "ι₁₅ ↦ σ₈"
    in output
  )


def test_phase75_probe_output_contains_higher_transport(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[6] n>=9 branch"
    in output
  )

  assert (
    "π_16^9 = Z/16{σ₉}"
    in output
  )

  assert (
    "Toda (4.5) stable-range transport"
    in output
  )


def test_phase75_probe_output_contains_aggregate_integration(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "[7] Proposition 5.15 integration"
    in output
  )

  assert (
    "TodaProp515FiniteDimensionalStatement"
    in output
  )


def test_phase75_probe_output_contains_provenance(
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
    "all eight mathematical branches "
    "are INFERENCE = True"
    in output
  )

  assert (
    "n>=9 range remains GIVEN = True"
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
    "exact direct aggregate premises = True"
    in output
  )


def test_phase75_probe_output_contains_representation_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Representation / completion boundary"
    in output
  )

  assert (
    "π_15^8 uses DirectSumGroup = True"
    in output
  )

  assert (
    "free σ₈ summand is first = True"
    in output
  )

  assert (
    "order-eight Eσ' summand is second = True"
    in output
  )

  assert (
    "stable (G_7;2) included = False"
    in output
  )


def test_phase75_probe_output_contains_literature(
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
    "Toda Proposition 5.15"
    in output
  )

  assert (
    "H. Toda"
    in output
  )


def test_phase75_probe_output_contains_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 75 representative probe boundary"
    in output
  )

  assert (
    "stable (G_7;2) result"
    in output
  )

  assert (
    "Toda (5.16)"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )


def test_phase75_probe_output_marks_hand_authored_presentation(
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
