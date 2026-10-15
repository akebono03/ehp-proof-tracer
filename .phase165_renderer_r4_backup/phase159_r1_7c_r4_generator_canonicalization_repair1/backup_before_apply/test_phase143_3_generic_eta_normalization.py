import inspect

from expression import Composition, GeneratorSymbol, HomotopyElement
from toda_calculation_facade import build_standard_toda_report
import toda_group_proof_generic_narrative_renderer as generic_renderer
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_eta_composition_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def _eta(index: int) -> HomotopyElement:
  return HomotopyElement(
    name="eta",
    dimension=index,
    source=index + 1,
    target=index,
    generator=GeneratorSymbol(family="η", index=index),
  )


def _pi6_3_steps():
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(group_result, max_depth=3)
  presentation = build_toda_group_proof_presentation(replay)
  return tuple(node.proof_step for node in presentation.nodes)


def test_phase143_3_compacts_two_consecutive_eta_factors():
  expression = Composition(left=_eta(7), right=_eta(8))
  assert _render_generic_eta_composition_latex(expression) == r"\eta_{7}^{2}"


def test_phase143_3_compacts_three_consecutive_eta_factors():
  expression = Composition(
    left=_eta(7),
    right=Composition(left=_eta(8), right=_eta(9)),
  )
  assert _render_generic_eta_composition_latex(expression) == r"\eta_{7}^{3}"


def test_phase143_3_accepts_other_composition_association():
  expression = Composition(
    left=Composition(left=_eta(7), right=_eta(8)),
    right=_eta(9),
  )
  assert _render_generic_eta_composition_latex(expression) == r"\eta_{7}^{3}"


def test_phase143_3_does_not_compact_nonconsecutive_eta_factors():
  expression = Composition(left=_eta(7), right=_eta(9))
  assert _render_generic_eta_composition_latex(expression) is None


def test_phase143_3_pi6_3_generic_step_uses_eta_cube():
  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in _pi6_3_steps()
  )
  assert any(r"\eta_{3}^{3}" in rendered for rendered in rendered_steps)
  assert all(
    r"\eta_{3}\eta_{4}\eta_{5}" not in rendered
    for rendered in rendered_steps
  )


def test_phase143_3_has_no_pi6_or_fixed_eta_replacement_table():
  source = inspect.getsource(
    generic_renderer._render_generic_eta_composition_latex
  )
  for fragment in (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    r"\eta_{2}\eta_{3}",
    r"\eta_{3}\eta_{4}",
    r"\eta_{3}\eta_{4}\eta_{5}",
  ):
    assert fragment not in source


def test_phase143_3_normalizer_ignores_non_expression_relation_side():
  steps = _pi6_3_steps()

  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in steps
  )

  assert len(rendered_steps) == len(steps)
