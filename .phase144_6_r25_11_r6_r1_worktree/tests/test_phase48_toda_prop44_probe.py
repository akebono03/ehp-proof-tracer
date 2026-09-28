from expression import (
  ScalarSymbol,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
)
from probes.probe_phase48_capabilities import (
  build_phase48_representative_result,
  decomposition_formula_text,
  decomposition_map_text,
  hopf_relation_text,
  injectivity_text,
  membership_text,
  restriction_text,
  suspension_map_text,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SuspensionInjectiveStatement,
)


def test_phase48_6_probe_formats_membership():
  representative = (
    build_phase48_representative_result()
  )

  assert membership_text(
    representative[
      "membership"
    ]
  ) == (
    "α ∈ π_{2n-1}^{n}"
  )


def test_phase48_6_probe_formats_hopf_relation():
  representative = (
    build_phase48_representative_result()
  )

  assert hopf_relation_text(
    representative[
      "hopf_relation"
    ]
  ) == (
    "H(α) = ι_(2n-1)"
  )


def test_phase48_6_probe_formats_decomposition_map():
  representative = (
    build_phase48_representative_result()
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


def test_phase48_6_probe_formats_decomposition_formula():
  representative = (
    build_phase48_representative_result()
  )

  assert decomposition_formula_text(
    representative[
      "decomposition_map"
    ]
  ) == (
    "Φ(β,γ) = "
    "Eβ + α∘γ"
  )


def test_phase48_6_probe_formats_suspension_map():
  representative = (
    build_phase48_representative_result()
  )

  assert suspension_map_text(
    representative[
      "suspension_map"
    ]
  ) == (
    "E: "
    "π_{i-1}^{n-1} → "
    "π_{i}^{n}"
  )


def test_phase48_6_probe_formats_first_summand_restriction():
  representative = (
    build_phase48_representative_result()
  )

  restriction_step = (
    representative[
      "restriction_steps"
    ][
      0
    ]
  )

  assert restriction_text(
    restriction_step.conclusion
  ) == (
    "Φ|_{π_{i-1}^{n-1}} = "
    "E: π_{i-1}^{n-1} → "
    "π_{i}^{n}"
  )


def test_phase48_6_probe_formats_injectivity_result():
  representative = (
    build_phase48_representative_result()
  )

  injectivity_step = (
    representative[
      "injectivity_steps"
    ][
      0
    ]
  )

  assert injectivity_text(
    injectivity_step.conclusion
  ) == (
    "E: "
    "π_{i-1}^{n-1} → "
    "π_{i}^{n} "
    "is injective"
  )


def test_phase48_6_representative_has_four_given_premises():
  representative = (
    build_phase48_representative_result()
  )

  assert len(
    representative[
      "premise_steps"
    ]
  ) == 4

  assert all(
    step.rule
    == ProofRule.GIVEN
    for step in representative[
      "premise_steps"
    ]
  )


def test_phase48_6_representative_derives_one_isomorphism():
  representative = (
    build_phase48_representative_result()
  )

  steps = representative[
    "isomorphism_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp44IsomorphismStatement,
  )


def test_phase48_6_representative_derives_one_restriction():
  representative = (
    build_phase48_representative_result()
  )

  steps = representative[
    "restriction_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp44FirstSummandRestrictionStatement,
  )


def test_phase48_6_representative_derives_one_injectivity():
  representative = (
    build_phase48_representative_result()
  )

  steps = representative[
    "injectivity_steps"
  ]

  assert len(
    steps
  ) == 1

  assert isinstance(
    steps[
      0
    ].conclusion,
    TodaProp44SuspensionInjectiveStatement,
  )


def test_phase48_6_isomorphism_preserves_phase47_premises():
  representative = (
    build_phase48_representative_result()
  )

  isomorphism_step = (
    representative[
      "isomorphism_steps"
    ][
      0
    ]
  )

  assert isomorphism_step.premises == (
    representative[
      "premise_steps"
    ][
      0
    ],
    representative[
      "premise_steps"
    ][
      1
    ],
    representative[
      "premise_steps"
    ][
      2
    ],
  )


def test_phase48_6_restriction_preserves_map_and_suspension_premises():
  representative = (
    build_phase48_representative_result()
  )

  restriction_step = (
    representative[
      "restriction_steps"
    ][
      0
    ]
  )

  assert restriction_step.premises == (
    representative[
      "premise_steps"
    ][
      2
    ],
    representative[
      "premise_steps"
    ][
      3
    ],
  )


def test_phase48_6_injectivity_uses_derived_isomorphism_and_restriction():
  representative = (
    build_phase48_representative_result()
  )

  injectivity_step = (
    representative[
      "injectivity_steps"
    ][
      0
    ]
  )

  assert injectivity_step.premises == (
    representative[
      "isomorphism_steps"
    ][
      0
    ],
    representative[
      "restriction_steps"
    ][
      0
    ],
  )


def test_phase48_6_all_derived_steps_are_inference_steps():
  representative = (
    build_phase48_representative_result()
  )

  derived_steps = (
    representative[
      "isomorphism_steps"
    ]
    + representative[
      "restriction_steps"
    ]
    + representative[
      "injectivity_steps"
    ]
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in derived_steps
  )


def test_phase48_6_injectivity_preserves_rule_provenance():
  representative = (
    build_phase48_representative_result()
  )

  injectivity_step = (
    representative[
      "injectivity_steps"
    ][
      0
    ]
  )

  assert (
    injectivity_step.inference_rule
    == representative[
      "injectivity_rule"
    ]
  )


def test_phase48_6_representative_reaches_fixed_point_in_two_rounds():
  representative = (
    build_phase48_representative_result()
  )

  result = representative[
    "result"
  ]

  assert (
    result.termination_reason
    == InferenceTerminationReason.FIXED_POINT
  )

  assert result.round_count == 2


def test_phase48_6_round_one_derives_isomorphism_and_restriction():
  representative = (
    build_phase48_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      0
    ].new_steps
  )

  assert len(
    new_steps
  ) == 2

  conclusions = tuple(
    step.conclusion
    for step in new_steps
  )

  assert any(
    isinstance(
      conclusion,
      TodaProp44IsomorphismStatement,
    )
    for conclusion in conclusions
  )

  assert any(
    isinstance(
      conclusion,
      TodaProp44FirstSummandRestrictionStatement,
    )
    for conclusion in conclusions
  )


