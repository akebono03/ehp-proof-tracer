from toda_calculation_facade import (
  build_standard_toda_report,
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


def test_phase159_r1_7c_r4_pi11_6_numbers_existing_hopf_reasoning():
  rendered = _public_narrative(
    6,
    5,
  )

  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}\tag{1}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}\tag{2}$ は全射."
    in rendered
  )
  assert (
    r"(1), (2) より, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型写像である."
    not in rendered
  )


def test_phase159_r1_7c_r4_pi3_2_keeps_existing_numbered_hopf_reasoning():
  rendered = _public_narrative(
    2,
    1,
  )

  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{1}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{2}$ は全射."
    in rendered
  )
  assert (
    r"(1), (2) より, $H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    in rendered
  )


def test_phase159_r1_7c_r4_delta_pairs_without_isomorphism_are_not_numbered():
  for n, k, map_text in (
    (
      3,
      6,
      r"\Delta: \pi_{9}^{5} \to \pi_{7}^{2}",
    ),
    (
      3,
      7,
      r"\Delta: \pi_{10}^{5} \to \pi_{8}^{2}",
    ),
  ):
    rendered = _public_narrative(
      n,
      k,
    )

    assert (
      "$"
      + map_text
      + "$ は単射."
      in rendered
    )
    assert (
      "$"
      + map_text
      + "$ は全射."
      in rendered
    )
    assert (
      "$"
      + map_text
      + r"\tag{"
      not in rendered
    )
    assert (
      "$"
      + map_text
      + "$ は同型."
      not in rendered
    )
    assert (
      "$"
      + map_text
      + "$ は同型写像である."
      not in rendered
    )


def test_phase159_r1_7c_r4_numbered_reasoning_is_general_not_pi11_hardcoded():
  from toda_group_proof_narrative_renderer import (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  )

  rendered = (
    "# Group proof narrative\n\n"
    "## 証明対象\n\n"
    "target\n\n"
    "## 使用する結果\n\n"
    "---\n\n"
    "## 証明\n\n"
    "$F: A \\to B$ は単射.\n"
    "$F: A \\to B$ は全射.\n"
    "$F: A \\to B$ は同型写像である.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  assert (
    r"$F: A \to B\tag{1}$ は単射."
    in normalized
  )
  assert (
    r"$F: A \to B\tag{2}$ は全射."
    in normalized
  )
  assert (
    r"(1), (2) より, $F: A \to B$ は同型."
    in normalized
  )
