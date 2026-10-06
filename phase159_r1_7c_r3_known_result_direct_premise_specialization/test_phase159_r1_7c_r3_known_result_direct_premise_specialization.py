from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  specialize_toda_group_proof_narrative_root_zero_direct_premises,
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


def _phase159_r1_7c_r3_presentation(
  n: int,
  k: int,
):
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

  return (
    build_toda_group_proof_presentation(
      replay
    )
  )


def _phase159_r1_7c_r3_render(
  n: int,
  k: int,
) -> str:
  presentation = (
    _phase159_r1_7c_r3_presentation(
      n,
      k,
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def _phase159_r1_7c_r3_proof_body(
  rendered: str,
) -> str:
  marker = "## 証明\n\n"

  assert marker in rendered

  return rendered.split(
    marker,
    1,
  )[1]


def test_phase159_r1_7c_r3_pi11_4_suppresses_known_pi10_3_ancestry():
  body = (
    _phase159_r1_7c_r3_proof_body(
      _phase159_r1_7c_r3_render(
        4,
        7,
      )
    )
  )

  assert (
    r"H: \pi_{10}^{3} \to \pi_{10}^{5}"
    not in body
  )
  assert (
    r"\Delta: \pi_{10}^{5} \to \pi_{8}^{2}"
    not in body
  )
  assert (
    r"\pi_{10}^{3} \xrightarrow{H} "
    r"\pi_{10}^{5} \xrightarrow{\Delta} "
    r"\pi_{8}^{2}"
    not in body
  )


def test_phase159_r1_7c_r3_pi11_4_specializes_aggregate_zero_premise():
  body = (
    _phase159_r1_7c_r3_proof_body(
      _phase159_r1_7c_r3_render(
        4,
        7,
      )
    )
  )

  assert (
    r"\pi_{10}^{3} = 0"
    in body
  )
  assert (
    r"\pi_{11}^{7} = 0"
    in body
  )
  assert (
    r"\pi_{n + 4}^{n} = 0"
    not in body
  )


def test_phase159_r1_7c_r3_pi11_4_renders_i11_decomposition_specialization():
  body = (
    _phase159_r1_7c_r3_proof_body(
      _phase159_r1_7c_r3_render(
        4,
        7,
      )
    )
  )
  specialized = (
    r"\pi_{10}^{3} \oplus "
    r"\pi_{11}^{7} "
    r"\xrightarrow{\cong} "
    r"\pi_{11}^{4}"
  )

  assert specialized in body
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である."
    not in body
  )
  assert (
    r"\pi_{11}^{4} = 0"
    in body
  )
  assert body.rstrip().endswith(
    r"$\square$"
  )


def test_phase159_r1_7c_r3_pi10_3_own_proof_keeps_exactness():
  body = (
    _phase159_r1_7c_r3_proof_body(
      _phase159_r1_7c_r3_render(
        3,
        7,
      )
    )
  )

  assert (
    r"\pi_{10}^{3} \xrightarrow{H} "
    r"\pi_{10}^{5} \xrightarrow{\Delta} "
    r"\pi_{8}^{2}"
    in body
  )


def test_phase159_r1_7c_r3_nonmatching_root_is_noop():
  presentation = (
    _phase159_r1_7c_r3_presentation(
      3,
      3,
    )
  )
  markdown = "sentinel"

  assert (
    specialize_toda_group_proof_narrative_root_zero_direct_premises(
      presentation,
      markdown,
    )
    == markdown
  )
