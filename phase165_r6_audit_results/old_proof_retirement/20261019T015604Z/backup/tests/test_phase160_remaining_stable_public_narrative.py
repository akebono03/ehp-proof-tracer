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


def test_phase160_r10_three_stem_public_narrative():
  rendered = _render(
    6,
    3,
  )

  assert (
    "**[R2] Proposition 5.6.**"
    in rendered
  )
  assert (
    r"$\pi_{8}^{5} = "
    r"\mathbb{Z}/8\{\nu_{5}\}$."
    in rendered
  )
  assert (
    r"$(n,m,k)=(5,6,3)"
    in rendered
  )
  assert (
    r"$E\nu_{5} = \nu_{6}$."
    in rendered
  )
  assert (
    r"$\pi_{9}^{6} = "
    r"\mathbb{Z}/8\{\nu_{6}\}$."
    in rendered
  )


def test_phase160_r10_four_stem_public_narrative():
  rendered = _render(
    7,
    4,
  )

  assert (
    "**[R2] Proposition 5.8.**"
    in rendered
  )
  assert (
    r"$\pi_{10}^{6} = 0$."
    in rendered
  )
  assert (
    r"$(n,m,k)=(6,7,4)"
    in rendered
  )
  assert (
    r"$E: \pi_{10}^{6} "
    r"\to \pi_{11}^{7}$ は同型."
    in rendered
  )
  assert (
    r"$\pi_{11}^{7} = 0$."
    in rendered
  )


def test_phase160_r10_five_stem_public_narrative():
  rendered = _render(
    8,
    5,
  )

  assert (
    "**[R2] Proposition 5.9.**"
    in rendered
  )
  assert (
    r"$\pi_{12}^{7} = 0$."
    in rendered
  )
  assert (
    r"$(n,m,k)=(7,8,5)"
    in rendered
  )
  assert (
    r"$\pi_{13}^{8} = 0$."
    in rendered
  )


def test_phase160_r10_six_stem_public_narrative_uses_nu_square():
  rendered = _render(
    9,
    6,
  )

  assert (
    "**[R2] Proposition 5.11.**"
    in rendered
  )
  assert (
    r"$\pi_{14}^{8} = "
    r"\mathbb{Z}/2\{\nu_{8}^{2}\}$."
    in rendered
  )
  assert (
    r"$(n,m,k)=(8,9,6)"
    in rendered
  )
  assert (
    r"$E\nu_{8}^{2} = "
    r"\nu_{9}^{2}$."
    in rendered
  )
  assert (
    r"$\pi_{15}^{9} = "
    r"\mathbb{Z}/2\{\nu_{9}^{2}\}$."
    in rendered
  )
  assert (
    r"\nu_{9}\nu_{12}"
    not in rendered
  )


def test_phase160_r10_canonical_bases_delegate():
  for n, k in (
    (
      5,
      3,
    ),
    (
      6,
      4,
    ),
    (
      7,
      5,
    ),
    (
      8,
      6,
    ),
  ):
    rendered = _render(
      n,
      k,
    )

    assert (
      (
        "$(n,m,k)=("
        + str(
          n
        )
        + ","
        + str(
          n
        )
        + ","
        + str(
          k
        )
        + ")"
      )
      not in rendered
    )
