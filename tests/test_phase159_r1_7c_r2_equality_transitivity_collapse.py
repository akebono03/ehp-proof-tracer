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


def test_phase159_r1_7c_r2_pi6_3_collapses_local_transitivity_chain():
  rendered = _render(
    3,
    3,
  )
  expected = (
    "[R2] より, "
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5} "
    r"= \eta_{3}^{3}$."
  )

  assert expected in rendered
  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$."
    not in rendered
  )
  assert (
    r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$."
    not in rendered
  )
  assert "(1) と (2) より," not in rendered


def test_phase159_r1_7c_r2_pi11_4_exactness_contract_is_preserved():
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
    "\\[\n"
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}."
    "\n\\]"
    in rendered
  )


def test_phase159_r1_7c_r2_helper_has_no_group_or_theorem_special_case():
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
