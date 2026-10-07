from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = ROOT / "tests" / "test_phase159_pi4_3_exactness_surjectivity_unification.py"


REASON_FUNCTION = r'''def _exactness_to_map_property_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  exactness_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  compatible_pairs = []

  if isinstance(
    conclusion,
    TodaSuspensionInjectiveStatement,
  ):
    zero_premises = tuple(
      premise
      for premise in proof_step.premises
      if isinstance(
        premise.conclusion,
        TodaDeltaZeroStatement,
      )
    )

    for zero_premise in zero_premises:
      zero_map = zero_premise.conclusion.map

      for exactness_premise in exactness_premises:
        window = exactness_premise.conclusion.window

        if (
          zero_map.source_group
          != window.source_term
          or zero_map.target_group
          != window.middle_term
          or window.middle_term
          != conclusion.map.source_group
          or window.target_term
          != conclusion.map.target_group
          or getattr(
            window.first_map,
            "name",
            None,
          )
          != "Δ"
          or getattr(
            window.second_map,
            "name",
            None,
          )
          != "E"
        ):
          continue

        compatible_pairs.append(
          (
            zero_premise,
            exactness_premise,
          )
        )

  elif isinstance(
    conclusion,
    TodaSuspensionSurjectiveStatement,
  ):
    zero_premises = tuple(
      premise
      for premise in proof_step.premises
      if isinstance(
        premise.conclusion,
        TodaPrimaryGroupZeroStatement,
      )
    )

    for zero_premise in zero_premises:
      zero_group = zero_premise.conclusion.group

      for exactness_premise in exactness_premises:
        window = exactness_premise.conclusion.window

        if (
          window.source_term
          != conclusion.map.source_group
          or window.middle_term
          != conclusion.map.target_group
          or zero_group
          != window.target_term
          or getattr(
            window.first_map,
            "name",
            None,
          )
          != "E"
          or getattr(
            window.second_map,
            "name",
            None,
          )
          != "H"
        ):
          continue

        compatible_pairs.append(
          (
            zero_premise,
            exactness_premise,
          )
        )

  else:
    return None

  if len(
    compatible_pairs
  ) != 1:
    return None

  zero_premise, exactness_premise = (
    compatible_pairs[0]
  )

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    ),
    premise_steps=(
      zero_premise,
      exactness_premise,
    ),
    conclusion_step=proof_step,
  )


'''

RENDERER_BRANCH = r'''  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    if len(reason.premise_steps) != 2:
      return None

    exactness_statement = (
      reason.premise_steps[1].conclusion
    )
    window = exactness_statement.window
    first_map_name = window.first_map.name
    second_map_name = window.second_map.name
    conclusion = reason.conclusion_step.conclusion

    if isinstance(
      conclusion,
      TodaSuspensionInjectiveStatement,
    ):
      return (
        "この完全性と "
        f"${first_map_name}=0$ より, "
        f"$\\ker {second_map_name}"
        f"=\\operatorname{{Im}}{first_map_name}=0$.\n"
        "したがって, "
      )

    if isinstance(
      conclusion,
      TodaSuspensionSurjectiveStatement,
    ):
      zero_statement = (
        reason.premise_steps[0].conclusion
      )
      zero_group_latex = (
        render_toda_primary_group_latex(
          zero_statement.group
        )
      )
      middle_group_latex = (
        render_toda_primary_group_latex(
          window.middle_term
        )
      )

      return (
        "この完全性と "
        f"${zero_group_latex}=0$ より, "
        f"$\\operatorname{{Im}}{first_map_name}"
        f"=\\ker {second_map_name}"
        f"={middle_group_latex}$.\n"
        "したがって, "
      )

    return None

'''

NORMALIZER = r'''
def _normalize_exactness_to_map_property_reason_prose(
  markdown: str,
  reason: TodaGroupProofNarrativeReason,
) -> str:
  if (
    reason.kind
    is not TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    return markdown

  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  if sentence is None:
    return markdown

  lines = sentence.splitlines()

  while (
    lines
    and lines[-1].strip()
    in {
      "以上より,",
      "したがって,",
      "これより,",
      "これらより,",
    }
  ):
    lines.pop()

  reason_body = "\n".join(
    lines
  ).strip()

  if not reason_body:
    return markdown

  paragraphs = markdown.split(
    "\n\n"
  )
  matching_indices = tuple(
    index
    for index, paragraph in enumerate(
      paragraphs
    )
    if paragraph.strip() == reason_body
  )

  if len(matching_indices) != 1:
    return markdown

  reason_index = matching_indices[0]

  if (
    reason_index > 0
    and paragraphs[
      reason_index - 1
    ].strip()
    == "これより,"
  ):
    paragraphs.pop(
      reason_index - 1
    )

  return "\n\n".join(
    paragraphs
  )


'''

