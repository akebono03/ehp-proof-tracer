from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_reference_body_duplicates,
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
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase154_r2_fix3_completes_bare_reference_marker_after_replacement():
  statement = (
    r"$(α, \beta) \mapsto Eα + \nu_{4}\beta: "
    r"\pi_{i - 1}^{3} \oplus \pi_{i}^{7} "
    r"\to \pi_{i}^{4}$ は同型写像である."
  )
  body = (
    "まず, "
    + statement
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == "まず, [R2]を用いる."


def test_phase154_r2_fix3_keeps_reference_marker_with_following_prose():
  statement = "$E: A \\xrightarrow{\\cong} B$"
  body = (
    "まず, "
    + statement
    + "を確認し, 次の計算へ進む。"
  )

  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert rendered == (
    "まず, [R2]を確認し, 次の計算へ進む。"
  )


def test_phase154_r2_fix3_pi11_4_has_complete_reference_use_sentence():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"[R2]より, $\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert "まず, [R2]を用いる." not in rendered
  assert (
    r"このことから, $\nu_{4}$ の分解写像は同型写像である."
    not in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered


def test_phase154_r2_fix3_keeps_previous_r2_repairs():
  pi10_4 = _render_group(
    4,
    6,
  )
  pi11_4 = _render_group(
    4,
    7,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in pi10_4
  )
  assert (
    r"$\nu_{4}$ の分解を用いる."
    in pi10_4
  )

  forbidden = (
    "Toda Proposition 5.15を用いる。",
    r"\text{ is injective}",
    r"\text{ is exact}",
    "である.を用いる。",
    "Toda (5.6) の ν₄ 分解同型",
  )

  for fragment in forbidden:
    assert fragment not in pi11_4
