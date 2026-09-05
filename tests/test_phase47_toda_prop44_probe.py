from expression import (
  ScalarSymbol,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase47_capabilities import (
  build_phase47_representative_result,
  decomposition_formula_text,
  decomposition_map_text,
  hopf_relation_text,
  membership_text,
  theorem_text,
)
from toda_rules import (
  TodaProp44IsomorphismStatement,
)


def test_phase47_6_probe_formats_membership_premise():
  representative = (
    build_phase47_representative_result()
  )

  assert membership_text(
    representative[
      "membership"
    ]
  ) == (
    "α ∈ π_{2n-1}^{n}"
  )


def test_phase47_6_probe_formats_hopf_premise():
  representative = (
    build_phase47_representative_result()
  )

  assert hopf_relation_text(
    representative[
      "hopf_relation"
    ]
  ) == (
    "H(α) = ι_(2n-1)"
  )


def test_phase47_6_probe_formats_decomposition_map():
  representative = (
    build_phase47_representative_result()
  )

  assert decomposition_map_text(
    representative[
      "decomposition_map"
    ]
  ) == (
    "Φ: "
    "π_{i-1}^{n-1} ⊕ "
    "π_{i}^{2n-1} → "
    "π_{i}^{n}"
  )


def test_phase47_6_probe_formats_decomposition_formula():
  representative = (
    build_phase47_representative_result()
  )

  assert decomposition_formula_text(
    representative[
      "decomposition_map"
    ]
  ) == (
    "Φ(β,γ) = "
    "Eβ + α∘γ"
  )


def test_phase47_6_probe_formats_theorem_result():
  representative = (
    build_phase47_representative_result()
  )

  theorem_step = (
    representative[
      "theorem_steps"
    ][
      0
    ]
  )

  assert theorem_text(
    theorem_step.conclusion
  ) == (
    "Φ: "
    "π_{i-1}^{n-1} ⊕ "
    "π_{i}^{2n-1} → "
    "π_{i}^{n} "
    "is isomorphism"
  )


def test_phase47_6_representative_has_exactly_one_theorem_step():
  representative = (
    build_phase47_representative_result()
  )

  theorem_steps = representative[
    "theorem_steps"
  ]

  assert len(
    theorem_steps
  ) == 1

  assert isinstance(
    theorem_steps[
      0
    ].conclusion,
    TodaProp44IsomorphismStatement,
  )


def test_phase47_6_representative_preserves_all_three_premises():
  representative = (
    build_phase47_representative_result()
  )

  theorem_step = (
    representative[
      "theorem_steps"
    ][
      0
    ]
  )

  assert theorem_step.premises == (
    representative[
      "premise_steps"
    ]
  )


def test_phase47_6_representative_preserves_inference_rule_provenance():
  representative = (
    build_phase47_representative_result()
  )

  theorem_step = (
    representative[
      "theorem_steps"
    ][
      0
    ]
  )

  assert theorem_step.rule == (
    ProofRule.INFERENCE
  )

  assert (
    theorem_step.inference_rule
    == representative[
      "theorem_rule"
    ]
  )


def test_phase47_6_representative_reaches_fixed_point_in_one_round():
  representative = (
    build_phase47_representative_result()
  )

  result = representative[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 1

  assert len(
    result.round_results[
      0
    ].new_steps
  ) == 1


def test_phase47_6_representative_supports_different_symbolic_instance():
  representative = (
    build_phase47_representative_result(
      i=ScalarSymbol(
        name="j",
      ),
      n=ScalarSymbol(
        name="m",
      ),
    )
  )

  assert membership_text(
    representative[
      "membership"
    ]
  ) == (
    "α ∈ π_{2m-1}^{m}"
  )

  assert decomposition_map_text(
    representative[
      "decomposition_map"
    ]
  ) == (
    "Φ: "
    "π_{j-1}^{m-1} ⊕ "
    "π_{j}^{2m-1} → "
    "π_{j}^{m}"
  )


def test_phase47_6_representative_does_not_create_generic_isomorphism():
  representative = (
    build_phase47_representative_result()
  )

  theorem_statement = (
    representative[
      "theorem_steps"
    ][
      0
    ].conclusion
  )

  assert not hasattr(
    theorem_statement,
    "generic_isomorphism",
  )

  assert not hasattr(
    theorem_statement,
    "injective",
  )


def test_phase47_6_representative_does_not_create_e_injectivity():
  representative = (
    build_phase47_representative_result()
  )

  theorem_statement = (
    representative[
      "theorem_steps"
    ][
      0
    ].conclusion
  )

  assert not hasattr(
    theorem_statement,
    "e_injective",
  )

  assert not hasattr(
    theorem_statement,
    "suspension_injective",
  )


