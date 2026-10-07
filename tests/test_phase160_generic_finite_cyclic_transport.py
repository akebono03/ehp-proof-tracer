from expression import (
  GeneratorSymbol,
  HomotopyElement,
  IteratedSuspension,
  ScalarSum,
)
from homotopy_groups import (
  FiniteCyclicGroup,
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
from toda_stable_group_transport import (
  toda_45_generic_finite_cyclic_transport_inference_rule,
)
from toda_stable_transport import (
  build_canonical_toda_45_isomorphism_step,
)


def _pi4_3_source_step():
  eta_3 = HomotopyElement(
    name="η₃",
    dimension=3,
    source=4,
    target=3,
    generator=GeneratorSymbol(
      family="η",
      index=3,
    ),
  )

  return ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=4,
        sphere_dimension=3,
      ),
      rhs=FiniteCyclicGroup(
        order=2,
        generator=eta_3,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )


def _pi16_9_source_step():
  sigma_9 = HomotopyElement(
    name="σ₉",
    dimension=9,
    source=16,
    target=9,
    generator=GeneratorSymbol(
      family="σ",
      index=9,
    ),
  )

  return ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
      rhs=FiniteCyclicGroup(
        order=16,
        generator=sigma_9,
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )


def test_phase160_r4_generic_rule_matches_pi4_3_canonical_transport():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  source_step = (
    _pi4_3_source_step()
  )
  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  assert find_inference_match(
    toda_45_generic_finite_cyclic_transport_inference_rule(),
    (
      source_step,
      isomorphism_step,
    ),
  ) is not None


def test_phase160_r4_pi4_3_transport_preserves_order_two():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  source_step = (
    _pi4_3_source_step()
  )
  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_generic_finite_cyclic_transport_inference_rule(),
      (
        source_step,
        isomorphism_step,
      ),
    )
  )

  expected = Relation(
    lhs=(
      isomorphism_step
      .conclusion
      .map
      .target_group
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=IteratedSuspension(
        expression=(
          source_step
          .conclusion
          .rhs
          .generator
        ),
        exponent=(
          isomorphism_step
          .conclusion
          .map
          .exponent
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  derived = next(
    step
    for step in result.steps
    if step.conclusion == expected
  )

  assert derived.rule == (
    ProofRule.INFERENCE
  )

  assert derived.premises == (
    source_step,
    isomorphism_step,
  )


def test_phase160_r4_pi4_3_transport_does_not_normalize_eta_generator():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  source_step = (
    _pi4_3_source_step()
  )
  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_generic_finite_cyclic_transport_inference_rule(),
      (
        source_step,
        isomorphism_step,
      ),
    )
  )

  derived = next(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and isinstance(
        step.conclusion.rhs,
        FiniteCyclicGroup,
      )
      and step.conclusion.lhs
      == (
        isomorphism_step
        .conclusion
        .map
        .target_group
      )
    )
  )

  assert isinstance(
    derived.conclusion.rhs.generator,
    IteratedSuspension,
  )

  assert (
    derived.conclusion.rhs.generator.expression
    == source_step.conclusion.rhs.generator
  )


def test_phase160_r4_generic_rule_matches_pi16_9_canonical_transport():
  target = TodaPrimaryGroup(
    group_dimension=17,
    sphere_dimension=10,
  )

  source_step = (
    _pi16_9_source_step()
  )
  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  assert find_inference_match(
    toda_45_generic_finite_cyclic_transport_inference_rule(),
    (
      source_step,
      isomorphism_step,
    ),
  ) is not None


def test_phase160_r4_pi16_9_transport_preserves_order_sixteen():
  target = TodaPrimaryGroup(
    group_dimension=17,
    sphere_dimension=10,
  )

  source_step = (
    _pi16_9_source_step()
  )
  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_generic_finite_cyclic_transport_inference_rule(),
      (
        source_step,
        isomorphism_step,
      ),
    )
  )

  expected = Relation(
    lhs=(
      isomorphism_step
      .conclusion
      .map
      .target_group
    ),
    rhs=FiniteCyclicGroup(
      order=16,
      generator=IteratedSuspension(
        expression=(
          source_step
          .conclusion
          .rhs
          .generator
        ),
        exponent=(
          isomorphism_step
          .conclusion
          .map
          .exponent
        ),
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert expected in tuple(
    step.conclusion
    for step in result.steps
  )


def test_phase160_r4_pi16_9_transport_does_not_normalize_sigma_generator():
  target = TodaPrimaryGroup(
    group_dimension=17,
    sphere_dimension=10,
  )

  source_step = (
    _pi16_9_source_step()
  )
  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_generic_finite_cyclic_transport_inference_rule(),
      (
        source_step,
        isomorphism_step,
      ),
    )
  )

  target_group = (
    isomorphism_step
    .conclusion
    .map
    .target_group
  )

  derived = next(
    step
    for step in result.steps
    if (
      isinstance(
        step.conclusion,
        Relation,
      )
      and step.conclusion.lhs
      == target_group
    )
  )

  assert isinstance(
    derived.conclusion.rhs.generator,
    IteratedSuspension,
  )

  assert (
    derived.conclusion.rhs.generator.expression
    == source_step.conclusion.rhs.generator
  )


def test_phase160_r4_rejects_source_group_from_different_stem():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  wrong_source = ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=16,
        sphere_dimension=9,
      ),
      rhs=FiniteCyclicGroup(
        order=16,
        generator=HomotopyElement(
          name="σ₉",
          dimension=9,
          source=16,
          target=9,
          generator=GeneratorSymbol(
            family="σ",
            index=9,
          ),
        ),
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  assert find_inference_match(
    toda_45_generic_finite_cyclic_transport_inference_rule(),
    (
      wrong_source,
      isomorphism_step,
    ),
  ) is None


def test_phase160_r4_accepts_structural_source_relation():
  target = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=4,
  )

  concrete_source = (
    _pi4_3_source_step()
  )

  structural_source = ProofStep(
    conclusion=Relation(
      lhs=TodaPrimaryGroup(
        group_dimension=ScalarSum(
          left=3,
          right=1,
        ),
        sphere_dimension=3,
      ),
      rhs=(
        concrete_source
        .conclusion
        .rhs
      ),
      relation_type=RelationType.EQUALITY,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  isomorphism_step = (
    build_canonical_toda_45_isomorphism_step(
      target
    )
  )

  assert find_inference_match(
    toda_45_generic_finite_cyclic_transport_inference_rule(),
    (
      structural_source,
      isomorphism_step,
    ),
  ) is not None
