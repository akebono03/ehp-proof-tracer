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


def _render_group(
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
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _reference_and_body(
  rendered: str,
) -> tuple[str, str]:
  if "---" in rendered:
    return tuple(
      rendered.split(
        "---",
        1,
      )
    )

  marker = "\n## 証明\n"

  if marker in rendered:
    return tuple(
      rendered.split(
        marker,
        1,
      )
    )

  return (
    "",
    rendered,
  )


def test_phase159_r1_7c_r4_repair9_final_reflexive_equality_is_suppressed():
  rendered = _render_group(
    3,
    3,
  )
  _, body = _reference_and_body(
    rendered
  )
  compact = re.sub(
    r"\s+",
    "",
    body,
  )

  assert (
    r"$\eta_{5}=\eta_{5}$"
    not in compact
  )
  assert (
    r"$\eta_5=\eta_5$"
    not in compact
  )


def test_phase159_r1_7c_r4_repair9_keeps_distinct_eta_canonicalization_relation():
  rendered = _render_group(
    3,
    3,
  )
  _, body = _reference_and_body(
    rendered
  )

  assert (
    (
      r"\eta_{3}\eta_{4}\eta_{5}"
      in body
      and r"\eta_{3}^{3}"
      in body
    )
    or (
      r"2\nu' = \eta_{3}^{3}"
      in body
    )
  )


def test_phase159_r1_7c_r4_repair9_every_pi15_reference_has_body_linkage():
  rendered = _render_group(
    8,
    7,
  )
  reference, body = (
    _reference_and_body(
      rendered
    )
  )

  reference_numbers = {
    int(number)
    for number in re.findall(
      r"\*\*\[R([0-9]+)\]",
      reference,
    )
  }
  body_numbers = {
    int(number)
    for number in re.findall(
      r"\[R([0-9]+)\]",
      body,
    )
  }

  assert reference_numbers
  assert (
    reference_numbers
    <= body_numbers
  )
