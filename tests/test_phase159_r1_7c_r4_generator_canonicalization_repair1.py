from expression import (
  Composition,
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _normalize_generic_narrative_statement_latex,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_proof_narrative_renderer import (
  render_toda_proof_statement_latex,
)


def _eta(
  index: int,
) -> HomotopyElement:
  return HomotopyElement(
    name=(
      "η"
      + str(
        index
      )
    ),
    dimension=index,
    source=index + 1,
    target=index,
    generator=GeneratorSymbol(
      family="η",
      index=index,
    ),
  )


def _pi6_3_public_narrative() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7c_r4_repair1_group_generator_uses_eta_power_notation():
  eta_5 = _eta(
    5
  )
  eta_6 = _eta(
    6
  )
  statement = Relation(
    lhs=TodaPrimaryGroup(
      group_dimension=7,
      sphere_dimension=5,
    ),
    rhs=FiniteCyclicGroup(
      order=2,
      generator=Composition(
        left=eta_5,
        right=eta_6,
      ),
    ),
    relation_type=RelationType.EQUALITY,
  )
  raw = render_toda_proof_statement_latex(
    statement
  )

  assert (
    raw
    == (
      r"\pi_{7}^{5} = "
      r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}"
    )
  )

  normalized = (
    _normalize_generic_narrative_statement_latex(
      statement,
      raw,
    )
  )

  assert (
    normalized
    == (
      r"\pi_{7}^{5} = "
      r"\mathbb{Z}/2\{\eta_{5}^{2}\}"
    )
  )


def test_phase159_r1_7c_r4_repair1_public_pi6_3_reference_uses_eta5_squared():
  rendered = _pi6_3_public_narrative()

  canonical = (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
  )
  expanded = (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}\eta_{6}\}$."
  )

  assert canonical in rendered
  assert expanded not in rendered


def test_phase159_r1_7c_r4_repair1_derivation_equality_keeps_expanded_left_side():
  rendered = _pi6_3_public_narrative()

  assert (
    r"\eta_{3}\eta_{4}\eta_{5}"
    in rendered
  )
  assert (
    r"\eta_{3}^{3}"
    in rendered
  )


def test_phase159_r1_7c_r4_repair1_hopf_calculation_keeps_eta5_squared_result():
  rendered = _pi6_3_public_narrative()

  assert (
    r"H\left(\nu'\eta_{6}\right) = \eta_{5}^{2}"
    in rendered
  )
