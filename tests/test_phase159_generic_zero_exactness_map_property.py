from homotopy_groups import (
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
