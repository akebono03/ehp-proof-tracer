from pathlib import Path
import re


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

RENDERER = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
TEST_FILE = REPO_ROOT / "tests" / "test_phase159_pi3_2_map_property_order.py"


NEW_FUNCTION = r"""def _phase159_reorder_unique_preimage_definition_premise_locality(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]
  had_trailing_newline = (
    rendered.endswith(
      "\n"
    )
  )
  paragraphs = proof_body.rstrip(
    "\n"
  ).split(
    "\n\n"
  )

  for node in semantic_presentation.nodes:
    consumer_step = node.proof_step
    consumer_line = (
      _phase159_unique_preimage_definition_line(
        consumer_step
      )
    )

    if consumer_line is None:
      continue

    group_map = getattr(
      consumer_step.conclusion,
      "map",
      None,
    )

    if group_map is None:
      continue

    isomorphism_premise = next(
      (
        premise_step
        for premise_step in consumer_step.premises
        if (
          isinstance(
            premise_step,
            ProofStep,
          )
          and isinstance(
            premise_step.conclusion,
            _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
          )
          and getattr(
            premise_step.conclusion,
            "map",
            None,
          )
          == group_map
        )
      ),
      None,
    )

    if isomorphism_premise is None:
      continue

    ordered_premises = (
      tuple(
        premise_step
        for premise_step in consumer_step.premises
        if premise_step is not isomorphism_premise
      )
      + (
        isomorphism_premise,
      )
    )

    consumer_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if consumer_line in paragraph
    )

    if len(
      consumer_matches
    ) != 1:
      continue

    premise_rows = []

    for premise_step in ordered_premises:
      premise_line = (
        _render_generic_narrative_step(
          premise_step
        )
      )

      if not premise_line:
        premise_rows = []
        break

      premise_matches = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if premise_line in paragraph
      )

      if len(
        premise_matches
      ) != 1:
        premise_rows = []
        break

      premise_rows.append(
        (
          premise_step,
          premise_matches[
            0
          ],
          paragraphs[
            premise_matches[
              0
            ]
          ],
        )
      )

    if len(
      premise_rows
    ) != len(
      ordered_premises
    ):
      continue

    premise_indices = tuple(
      row[
        1
      ]
      for row in premise_rows
    )

    if len(
      set(
        premise_indices
      )
    ) != len(
      premise_indices
    ):
      continue

    if consumer_matches[
      0
    ] in premise_indices:
      continue

    premise_paragraph_by_step_id = {
      id(
        premise_step
      ): paragraph
      for (
        premise_step,
        _,
        paragraph,
      ) in premise_rows
    }

    for premise_index in sorted(
      premise_indices,
      reverse=True,
    ):
      paragraphs.pop(
        premise_index
      )

    consumer_matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if consumer_line in paragraph
    )

    if len(
      consumer_matches
    ) != 1:
      continue

    consumer_index = consumer_matches[
      0
    ]

    for premise_step in ordered_premises:
      paragraphs.insert(
        consumer_index,
        premise_paragraph_by_step_id[
          id(
            premise_step
          )
        ],
      )
      consumer_index += 1

  result = (
    prefix
    + "\n\n".join(
      paragraphs
    )
  )

  if had_trailing_newline:
    result += "\n"

  return result
"""


NEW_TEST_FILE = r"""from tests.test_phase143_19_method_evidence import (
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
"""


def insert_function_if_needed(
  text: str,
) -> str:
  name = (
    "def _phase159_reorder_unique_preimage_definition_premise_locality("
  )

  if name in text:
    return text

  marker = (
    "def _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions("
  )

  if marker not in text:
    raise RuntimeError(
      "Could not find locality-function insertion marker."
    )

  return text.replace(
    marker,
    NEW_FUNCTION
    + "\n\n"
    + marker,
    1,
  )


def insert_render_call_if_needed(
  text: str,
) -> str:
  call = (
    "    _phase159_reorder_unique_preimage_definition_premise_locality(\n"
    "      presentation,\n"
    "      rendered,\n"
    "    )"
  )

  if call in text:
    return text

  function_start = text.find(
    "def render_toda_group_proof_narrative_markdown("
  )

  if function_start < 0:
    raise RuntimeError(
      "Could not find render_toda_group_proof_narrative_markdown()."
    )

  function_text = text[
    function_start:
  ]

  anchor = (
    "  rendered = (\n"
    "    _phase158_normalize_public_narrative_contract(\n"
    "      presentation,\n"
    "      rendered,\n"
    "    )\n"
    "  )\n"
  )

  anchor_index = function_text.find(
    anchor
  )

  if anchor_index < 0:
    raise RuntimeError(
      "Could not find normalize-public-contract anchor "
      "inside render_toda_group_proof_narrative_markdown()."
    )

  insertion = (
    anchor
    + "  rendered = (\n"
    + call
    + "\n"
    + "  )\n"
  )

  absolute_index = (
    function_start
    + anchor_index
  )

  return (
    text[
      :absolute_index
    ]
    + function_text[
      :anchor_index
    ]
    + insertion
    + function_text[
      anchor_index + len(
        anchor
      ):
    ]
  )


def main() -> None:
  renderer_text = RENDERER.read_text(
    encoding="utf-8"
  )

  renderer_text = insert_function_if_needed(
    renderer_text
  )
  renderer_text = insert_render_call_if_needed(
    renderer_text
  )

  RENDERER.write_text(
    renderer_text,
    encoding="utf-8",
  )

  TEST_FILE.write_text(
    NEW_TEST_FILE,
    encoding="utf-8",
  )

  print(
    "Applied semantic definition-premise locality repair1."
  )
  print(
    "Updated: toda_group_proof_narrative_renderer.py"
  )
  print(
    "Updated: tests/test_phase159_pi3_2_map_property_order.py"
  )


if __name__ == "__main__":
  main()
