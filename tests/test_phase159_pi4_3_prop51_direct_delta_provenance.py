from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  FreeCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  Relation,
  RelationType,
  find_inference_match,
  run_inference_until_stable_with_history,
)
from toda_delta_image_rules import (
  free_cyclic_generator_delta_image_inference_rule,
)
from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaImageUpToSignStatement,
)
from toda_upstream_bootstrap import (
  _build_phase50_result,
)


def _build_direct_delta_data():
  pi_5_5 = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=5,
  )
  pi_3_2 = TodaPrimaryGroup(
    group_dimension=3,
    sphere_dimension=2,
  )
  iota_5 = HomotopyElement(
    name="ι_5",
    dimension=5,
    generator=GeneratorSymbol(
      family="ι",
      index=5,
    ),
  )
  eta_2 = HomotopyElement(
    name="η₂",
    dimension=2,
    source=3,
    target=2,
    generator=GeneratorSymbol(
      family="η",
      index=2,
    ),
  )
  two_eta_2 = Multiple(
    coefficient=2,
    expression=eta_2,
  )
  delta_map = TodaDeltaMap(
    source_group=pi_5_5,
    target_group=pi_3_2,
  )
  source_relation = Relation(
    lhs=pi_5_5,
    rhs=FreeCyclicGroup(
      generator=iota_5,
    ),
    relation_type=(
      RelationType.EQUALITY
    ),
  )
  delta_relation = (
    TodaDeltaImageUpToSignStatement(
      map=delta_map,
      element=iota_5,
      positive_value=two_eta_2,
    )
  )
  expected_image = (
    TodaDeltaImageFreeCyclicStatement(
      map=delta_map,
      image_group=FreeCyclicGroup(
        generator=two_eta_2,
      ),
    )
  )

  return {
    "pi_5_5": pi_5_5,
    "pi_3_2": pi_3_2,
    "iota_5": iota_5,
    "eta_2": eta_2,
    "two_eta_2": two_eta_2,
    "delta_map": delta_map,
    "source_relation": source_relation,
    "delta_relation": delta_relation,
    "expected_image": expected_image,
  }


def test_phase159_repair1_generic_direct_delta_image_rule_matches():
  data = _build_direct_delta_data()

  steps = (
    ProofStep(
      conclusion=data[
        "source_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    free_cyclic_generator_delta_image_inference_rule(),
    steps,
  ) is not None


def test_phase159_repair1_generic_direct_delta_image_rule_derives_image():
  data = _build_direct_delta_data()

  source_step = ProofStep(
    conclusion=data[
      "source_relation"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )
  delta_step = ProofStep(
    conclusion=data[
      "delta_relation"
    ],
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      free_cyclic_generator_delta_image_inference_rule(),
      (
        source_step,
        delta_step,
      ),
    )
  )

  derived = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == data[
        "expected_image"
      ]
    )
  )

  assert len(derived) == 1
  assert derived[0].premises == (
    source_step,
    delta_step,
  )


def test_phase159_repair1_generic_direct_delta_image_rule_rejects_wrong_generator():
  data = _build_direct_delta_data()

  wrong_generator = HomotopyElement(
    name="x",
    dimension=5,
    generator=GeneratorSymbol(
      family="x",
      index=5,
    ),
  )

  wrong_source_relation = Relation(
    lhs=data[
      "pi_5_5"
    ],
    rhs=FreeCyclicGroup(
      generator=wrong_generator,
    ),
    relation_type=(
      RelationType.EQUALITY
    ),
  )

  steps = (
    ProofStep(
      conclusion=wrong_source_relation,
      premises=(),
      rule=ProofRule.GIVEN,
    ),
    ProofStep(
      conclusion=data[
        "delta_relation"
      ],
      premises=(),
      rule=ProofRule.GIVEN,
    ),
  )

  assert find_inference_match(
    free_cyclic_generator_delta_image_inference_rule(),
    steps,
  ) is None


def test_phase159_repair1_phase50_image_uses_prop51_direct_delta_statement():
  phase50 = _build_phase50_result()

  image_steps = tuple(
    step
    for step in phase50[
      "result"
    ].steps
    if isinstance(
      step.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )

  assert len(image_steps) == 1

  image_step = image_steps[0]

  direct_delta_premises = tuple(
    premise
    for premise in image_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaImageUpToSignStatement,
    )
  )

  assert len(
    direct_delta_premises
  ) == 1

  direct_delta_step = (
    direct_delta_premises[0]
  )

  assert (
    direct_delta_step
    .inference_rule
    is not None
  )
  assert (
    direct_delta_step
    .inference_rule
    .literature_reference
    is not None
  )
  assert (
    direct_delta_step
    .inference_rule
    .literature_reference
    .locator
    == "Proposition 5.1"
  )

  positive_value = (
    direct_delta_step
    .conclusion
    .positive_value
  )

  assert isinstance(
    positive_value,
    Multiple,
  )
  assert positive_value.coefficient == 2
  assert (
    positive_value
    .expression
    .generator
    == GeneratorSymbol(
      family="η",
      index=2,
    )
  )


def test_phase159_repair1_final_step_ancestry_contains_prop51_direct_delta():
  phase50 = _build_phase50_result()

  pending = [
    phase50[
      "final_group_step"
    ]
  ]
  seen = set()
  ancestry = []

  while pending:
    step = pending.pop()
    step_id = id(step)

    if step_id in seen:
      continue

    seen.add(step_id)
    ancestry.append(step)
    pending.extend(
      step.premises
    )

  direct_delta_steps = tuple(
    step
    for step in ancestry
    if (
      isinstance(
        step.conclusion,
        TodaDeltaImageUpToSignStatement,
      )
      and (
        step.inference_rule
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        is not None
      )
      and (
        step.inference_rule
        .literature_reference
        .locator
        == "Proposition 5.1"
      )
    )
  )

  assert len(
    direct_delta_steps
  ) == 1
