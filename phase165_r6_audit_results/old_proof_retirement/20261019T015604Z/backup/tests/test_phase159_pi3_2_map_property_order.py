from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


H_MAP = (
  r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
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
PI3_3_GROUP = (
  r"\pi_{3}^{3} = "
  r"\mathbb{Z}\{\iota_{3}\}"
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


def _paragraphs(
  body: str,
) -> tuple[str, ...]:
  return tuple(
    paragraph.strip()
    for paragraph in body.split(
      "\n\n"
    )
    if paragraph.strip()
  )


def _map_property_index(
  paragraphs: tuple[str, ...],
  property_text: str,
) -> int:
  matches = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if (
      H_MAP in paragraph
      and property_text in paragraph
    )
  )

  assert len(
    matches
  ) == 1

  return matches[
    0
  ]


def test_phase159_pi3_2_bijectivity_precedes_isomorphism():
  body = _phase159_pi3_2_public_body()
  paragraphs = _paragraphs(
    body
  )

  injective_index = _map_property_index(
    paragraphs,
    "は単射",
  )
  surjective_index = _map_property_index(
    paragraphs,
    "は全射",
  )
  isomorphism_index = _map_property_index(
    paragraphs,
    "は同型",
  )

  assert injective_index < isomorphism_index
  assert surjective_index < isomorphism_index


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


def test_phase159_pi3_2_definition_premises_are_local_to_semantic_consumer():
  body = _phase159_pi3_2_public_body()
  paragraphs = _paragraphs(
    body
  )

  group_matches = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if PI3_3_GROUP in paragraph
  )
  definition_matches = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if ETA2_DEFINITION in paragraph
  )

  assert len(
    group_matches
  ) == 1
  assert len(
    definition_matches
  ) == 1

  group_index = group_matches[
    0
  ]
  isomorphism_index = _map_property_index(
    paragraphs,
    "は同型",
  )
  definition_index = definition_matches[
    0
  ]
  surjective_index = _map_property_index(
    paragraphs,
    "は全射",
  )

  assert surjective_index < group_index
  assert group_index + 1 == isomorphism_index
  assert isomorphism_index + 1 == definition_index
