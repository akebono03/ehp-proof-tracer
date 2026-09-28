from functools import lru_cache

from proof import (
  ProofRule,
)
from probes.probe_phase66_capabilities import (
  build_phase66_representative_result,
  main,
)
from toda_rules import (
  Toda58EquationStatement,
)


@lru_cache(maxsize=1)
def build_phase66_probe_data():
  return (
    build_phase66_representative_result()
  )


def test_phase66_probe_derives_equation58_aggregate():
  data = build_phase66_probe_data()

  step = data[
    "integration_step"
  ]

  assert isinstance(
    step.conclusion,
    Toda58EquationStatement,
  )

  assert (
    step.rule
    == ProofRule.INFERENCE
  )


def test_phase66_probe_final_aggregate_is_not_given():
  data = build_phase66_probe_data()

  assert (
    data[
      "integration_step"
    ].rule
    != ProofRule.GIVEN
  )


def test_phase66_probe_delta_nu_is_derived():
  data = build_phase66_probe_data()

  assert (
    data[
      "delta_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_probe_whitehead_nu_is_derived():
  data = build_phase66_probe_data()

  assert (
    data[
      "whitehead_nu_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_probe_delta_whitehead_is_derived():
  data = build_phase66_probe_data()

  assert (
    data[
      "delta_whitehead_step"
    ].rule
    == ProofRule.INFERENCE
  )


def test_phase66_probe_final_premises_are_expected():
  data = build_phase66_probe_data()

  assert (
    data[
      "integration_step"
    ].premises
    == (
      data[
        "delta_nu_step"
      ],
      data[
        "whitehead_nu_step"
      ],
      data[
        "delta_whitehead_step"
      ],
    )
  )


def test_phase66_probe_output_contains_final_result(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Toda Equation (5.8) result"
    in output
  )

  assert (
    "±(2ν₄-Eν′)"
    in output
  )

  assert (
    "±[ι₄,ι₄]"
    in output
  )


def test_phase66_probe_output_contains_phase65_upstream(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 65:"
    in output
  )

  assert (
    "π_7^4 = "
    "Z{ν₄} ⊕ Z/4{Eν′}"
    in output
  )


def test_phase66_probe_output_contains_phase60_upstream(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 60:"
    in output
  )

  assert (
    "[ι₄,ι₄] Whitehead "
    "correction data"
    in output
  )


def test_phase66_probe_output_contains_common_representative_flow(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "same positive representative:"
    in output
  )

  assert (
    "2ν₄-Eν′"
    in output
  )

  assert (
    "Δ(ι₉)=±[ι₄,ι₄]"
    in output
  )


def test_phase66_probe_output_contains_provenance(
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


def test_phase66_probe_output_contains_fixed_point(
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


def test_phase66_probe_output_contains_literature(
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
    "[Toda (5.8)]"
    in output
  )

  assert (
    "Locator: Equation (5.8)"
    in output
  )

  assert (
    "Author: H. Toda"
    in output
  )


def test_phase66_probe_output_contains_proof_record(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Proof record"
    in output
  )

  assert (
    "docs/proof_records.md"
    in output
  )

  assert (
    "Toda Equation (5.8)"
    in output
  )


def test_phase66_probe_does_not_claim_automatic_narrative(
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


def test_phase66_probe_output_contains_completion_boundary(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "Phase 66 completion boundary"
    in output
  )

  assert (
    "automatic proof narrative generation"
    in output
  )

  assert (
    "persistent Proof Repository"
    in output
  )


def test_phase66_probe_output_contains_proof_record_foundation(
  capsys,
):
  main()

  output = (
    capsys
    .readouterr()
    .out
  )

  assert (
    "docs/proof_records.md foundation"
    in output
  )
