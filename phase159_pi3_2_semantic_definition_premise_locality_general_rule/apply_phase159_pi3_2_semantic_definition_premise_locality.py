from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent

RENDERER = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
TEST_FILE = REPO_ROOT / "tests" / "test_phase159_pi3_2_map_property_order.py"

NEW_FUNCTION = 'def _phase159_reorder_unique_preimage_definition_premise_locality(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  proof_marker = "## 証明\\n\\n"\n  marker_index = rendered.find(\n    proof_marker\n  )\n\n  if marker_index < 0:\n    return rendered\n\n  semantic_presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  proof_start = (\n    marker_index\n    + len(\n      proof_marker\n    )\n  )\n  prefix = rendered[\n    :proof_start\n  ]\n  proof_body = rendered[\n    proof_start:\n  ]\n  had_trailing_newline = (\n    rendered.endswith(\n      "\\n"\n    )\n  )\n  paragraphs = proof_body.rstrip(\n    "\\n"\n  ).split(\n    "\\n\\n"\n  )\n\n  for node in semantic_presentation.nodes:\n    consumer_step = node.proof_step\n    consumer_line = (\n      _phase159_unique_preimage_definition_line(\n        consumer_step\n      )\n    )\n\n    if consumer_line is None:\n      continue\n\n    group_map = getattr(\n      consumer_step.conclusion,\n      "map",\n      None,\n    )\n\n    if group_map is None:\n      continue\n\n    isomorphism_premise = next(\n      (\n        premise_step\n        for premise_step in consumer_step.premises\n        if (\n          isinstance(\n            premise_step,\n            ProofStep,\n          )\n          and isinstance(\n            premise_step.conclusion,\n            _GENERIC_ISOMORPHISM_STATEMENT_TYPES,\n          )\n          and getattr(\n            premise_step.conclusion,\n            "map",\n            None,\n          )\n          == group_map\n        )\n      ),\n      None,\n    )\n\n    if isomorphism_premise is None:\n      continue\n\n    ordered_premises = (\n      tuple(\n        premise_step\n        for premise_step in consumer_step.premises\n        if premise_step is not isomorphism_premise\n      )\n      + (\n        isomorphism_premise,\n      )\n    )\n\n    if not ordered_premises:\n      continue\n\n    consumer_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if consumer_line in paragraph\n    )\n\n    if len(\n      consumer_matches\n    ) != 1:\n      continue\n\n    premise_rows = []\n\n    for premise_step in ordered_premises:\n      premise_line = (\n        _render_generic_narrative_step(\n          premise_step\n        )\n      )\n\n      if not premise_line:\n        premise_rows = []\n        break\n\n      premise_matches = tuple(\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if premise_line in paragraph\n      )\n\n      if len(\n        premise_matches\n      ) != 1:\n        premise_rows = []\n        break\n\n      premise_rows.append(\n        (\n          premise_step,\n          premise_matches[\n            0\n          ],\n          paragraphs[\n            premise_matches[\n              0\n            ]\n          ],\n        )\n      )\n\n    if len(\n      premise_rows\n    ) != len(\n      ordered_premises\n    ):\n      continue\n\n    premise_indices = tuple(\n      row[\n        1\n      ]\n      for row in premise_rows\n    )\n\n    if len(\n      set(\n        premise_indices\n      )\n    ) != len(\n      premise_indices\n    ):\n      continue\n\n    if consumer_matches[\n      0\n    ] in premise_indices:\n      continue\n\n    premise_paragraph_by_step_id = {\n      id(\n        premise_step\n      ): paragraph\n      for (\n        premise_step,\n        _,\n        paragraph,\n      ) in premise_rows\n    }\n\n    for premise_index in sorted(\n      premise_indices,\n      reverse=True,\n    ):\n      paragraphs.pop(\n        premise_index\n      )\n\n    consumer_matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if consumer_line in paragraph\n    )\n\n    if len(\n      consumer_matches\n    ) != 1:\n      continue\n\n    consumer_index = consumer_matches[\n      0\n    ]\n\n    for premise_step in ordered_premises:\n      paragraphs.insert(\n        consumer_index,\n        premise_paragraph_by_step_id[\n          id(\n            premise_step\n          )\n        ],\n      )\n      consumer_index += 1\n\n  result = (\n    prefix\n    + "\\n\\n".join(\n      paragraphs\n    )\n  )\n\n  if had_trailing_newline:\n    result += "\\n"\n\n  return result\n'
OLD_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_reorder_unique_preimage_definition_premise_locality(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n'
TEST_FUNCTION = 'def test_phase159_pi3_2_definition_premises_are_local_to_semantic_consumer():\n  body = _phase159_pi3_2_public_body()\n  paragraphs = tuple(\n    paragraph.strip()\n    for paragraph in body.split(\n      "\\n\\n"\n    )\n    if paragraph.strip()\n  )\n\n  group_structure = (\n    r"\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}"\n  )\n\n  group_index = next(\n    index\n    for index, paragraph in enumerate(\n      paragraphs\n    )\n    if group_structure in paragraph\n  )\n  isomorphism_index = next(\n    index\n    for index, paragraph in enumerate(\n      paragraphs\n    )\n    if H_ISOMORPHISM in paragraph\n  )\n  definition_index = next(\n    index\n    for index, paragraph in enumerate(\n      paragraphs\n    )\n    if ETA2_DEFINITION in paragraph\n  )\n  surjective_index = next(\n    index\n    for index, paragraph in enumerate(\n      paragraphs\n    )\n    if H_SURJECTIVE in paragraph\n  )\n\n  assert surjective_index < group_index\n  assert group_index + 1 == isomorphism_index\n  assert isomorphism_index + 1 == definition_index\n'


def main() -> None:
    renderer_text = RENDERER.read_text(encoding="utf-8")

    function_name = (
        "def _phase159_reorder_unique_preimage_definition_premise_locality("
    )

    if function_name not in renderer_text:
        insertion_marker = (
            "def _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions("
        )
        if insertion_marker not in renderer_text:
            raise RuntimeError(
                "Could not find insertion marker in "
                "toda_group_proof_narrative_renderer.py"
            )
        renderer_text = renderer_text.replace(
            insertion_marker,
            NEW_FUNCTION + "\n\n" + insertion_marker,
            1,
        )

    if NEW_RENDER not in renderer_text:
        if OLD_RENDER not in renderer_text:
            raise RuntimeError(
                "Could not find the current "
                "render_toda_group_proof_narrative_markdown() body."
            )
        renderer_text = renderer_text.replace(
            OLD_RENDER,
            NEW_RENDER,
            1,
        )

    RENDERER.write_text(
        renderer_text,
        encoding="utf-8",
    )

    test_text = TEST_FILE.read_text(
        encoding="utf-8",
    )

    test_name = (
        "def test_phase159_pi3_2_definition_premises_are_local_to_semantic_consumer():"
    )

    if test_name not in test_text:
        test_text = (
            test_text.rstrip()
            + "\n\n\n"
            + TEST_FUNCTION
            + "\n"
        )

    TEST_FILE.write_text(
        test_text,
        encoding="utf-8",
    )

    print("Applied semantic definition-premise locality rule.")
    print(f"Updated: {RENDERER.relative_to(REPO_ROOT)}")
    print(f"Updated: {TEST_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
