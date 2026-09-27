from audit_phase144_6_r5_17e import (
  ArchitectureCandidate,
  ArchitectureDecision,
  architecture_criteria,
  audit_architecture_inputs,
  decide_architecture,
)


def test_phase144_6_r5_17e_audits_six_representative_groups():
  summary = audit_architecture_inputs()

  assert summary.group_count == 6
  assert summary.argument_count > 0
  assert summary.supporting_block_count > 0


def test_phase144_6_r5_17e_confirms_child_argument_composition_exists():
  summary = audit_architecture_inputs()

  assert summary.child_argument_edge_count > 0


def test_phase144_6_r5_17e_confirms_semantic_only_support_exists():
  summary = audit_architecture_inputs()

  assert summary.semantic_only_support_count > 0


def test_phase144_6_r5_17e_confirms_other_is_fully_explained():
  summary = audit_architecture_inputs()

  assert summary.other_provider_count == 9
  assert summary.aggregate_other_provider_count == 3
  assert summary.provenance_only_other_provider_count == 6
  assert summary.unresolved_other_provider_count == 0


def test_phase144_6_r5_17e_confirms_argument_local_body_boundaries():
  summary = audit_architecture_inputs()

  assert summary.local_body_boundary_violations == 0


def test_phase144_6_r5_17e_rejects_evidence_first_for_every_decision_criterion():
  summary = audit_architecture_inputs()
  criteria = architecture_criteria(summary)

  assert criteria
  assert all(
    criterion.evidence_first is ArchitectureDecision.REJECT
    for criterion in criteria
  )


def test_phase144_6_r5_17e_accepts_argument_first_for_every_decision_criterion():
  summary = audit_architecture_inputs()
  criteria = architecture_criteria(summary)

  assert all(
    criterion.argument_first is ArchitectureDecision.ACCEPT
    for criterion in criteria
  )


def test_phase144_6_r5_17e_selects_argument_first_architecture():
  summary = audit_architecture_inputs()

  assert decide_architecture(summary) is ArchitectureCandidate.ARGUMENT_FIRST
