from expression import (
  HomotopyElement,
  Sum,
  Suspension,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaPrimaryGroup,
  TodaProp44DecompositionMap,
  TodaSuspensionMap,
)
from test_phase48_toda_prop44_first_summand_restriction import (
  build_phase48_3_data,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaProp44FirstSummandRestrictionStatement,
)


def test_phase143_75af_renders_first_summand_restriction():
  data = build_phase48_3_data()

  statement = TodaProp44FirstSummandRestrictionStatement(
    decomposition_map=data["decomposition_map"],
    suspension_map=data["suspension_map"],
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert rendered is not None
  assert r"\left." in rendered
  assert r"\right|_{" in rendered
  assert r"E: " in rendered
  assert r"\text{ is injective}" not in rendered
  assert r"\text{ is an isomorphism}" not in rendered


def test_phase143_75af_uses_first_class_formula_and_maps():
  first = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )
  second = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=9,
  )
  target = TodaPrimaryGroup(
    group_dimension=12,
    sphere_dimension=6,
  )
  beta = HomotopyElement(
    name="β",
    dimension=11,
  )
  delta = HomotopyElement(
    name="δ",
    dimension=12,
  )
  formula = Sum(
    left=Suspension(
      expression=beta,
    ),
    right=delta,
  )

  decomposition_map = TodaProp44DecompositionMap(
    source_group=DirectSumGroup(
      summands=(
        first,
        second,
      )
    ),
    target_group=target,
    alpha=delta,
    beta=beta,
    gamma=delta,
    formula=formula,
  )
  suspension_map = TodaSuspensionMap(
    source_group=first,
    target_group=target,
  )

  statement = TodaProp44FirstSummandRestrictionStatement(
    decomposition_map=decomposition_map,
    suspension_map=suspension_map,
  )

  assert render_toda_proof_statement_latex(
    statement
  ) == (
    r"\left.\left(Eβ + δ\right)"
    r"\right|_{\pi_{11}^{5}}"
    r" = E: \pi_{11}^{5} \to \pi_{12}^{6}"
  )


def test_phase143_75af_does_not_render_rule_name():
  data = build_phase48_3_data()

  statement = TodaProp44FirstSummandRestrictionStatement(
    decomposition_map=data["decomposition_map"],
    suspension_map=data["suspension_map"],
  )

  rendered = render_toda_proof_statement_latex(
    statement
  )

  assert rendered is not None
  assert "Toda Proposition" not in rendered
  assert "4.4" not in rendered
