from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _render(
  n: int,
) -> str:
  presentation, _, _, _ = (
    _method_evidence_data(
      n,
      2,
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase160_r9_pi7_5_uses_toda45_and_pi6_4_canonical_base():
  rendered = _render(
    5
  )

  assert (
    "**[R1] (4.5).**"
    in rendered
  )
  assert (
    "**[R2] Proposition 5.3.**"
    in rendered
  )
  assert (
    r"$\pi_{6}^{4} = "
    r"\mathbb{Z}/2\{\eta_{4}^{2}\}$."
    in rendered
  )


def test_phase160_r9_pi7_5_body_uses_eta_square_not_expanded_composition():
  rendered = _render(
    5
  )
  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"[R1]を $(n,m,k)=(4,5,2)$ "
    r"に適用すると, "
    r"$E: \pi_{6}^{4} "
    r"\to \pi_{7}^{5}$ は同型."
    in proof_body
  )
  assert (
    r"$E\eta_{4}^{2} = "
    r"\eta_{5}^{2}$."
    in proof_body
  )
  assert (
    r"$\pi_{7}^{5} = "
    r"\mathbb{Z}/2\{\eta_{5}^{2}\}$."
    in proof_body
  )
  assert (
    r"\eta_{5}\eta_{6}"
    not in proof_body
  )


def test_phase160_r9_pi8_6_uses_same_generic_stable_shape():
  rendered = _render(
    6
  )

  assert (
    r"$(n,m,k)=(4,6,2)"
    in rendered
  )
  assert (
    r"$E^{2}: \pi_{6}^{4} "
    r"\to \pi_{8}^{6}$ は同型."
    in rendered
  )
  assert (
    r"$E^{2}\eta_{4}^{2} = "
    r"\eta_{6}^{2}$."
    in rendered
  )
  assert (
    r"$\pi_{8}^{6} = "
    r"\mathbb{Z}/2\{\eta_{6}^{2}\}$."
    in rendered
  )


def test_phase160_r9_pi6_4_canonical_base_delegates_to_existing_renderer():
  rendered = _render(
    4
  )

  assert (
    r"$(n,m,k)=(4,4,2)"
    not in rendered
  )


def test_phase160_r9_k2_public_narrative_has_no_symbolic_or_expanded_generator():
  rendered = _render(
    5
  )

  assert (
    r"\pi_{n+2}^{n}"
    not in rendered
  )
  assert (
    r"\eta_{n}\eta_{n+1}"
    not in rendered
  )
  assert (
    r"\eta_{4}\eta_{5}"
    not in rendered
  )
