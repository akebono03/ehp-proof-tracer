from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _render(
  n: int,
  k: int,
) -> str:
  presentation, _, _, _ = (
    _method_evidence_data(
      n,
      k,
    )
  )

  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase160_r7_pi17_10_uses_general_toda45_and_canonical_base():
  rendered = _render(
    10,
    7,
  )

  assert (
    "**[R1] (4.5).**"
    in rendered
  )
  assert (
    r"$n \ge k + 2$ のとき, "
    r"$E^{m-n}: "
    r"\pi_{n+k}^{n} "
    r"\to "
    r"\pi_{m+k}^{m}$ は同型."
    in rendered
  )
  assert (
    "**[R2] Proposition 5.15.**"
    in rendered
  )
  assert (
    r"$\pi_{16}^{9} = "
    r"\mathbb{Z}/16\{\sigma_{9}\}$."
    in rendered
  )


def test_phase160_r7_pi17_10_body_is_concrete_stable_transport():
  rendered = _render(
    10,
    7,
  )

  proof_body = rendered.split(
    "## 証明\n\n",
    1,
  )[1]

  assert (
    r"[R1]を $(n,m,k)=(9,10,7)$ "
    r"に適用すると, "
    r"$E: \pi_{16}^{9} "
    r"\to \pi_{17}^{10}$ は同型."
    in proof_body
  )
  assert (
    r"$E\sigma_{9} = \sigma_{10}$."
    in proof_body
  )
  assert (
    r"$\pi_{17}^{10} = "
    r"\mathbb{Z}/16\{\sigma_{10}\}$."
    in proof_body
  )


def test_phase160_r7_pi17_10_omits_internal_symbolic_prose():
  rendered = _render(
    10,
    7,
  )

  assert (
    "σ-family の定義より"
    not in rendered
  )
  assert (
    "`σn`"
    not in rendered
  )
  assert (
    "`σ9`"
    not in rendered
  )
  assert (
    "`πn+7n`"
    not in rendered
  )
  assert (
    r"\pi_{n+7}^{n}"
    not in rendered
  )


def test_phase160_r7_pi18_11_uses_same_generic_stable_shape():
  rendered = _render(
    11,
    7,
  )

  assert (
    r"$(n,m,k)=(9,11,7)"
    in rendered
  )
  assert (
    r"$E^{2}: \pi_{16}^{9} "
    r"\to \pi_{18}^{11}$ は同型."
    in rendered
  )
  assert (
    r"$E^{2}\sigma_{9} = "
    r"\sigma_{11}$."
    in rendered
  )
  assert (
    r"$\pi_{18}^{11} = "
    r"\mathbb{Z}/16\{\sigma_{11}\}$."
    in rendered
  )


def test_phase160_r7_pi5_4_preserves_phase159_contract():
  rendered = _render(
    4,
    1,
  )

  assert (
    "**[R2] Proposition 5.1.**"
    in rendered
  )
  assert (
    r"$\pi_{4}^{3} = "
    r"\mathbb{Z}/2\{\eta_{3}\}$."
    in rendered
  )
  assert (
    r"$(n,m,k)=(3,4,1)"
    in rendered
  )
  assert (
    r"$E: \pi_{4}^{3} "
    r"\to \pi_{5}^{4}$ は同型."
    in rendered
  )
  assert (
    r"$E\eta_{3} = \eta_{4}$."
    in rendered
  )
  assert (
    r"$\pi_{5}^{4} = "
    r"\mathbb{Z}/2\{\eta_{4}\}$."
    in rendered
  )


def test_phase160_r7_canonical_bases_delegate_to_existing_renderer():
  pi4_3 = _render(
    3,
    1,
  )
  pi16_9 = _render(
    9,
    7,
  )

  assert (
    r"$(n,m,k)=(3,3,1)"
    not in pi4_3
  )
  assert (
    r"$(n,m,k)=(9,9,7)"
    not in pi16_9
  )
