from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from probes.probe_phase52_capabilities import (
  build_phase52_representative_result,
)
from probes.probe_phase54_capabilities import (
  build_phase54_representative_result,
)
from toda_rules import (
  TodaDeltaImageUpToSignStatement,
)


def build_phase55_4_dependency():
  phase52 = (
    build_phase52_representative_result()
  )

  phase54 = (
    build_phase54_representative_result()
  )

  assert len(
    phase52[
      "delta_two_eta_2_steps"
    ]
  ) == 1

  assert len(
    phase54[
      "final_steps"
    ]
  ) == 1

  delta_iota5_step = (
    phase52[
      "delta_two_eta_2_steps"
    ][
      0
    ]
  )

  higher_eta_group_step = (
    phase54[
      "final_steps"
    ][
      0
    ]
  )

  return {
    "phase52": phase52,
    "phase54": phase54,
    "delta_iota5_step": (
      delta_iota5_step
    ),
    "higher_eta_group_step": (
      higher_eta_group_step
    ),
  }


def test_phase55_4_delta_iota5_two_eta2_is_derived():
  dependency = (
    build_phase55_4_dependency()
  )

  step = dependency[
    "delta_iota5_step"
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaDeltaImageUpToSignStatement,
  )

  assert (
    step.conclusion.positive_value
    == dependency[
      "phase52"
    ][
      "two_eta_2"
    ]
  )


def test_phase55_4_delta_iota5_preserves_phase52_provenance():
  dependency = (
    build_phase55_4_dependency()
  )

  step = dependency[
    "delta_iota5_step"
  ]

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda Delta iota_5 "
      "twice eta_2 up-to-sign bridge"
    )
  )

  assert len(
    step.premises
  ) == 2

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )


def test_phase55_4_higher_eta_group_is_derived():
  dependency = (
    build_phase55_4_dependency()
  )

  step = dependency[
    "higher_eta_group_step"
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  relation = step.conclusion

  assert isinstance(
    relation,
    Relation,
  )

  assert (
    relation.relation_type
    == RelationType.EQUALITY
  )

  assert (
    relation
    == dependency[
      "phase54"
    ][
      "final_relation"
    ]
  )


def test_phase55_4_higher_eta_group_has_expected_finite_cyclic_structure():
  dependency = (
    build_phase55_4_dependency()
  )

  relation = (
    dependency[
      "higher_eta_group_step"
    ].conclusion
  )

  assert isinstance(
    relation.rhs,
    FiniteCyclicGroup,
  )

  assert relation.rhs.order == 2

  assert (
    relation.rhs.generator
    == dependency[
      "phase54"
    ][
      "eta_n_definition"
    ].element
  )


def test_phase55_4_higher_eta_group_preserves_phase54_provenance():
  dependency = (
    build_phase55_4_dependency()
  )

  step = dependency[
    "higher_eta_group_step"
  ]

  assert step.inference_rule is not None

  assert (
    step.inference_rule.name
    == (
      "Toda higher eta-family "
      "finite-cyclic generator bridge"
    )
  )

  assert len(
    step.premises
  ) == 2

  assert all(
    premise.rule
    == ProofRule.INFERENCE
    for premise in step.premises
  )

  assert (
    dependency[
      "phase54"
    ][
      "transported_steps"
    ][
      0
    ]
    in step.premises
  )

  assert (
    dependency[
      "phase54"
    ][
      "higher_eta_steps"
    ][
      0
    ]
    in step.premises
  )


def test_phase55_4_prop51_dependencies_are_not_given_premises():
  dependency = (
    build_phase55_4_dependency()
  )

  phase52_initial_conclusions = tuple(
    step.conclusion
    for step in dependency[
      "phase52"
    ][
      "premise_steps"
    ]
  )

  phase54_initial_conclusions = tuple(
    step.conclusion
    for step in dependency[
      "phase54"
    ][
      "premise_steps"
    ]
  )

  assert (
    dependency[
      "delta_iota5_step"
    ].conclusion
    not in phase52_initial_conclusions
  )

  assert (
    dependency[
      "higher_eta_group_step"
    ].conclusion
    not in phase54_initial_conclusions
  )


def test_phase55_4_prop51_dependencies_preserve_inference_provenance():
  dependency = (
    build_phase55_4_dependency()
  )

  steps = (
    dependency[
      "delta_iota5_step"
    ],
    dependency[
      "higher_eta_group_step"
    ],
  )

  assert all(
    step.rule
    == ProofRule.INFERENCE
    for step in steps
  )

  assert all(
    step.inference_rule
    is not None
    for step in steps
  )


