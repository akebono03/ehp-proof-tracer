from expression import (
  HomotopyElement,
  MapSymbol,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from proof import (
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_renderer import (
  _render_group_proof_narrative_fact,
)
from toda_rules import (
  TodaPi32Eta2DefinitionStatement,
  TodaProp44IsomorphismStatement,
)


def _step(
  conclusion,
):
  return ProofStep(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )


def test_phase143_74b_homotopy_group_renders_as_pi_group():
  rendered = _render_group_proof_narrative_fact(
    _step(
      HomotopyGroup(
        group_dimension=14,
        sphere_dimension=7,
      )
    )
  )

  assert rendered == r"$\pi_{14}^{7}$"


def test_phase143_74b_ehp_exactness_window_renders_semantic_sequence():
  rendered = _render_group_proof_narrative_fact(
    _step(
      HomotopyEHPExactnessWindow(
        source_term=HomotopyGroup(15, 15),
        middle_term=HomotopyGroup(15, 8),
        target_term=HomotopyGroup(13, 7),
        first_map=MapSymbol("H"),
        second_map=MapSymbol("P"),
      )
    )
  )

  assert "HomotopyEHPExactnessWindow" not in rendered
  assert r"\xrightarrow{H}" in rendered
  assert r"\xrightarrow{P}" in rendered


def test_phase143_74b_eta2_definition_renders_hopf_relation():
  source = TodaPrimaryGroup(3, 2)
  target = TodaPrimaryGroup(3, 3)
  eta_2 = HomotopyElement(
    name="eta_2",
    dimension=3,
  )
  iota_3 = HomotopyElement(
    name="iota_3",
    dimension=3,
  )

  rendered = _render_group_proof_narrative_fact(
    _step(
      TodaPi32Eta2DefinitionStatement(
        map=TodaHopfInvariantMap(
          source_group=source,
          target_group=target,
        ),
        element=eta_2,
        image=iota_3,
      )
    )
  )

  assert "TodaPi32Eta2DefinitionStatement" not in rendered
  assert rendered.startswith("$H(")
  assert " = " in rendered


def test_phase143_74b_primary_membership_renders_semantic_membership():
  element = HomotopyElement(
    name="x",
    dimension=6,
  )

  rendered = _render_group_proof_narrative_fact(
    _step(
      TodaPrimaryGroupMembershipStatement(
        element=element,
        group=TodaPrimaryGroup(6, 4),
      )
    )
  )

  assert "TodaPrimaryGroupMembershipStatement" not in rendered
  assert r"\in \pi_{6}^{4}" in rendered


def test_phase143_74b_prop44_isomorphism_renders_decomposition_semantics():
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
  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(),
    ),
    target_group=TodaPrimaryGroup(7, 4),
    alpha=beta,
    beta=beta,
    gamma=gamma,
    formula=formula,
  )

  rendered = _render_group_proof_narrative_fact(
    _step(
      TodaProp44IsomorphismStatement(
        map=decomposition_map,
      )
    )
  )

  assert "TodaProp44IsomorphismStatement" not in rendered
  assert r"\mapsto" in rendered
  assert r"\text{は同型写像}" in rendered


def test_phase143_74b_suspension_isomorphism_renders_semantic_map():
  rendered = _render_group_proof_narrative_fact(
    _step(
      TodaSuspensionIsomorphismStatement(
        map=TodaSuspensionMap(
          source_group=TodaPrimaryGroup(6, 4),
          target_group=TodaPrimaryGroup(7, 5),
        )
      )
    )
  )

  assert (
    rendered
    == r"$E: \pi_{6}^{4} \xrightarrow{\cong} \pi_{7}^{5}$"
  )
