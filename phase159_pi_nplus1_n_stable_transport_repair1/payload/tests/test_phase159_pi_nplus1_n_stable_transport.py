import pytest

from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


@pytest.mark.parametrize(
  "n",
  (
    4,
    5,
    6,
  ),
)
def test_phase159_pi_nplus1_n_uses_common_toda45_transport_proof(
  n,
):
  presentation, _, _, _ = (
    _method_evidence_data(
      n,
      1,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  exponent = n - 3

  assert "**[R1] (4.5).**" in rendered
  assert (
    "$n \\ge k + 2$ のとき,"
    in rendered
  )
  assert (
    "$E^{m - n}: \\pi_{n + k}^{n} "
    "\\to \\pi_{m + k}^{m}$ は同型."
    in rendered
  )
  assert (
    "**[R2] Proposition 5.1.**"
    in rendered
  )
  assert (
    "$\\pi_{4}^{3} = "
    "\\mathbb{Z}/2\\{\\eta_{3}\\}$."
    in rendered
  )
  assert (
    f"$(n,m,k)=(3,{n},1)$"
    in rendered
  )
  assert (
    f"E^{{{exponent}}}: "
    f"\\pi_{{4}}^{{3}} \\longrightarrow "
    f"\\pi_{{{n + 1}}}^{{{n}}}"
    in rendered
  )
  assert (
    f"E^{{{exponent}}}\\eta_{{3}} "
    f"= \\eta_{{{n}}}."
    in rendered
  )
  final_result = (
    f"\\pi_{{{n + 1}}}^{{{n}}} "
    f"= \\mathbb{{Z}}/2\\{{\\eta_{{{n}}}\\}}."
  )
  assert rendered.count(
    final_result
  ) == 2
  assert "\\tag{" not in rendered


def test_phase159_pi5_4_does_not_rederive_generic_target_family_in_body():
  presentation, _, _, _ = (
    _method_evidence_data(
      4,
      1,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{E^{n - 3}\eta_{3}\}"
    not in proof_body
  )
  assert (
    r"\pi_{n + 1}^{n} = "
    r"\mathbb{Z}/2\{\eta_{n}\}"
    not in proof_body
  )
  assert (
    r"E^{n - 3}: \pi_{3 + 1}^{3} "
    r"\to \pi_{n + 1}^{n}"
    not in rendered
  )


def test_phase159_pi4_3_remains_on_existing_narrative_route():
  presentation, _, _, _ = (
    _method_evidence_data(
      3,
      1,
    )
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  assert (
    r"\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}."
    in rendered
  )
  assert (
    r"\operatorname{Im}\Delta"
    in rendered
  )
  assert "**[R1] (4.5).**" not in rendered
