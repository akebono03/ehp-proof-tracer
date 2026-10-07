from __future__ import annotations
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
RENDERER = ROOT / "toda_group_proof_narrative_reason_renderer.py"
PHASE150_TEST = ROOT / "tests" / "test_phase150_rc4_5c_2_exactness_to_map_property.py"
PHASE159_SURJ_TEST = ROOT / "tests" / "test_phase159_pi4_3_exactness_surjectivity_unification.py"
NEW_TEST = ROOT / "tests" / "test_phase159_generic_zero_exactness_map_property.py"

REASON_FUNCTION = r"""def _exactness_to_map_property_reason(
  proof_step: ProofStep,
) -> TodaGroupProofNarrativeReason | None:
  conclusion = proof_step.conclusion

  injective_types = (
    TodaDeltaInjectiveStatement,
    TodaHopfInvariantInjectiveStatement,
    TodaSuspensionInjectiveStatement,
  )
  surjective_types = (
    TodaDeltaSurjectiveStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaSuspensionSurjectiveStatement,
  )
  zero_map_types = (
    TodaDeltaZeroStatement,
    TodaHopfInvariantZeroStatement,
    TodaSuspensionZeroStatement,
  )

  if isinstance(conclusion, injective_types):
    conclusion_kind = "injective"
  elif isinstance(conclusion, surjective_types):
    conclusion_kind = "surjective"
  else:
    return None

  exactness_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      TodaProp42ExactnessStatement,
    )
  )
  zero_premises = tuple(
    premise
    for premise in proof_step.premises
    if isinstance(
      premise.conclusion,
      (
        TodaPrimaryGroupZeroStatement,
        *zero_map_types,
      ),
    )
  )

  compatible_pairs = []

  for zero_premise in zero_premises:
    zero_statement = zero_premise.conclusion

    for exactness_premise in exactness_premises:
      window = exactness_premise.conclusion.window
      conclusion_map = conclusion.map

      if conclusion_kind == "injective":
        if (
          conclusion_map.source_group
          != window.middle_term
          or conclusion_map.target_group
          != window.target_term
          or getattr(
            conclusion_map,
            "name",
            None,
          )
          != getattr(
            window.second_map,
            "name",
            None,
          )
        ):
          continue

        if isinstance(
          zero_statement,
          TodaPrimaryGroupZeroStatement,
        ):
          if zero_statement.group != window.source_term:
            continue
        else:
          zero_map = zero_statement.map
          if (
            zero_map.source_group
            != window.source_term
            or zero_map.target_group
            != window.middle_term
            or getattr(
              zero_map,
              "name",
              None,
            )
            != getattr(
              window.first_map,
              "name",
              None,
            )
          ):
            continue

      else:
        if (
          conclusion_map.source_group
          != window.source_term
          or conclusion_map.target_group
          != window.middle_term
          or getattr(
            conclusion_map,
            "name",
            None,
          )
          != getattr(
            window.first_map,
            "name",
            None,
          )
        ):
          continue

        if isinstance(
          zero_statement,
          TodaPrimaryGroupZeroStatement,
        ):
          if zero_statement.group != window.target_term:
            continue
        else:
          zero_map = zero_statement.map
          if (
            zero_map.source_group
            != window.middle_term
            or zero_map.target_group
            != window.target_term
            or getattr(
              zero_map,
              "name",
              None,
            )
            != getattr(
              window.second_map,
              "name",
              None,
            )
          ):
            continue

      compatible_pairs.append(
        (
          zero_premise,
          exactness_premise,
        )
      )

  if len(compatible_pairs) != 1:
    return None

  zero_premise, exactness_premise = compatible_pairs[0]

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


"""

RENDERER_BRANCH = r"""  if (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  ):
    if len(reason.premise_steps) != 2:
      return None

    conclusion = (
      _render_generic_narrative_step(
        reason.conclusion_step
      )
    )
    if not conclusion:
      return None

    concise_conclusion = conclusion

    for verbose, concise in (
      (" は単射である.", " は単射."),
      (" は全射である.", " は全射."),
    ):
      if concise_conclusion.endswith(
        verbose
      ):
        concise_conclusion = (
          concise_conclusion[
            :-len(verbose)
          ]
          + concise
        )
        break

    return (
      "完全性より, "
      + concise_conclusion
    )

"""

PHASE150_VISIBLE_TEST = r"""def test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
    reason_sidecar,
  ) = _pi6_reason_data()

  reason = next(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
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

  assert sentence == (
    "完全性より, "
    "$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
  )
  assert rendered.count(sentence) == 1
  assert (
    "この完全性と $Δ=0$ より"
    not in rendered
  )


"""

