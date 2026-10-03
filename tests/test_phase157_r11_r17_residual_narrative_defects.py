import re

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


TARGETS = (
  (3, 3),
  (4, 6),
  (5, 3),
  (5, 7),
  (8, 7),
  (9, 7),
)

REFERENCE_HEADER_RE = re.compile(
  r"\*\*\[R([0-9]+)\] ([^\n]+?)\.\*\*"
)
REFERENCE_MARKER_RE = re.compile(
  r"\[R([0-9]+)\]"
)


def _render(
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


def _reference_and_body(
  n: int,
  k: int,
) -> tuple[
  str,
  str,
]:
  rendered = _render(
    n,
    k,
  )

  return tuple(
    rendered.split(
      "\n## 証明\n",
      1,
    )
  )


def test_phase157_r11_r17_pi6_3_zero_map_statement_precedes_its_use():
  _, body = _reference_and_body(
    3,
    3,
  )

  zero_map = (
    r"$\Delta: \pi_{7}^{5} \to \pi_{5}^{2}$ "
    "は零写像である."
  )
  use = (
    "この完全性と $Δ=0$ より, "
    r"$\ker E=\operatorname{Im}Δ=0$ である."
  )

  assert zero_map in body
  assert use in body
  assert body.index(
    zero_map
  ) < body.index(
    use
  )


def test_phase157_r11_r17_pi6_3_keeps_first_delta_sequence_but_trims_second():
  _, body = _reference_and_body(
    3,
    3,
  )

  first_sequence = (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$."
  )
  redundant_four_term = (
    r"$\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$."
  )
  trimmed_sequence = (
    r"$\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$."
  )

  assert first_sequence in body
  assert redundant_four_term not in body
  assert trimmed_sequence in body


def test_phase157_r11_r17_target_groups_have_no_standalone_connectors():
  connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }

  for n, k in TARGETS:
    _, body = _reference_and_body(
      n,
      k,
    )
    body_paragraphs = tuple(
      paragraph.strip()
      for paragraph in body.split(
        "\n\n"
      )
      if paragraph.strip()
    )

    assert not (
      connectors
      & set(
        body_paragraphs
      )
    )


def test_phase157_r11_r17_pi6_3_repeated_numeric_equality_is_normalized():
  _, body = _reference_and_body(
    3,
    3,
  )

  assert (
    r"\operatorname{ord}(\nu')=4=4"
    not in body
  )
  assert (
    r"\operatorname{ord}(\nu')=4"
    in body
  )


def test_phase157_r11_r17_target_group_public_references_have_body_markers():
  for n, k in TARGETS:
    reference, body = _reference_and_body(
      n,
      k,
    )
    headers = tuple(
      int(
        match.group(
          1
        )
      )
      for match in REFERENCE_HEADER_RE.finditer(
        reference
      )
    )
    markers = {
      int(
        match.group(
          1
        )
      )
      for match in REFERENCE_MARKER_RE.finditer(
        body
      )
    }

    assert set(
      headers
    ) <= markers


def test_phase157_r11_r17_ancestry_only_references_are_not_public():
  pi12_reference, _ = _reference_and_body(
    5,
    7,
  )
  pi16_reference, _ = _reference_and_body(
    9,
    7,
  )

  assert "(5.5)" not in pi12_reference
  assert "Lemma 5.13" not in pi16_reference


def test_phase157_r11_r17_needed_references_remain_public_and_linked():
  pi10_reference, pi10_body = _reference_and_body(
    4,
    6,
  )
  pi12_reference, pi12_body = _reference_and_body(
    5,
    7,
  )
  pi16_reference, pi16_body = _reference_and_body(
    9,
    7,
  )

  assert "Lemma 5.4" in pi10_reference
  assert "[R1]" in pi10_body

  assert "Lemma 5.13" in pi12_reference
  assert "[R1]" in pi12_body

  assert "Lemma 5.14" in pi16_reference
  assert "[R1]" in pi16_body
