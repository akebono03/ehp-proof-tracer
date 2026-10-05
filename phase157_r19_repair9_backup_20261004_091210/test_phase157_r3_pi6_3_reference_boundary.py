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


def _render_pi6_3(
  depth: int,
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


def _reference_and_body(
  rendered: str,
) -> tuple[str, str]:
  marker = "\n## 証明\n"
  assert marker in rendered

  reference, body = rendered.split(
    marker,
    1,
  )

  return (
    reference.rstrip(),
    body.lstrip(),
  )


def test_phase157_r3_pi6_3_reference_uses_earlier_prop56_group_result():
  reference, _ = _reference_and_body(
    _render_pi6_3(2)
  )

  assert "Proposition 5.6" in reference
  assert (
    r"\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}"
    in reference
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}"
    not in reference
  )
  assert r"\pi_{7}^{4}" not in reference
  assert r"\pi_{8}^{5}" not in reference


def test_phase157_r3_pi6_3_reference_keeps_only_fixed_prop53_group_fact():
  reference, body = _reference_and_body(
    _render_pi6_3(3)
  )

  assert "Proposition 5.3" in reference
  assert (
    r"\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}"
    in reference
  )
  assert (
    r"H: \pi_{6}^{3} \to \pi_{6}^{5}"
    not in reference
  )
  assert (
    r"H: \pi_{6}^{3} \to \pi_{6}^{5}"
    in body
  )


def test_phase157_r3_pi6_3_reference_rehomes_pi6_5_to_prop51_fixed_family():
  reference, _ = _reference_and_body(
    _render_pi6_3(2)
  )

  assert "Proposition 5.1" in reference
  assert (
    r"\pi_{6}^{5} = \mathbb{Z}/2\{\eta_{5}\}"
    in reference
  )
  assert "Lemma 5.4" not in reference


def test_phase157_r3_pi6_3_reference_excludes_untracked_proof_machinery():
  reference, _ = _reference_and_body(
    _render_pi6_3(3)
  )

  assert "(5.2)" not in reference
  assert "Lemma 5.4" not in reference
  assert "Lemma 5.2" not in reference
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    not in reference
  )


def test_phase157_r3_pi6_3_reference_retains_fixed_53_components():
  reference, _ = _reference_and_body(
    _render_pi6_3(2)
  )

  assert "(5.3)" in reference
  assert r"\nu' \in \pi_{6}^{3}" in reference
  assert r"2\nu' = " in reference


def test_phase157_r3_pi6_3_body_keeps_prop56_derived_injectivity():
  _, body = _reference_and_body(
    _render_pi6_3(2)
  )

  assert (
    r"E: \pi_{5}^{2} \to \pi_{6}^{3}"
    in body
  )
  assert "単射" in body


def test_phase157_r3_pi6_3_depth3_suppresses_prop53_internal_suspension():
  reference, body = _reference_and_body(
    _render_pi6_3(3)
  )

  assert "Proposition 5.3" in reference
  assert (
    r"\pi_{7}^{5} = \mathbb{Z}/2\{\eta_{5}^{2}\}"
    in reference
  )
  assert (
    r"E: \pi_{4}^{2} \to \pi_{5}^{3}"
    not in reference
  )
  assert (
    r"E: \pi_{4}^{2} \to \pi_{5}^{3}"
    not in body
  )


def test_phase157_r3_pi6_3_preserves_phase156_bracket_boundary_collapse():
  rendered = _render_pi6_3(3)

  assert "Lemma 5.2" not in rendered
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    not in rendered
  )


def test_phase157_r3_pi6_3_same_proposition_earlier_component_survives_root_exclusion():
  reference, _ = _reference_and_body(
    _render_pi6_3(2)
  )

  assert "Proposition 5.6" in reference
  assert (
    r"\pi_{5}^{2} = \mathbb{Z}/2\{\eta_{2}^{3}\}"
    in reference
  )