TEST_SOURCE = r'''import inspect

from homotopy_groups import (
  TodaPrimaryGroupZeroStatement,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_rules import (
  TodaProp42ExactnessStatement,
  TodaSuspensionSurjectiveStatement,
)


def _pi4_3_surjectivity_reason_data():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    1,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  return (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  )


def test_phase159_pi4_3_builds_exactness_to_surjectivity_reason():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_surjectivity_reason_data()

  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and isinstance(
        reason.conclusion_step.conclusion,
        TodaSuspensionSurjectiveStatement,
      )
    )
  )

  assert len(reasons) == 1
  reason = reasons[0]

  assert len(reason.premise_steps) == 2
  assert isinstance(
    reason.premise_steps[0].conclusion,
    TodaPrimaryGroupZeroStatement,
  )
  assert isinstance(
    reason.premise_steps[1].conclusion,
    TodaProp42ExactnessStatement,
  )

  zero_group = (
    reason.premise_steps[0].conclusion.group
  )
  window = (
    reason.premise_steps[1].conclusion.window
  )
  surjective_map = (
    reason.conclusion_step.conclusion.map
  )

  assert (
    window.source_term
    == surjective_map.source_group
  )
  assert (
    window.middle_term
    == surjective_map.target_group
  )
  assert zero_group == window.target_term
  assert window.first_map.name == "E"
  assert window.second_map.name == "H"


def test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_surjectivity_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and isinstance(
        reason.conclusion_step.conclusion,
        TodaSuspensionSurjectiveStatement,
      )
    )
  )
  sentence = (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
  )
  rendered = (
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )

  assert sentence is not None
  assert sentence.startswith(
    "この完全性と "
  )
  assert r"$\pi_{4}^{5}=0$" in sentence
  assert (
    r"$\operatorname{Im}E=\ker H=\pi_{4}^{3}$."
    in sentence
  )
  assert rendered.count(sentence) == 1
  assert (
    "これより, この完全性と "
    not in rendered
  )

  conclusion = (
    "$E: \\pi_{3}^{2} \\to \\pi_{4}^{3}$ "
    "は全射."
  )
  assert conclusion in rendered
  assert rendered.index(sentence) < rendered.index(
    conclusion
  )


def test_phase159_exactness_to_map_property_builder_has_no_pi4_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module._exactness_to_map_property_reason
  )

  forbidden_fragments = (
    "(4, 3)",
    "pi4",
    "eta_2",
    "η₂",
    "Proposition 5.1",
    "inference_rule",
    ".rule",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
'''


def insert_import_item(
    text: str,
    block_start: str,
    item_line: str,
) -> str:
    if item_line in text:
        return text

    start = text.find(block_start)
    if start < 0:
        raise RuntimeError(
            f"import block not found: {block_start}"
        )

    end = text.find(")\n", start)
    if end < 0:
        raise RuntimeError(
            f"import block end not found: {block_start}"
        )

    return (
        text[:end]
        + item_line
        + text[end:]
    )


def replace_function(
    text: str,
    name: str,
    replacement: str,
) -> str:
    marker = f"def {name}("
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(
            f"function not found: {name}"
        )

    next_def = text.find(
        "\ndef ",
        start + len(marker),
    )
    if next_def < 0:
        raise RuntimeError(
            f"next function not found after: {name}"
        )

    return (
        text[:start]
        + replacement
        + text[next_def + 1:]
    )


def replace_renderer_branch(
    text: str,
) -> str:
    kind_marker = (
        "  if (\n"
        "    reason.kind\n"
        "    is TodaGroupProofNarrativeReasonKind\n"
        "    .EXACTNESS_TO_MAP_PROPERTY\n"
        "  ):\n"
    )
    start = text.find(kind_marker)
    if start < 0:
        raise RuntimeError(
            "EXACTNESS_TO_MAP_PROPERTY renderer branch not found"
        )

    next_marker = (
        "  if (\n"
        "    reason.kind\n"
        "    is TodaGroupProofNarrativeReasonKind\n"
        "    .EXACTNESS_TO_KERNEL\n"
        "  ):\n"
    )
    end = text.find(
        next_marker,
        start + len(kind_marker),
    )

    if end < 0:
        next_marker = (
            "  if (\n"
            "    reason.kind\n"
            "    is TodaGroupProofNarrativeReasonKind\n"
            "    .INJECTIVE_IMAGE_ORDER\n"
            "  ):\n"
        )
        end = text.find(
            next_marker,
            start + len(kind_marker),
        )

    if end < 0:
        raise RuntimeError(
            "next reason renderer branch not found"
        )

    return (
        text[:start]
        + RENDERER_BRANCH
        + "\n"
        + text[end:]
    )


