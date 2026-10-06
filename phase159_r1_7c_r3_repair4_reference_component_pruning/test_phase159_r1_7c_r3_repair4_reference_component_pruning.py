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


def _phase159_r1_7c_r3_repair4_render(
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
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
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


def _phase159_r1_7c_r3_repair4_reference_part(
  rendered: str,
) -> str:
  marker = "---\n\n## 証明"

  assert marker in rendered

  return rendered.split(
    marker,
    1,
  )[0]


def test_phase159_r1_7c_r3_repair4_pi11_4_prop515_keeps_only_used_component():
  reference_part = (
    _phase159_r1_7c_r3_repair4_reference_part(
      _phase159_r1_7c_r3_repair4_render(
        4,
        7,
      )
    )
  )

  assert (
    "**[R1] Proposition 5.15.**"
    in reference_part
  )
  assert (
    r"\pi_{10}^{3} = 0"
    in reference_part
  )
  assert (
    r"\pi_{9}^{2} = 0"
    not in reference_part
  )


def test_phase159_r1_7c_r3_repair4_pi11_4_prop58_keeps_only_used_range_component():
  reference_part = (
    _phase159_r1_7c_r3_repair4_reference_part(
      _phase159_r1_7c_r3_repair4_render(
        4,
        7,
      )
    )
  )

  assert (
    "**[R2] Proposition 5.8.**"
    in reference_part
  )
  assert (
    r"\pi_{n + 4}^{n} = 0"
    in reference_part
  )
  assert (
    r"n \ge 6"
    in reference_part
  )
  assert (
    r"\pi_{6}^{2}"
    not in reference_part
  )
  assert (
    r"\pi_{7}^{3}"
    not in reference_part
  )
  assert (
    r"\pi_{8}^{4}"
    not in reference_part
  )
  assert (
    r"\pi_{9}^{5}"
    not in reference_part
  )


def test_phase159_r1_7c_r3_repair4_pi11_4_keeps_prop44_reference():
  reference_part = (
    _phase159_r1_7c_r3_repair4_reference_part(
      _phase159_r1_7c_r3_repair4_render(
        4,
        7,
      )
    )
  )

  assert (
    "**[R3] Proposition 4.4.**"
    in reference_part
  )
  assert (
    r"\pi_{i - 1}^{3} \oplus "
    r"\pi_{i}^{7} \to \pi_{i}^{4}"
    in reference_part
  )


def test_phase159_r1_7c_r3_repair4_pi11_4_body_contract_is_unchanged():
  rendered = (
    _phase159_r1_7c_r3_repair4_render(
      4,
      7,
    )
  )
  body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"\pi_{10}^{3} = 0"
    in body
  )
  assert (
    r"\pi_{11}^{7} = 0"
    in body
  )
  assert (
    r"\pi_{10}^{3} \oplus "
    r"\pi_{11}^{7} "
    r"\xrightarrow{\cong} "
    r"\pi_{11}^{4}"
    in body
  )
  assert body.rstrip().endswith(
    "□"
  )


def test_phase159_r1_7c_r3_repair4_nonmatching_pi6_3_reference_is_unchanged():
  reference_part = (
    _phase159_r1_7c_r3_repair4_reference_part(
      _phase159_r1_7c_r3_repair4_render(
        3,
        3,
      )
    )
  )

  assert (
    "(5.3)"
    in reference_part
  )
