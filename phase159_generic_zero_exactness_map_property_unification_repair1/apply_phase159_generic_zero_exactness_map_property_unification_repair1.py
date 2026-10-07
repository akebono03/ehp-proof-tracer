from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REASONS = ROOT / "toda_group_proof_narrative_reasons.py"
TEST = ROOT / "tests" / "test_phase159_generic_zero_exactness_map_property.py"


NEW_FUNCTION = r'''def _exactness_to_map_property_reason(
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

  def map_name(
    group_map,
  ) -> str | None:
    if isinstance(
      group_map,
      TodaSuspensionMap,
    ):
      return "E"

    if isinstance(
      group_map,
      TodaHopfInvariantMap,
    ):
      return "H"

    if isinstance(
      group_map,
      TodaDeltaMap,
    ):
      return "Δ"

    return getattr(
      group_map,
      "name",
      None,
    )

  if isinstance(
    conclusion,
    injective_types,
  ):
    conclusion_kind = "injective"
  elif isinstance(
    conclusion,
    surjective_types,
  ):
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
          or map_name(
            conclusion_map
          )
          != map_name(
            window.second_map
          )
        ):
          continue

        if isinstance(
          zero_statement,
          TodaPrimaryGroupZeroStatement,
        ):
          if (
            zero_statement.group
            != window.source_term
          ):
            continue
        else:
          zero_map = zero_statement.map

          if (
            zero_map.source_group
            != window.source_term
            or zero_map.target_group
            != window.middle_term
            or map_name(
              zero_map
            )
            != map_name(
              window.first_map
            )
          ):
            continue

      else:
        if (
          conclusion_map.source_group
          != window.source_term
          or conclusion_map.target_group
          != window.middle_term
          or map_name(
            conclusion_map
          )
          != map_name(
            window.first_map
          )
        ):
          continue

        if isinstance(
          zero_statement,
          TodaPrimaryGroupZeroStatement,
        ):
          if (
            zero_statement.group
            != window.target_term
          ):
            continue
        else:
          zero_map = zero_statement.map

          if (
            zero_map.source_group
            != window.middle_term
            or zero_map.target_group
            != window.target_term
            or map_name(
              zero_map
            )
            != map_name(
              window.second_map
            )
          ):
            continue

      compatible_pairs.append(
        (
          zero_premise,
          exactness_premise,
        )
      )

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


TEST_SOURCE = r'''from homotopy_groups import (
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
      _step(
        exactness
      ),
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
      _step(
        exactness
      ),
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
      r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
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
      _step(
        exactness
      ),
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
      r"$E: \pi_{10}^{4} \to \pi_{11}^{5}$ は全射."
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
      _step(
        exactness
      ),
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
      r"$E: \pi_{10}^{4} \to \pi_{11}^{5}$ は全射."
    )
  )
'''


def ensure_import_item(
    text: str,
    block_start: str,
    item: str,
) -> str:
    if item in text:
        return text

    start = text.find(
        block_start
    )
    if start < 0:
        raise RuntimeError(
            f"import block not found: {block_start}"
        )

    end = text.find(
        ")\n",
        start,
    )
    if end < 0:
        raise RuntimeError(
            f"import block end not found: {block_start}"
        )

    return (
        text[:end]
        + item
        + text[end:]
    )


def replace_function(
    text: str,
    function_name: str,
    replacement: str,
) -> str:
    marker = f"def {function_name}("
    start = text.find(
        marker
    )

    if start < 0:
        raise RuntimeError(
            f"function not found: {function_name}"
        )

    next_def = text.find(
        "\ndef ",
        start + len(marker),
    )

    if next_def < 0:
        raise RuntimeError(
            f"next function not found after: {function_name}"
        )

    return (
        text[:start]
        + replacement
        + text[next_def + 1:]
    )


def main() -> None:
    reasons_text = REASONS.read_text(
        encoding="utf-8"
    )

    for item in (
        "  TodaDeltaMap,\n",
        "  TodaHopfInvariantMap,\n",
        "  TodaSuspensionMap,\n",
    ):
        reasons_text = ensure_import_item(
            reasons_text,
            "from homotopy_groups import (\n",
            item,
        )

    reasons_text = replace_function(
        reasons_text,
        "_exactness_to_map_property_reason",
        NEW_FUNCTION,
    )

    REASONS.write_text(
        reasons_text,
        encoding="utf-8",
    )

    TEST.write_text(
        TEST_SOURCE,
        encoding="utf-8",
    )

    print(
        "Phase 159 generic zero/exactness "
        "map-property unification repair1 applied."
    )


if __name__ == "__main__":
    main()
