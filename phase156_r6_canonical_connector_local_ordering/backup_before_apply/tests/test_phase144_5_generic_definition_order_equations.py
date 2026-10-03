import inspect
import re

from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_equation_numbering import (
  number_toda_group_proof_narrative_equations,
  toda_group_proof_narrative_equation_reference,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _render_multi_argument(
  n,
  k,
):
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    n,
    k,
  )

  return (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )


def test_phase144_5_r2_numbers_only_calculation_chain_equations():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert r"$2\nu' = \eta_{3}E\eta_{3}\eta_{5}\tag{1}$" in rendered
  assert (
    r"$\eta_{3}E\eta_{3}\eta_{5} = "
    r"\eta_{3}^{3}\tag{2}$"
    in rendered
  )
  assert "(1) と (2) より, " in rendered
  assert r"$2\nu' = \eta_{3}^{3}\tag{3}$" in rendered
  assert (
    r"$\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}\tag{"
    not in rendered
  )
  assert (
    r"$\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}\tag{"
    not in rendered
  )


def test_phase144_5_r2_equation_reference_uses_parenthesized_number():
  assert (
    toda_group_proof_narrative_equation_reference(
      7
    )
    == "(7)"
  )


def test_phase144_5_r2_pi6_3_keeps_definition_and_order_purposes():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert r"$\nu'$ を定める." in rendered
  assert (
    r"$\nu'$ の位数を決定するために, "
    r"次の完全列を考える."
    in rendered
  )


def test_phase144_5_r2_pi6_3_uses_actual_equation_references():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert "(1) と (2) より, " in rendered
  assert "(4) と (5) より, " in rendered
  assert r"$2\nu' = \eta_{3}^{3}\tag{3}$" in rendered
  assert (
    r"$H\left(\nu'\right) = \eta_{5}\tag{6}$"
    in rendered
  )


def test_phase144_5_r2_pi6_3_does_not_number_every_display_equation():
  rendered = _render_multi_argument(
    3,
    3,
  )

  tags = tuple(
    int(
      value
    )
    for value in re.findall(
      r"\\tag\{(\d+)\}",
      rendered,
    )
  )

  assert tags == (
    1,
    2,
    3,
    4,
    5,
    6,
  )
  assert (
    r"\pi_{4}^{3} = \mathbb{Z}/2\{\eta_{3}\}\tag{"
    not in rendered
  )
  assert (
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}\tag{"
    not in rendered
  )


def test_phase144_5_r2_numbering_has_no_target_hardcoding():
  source = inspect.getsource(
    number_toda_group_proof_narrative_equations
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