PHASE159_SURJ_VISIBLE_TEST = r"""def test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector():
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

  assert sentence == (
    "完全性より, "
    "$E: \pi_{3}^{2} \to \pi_{4}^{3}$ は全射."
  )
  assert rendered.count(sentence) == 1
  assert "この完全性と " not in rendered
  assert (
    "これより, 完全性より,"
    not in rendered
  )


"""

NEW_TEST_SOURCE = r"""from homotopy_groups import (
  TodaDeltaMap,
  TodaEHPExactnessWindow,
  TodaHopfInvariantMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
  TodaSuspensionMap,
)
from map_facts import (
  EHP_DELTA_MAP,
  EHP_E_MAP,
  EHP_H_MAP,
)
from proof import (
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_reason_renderer import (
  render_toda_group_proof_narrative_reason_sentence,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  _exactness_to_map_property_reason,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionSurjectiveStatement,
)


def _step(
  conclusion,
) -> ProofStep:
  return ProofStep(
    conclusion=conclusion,
    premises=(),
    rule=ProofRule.GIVEN,
  )


def _groups():
  a = TodaPrimaryGroup(
    group_dimension=10,
    sphere_dimension=4,
  )
  b = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=5,
  )
  c = TodaPrimaryGroup(
    group_dimension=11,
    sphere_dimension=11,
  )
  return a, b, c


def _e_h_exactness():
  a, b, c = _groups()
  exactness = TodaProp42ExactnessStatement(
    window=TodaEHPExactnessWindow(
      source_term=a,
      middle_term=b,
      target_term=c,
      first_map=EHP_E_MAP,
      second_map=EHP_H_MAP,
    ),
  )
  return a, b, c, exactness


def test_phase159_zero_left_group_plus_exactness_implies_second_map_injective():
  a, b, c, exactness = _e_h_exactness()
  proof_step = ProofStep(
    conclusion=TodaHopfInvariantInjectiveStatement(
      map=TodaHopfInvariantMap(
        source_group=b,
        target_group=c,
      ),
    ),
    premises=(
      _step(
        TodaPrimaryGroupZeroStatement(
          group=a,
        )
      ),
      _step(exactness),
    ),
    rule=ProofRule.INFERENCE,
  )

  reason = _exactness_to_map_property_reason(
    proof_step
  )

  assert reason is not None
  assert (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .EXACTNESS_TO_MAP_PROPERTY
  )


def test_phase159_zero_first_map_plus_exactness_implies_second_map_injective():
  source = TodaPrimaryGroup(
    group_dimension=7,
    sphere_dimension=5,
  )
  middle = TodaPrimaryGroup(
    group_dimension=5,
    sphere_dimension=2,
  )
  target = TodaPrimaryGroup(
    group_dimension=6,
    sphere_dimension=3,
  )
  exactness = TodaProp42ExactnessStatement(
    window=TodaEHPExactnessWindow(
      source_term=source,
      middle_term=middle,
      target_term=target,
      first_map=EHP_DELTA_MAP,
      second_map=EHP_E_MAP,
    ),
  )
  proof_step = ProofStep(
    conclusion=TodaSuspensionInjectiveStatement(
      map=TodaSuspensionMap(
        source_group=middle,
        target_group=target,
      ),
    ),
    premises=(
      _step(
        TodaDeltaZeroStatement(
          map=TodaDeltaMap(
            source_group=source,
            target_group=middle,
          ),
        )
      ),
      _step(exactness),
    ),
    rule=ProofRule.INFERENCE,
  )

  reason = _exactness_to_map_property_reason(
    proof_step
  )

  assert reason is not None
  assert (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    == (
      "完全性より, "
      "$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
    )
  )


def test_phase159_zero_right_group_plus_exactness_implies_first_map_surjective():
  a, b, c, exactness = _e_h_exactness()
  proof_step = ProofStep(
    conclusion=TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=a,
        target_group=b,
      ),
    ),
    premises=(
      _step(
        TodaPrimaryGroupZeroStatement(
          group=c,
        )
      ),
      _step(exactness),
    ),
    rule=ProofRule.INFERENCE,
  )

  reason = _exactness_to_map_property_reason(
    proof_step
  )

  assert reason is not None
  assert (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    == (
      "完全性より, "
      "$E: \pi_{10}^{4} \to \pi_{11}^{5}$ は全射."
    )
  )


def test_phase159_zero_second_map_plus_exactness_implies_first_map_surjective():
  a, b, c, exactness = _e_h_exactness()
  proof_step = ProofStep(
    conclusion=TodaSuspensionSurjectiveStatement(
      map=TodaSuspensionMap(
        source_group=a,
        target_group=b,
      ),
    ),
    premises=(
      _step(
        TodaHopfInvariantZeroStatement(
          map=TodaHopfInvariantMap(
            source_group=b,
            target_group=c,
          ),
        )
      ),
      _step(exactness),
    ),
    rule=ProofRule.INFERENCE,
  )

  reason = _exactness_to_map_property_reason(
    proof_step
  )

  assert reason is not None
  assert (
    render_toda_group_proof_narrative_reason_sentence(
      reason
    )
    == (
      "完全性より, "
      "$E: \pi_{10}^{4} \to \pi_{11}^{5}$ は全射."
    )
  )
"""


