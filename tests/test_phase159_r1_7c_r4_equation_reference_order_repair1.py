from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _public_narrative(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
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


def test_phase159_r1_7c_r4_pi5_3_places_isomorphism_after_both_numbered_premises():
  rendered = _public_narrative(
    3,
    2,
  )

  injective = (
    r"$E: \pi_{4}^{2} \to \pi_{5}^{3}\tag{1}$ は単射."
  )
  surjective = (
    r"これより, $E: \pi_{4}^{2} \to \pi_{5}^{3}\tag{2}$ は全射."
  )
  isomorphism = (
    r"(1), (2) より, $E: \pi_{4}^{2} \to \pi_{5}^{3}$ は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert isomorphism in rendered
  assert (
    rendered.index(
      injective
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      isomorphism
    )
  )


def test_phase159_r1_7c_r4_pi3_2_keeps_valid_backward_equation_references():
  rendered = _public_narrative(
    2,
    1,
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{1}$ は単射."
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{2}$ は全射."
  )
  isomorphism = (
    r"(1), (2) より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )

  assert (
    rendered.index(
      injective
    )
    < rendered.index(
      surjective
    )
    < rendered.index(
      isomorphism
    )
  )


def test_phase159_r1_7c_r4_reorder_helper_moves_only_forward_reference_conclusion():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明\n\n"
    "(1), (2) より, $F: A \\to B$ は同型.\n\n"
    "$F: A \\to B\\tag{1}$ は単射.\n\n"
    "$F: A \\to B\\tag{2}$ は全射.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

  injective = (
    r"$F: A \to B\tag{1}$ は単射."
  )
  surjective = (
    r"$F: A \to B\tag{2}$ は全射."
  )
  isomorphism = (
    r"(1), (2) より, $F: A \to B$ は同型."
  )

  assert (
    normalized.index(
      injective
    )
    < normalized.index(
      surjective
    )
    < normalized.index(
      isomorphism
    )
  )


def test_phase159_r1_7c_r4_reorder_helper_leaves_missing_reference_untouched():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明\n\n"
    "(1), (2) より, $F: A \\to B$ は同型.\n\n"
    "$F: A \\to B\\tag{1}$ は単射.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

  assert normalized == rendered
