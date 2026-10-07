from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


ZERO_GROUP = (
  "[R1]より, "
  r"$\pi_{2}^{1} = 0$."
)
H_INJECTIVE = (
  "完全性より, "
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は単射."
)
E_ISOMORPHISM = (
  "[R1]より, "
  r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
  "は同型."
)
E_INJECTIVE = (
  r"$E: \pi_{1}^{1} \to \pi_{2}^{2}$ "
  "は単射."
)
DELTA_ZERO = (
  "完全性より, "
  r"$\Delta: \pi_{3}^{3} \to \pi_{1}^{1}$ "
  "は零写像."
)
H_SURJECTIVE = (
  "完全性より, "
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は全射."
)
H_ISOMORPHISM = (
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は同型."
)
PI3_TARGET = (
  "[R1]より, "
  r"$\pi_{3}^{3} = "
  r"\mathbb{Z}\{\iota_{3}\}$."
)
ETA2_DEFINITION = (
  "この同型写像により, "
  r"$H(\eta_{2}) = \iota_{3}$ "
  "となる "
  r"$\eta_{2} \in \pi_{3}^{2}$ "
  "が一意に存在する."
)
FINAL_GROUP = (
  "以上より, "
  r"$\pi_{3}^{2} = "
  r"\mathbb{Z}\{\eta_{2}\}$."
)


def _phase159_pi3_2_paragraphs() -> tuple[
  str,
  ...,
]:
  (
    presentation,
    _,
    _,
    _,
  ) = _method_evidence_data(
    2,
    1,
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  body = rendered.split(
    "\n## 証明\n",
    1,
  )[1]

  return tuple(
    paragraph.strip()
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )


def test_phase159_pi3_2_zero_group_immediately_precedes_h_injective():
  paragraphs = (
    _phase159_pi3_2_paragraphs()
  )

  assert (
    paragraphs.index(
      H_INJECTIVE
    )
    == paragraphs.index(
      ZERO_GROUP
    ) + 1
  )


def test_phase159_pi3_2_e_branch_stays_in_dependency_order():
  paragraphs = (
    _phase159_pi3_2_paragraphs()
  )

  assert (
    paragraphs.index(
      E_ISOMORPHISM
    )
    < paragraphs.index(
      E_INJECTIVE
    )
    < paragraphs.index(
      DELTA_ZERO
    )
    < paragraphs.index(
      H_SURJECTIVE
    )
  )
  assert (
    paragraphs.index(
      H_SURJECTIVE
    )
    == paragraphs.index(
      DELTA_ZERO
    ) + 1
  )


def test_phase159_pi3_2_bijectivity_precedes_isomorphism():
  paragraphs = (
    _phase159_pi3_2_paragraphs()
  )

  assert paragraphs.index(
    H_INJECTIVE
  ) < paragraphs.index(
    H_ISOMORPHISM
  )
  assert paragraphs.index(
    H_SURJECTIVE
  ) < paragraphs.index(
    H_ISOMORPHISM
  )


def test_phase159_pi3_2_definition_direct_premises_are_adjacent_in_proofstep_order():
  paragraphs = (
    _phase159_pi3_2_paragraphs()
  )

  h_isomorphism_index = paragraphs.index(
    H_ISOMORPHISM
  )
  pi3_target_index = paragraphs.index(
    PI3_TARGET
  )
  definition_index = paragraphs.index(
    ETA2_DEFINITION
  )

  assert (
    pi3_target_index
    == h_isomorphism_index + 1
  )
  assert (
    definition_index
    == pi3_target_index + 1
  )


def test_phase159_pi3_2_definition_precedes_final_group_and_qed_remains_last():
  paragraphs = (
    _phase159_pi3_2_paragraphs()
  )

  assert paragraphs.index(
    ETA2_DEFINITION
  ) < paragraphs.index(
    FINAL_GROUP
  )
  assert paragraphs[-1] == "□"
