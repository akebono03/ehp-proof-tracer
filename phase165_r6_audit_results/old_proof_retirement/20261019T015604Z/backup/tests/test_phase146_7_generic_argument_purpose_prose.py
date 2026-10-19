from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
)


def test_phase146_7_order_exactness_combines_purpose_and_method():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  rendered = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      sidecar,
      arguments,
    )
  )

  assert (
    "$\\nu'$ の位数を決定するために, "
    "次の完全列を考える."
    in rendered
  )
  assert (
    "$\\nu'$ の位数を決定する."
    "そのために, 次の完全列を考える."
    not in rendered
  )


def test_phase146_7_rule_is_not_pi6_specific():
  source = (
    __import__(
      "inspect"
    ).getsource(
      __import__(
        "toda_group_proof_narrative_argument_renderer"
      ).render_toda_group_proof_narrative_argument_header_method_section
    )
  )

  assert "nu_prime" not in source
  assert "ν′" not in source
  assert "pi6" not in source.lower()
  assert "group_dimension" not in source
  assert "sphere_dimension" not in source


def test_phase146_7_non_exactness_purpose_is_unchanged():
  (
    presentation,
    blocks,
    sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )

  definition_argument = next(
    argument
    for argument in arguments
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    )
  )

  assert definition_argument is not None
