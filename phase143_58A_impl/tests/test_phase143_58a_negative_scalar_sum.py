from expression import (
  ScalarSum,
  ScalarSymbol,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def test_phase143_58a_negative_scalar_sum_renders_as_subtraction():
  value = ScalarSum(
    left=ScalarSymbol(
      "i"
    ),
    right=-1,
  )

  assert (
    _render_scalar_latex(
      value
    )
    == "i - 1"
  )


def test_phase143_58a_positive_scalar_sum_keeps_existing_rendering():
  value = ScalarSum(
    left=ScalarSymbol(
      "i"
    ),
    right=1,
  )

  assert (
    _render_scalar_latex(
      value
    )
    == "i + 1"
  )


def test_phase143_58a_pi6_3_narrative_normalizes_negative_scalar_sum():
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
    r"$\pi_{i - 1}^{1} = 0$"
    in rendered
  )
  assert "i + -1" not in rendered
