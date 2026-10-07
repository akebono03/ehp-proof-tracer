from expression import (
  GeneratorSymbol,
  HomotopyElement,
)
from homotopy_groups import (
  FiniteCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  LiteratureReference,
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_repeated_root_semantic_conclusion,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_statement_identity import (
  toda_group_proof_narrative_statement_semantic_key,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


PI4_3 = r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$"


def _phase159_pi4_3_presentation():
  report = build_standard_toda_report(
    n=3,
    k=1,
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
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_semantic_statement_key_ignores_relation_provenance_metadata():
  group = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )
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
  finite_group = FiniteCyclicGroup(
    order=2,
    generator=eta_3,
  )
  plain = Relation(
    lhs=group,
    rhs=finite_group,
    relation_type=RelationType.EQUALITY,
  )
  attributed = Relation(
    lhs=group,
    rhs=finite_group,
    relation_type=RelationType.EQUALITY,
    source=LiteratureReference(
      label="synthetic source",
    ),
    note="synthetic note",
  )

  assert (
    toda_group_proof_narrative_statement_semantic_key(
      plain
    )
    == toda_group_proof_narrative_statement_semantic_key(
      attributed
    )
  )


def test_phase159_semantic_statement_key_distinguishes_different_group_claims():
  group = TodaPrimaryGroup(
    group_dimension=4,
    sphere_dimension=3,
  )
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
  order_two = Relation(
    lhs=group,
    rhs=FiniteCyclicGroup(
      order=2,
      generator=eta_3,
    ),
    relation_type=RelationType.EQUALITY,
  )
  order_four = Relation(
    lhs=group,
    rhs=FiniteCyclicGroup(
      order=4,
      generator=eta_3,
    ),
    relation_type=RelationType.EQUALITY,
  )

  assert (
    toda_group_proof_narrative_statement_semantic_key(
      order_two
    )
    != toda_group_proof_narrative_statement_semantic_key(
      order_four
    )
  )


def test_phase159_root_semantic_conclusion_prefers_connected_final_form():
  presentation = (
    _phase159_pi4_3_presentation()
  )
  markdown = (
    "support\n\n"
    + PI4_3
    + "\n\n"
    + "以上より, "
    + PI4_3
  )

  rendered = (
    suppress_toda_group_proof_narrative_repeated_root_semantic_conclusion(
      presentation,
      markdown,
    )
  )

  assert rendered.count(
    PI4_3
  ) == 1
  assert (
    "以上より, "
    + PI4_3
  ) in rendered


def test_phase159_root_semantic_conclusion_keeps_single_bare_form_when_no_connector_exists():
  presentation = (
    _phase159_pi4_3_presentation()
  )
  markdown = (
    "support\n\n"
    + PI4_3
  )

  rendered = (
    suppress_toda_group_proof_narrative_repeated_root_semantic_conclusion(
      presentation,
      markdown,
    )
  )

  assert rendered == markdown


def test_phase159_pi4_3_public_narrative_emits_final_group_conclusion_once():
  presentation = (
    _phase159_pi4_3_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  proof_body = rendered.split(
    "## 証明",
    1,
  )[1]

  assert proof_body.count(
    r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}"
  ) == 1
  assert (
    "以上より, "
    + r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}$."
  ) in proof_body
  assert rendered.rstrip().endswith(
    "□"
  )
