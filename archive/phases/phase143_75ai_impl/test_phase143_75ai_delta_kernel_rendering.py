from expression import (
  GeneratorSymbol,
  HomotopyElement,
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaDeltaMap,
  TodaPrimaryGroup,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)
from toda_rules import (
  TodaProp59DeltaKernelStatement,
)


def build_statement(
  source_dimension=8,
  source_sphere=5,
  target_dimension=6,
  target_sphere=2,
  order=2,
  coefficient=4,
):
  nu_5 = HomotopyElement(
    name="ν_5",
    dimension=5,
    source=8,
    target=5,
    generator=GeneratorSymbol(
      family="ν",
      index=5,
    ),
  )

  return TodaProp59DeltaKernelStatement(
    map=TodaDeltaMap(
      source_group=TodaPrimaryGroup(
        group_dimension=source_dimension,
        sphere_dimension=source_sphere,
      ),
      target_group=TodaPrimaryGroup(
        group_dimension=target_dimension,
        sphere_dimension=target_sphere,
      ),
    ),
    kernel_group=FiniteCyclicGroup(
      order=order,
      generator=Multiple(
        coefficient=coefficient,
        expression=nu_5,
      ),
    ),
  )


def test_phase143_75ai_renders_canonical_kernel_statement():
  assert render_toda_proof_statement_latex(
    build_statement()
  ) == (
    r"\ker\left("
    r"\Delta: \pi_{8}^{5} \to \pi_{6}^{2}"
    r"\right)"
    r" = \mathbb{Z}/2\{4\nu_{5}\}"
  )


def test_phase143_75ai_uses_first_class_map_groups():
  rendered = render_toda_proof_statement_latex(
    build_statement(
      source_dimension=17,
      source_sphere=9,
      target_dimension=15,
      target_sphere=4,
    )
  )

  assert (
    r"\Delta: \pi_{17}^{9} \to \pi_{15}^{4}"
    in rendered
  )


def test_phase143_75ai_uses_first_class_kernel_group():
  rendered = render_toda_proof_statement_latex(
    build_statement(
      order=4,
      coefficient=2,
    )
  )

  assert (
    r"\mathbb{Z}/4\{2\nu_{5}\}"
    in rendered
  )


def test_phase143_75ai_does_not_render_rule_name():
  rendered = render_toda_proof_statement_latex(
    build_statement()
  )

  assert "Toda Proposition" not in rendered
  assert "Delta nu_5 kernel" not in rendered
