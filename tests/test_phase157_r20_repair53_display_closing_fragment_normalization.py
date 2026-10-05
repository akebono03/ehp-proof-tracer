from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _normalize_toda_group_proof_narrative_display_closing_fragments,
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase157_r20_repair53_helper_merges_only_display_closing_fragment_gap():
  rendered = (
    "前文.\n"
    "\n"
    "\\[\n"
    "x=y\n"
    "\\]\n"
    "\n"
    "を得る.\n"
    "\n"
    "後文.\n"
  )

  normalized = (
    _normalize_toda_group_proof_narrative_display_closing_fragments(
      rendered
    )
  )

  assert (
    "\\]\nを得る."
    in normalized
  )
  assert (
    "\\]\n\nを得る."
    not in normalized
  )
  assert (
    "前文.\n\n\\["
    in normalized
  )
  assert (
    "を得る.\n\n後文."
    in normalized
  )


def test_phase157_r20_repair53_pi8_5_has_no_isolated_closing_fragment():
  rendered = _render_group(
    5,
    3,
  )

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  assert "を得る." not in paragraphs
  assert (
    r"\pi_{8}^{5} = "
    r"\mathbb{Z}/8\{\nu_{5}\}"
    in rendered
  )


def test_phase157_r20_repair53_pi15_8_has_no_isolated_closing_fragments():
  rendered = _render_group(
    8,
    7,
  )

  paragraphs = tuple(
    paragraph.strip()
    for paragraph in rendered.split(
      "\n\n"
    )
    if paragraph.strip()
  )

  assert "である." not in paragraphs
  assert "を得る." not in paragraphs
  assert (
    r"\pi_{15}^{8} = "
    r"\mathbb{Z}\{\sigma_{8}\} "
    r"\oplus "
    r"\mathbb{Z}/8\{E\sigma'\}"
    in rendered
  )


def test_phase157_r20_repair53_pi6_3_public_narrative_is_unchanged_by_fragment_rule():
  rendered = _render_group(
    3,
    3,
  )

  assert (
    r"$E(\eta_{2}^{3})="
    r"\eta_{3}^{3}\neq0$"
    in rendered
  )
  assert (
    r"$\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}$."
    in rendered
  )
  assert rendered.rstrip().endswith(
    r"$\square$"
  )
