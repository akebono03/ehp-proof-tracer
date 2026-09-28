from expression import (
  MapApplication,
)
from homotopy_groups import (
  FreeCyclicGroup,
)
from map_facts import (
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  Relation,
  RelationType,
)
from probes.probe_phase49_capabilities import (
  build_phase49_representative_result,
)
from toda_rules import (
  TodaPi32Eta2DefinitionStatement,
)


def build_phase55_3_dependency():
  phase49 = (
    build_phase49_representative_result()
  )

  assert len(
    phase49[
      "eta_2_definition_steps"
    ]
  ) == 1

  assert len(
    phase49[
      "hopf_relation_steps"
    ]
  ) == 1

  assert len(
    phase49[
      "final_group_steps"
    ]
  ) == 1

  eta_2_definition_step = (
    phase49[
      "eta_2_definition_steps"
    ][
      0
    ]
  )

  hopf_relation_step = (
    phase49[
      "hopf_relation_steps"
    ][
      0
    ]
  )

  pi3_2_group_step = (
    phase49[
      "final_group_steps"
    ][
      0
    ]
  )

  return {
    "phase49": phase49,
    "eta_2_definition_step": (
      eta_2_definition_step
    ),
    "hopf_relation_step": (
      hopf_relation_step
    ),
    "pi3_2_group_step": (
      pi3_2_group_step
    ),
  }


def test_phase55_3_phase49_dependency_derives_eta2_definition():
  dependency = (
    build_phase55_3_dependency()
  )

  step = dependency[
    "eta_2_definition_step"
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    TodaPi32Eta2DefinitionStatement,
  )

  assert (
    step.conclusion.element.name
    == "η₂"
  )

  assert (
    step.conclusion.image.name
    == "ι_3"
  )


def test_phase55_3_h_eta2_equals_iota3_is_derived():
  dependency = (
    build_phase55_3_dependency()
  )

  step = dependency[
    "hopf_relation_step"
  ]

  assert step.rule == (
    ProofRule.INFERENCE
  )

  assert isinstance(
    step.conclusion,
    Relation,
  )

  assert (
    step.conclusion.relation_type
    == RelationType.EQUALITY
  )

  assert isinstance(
    step.conclusion.lhs,
    MapApplication,
  )

  assert (
    step.conclusion.lhs.map
    == EHP_H_MAP
  )

  assert (
    step.conclusion.lhs.expression.name
    == "η₂"
  )

  assert (
    step.conclusion.rhs.name
    == "ι_3"
  )


def test_phase55_3_pi3_2_equals_free_eta2_is_derived():
  dependency = (
    build_phase55_3_dependency()
  )

  step = dependency[
    "pi3_2_group_step"
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
    relation.lhs
    == dependency[
      "phase49"
    ][
      "pi_3_2"
    ]
  )

  assert isinstance(
    relation.rhs,
    FreeCyclicGroup,
  )

  assert (
    relation.rhs.generator.name
    == "η₂"
  )


def test_phase55_3_hopf_relation_depends_on_derived_eta2_definition():
  dependency = (
    build_phase55_3_dependency()
  )

  eta_2_definition_step = (
    dependency[
      "eta_2_definition_step"
    ]
  )

  hopf_relation_step = (
    dependency[
      "hopf_relation_step"
    ]
  )

  assert (
    hopf_relation_step.premises
    == (
      eta_2_definition_step,
    )
  )

  assert (
    eta_2_definition_step.rule
    == ProofRule.INFERENCE
  )

  assert hopf_relation_step.inference_rule is not None

  assert (
    hopf_relation_step
    .inference_rule
    .name
    == (
      "Toda pi_3^2 eta_2 "
      "Hopf relation"
    )
  )


def test_phase55_3_pi3_2_group_result_uses_derived_eta2_definition():
  dependency = (
    build_phase55_3_dependency()
  )

  eta_2_definition_step = (
    dependency[
      "eta_2_definition_step"
    ]
  )

  pi3_2_group_step = (
    dependency[
      "pi3_2_group_step"
    ]
  )

  assert (
    eta_2_definition_step
    in pi3_2_group_step.premises
  )

  assert (
    eta_2_definition_step.rule
    == ProofRule.INFERENCE
  )

  assert pi3_2_group_step.inference_rule is not None

  assert (
    pi3_2_group_step
    .inference_rule
    .name
    == (
      "Toda pi_3^2 free cyclic "
      "generator transport"
    )
  )


def test_phase55_3_prop51_dependencies_are_not_given_premises():
  dependency = (
    build_phase55_3_dependency()
  )

  phase49 = dependency[
    "phase49"
  ]

  initial_conclusions = tuple(
    step.conclusion
    for step in phase49[
      "premise_steps"
    ]
  )

  assert (
    dependency[
      "hopf_relation_step"
    ].conclusion
    not in initial_conclusions
  )

  assert (
    dependency[
      "pi3_2_group_step"
    ].conclusion
    not in initial_conclusions
  )


def test_phase55_3_prop51_dependencies_preserve_inference_provenance():
  dependency = (
    build_phase55_3_dependency()
  )

  steps = (
    dependency[
      "pi3_2_group_step"
    ],
    dependency[
      "hopf_relation_step"
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


