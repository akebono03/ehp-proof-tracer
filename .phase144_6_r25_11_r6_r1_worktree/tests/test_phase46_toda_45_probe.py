from expression import (
  ScalarSymbol,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase46_capabilities import (
  build_phase46_representative_result,
  inequality_text,
  suspension_map_text,
  theorem_text,
)
from toda_rules import (
  Toda45IsomorphismStatement,
)


def test_phase46_6_probe_formats_stable_range_premise():
  representative = (
    build_phase46_representative_result()
  )

  assert inequality_text(
    representative[
      "stable_range"
    ]
  ) == "n ≥ k+2"


def test_phase46_6_probe_formats_suspension_range_premise():
  representative = (
    build_phase46_representative_result()
  )

  assert inequality_text(
    representative[
      "suspension_range"
    ]
  ) == "m ≥ n"


def test_phase46_6_probe_formats_iterated_suspension_map():
  representative = (
    build_phase46_representative_result()
  )

  assert suspension_map_text(
    representative[
      "suspension_map"
    ]
  ) == (
    "E^(m-n): "
    "π_{n+k}^{n} → "
    "π_{m+k}^{m}"
  )


def test_phase46_6_probe_formats_theorem_result():
  representative = (
    build_phase46_representative_result()
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
    "E^(m-n): "
    "π_{n+k}^{n} → "
    "π_{m+k}^{m} "
    "is isomorphism"
  )


def test_phase46_6_representative_has_exactly_one_theorem_step():
  representative = (
    build_phase46_representative_result()
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
    Toda45IsomorphismStatement,
  )


def test_phase46_6_representative_preserves_all_three_premises():
  representative = (
    build_phase46_representative_result()
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


def test_phase46_6_representative_preserves_inference_rule_provenance():
  representative = (
    build_phase46_representative_result()
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


def test_phase46_6_representative_reaches_fixed_point_in_one_round():
  representative = (
    build_phase46_representative_result()
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


def test_phase46_6_representative_supports_different_symbolic_instance():
  representative = (
    build_phase46_representative_result(
      n=ScalarSymbol(
        name="q",
      ),
      k=ScalarSymbol(
        name="j",
      ),
      m=ScalarSymbol(
        name="r",
      ),
    )
  )

  assert inequality_text(
    representative[
      "stable_range"
    ]
  ) == "q ≥ j+2"

  assert inequality_text(
    representative[
      "suspension_range"
    ]
  ) == "r ≥ q"

  assert suspension_map_text(
    representative[
      "suspension_map"
    ]
  ) == (
    "E^(r-q): "
    "π_{q+j}^{q} → "
    "π_{r+j}^{r}"
  )


def test_phase46_6_representative_does_not_create_generic_isomorphism():
  representative = (
    build_phase46_representative_result()
  )

  conclusions = tuple(
    step.conclusion
    for step in representative[
      "result"
    ].steps
  )

  theorem_statement = (
    representative[
      "theorem_steps"
    ][
      0
    ].conclusion
  )

  assert theorem_statement in (
    conclusions
  )

  assert not hasattr(
    theorem_statement,
    "generic_isomorphism",
  )
