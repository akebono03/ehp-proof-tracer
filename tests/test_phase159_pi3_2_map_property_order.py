from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


H_INJECTIVE = (
  "完全性より, "
  r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
  "は単射."
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


def _phase159_pi3_2_public_body() -> str:
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

  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase159_pi3_2_bijectivity_precedes_isomorphism():
  body = _phase159_pi3_2_public_body()

  assert H_INJECTIVE in body
  assert H_SURJECTIVE in body
  assert H_ISOMORPHISM in body

  assert body.index(
    H_INJECTIVE
  ) < body.index(
    H_ISOMORPHISM
  )
  assert body.index(
    H_SURJECTIVE
  ) < body.index(
    H_ISOMORPHISM
  )


def test_phase159_pi3_2_isomorphism_precedes_eta2_definition_and_final_group():
  body = _phase159_pi3_2_public_body()

  assert H_ISOMORPHISM in body
  assert ETA2_DEFINITION in body
  assert FINAL_GROUP in body

  assert body.index(
    H_ISOMORPHISM
  ) < body.index(
    ETA2_DEFINITION
  )
  assert body.index(
    ETA2_DEFINITION
  ) < body.index(
    FINAL_GROUP
  )
