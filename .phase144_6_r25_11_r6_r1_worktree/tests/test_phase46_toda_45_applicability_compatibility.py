from typing import (
  get_type_hints,
)

from expression import (
  MapSymbol,
  ScalarProduct,
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from map_property_rules import (
  InjectiveMapStatement,
  IsomorphismStatement,
  isomorphism_implies_injective_inference_rule,
)
from proof import (
  InferenceTerminationReason,
  ProofRule,
  ProofStep,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
)


def build_phase46_5_data(
  n_name="n",
  k_name="k",
  m_name="m",
):
  n = ScalarSymbol(
    name=n_name,
  )

  k = ScalarSymbol(
    name=k_name,
  )

  m = ScalarSymbol(
    name=m_name,
  )

  stable_range = ScalarGreaterEqualStatement(
    left=n,
    right=ScalarSum(
      left=k,
      right=2,
    ),
  )

  suspension_range = ScalarGreaterEqualStatement(
    left=m,
    right=n,
  )

  suspension_map = TodaIteratedSuspensionMap(
    exponent=ScalarSum(
      left=m,
      right=ScalarProduct(
        left=-1,
        right=n,
      ),
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=n,
        right=k,
      ),
      sphere_dimension=n,
    ),
    target_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=m,
        right=k,
      ),
      sphere_dimension=m,
    ),
  )

  return {
    "n": n,
    "k": k,
    "m": m,
    "stable_range": stable_range,
    "suspension_range": suspension_range,
    "suspension_map": suspension_map,
  }


def build_phase46_5_steps(
  data,
):
  return (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )


def test_phase46_5_valid_instance_has_exactly_one_theorem_conclusion():
  data = build_phase46_5_data()

  steps = build_phase46_5_steps(
    data
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_isomorphism_inference_rule(),
      steps,
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda45IsomorphismStatement,
    )
  )

  assert len(
    derived
  ) == 1

  assert derived[
    0
  ].conclusion == (
    Toda45IsomorphismStatement(
      map=data[
        "suspension_map"
      ],
    )
  )


def test_phase46_5_valid_instance_preserves_full_provenance():
  data = build_phase46_5_data()

  steps = build_phase46_5_steps(
    data
  )

  rule = (
    toda_45_isomorphism_inference_rule()
  )

  result = (
    run_inference_until_stable_with_history(
      rule,
      steps,
    )
  )

  derived = next(
    step
    for step in result.steps
    if isinstance(
      step.conclusion,
      Toda45IsomorphismStatement,
    )
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.premises == steps

  assert (
    derived.inference_rule
    == rule
  )


def test_phase46_5_valid_instance_reaches_fixed_point_in_one_round():
  data = build_phase46_5_data()

  result = (
    run_inference_until_stable_with_history(
      toda_45_isomorphism_inference_rule(),
      build_phase46_5_steps(
        data
      ),
    )
  )

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


def test_phase46_5_rule_rejects_missing_stable_range_premise():
  data = build_phase46_5_data()

  steps = build_phase46_5_steps(
    data
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    (
      steps[
        1
      ],
      steps[
        2
      ],
    ),
  ) is None


def test_phase46_5_rule_rejects_missing_suspension_range_premise():
  data = build_phase46_5_data()

  steps = build_phase46_5_steps(
    data
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    (
      steps[
        0
      ],
      steps[
        2
      ],
    ),
  ) is None


def test_phase46_5_rule_rejects_missing_map_premise():
  data = build_phase46_5_data()

  steps = build_phase46_5_steps(
    data
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    (
      steps[
        0
      ],
      steps[
        1
      ],
    ),
  ) is None


def test_phase46_5_rule_rejects_stable_range_from_different_n_instance():
  data = build_phase46_5_data()

  other = build_phase46_5_data(
    n_name="q",
  )

  steps = (
    ProofStep(
      conclusion=other[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_5_rule_rejects_suspension_range_from_different_m_instance():
  data = build_phase46_5_data()

  other = build_phase46_5_data(
    m_name="q",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_5_rule_rejects_map_from_different_k_instance():
  data = build_phase46_5_data()

  other = build_phase46_5_data(
    k_name="j",
  )

  steps = (
    ProofStep(
      conclusion=data[
        "stable_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "suspension_range"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=other[
        "suspension_map"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    toda_45_isomorphism_inference_rule(),
    steps,
  ) is None


def test_phase46_5_different_toda_45_instances_remain_distinct():
  first = build_phase46_5_data()

  second = build_phase46_5_data(
    n_name="q",
    k_name="j",
    m_name="r",
  )

  first_statement = (
    Toda45IsomorphismStatement(
      map=first[
        "suspension_map"
      ],
    )
  )

  second_statement = (
    Toda45IsomorphismStatement(
      map=second[
        "suspension_map"
      ],
    )
  )

  assert (
    first_statement
    != second_statement
  )


def test_phase46_5_generic_isomorphism_statement_map_is_still_map_symbol():
  type_hints = get_type_hints(
    IsomorphismStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase46_5_generic_injective_statement_map_is_still_map_symbol():
  type_hints = get_type_hints(
    InjectiveMapStatement
  )

  assert type_hints[
    "map"
  ] is MapSymbol


def test_phase46_5_toda_iterated_suspension_map_is_not_map_symbol():
  data = build_phase46_5_data()

  assert not isinstance(
    data[
      "suspension_map"
    ],
    MapSymbol,
  )


def test_phase46_5_toda_theorem_statement_is_not_generic_isomorphism():
  data = build_phase46_5_data()

  statement = Toda45IsomorphismStatement(
    map=data[
      "suspension_map"
    ],
  )

  assert not isinstance(
    statement,
    IsomorphismStatement,
  )


def test_phase46_5_generic_isomorphism_rule_does_not_match_toda_theorem():
  data = build_phase46_5_data()

  theorem_step = ProofStep(
    conclusion=Toda45IsomorphismStatement(
      map=data[
        "suspension_map"
      ],
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  assert find_inference_match(
    isomorphism_implies_injective_inference_rule(),
    (
      theorem_step,
    ),
  ) is None


def test_phase46_5_no_generic_bridge_is_present_on_toda_statement():
  data = build_phase46_5_data()

  statement = Toda45IsomorphismStatement(
    map=data[
      "suspension_map"
    ],
  )

  assert not hasattr(
    statement,
    "generic_map",
  )

  assert not hasattr(
    statement,
    "generic_isomorphism",
  )

  assert not hasattr(
    statement,
    "injective",
  )