def ensure_import_item(text, block_start, item):
  if item in text:
    return text
  start = text.find(block_start)
  if start < 0:
    raise RuntimeError(f"import block not found: {block_start}")
  end = text.find(")\n", start)
  if end < 0:
    raise RuntimeError(f"import block end not found: {block_start}")
  return text[:end] + item + text[end:]


def replace_function(text, function_name, replacement):
  marker = f"def {function_name}("
  start = text.find(marker)
  if start < 0:
    raise RuntimeError(f"function not found: {function_name}")
  next_def = text.find("\ndef ", start + len(marker))
  if next_def < 0:
    raise RuntimeError(f"next function not found after: {function_name}")
  return text[:start] + replacement + text[next_def + 1:]


def replace_reason_branch(text):
  marker = (
    "  if (\n"
    "    reason.kind\n"
    "    is TodaGroupProofNarrativeReasonKind\n"
    "    .EXACTNESS_TO_MAP_PROPERTY\n"
    "  ):\n"
  )
  start = text.find(marker)
  if start < 0:
    raise RuntimeError("EXACTNESS_TO_MAP_PROPERTY renderer branch not found")
  candidates = (
    "  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .EXACTNESS_TO_KERNEL\n  ):\n",
    "  if (\n    reason.kind\n    is TodaGroupProofNarrativeReasonKind\n    .INJECTIVE_IMAGE_ORDER\n  ):\n",
  )
  ends = [text.find(c, start + len(marker)) for c in candidates]
  ends = [x for x in ends if x >= 0]
  if not ends:
    raise RuntimeError("next reason renderer branch not found")
  end = min(ends)
  return text[:start] + RENDERER_BRANCH + "\n" + text[end:]


def main():
  reasons_text = REASONS.read_text(encoding="utf-8")
  reasons_text = ensure_import_item(
    reasons_text,
    "from homotopy_groups import (\n",
    "  TodaPrimaryGroupZeroStatement,\n",
  )
  for item in (
    "  TodaDeltaInjectiveStatement,\n",
    "  TodaDeltaSurjectiveStatement,\n",
    "  TodaHopfInvariantInjectiveStatement,\n",
    "  TodaHopfInvariantZeroStatement,\n",
    "  TodaSuspensionSurjectiveStatement,\n",
    "  TodaSuspensionZeroStatement,\n",
  ):
    reasons_text = ensure_import_item(
      reasons_text,
      "from toda_rules import (\n",
      item,
    )
  reasons_text = replace_function(
    reasons_text,
    "_exactness_to_map_property_reason",
    REASON_FUNCTION,
  )
  REASONS.write_text(reasons_text, encoding="utf-8")

  renderer_text = RENDERER.read_text(encoding="utf-8")
  renderer_text = replace_reason_branch(renderer_text)
  RENDERER.write_text(renderer_text, encoding="utf-8")

  phase150_text = PHASE150_TEST.read_text(encoding="utf-8")
  phase150_text = replace_function(
    phase150_text,
    "test_phase150_rc4_5c_2_exactness_reason_is_visible_before_injective_conclusion",
    PHASE150_VISIBLE_TEST,
  )
  PHASE150_TEST.write_text(phase150_text, encoding="utf-8")

  phase159_text = PHASE159_SURJ_TEST.read_text(encoding="utf-8")
  phase159_text = replace_function(
    phase159_text,
    "test_phase159_pi4_3_surjectivity_reason_is_visible_without_double_connector",
    PHASE159_SURJ_VISIBLE_TEST,
  )
  PHASE159_SURJ_TEST.write_text(phase159_text, encoding="utf-8")

  NEW_TEST.write_text(NEW_TEST_SOURCE, encoding="utf-8")
  print("Phase 159 generic zero/exactness map-property unification applied.")


if __name__ == "__main__":
  main()