def test_phase48_6_round_two_derives_injectivity():
  representative = (
    build_phase48_representative_result()
  )

  new_steps = (
    representative[
      "result"
    ].round_results[
      1
    ].new_steps
  )

  assert len(
    new_steps
  ) == 1

  assert isinstance(
    new_steps[
      0
    ].conclusion,
    TodaProp44SuspensionInjectiveStatement,
  )


def test_phase48_6_injectivity_retains_specific_source_and_target():
  representative = (
    build_phase48_representative_result()
  )

  statement = (
    representative[
      "injectivity_steps"
    ][
      0
    ].conclusion
  )

  assert statement.map.source_group == (
    representative[
      "first_summand"
    ]
  )

  assert statement.map.target_group == (
    representative[
      "target_group"
    ]
  )


def test_phase48_6_representative_supports_different_symbolic_instance():
  representative = (
    build_phase48_representative_result(
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

  assert suspension_map_text(
    representative[
      "suspension_map"
    ]
  ) == (
    "E: "
    "π_{j-1}^{m-1} → "
    "π_{j}^{m}"
  )

  assert injectivity_text(
    representative[
      "injectivity_steps"
    ][
      0
    ].conclusion
  ) == (
    "E: "
    "π_{j-1}^{m-1} → "
    "π_{j}^{m} "
    "is injective"
  )



