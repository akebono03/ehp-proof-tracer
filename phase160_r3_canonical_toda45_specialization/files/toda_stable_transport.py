from expression import (
  ScalarProduct,
  ScalarSum,
)
from homotopy_groups import (
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
)
from proof import (
  ProofRule,
  ProofStep,
  run_inference_until_stable_with_history,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from stable_rules import (
  canonical_toda_stable_base,
  toda_primary_group_stem,
  toda_stable_transport_exponent,
)
from toda_rules import (
  Toda45IsomorphismStatement,
  toda_45_isomorphism_inference_rule,
)


def build_canonical_toda_stable_transport_map(
  target: TodaPrimaryGroup,
) -> TodaIteratedSuspensionMap:
  toda_stable_transport_exponent(
    target
  )

  stem = toda_primary_group_stem(
    target
  )
  base = canonical_toda_stable_base(
    target
  )

  base_sphere_dimension = (
    base.sphere_dimension
  )
  target_sphere_dimension = (
    target.sphere_dimension
  )

  return TodaIteratedSuspensionMap(
    exponent=ScalarSum(
      left=target_sphere_dimension,
      right=ScalarProduct(
        left=-1,
        right=base_sphere_dimension,
      ),
    ),
    source_group=TodaPrimaryGroup(
      group_dimension=ScalarSum(
        left=base_sphere_dimension,
        right=stem,
      ),
      sphere_dimension=base_sphere_dimension,
    ),
    target_group=target,
  )


def build_canonical_toda_45_isomorphism_step(
  target: TodaPrimaryGroup,
) -> ProofStep:
  stem = toda_primary_group_stem(
    target
  )
  base = canonical_toda_stable_base(
    target
  )
  transport_map = (
    build_canonical_toda_stable_transport_map(
      target
    )
  )

  base_sphere_dimension = (
    base.sphere_dimension
  )
  target_sphere_dimension = (
    target.sphere_dimension
  )

  stable_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=base_sphere_dimension,
      right=ScalarSum(
        left=stem,
        right=2,
      ),
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_range_step = ProofStep(
    conclusion=ScalarGreaterEqualStatement(
      left=target_sphere_dimension,
      right=base_sphere_dimension,
    ),
    premises=(),
    rule=ProofRule.GIVEN,
  )

  suspension_map_step = ProofStep(
    conclusion=transport_map,
    premises=(),
    rule=ProofRule.GIVEN,
  )

  result = (
    run_inference_until_stable_with_history(
      toda_45_isomorphism_inference_rule(),
      (
        stable_range_step,
        suspension_range_step,
        suspension_map_step,
      ),
    )
  )

  matches = tuple(
    step
    for step in result.steps
    if (
      step.conclusion
      == Toda45IsomorphismStatement(
        map=transport_map,
      )
    )
  )

  if len(matches) != 1:
    raise ValueError(
      "expected exactly one canonical "
      "Toda (4.5) isomorphism step"
    )

  return matches[0]
