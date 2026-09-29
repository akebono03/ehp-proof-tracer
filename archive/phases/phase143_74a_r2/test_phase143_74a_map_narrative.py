from expression import (
  HomotopyElement,
  ScalarSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaDeltaMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from proof import (
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)


def _step(
  conclusion,
):
  return ProofStep(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )


def test_phase143_74a_suspension_map_renders_semantic_map():
  source = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=4,
  )
  target = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )

  assert (
    _render_group_proof_narrative_fact(
      _step(
        TodaSuspensionMap(
          source_group=source,
          target_group=target,
        )
      )
    )
    == r"$E: \pi_{6}^{4} \to \pi_{7}^{5}$"
  )


def test_phase143_74a_iterated_suspension_map_renders_symbolic_exponent():
  n = ScalarSymbol(
    name="n",
  )
  source = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )
  target = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=6,
  )

  assert (
    _render_group_proof_narrative_fact(
      _step(
        TodaIteratedSuspensionMap(
          exponent=n,
          source_group=source,
          target_group=target,
        )
      )
    )
    == r"$E^{n}: \pi_{6}^{3} \to \pi_{9}^{6}$"
  )


def test_phase143_74a_delta_map_renders_semantic_map():
  source = TodaPrimaryGroup(
    group_dimension=9,
    sphere_dimension=9,
  )
  target = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=4,
  )

  assert (
    _render_group_proof_narrative_fact(
      _step(
        TodaDeltaMap(
          source_group=source,
          target_group=target,
        )
      )
    )
    == r"$\Delta: \pi_{9}^{9} \to \pi_{7}^{4}$"
  )


def test_phase143_74a_prop44_decomposition_map_renders_formula():
  beta = HomotopyElement(
    name="beta",
    dimension=6,
  )
  gamma = HomotopyElement(
    name="gamma",
    dimension=6,
  )
  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=gamma,
  )

  decomposition_map = (
    TodaProp44DecompositionMap(
      source_group=DirectSumGroup(
        summands=(),
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=7,
        sphere_dimension=4,
      ),
      alpha=beta,
      beta=beta,
      gamma=gamma,
      formula=formula,
    )
  )

  rendered = (
    _render_group_proof_narrative_fact(
      _step(
        decomposition_map
      )
    )
  )

  assert (
    "TodaProp44DecompositionMap"
    not in rendered
  )
  assert r"\mapsto" in rendered
