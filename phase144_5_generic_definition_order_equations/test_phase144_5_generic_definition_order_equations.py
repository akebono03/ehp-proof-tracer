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


def test_phase144_5_equation_numbering_is_generic_and_sequential():
  markdown = (
    "$a=b$\\n\\n"
    "したがって、\\n\\n"
    "$c=d$"
  )

  rendered = (
    number_toda_group_proof_narrative_equations(
      markdown
    )
  )

  assert "$a=b\\\\tag{1}$" in rendered
  assert "$c=d\\\\tag{2}$" in rendered


def test_phase144_5_equation_reference_uses_parenthesized_number():
  assert (
    toda_group_proof_narrative_equation_reference(
      7
    )
    == "(7)"
  )


def test_phase144_5_pi6_3_generic_argument_narrative_has_definition_purpose():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert "$\\\\nu'$ を定める." in rendered


def test_phase144_5_pi6_3_generic_argument_narrative_has_order_purpose():
  rendered = _render_multi_argument(
    3,
    3,
  )

  assert "$\\\\nu'$ の位数を決定する." in rendered


def test_phase144_5_pi6_3_generic_argument_narrative_numbers_equations():
  rendered = _render_multi_argument(
    3,
    3,
  )

  tags = tuple(
    int(
      value
    )
    for value in re.findall(
      r"\\\\tag\\{(\\d+)\\}",
      rendered,
    )
  )

  assert tags
  assert tags == tuple(
    range(
      1,
      len(
        tags
      ) + 1,
    )
  )


def test_phase144_5_generic_numbering_has_no_pi6_target_hardcoding():
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
