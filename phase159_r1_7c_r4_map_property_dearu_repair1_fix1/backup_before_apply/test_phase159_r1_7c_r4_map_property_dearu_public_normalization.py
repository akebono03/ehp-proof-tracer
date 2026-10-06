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


def test_phase159_r1_7c_r4_public_map_property_prose_removes_dearu():
  targets = (
    (
      6,
      5,
    ),
    (
      6,
      6,
    ),
    (
      7,
      6,
    ),
    (
      9,
      7,
    ),
  )

  for n, k in targets:
    rendered = _public_narrative(
      n,
      k,
    )
    proof_body = rendered.split(
      "## 証明\n\n",
      1,
    )[
      1
    ]

    assert "は単射である." not in proof_body
    assert "は全射である." not in proof_body


def test_phase159_r1_7c_r4_pi11_6_uses_concise_map_property_prose():
  rendered = _public_narrative(
    6,
    5,
  )

  assert (
    r"$\Delta: \pi_{10}^{9} \to \pi_{8}^{4}$ は単射."
    in rendered
  )
  assert (
    r"$E: \pi_{9}^{4} \to \pi_{10}^{5}$ は全射."
    in rendered
  )
  assert (
    r"[R1] より, $H: \pi_{7}^{3} \to \pi_{7}^{5}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は全射."
    in rendered
  )


def test_phase159_r1_7c_r4_pi16_9_aggregate_line_is_concise():
  rendered = _public_narrative(
    9,
    7,
  )

  assert (
    r"$|\pi_{16}^{9}| = 16$ であり, "
    r"$E^{4}: \pi_{12}^{5} \to \pi_{16}^{9}$ は単射."
    in rendered
  )


def test_phase159_r1_7c_r4_reference_section_is_not_normalized():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明対象\n\n"
    "target\n\n"
    "## 使用する結果\n\n"
    "Reference map は単射である.\n\n"
    "---\n\n"
    "## 証明\n\n"
    "Proof map は単射である.\n"
  )

  from toda_group_proof_narrative_renderer import (
    _phase159_r1_7c_r4_normalize_public_map_property_prose,
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )

  assert (
    "Reference map は単射である."
    in normalized
  )
  assert (
    "Proof map は単射."
    in normalized
  )
  assert (
    "Proof map は単射である."
    not in normalized
  )
