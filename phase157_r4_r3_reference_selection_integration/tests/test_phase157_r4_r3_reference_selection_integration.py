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


CASES = (
  ("pi_8^5", 5, 3),
  ("pi_10^4", 4, 6),
  ("pi_12^5", 5, 7),
  ("pi_15^8", 8, 7),
  ("pi_16^9", 9, 7),
)


def _render(
  n: int,
  k: int,
  depth: int = 3,
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
    max_depth=depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def _reference_section(
  rendered: str,
) -> str:
  if "## 使用する結果" in rendered:
    start = rendered.index(
      "## 使用する結果"
    )
    proof = rendered.find(
      "## 証明",
      start,
    )
    assert proof >= 0
    return rendered[
      start:
      proof
    ]

  marker = "使用する結果を先にまとめる."
  start = rendered.find(
    marker
  )
  assert start >= 0

  body_markers = (
    "\n\nまず,",
    "\n\n次に,",
    "\n\n最後に,",
    "\n\n$\\pi_",
    "\n\nこの群構造",
  )
  positions = tuple(
    position
    for body_marker in body_markers
    for position in (
      rendered.find(
        body_marker,
        start + len(
          marker
        ),
      ),
    )
    if position >= 0
  )

  assert positions
  return rendered[
    start:
    min(
      positions
    )
  ]


def test_phase157_r4_r3_representatives_have_reference_sections():
  for _, n, k in CASES:
    reference = _reference_section(
      _render(
        n,
        k,
      )
    )

    assert "[R" in reference


def test_phase157_r4_r3_prop511_proof_internal_map_facts_are_not_references():
  reference = _reference_section(
    _render(
      5,
      7,
    )
  )

  assert (
    r"H: \pi_{12}^{5} \to \pi_{12}^{9} は単射"
    not in reference
  )


def test_phase157_r4_r3_prop515_proof_internal_decomposition_is_not_reference():
  reference = _reference_section(
    _render(
      8,
      7,
    )
  )

  assert (
    r"\left(α, \beta\right) \mapsto Eα + \sigma_{8}\beta"
    not in reference
  )


def test_phase157_r4_r3_prop515_same_theorem_target_and_later_result_are_not_references():
  reference = _reference_section(
    _render(
      8,
      7,
    )
  )

  assert (
    r"\pi_{15}^{8} = "
    not in reference
  )
  assert (
    r"\pi_{n + 7}^{n}"
    not in reference
  )
  assert (
    r"\pi_{14}^{7}"
    in reference
  )


def test_phase157_r4_r3_prop511_same_theorem_earlier_result_is_reference_for_pi12_5():
  reference = _reference_section(
    _render(
      5,
      7,
    )
  )

  assert "Proposition 5.11" in reference
  assert (
    r"\pi_{10}^{4}"
    in reference
    or r"\pi_{11}^{5}"
    in reference
    or r"\pi_{12}^{6}"
    in reference
  )


def test_phase157_r4_r3_lemma513_fixed_statement_can_remain_reference():
  reference = _reference_section(
    _render(
      5,
      7,
    )
  )

  assert "Lemma 5.13" in reference
  assert "\\sigma'''" in reference


def test_phase157_r4_r3_pi16_9_reference_does_not_use_target_prop515_group_result():
  reference = _reference_section(
    _render(
      9,
      7,
    )
  )

  assert (
    r"\pi_{16}^{9} = "
    not in reference
  )


def test_phase157_r4_r3_representative_reference_sections_do_not_expose_known_internal_phrases():
  forbidden = (
    "は単射である.",
    "は全射である.",
    "is exact",
    "transported decomposition",
  )

  for _, n, k in CASES:
    reference = _reference_section(
      _render(
        n,
        k,
      )
    )

    for phrase in forbidden:
      assert phrase not in reference
