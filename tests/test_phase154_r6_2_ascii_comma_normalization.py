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


REPRESENTATIVES = (
  ("pi6_3", 3, 3),
  ("pi10_4", 4, 6),
  ("pi11_4", 4, 7),
  ("pi12_5", 5, 7),
  ("pi16_9", 9, 7),
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


def _strip_inline_math(
  line: str,
) -> str:
  return re.sub(
    r"\$[^$]*\$",
    "MATH",
    line,
  )


def _japanese_prose_lines_with_japanese_comma(
  rendered: str,
) -> tuple[
  str,
  ...,
]:
  result = []

  for line in rendered.splitlines():
    stripped = line.strip()

    if not stripped:
      continue

    if stripped.startswith(
      "**[R"
    ):
      continue

    prose = _strip_inline_math(
      stripped
    )

    if not re.search(
      r"[ぁ-んァ-ヶ一-龠々]",
      prose,
    ):
      continue

    if "、" in prose:
      result.append(
        stripped
      )

  return tuple(
    result
  )


def test_phase154_r6_2_representative_narratives_have_no_japanese_comma_prose():
  for _, n, k in REPRESENTATIVES:
    rendered = _render_group(
      n,
      k,
    )

    assert (
      _japanese_prose_lines_with_japanese_comma(
        rendered
      )
      == ()
    )


def test_phase154_r6_2_pi11_4_uses_ascii_comma_space_and_ascii_period():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"まず, $H: \pi_{10}^{3} \to \pi_{10}^{5}$ は単射である."
    in rendered
  )
  assert (
    r"また, $\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は単射である."
    in rendered
  )
  assert (
    r"さらに, $\pi_{10}^{3} \xrightarrow{H} "
    r"\pi_{10}^{5} \xrightarrow{Δ} \pi_{8}^{2}$ "
    r"は完全である."
    in rendered
  )
  assert (
    r"[R2]より, $\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert (
    r"したがって, $\pi_{11}^{4} = 0$を得る."
    in rendered
  )


def test_phase154_r6_2_keeps_reference_title_punctuation():
  rendered = _render_group(
    4,
    7,
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "**[R2] Proposition 4.4.**" in rendered


def test_phase154_r6_2_preserves_existing_math_list_ascii_commas():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"$\pi_{6}^{2} = \mathbb{Z}/4\{\eta_{2}\nu'\}$, "
    in rendered
  )
  assert (
    r"$\pi_{7}^{3} = \mathbb{Z}/2\{\nu'\eta_{6}\}$, "
    in rendered
  )