def ensure_post_normalizer(
    text: str,
) -> str:
    call = (
        "      _normalize_exactness_to_map_property_reason_prose(\n"
        "        rendered,\n"
        "        reason,\n"
        "      )"
    )
    if call in text:
        return text

    kernel_loop = (
        "  for reason in reason_sidecar.reasons:\n"
        "    rendered = (\n"
        "      _normalize_exactness_to_kernel_reason_prose(\n"
    )

    insertion = (
        "  for reason in reason_sidecar.reasons:\n"
        "    rendered = (\n"
        "      _normalize_exactness_to_map_property_reason_prose(\n"
        "        rendered,\n"
        "        reason,\n"
        "      )\n"
        "    )\n\n"
    )

    if kernel_loop in text:
        return text.replace(
            kernel_loop,
            insertion + kernel_loop,
            1,
        )

    return_marker = "\n  return rendered\n"
    index = text.rfind(
        return_marker
    )
    if index < 0:
        raise RuntimeError(
            "insert reason prose return marker not found"
        )

    return (
        text[:index]
        + "\n"
        + insertion
        + text[index:]
    )


def main() -> None:
    reasons_text = REASONS.read_text(
        encoding="utf-8"
    )

    reasons_text = insert_import_item(
        reasons_text,
        "from homotopy_groups import (\n",
        "  TodaPrimaryGroupZeroStatement,\n",
    )
    reasons_text = insert_import_item(
        reasons_text,
        "from toda_rules import (\n",
        "  TodaSuspensionSurjectiveStatement,\n",
    )
    reasons_text = replace_function(
        reasons_text,
        "_exactness_to_map_property_reason",
        REASON_FUNCTION,
    )

    REASONS.write_text(
        reasons_text,
        encoding="utf-8",
    )

    renderer_text = RENDERER.read_text(
        encoding="utf-8"
    )

    if "from toda_rules import (\n" not in renderer_text:
        anchor = (
            "from toda_group_proof_narrative_reasons import (\n"
        )
        index = renderer_text.find(anchor)
        if index < 0:
            raise RuntimeError(
                "renderer import anchor not found"
            )
        renderer_text = (
            renderer_text[:index]
            + "from toda_rules import (\n"
            + "  TodaSuspensionInjectiveStatement,\n"
            + "  TodaSuspensionSurjectiveStatement,\n"
            + ")\n"
            + renderer_text[index:]
        )
    else:
        renderer_text = insert_import_item(
            renderer_text,
            "from toda_rules import (\n",
            "  TodaSuspensionInjectiveStatement,\n",
        )
        renderer_text = insert_import_item(
            renderer_text,
            "from toda_rules import (\n",
            "  TodaSuspensionSurjectiveStatement,\n",
        )

    if "render_toda_primary_group_latex," not in renderer_text:
        if "from toda_proof_narrative_renderer import (\n" in renderer_text:
            renderer_text = insert_import_item(
                renderer_text,
                "from toda_proof_narrative_renderer import (\n",
                "  render_toda_primary_group_latex,\n",
            )
        else:
            anchor = (
                "from toda_group_proof_narrative_reasons import (\n"
            )
            index = renderer_text.find(anchor)
            renderer_text = (
                renderer_text[:index]
                + "from toda_proof_narrative_renderer import (\n"
                + "  render_toda_primary_group_latex,\n"
                + ")\n"
                + renderer_text[index:]
            )

    renderer_text = replace_renderer_branch(
        renderer_text
    )

    if (
        "def _normalize_exactness_to_map_property_reason_prose("
        not in renderer_text
    ):
        marker = (
            "def _normalize_exactness_to_kernel_reason_prose("
        )
        index = renderer_text.find(marker)
        if index < 0:
            marker = (
                "def insert_toda_group_proof_narrative_reason_prose("
            )
            index = renderer_text.find(marker)
        if index < 0:
            raise RuntimeError(
                "normalizer insertion marker not found"
            )
        renderer_text = (
            renderer_text[:index]
            + NORMALIZER
            + renderer_text[index:]
        )

    renderer_text = ensure_post_normalizer(
        renderer_text
    )

    RENDERER.write_text(
        renderer_text,
        encoding="utf-8",
    )

    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 pi_4^3 exactness-to-surjectivity "
        "unification applied."
    )


if __name__ == "__main__":
    main()
