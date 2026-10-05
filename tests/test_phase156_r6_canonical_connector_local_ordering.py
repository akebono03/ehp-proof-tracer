from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  normalize_toda_group_proof_narrative_connectors,
  order_toda_group_proof_narrative_local_equation_derivations,
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


def _render_pi6_3(
  depth: int = 2,
) -> str:
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
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase156_r6_pi6_53_uses_canonical_suspended_eta_expression():
  rendered = _render_pi6_3()

  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}$"
    in rendered
  )
  assert (
    r"$2\nu' = \eta_{3}E\eta_{3}\eta_{5}$"
    not in rendered
  )


def test_phase156_r6_pi6_local_calculation_uses_canonical_eta_expression():
  rendered = _render_pi6_3()

  equation_one = (
    r"$2\nu' = "
    r"\eta_{3}\eta_{4}\eta_{5}\tag{1}$"
  )
  equation_two = (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
  )

  assert equation_one in rendered
  assert equation_two in rendered


def test_phase156_r6_connector_normalization_removes_only_redundant_generic_connector():
  markdown = (
    "$a=b$\n\n"
    "以上より,\n\n"
    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,\n\n"
    "$G=H$"
  )

  rendered = normalize_toda_group_proof_narrative_connectors(
    markdown
  )

  assert "以上より," not in rendered
  assert (
    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
    in rendered
  )


def test_phase156_r6_local_ordering_moves_derived_equation_next_to_sources():
  markdown = (
    "$a=b\\tag{1}$\n\n"
    "$b=c\\tag{2}$\n\n"
    "$x=y$\n\n"
    "(1) と (2) より, \n\n"
    "$a=c\\tag{3}$"
  )

  rendered = order_toda_group_proof_narrative_local_equation_derivations(
    markdown
  )

  assert (
    rendered.index(
      r"$a=b\tag{1}$"
    )
    < rendered.index(
      r"$b=c\tag{2}$"
    )
    < rendered.index(
      "(1) と (2) より,"
    )
    < rendered.index(
      r"$a=c\tag{3}$"
    )
    < rendered.index(
      "$x=y$"
    )
  )


def test_phase156_r6_pi6_places_equation3_before_transport_and_order():
  rendered = _render_pi6_3()

  equation_two = (
    r"$\eta_{3}\eta_{4}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
  )
  connector = "(1) と (2) より,"
  equation_three = (
    r"$2\nu' = \eta_{3}^{3}\tag{3}$"
  )
  transported_group_body = (
    "[R1]より, "
    r"$\pi_{5}^{2} = "
    r"\mathbb{Z}/2\{\eta_{2}\eta_{3}\eta_{4}\}$."
  )
  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射である."
  )
  eta_cube_order = (
    r"$\operatorname{ord}\left(\eta_{3}^{3}\right) = 2$"
  )

  assert (
    rendered.index(
      equation_two
    )
    < rendered.index(
      connector
    )
    < rendered.index(
      equation_three
    )
    < rendered.index(
      transported_group_body
    )
    < rendered.index(
      injectivity
    )
    < rendered.index(
      eta_cube_order
    )
  )


def test_phase156_r6_pi6_has_no_redundant_consecutive_result_connectors():
  rendered = _render_pi6_3()

  assert (
    "以上より,\n\n"
    "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
    not in rendered
  )
