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


def test_phase144_5_r2_render_equivalent_transitions_are_not_numbered():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    r"$2\nu' = \eta_{3}^{3}\tag{"
    not in rendered
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5}\tag{"
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


def test_phase144_5_r2_reflexive_support_equations_are_not_numbered():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert (
    r"$\eta_{3}^{3} = \eta_{3}^{3}\tag{"
    not in rendered
  )
  assert (
    r"$\eta_{5} = \eta_{5}\tag{"
    not in rendered
  )


def test_phase144_5_r2_pi6_3_has_no_duplicate_equation_tags():
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

  assert len(
    tags
  ) == len(
    set(
      tags
    )
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
