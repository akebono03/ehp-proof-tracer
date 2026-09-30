from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_transition_renderer import (
  render_toda_group_proof_narrative_transition_connector,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransitionRole,
  extract_toda_group_proof_narrative_transitions,
)
from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)


def _phase150_rc4_7b_pi12_transitions():
  (
    presentation,
    blocks,
    _sidecar,
    arguments,
  ) = _method_evidence_data(
    5,
    7,
  )
  return extract_toda_group_proof_narrative_transitions(
    presentation,
    blocks,
    arguments,
  )


def test_phase150_rc4_7b_target_support_gets_conclusion_connector():
  transitions = _phase150_rc4_7b_pi12_transitions()

  target_support = next(
    transition
    for transition in transitions
    if (
      transition.role
      is TodaGroupProofNarrativeTransitionRole.SUPPORT
      and transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.TARGET
    )
  )

  assert (
    render_toda_group_proof_narrative_transition_connector(
      target_support
    )
    == "以上より、"
  )


def test_phase150_rc4_7b_definition_support_keeps_no_connector():
  transitions = _phase150_rc4_7b_pi12_transitions()

  definition_support = next(
    transition
    for transition in transitions
    if (
      transition.role
      is TodaGroupProofNarrativeTransitionRole.SUPPORT
      and transition.target_block.role
      is TodaGroupProofNarrativeMathematicalBlockRole.DEFINITION
    )
  )

  assert (
    render_toda_group_proof_narrative_transition_connector(
      definition_support
    )
    is None
  )
