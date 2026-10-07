import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_collapse_equality_transitivity_chains,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
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


def test_phase159_r1_7c_r2_repair6_pi6_3_uses_public_semantic_chain():
  rendered = _render(
    3,
    3,
  )

  expected = (
    r"[R2] より, "
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5} "
    r"= \eta_{3}^{3}$."
  )

  assert expected in rendered
  assert (
    r"\eta_{3}E\eta_{3}\eta_{5}"
    not in rendered
  )
  assert "(1) と (2) より," not in rendered


def test_phase159_r1_7c_r2_repair6_identity_transitivity_stays_compact():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in rendered
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5} = \eta_{5}$."
    not in rendered
  )


def test_phase159_r1_7c_r2_repair6_preserves_pi6_map_property_contract():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射."
    in rendered
  )


def test_phase159_r1_7c_r2_repair6_preserves_pi11_exactness_contract():
  rendered = _render(
    4,
    7,
  )

  assert (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
    in rendered
  )
  assert (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は全射."
    in rendered
  )


def test_phase159_r1_7c_r2_repair6_has_no_group_or_theorem_special_case():
  source = inspect.getsource(
    _phase159_r1_7c_collapse_equality_transitivity_chains
  )

  forbidden = (
    "pi6",
    "(6, 3)",
    "nu_prime",
    "ν'",
    "Proposition 5.6",
    "Proposition 5.15",
  )

  for fragment in forbidden:
    assert fragment not in source
