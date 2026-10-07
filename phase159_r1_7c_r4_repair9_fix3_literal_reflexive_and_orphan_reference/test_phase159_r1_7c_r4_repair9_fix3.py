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


def _sections(
  rendered: str,
) -> tuple[
  str,
  str,
]:
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


def test_phase159_r1_7c_r4_repair9_fix3_suppresses_only_literal_reflexive_equality():
  rendered = _render_group(
    3,
    3,
  )
  _, body = _sections(
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
    r"$2\nu' = \eta_{3}^{3}"
    in body
  )


def test_phase159_r1_7c_r4_repair9_fix3_pi15_has_no_orphan_reference():
  rendered = _render_group(
    8,
    7,
  )
  reference, body = _sections(
    rendered
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

  assert (
    reference_numbers
    <= body_numbers
  )


def test_phase159_r1_7c_r4_repair9_fix3_pi15_keeps_generic_transport_before_target():
  rendered = _render_group(
    8,
    7,
  )

  transported = (
    r"$\pi_{15}^{8} \cong "
    r"\mathbb{Z}/8\{E\sigma'\} "
    r"\oplus \mathbb{Z}\{\sigma_{8}\}$"
  )
  target = (
    r"$\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus \mathbb{Z}/8\{E\sigma'\}$"
  )

  assert transported in rendered
  assert target in rendered
  assert rendered.index(
    transported
  ) < rendered.index(
    target
  )
