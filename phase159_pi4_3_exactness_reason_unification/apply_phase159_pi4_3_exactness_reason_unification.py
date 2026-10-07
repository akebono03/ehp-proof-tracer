from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
TEST = ROOT / "tests" / "test_phase159_pi4_3_exactness_reason_unification.py"


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one match, found {count}"
        )
    return text.replace(old, new, 1)


def patch_reasons() -> None:
    text = REASONS.read_text(encoding="utf-8")

    old_import = '''from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)
'''
    new_import = '''from toda_rules import (
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)
'''
    text = replace_once(
        text,
        old_import,
        new_import,
        label="toda_rules import",
    )

    old_enum = '''  EXACTNESS_TO_MAP_PROPERTY = (
    "exactness_to_map_property"
  )
  INJECTIVE_IMAGE_ORDER = (
'''
    new_enum = '''  EXACTNESS_TO_MAP_PROPERTY = (
    "exactness_to_map_property"
  )
  EXACTNESS_TO_KERNEL = (
    "exactness_to_kernel"
  )
  INJECTIVE_IMAGE_ORDER = (
'''
    text = replace_once(
        text,
        old_enum,
        new_enum,
        label="reason kind",
    )

    anchor = '''def _injective_image_order_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
'''
    new_function = '''def _exactness_to_kernel_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  if not isinstance(
    conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  ):
    return None

  image_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaDeltaImageFreeCyclicStatement,
    )
  )
  exactness_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )

  compatible_pairs = []

  for image_premise in image_premises:
    image_statement = image_premise.conclusion
    image_map = image_statement.map

    for exactness_premise in exactness_premises:
      window = exactness_premise.conclusion.window

      if (
        image_map.source_group
        != window.source_term
        or image_map.target_group
        != window.middle_term
        or window.middle_term
        != conclusion.map.source_group
        or window.target_term
        != conclusion.map.target_group
        or image_statement.image_group
        != conclusion.kernel_group
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
          image_premise,
          exactness_premise,
        )
      )

  if len(
    compatible_pairs
  ) != 1:
    return None

  image_premise, exactness_premise = (
    compatible_pairs[0]
  )

  return TodaGroupProofNarrativeReason(
    kind=(
      TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
    ),
    premise_steps=(
      image_premise,
      exactness_premise,
    ),
    conclusion_step=proof_step,
  )


''' + anchor
    text = replace_once(
        text,
        anchor,
        new_function,
        label="exactness-to-kernel function insertion",
    )

    old_loop = '''    if exactness_reason is not None:
      append_if_visible(exactness_reason)

    injective_image_order_reason = (
'''
    new_loop = '''    if exactness_reason is not None:
      append_if_visible(exactness_reason)

    exactness_kernel_reason = (
      _exactness_to_kernel_reason(
        node.proof_step
      )
    )
    if exactness_kernel_reason is not None:
      append_if_visible(
        exactness_kernel_reason
      )

    injective_image_order_reason = (
'''
    text = replace_once(
        text,
        old_loop,
        new_loop,
        label="reason-sidecar integration",
    )

    REASONS.write_text(text, encoding="utf-8")


def patch_renderer() -> None:
    text = RENDERER.read_text(encoding="utf-8")

    old_imports = '''from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_expression_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
  TodaGroupProofNarrativeReasonSidecar,
)
'''
    new_imports = '''from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_expression_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
  TodaGroupProofNarrativeReasonSidecar,
)
from toda_proof_narrative_renderer import (
  render_toda_raw_group_structure_latex,
)
'''
    text = replace_once(
        text,
        old_imports,
        new_imports,
        label="reason renderer imports",
    )

    anchor = '''  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .INJECTIVE_IMAGE_ORDER
  ):
'''
    new_branch = '''  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_KERNEL
  ):
    if len(reason.premise_steps) != 2:
      return None

    image_statement = (
      reason.premise_steps[0].conclusion
    )
    exactness_statement = (
      reason.premise_steps[1].conclusion
    )
    conclusion = (
      reason.conclusion_step.conclusion
    )
    window = exactness_statement.window
    first_map_name = window.first_map.name
    second_map_name = window.second_map.name
    group_latex = (
      render_toda_raw_group_structure_latex(
        conclusion.kernel_group
      )
    )

    if (
      image_statement.image_group
      != conclusion.kernel_group
    ):
      return None

    return (
      "完全性より, "
      f"$\\\\ker {second_map_name}"
      f"=\\\\operatorname{{Im}}{first_map_name}"
      f"={group_latex}$ である."
    )

''' + anchor
    text = replace_once(
        text,
        anchor,
        new_branch,
        label="exactness-to-kernel rendering branch",
    )

    RENDERER.write_text(text, encoding="utf-8")


def install_test() -> None:
    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )


TEST_SOURCE = r'''import inspect

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
  TodaDeltaImageFreeCyclicStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionKernelFreeCyclicStatement,
)


def _pi4_3_reason_data():
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


def test_phase159_pi4_3_builds_generic_exactness_to_kernel_reason():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_reason_data()

  reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
    )
  )

  assert len(reasons) == 1
  reason = reasons[0]

  assert isinstance(
    reason.conclusion_step.conclusion,
    TodaSuspensionKernelFreeCyclicStatement,
  )
  assert len(reason.premise_steps) == 2
  assert isinstance(
    reason.premise_steps[0].conclusion,
    TodaDeltaImageFreeCyclicStatement,
  )
  assert isinstance(
    reason.premise_steps[1].conclusion,
    TodaProp42ExactnessStatement,
  )

  image_statement = (
    reason.premise_steps[0].conclusion
  )
  window = (
    reason.premise_steps[1]
    .conclusion
    .window
  )
  kernel_statement = (
    reason.conclusion_step.conclusion
  )

  assert (
    image_statement.map.source_group
    == window.source_term
  )
  assert (
    image_statement.map.target_group
    == window.middle_term
  )
  assert (
    window.middle_term
    == kernel_statement.map.source_group
  )
  assert (
    window.target_term
    == kernel_statement.map.target_group
  )
  assert (
    image_statement.image_group
    == kernel_statement.kernel_group
  )
  assert window.first_map.name == "Δ"
  assert window.second_map.name == "E"


def test_phase159_pi4_3_exactness_reason_is_visible_before_kernel_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi4_3_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_KERNEL
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
    "完全性より, "
  )
  assert (
    r"$\ker E=\operatorname{Im}Δ="
    in sentence
  )
  assert rendered.count(sentence) == 1

  kernel_conclusion = next(
    (
      paragraph
      for paragraph in rendered.split(
        "\n\n"
      )
      if (
        r"\ker\left(E: "
        in paragraph
      )
    ),
    None,
  )
  assert kernel_conclusion is not None
  assert (
    rendered.index(sentence)
    < rendered.index(kernel_conclusion)
  )


def test_phase159_exactness_to_kernel_builder_has_no_pi4_or_rule_name_special_case():
  import toda_group_proof_narrative_reasons as module

  source = inspect.getsource(
    module._exactness_to_kernel_reason
  )

  forbidden_fragments = (
    "(4, 3)",
    "pi4",
    "eta_2",
    "η₂",
    "inference_rule",
    ".rule",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
'''


def main() -> None:
    patch_reasons()
    patch_renderer()
    install_test()
    print(
        "Phase 159 pi_4^3 exactness reason unification applied."
    )


if __name__ == "__main__":
    main()
