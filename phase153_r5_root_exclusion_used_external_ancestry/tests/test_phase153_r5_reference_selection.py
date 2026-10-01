from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_proof_dependency import (
  TodaProofEdge,
)


def _reference():
  return LiteratureReference(
    label="Toda Proposition 5.15",
    locator="Proposition 5.15",
  )


def _step(
  conclusion,
  premises=(),
):
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="Toda Proposition 5.15 test",
      literature_reference=_reference(),
    ),
  )


def test_phase153_r5_root_is_excluded_when_external_used_candidate_exists():
  external_step = _step(
    "external ancestry statement"
  )
  root_step = _step(
    "root statement",
    premises=(
      external_step,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(),
    proof_steps=(
      root_step,
      external_step,
    ),
  )
  edge = TodaProofEdge(
    parent_step=root_step,
    premise_step=external_step,
    premise_index=0,
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        root_step,
        external_step,
      ),
      (
        edge,
      ),
      root_step=root_step,
    )
  )

  assert selected == (
    external_step,
  )


def test_phase153_r5_root_only_candidate_produces_no_external_statement():
  root_step = _step(
    "root statement"
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(),
    proof_steps=(
      root_step,
    ),
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        root_step,
      ),
      (),
      root_step=root_step,
    )
  )

  assert selected == ()


def test_phase153_r5_used_external_candidate_is_preferred_over_unused_external_candidate():
  used_step = _step(
    "used external ancestry statement"
  )
  unused_step = _step(
    "unused external statement"
  )
  parent_step = _step(
    "parent statement",
    premises=(
      used_step,
    ),
  )
  root_step = _step(
    "root statement",
    premises=(
      parent_step,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(),
    proof_steps=(
      root_step,
      unused_step,
      used_step,
    ),
  )
  edges = (
    TodaProofEdge(
      parent_step=root_step,
      premise_step=parent_step,
      premise_index=0,
    ),
    TodaProofEdge(
      parent_step=parent_step,
      premise_step=used_step,
      premise_index=0,
    ),
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        root_step,
        unused_step,
        used_step,
      ),
      edges,
      root_step=root_step,
    )
  )

  assert selected == (
    used_step,
  )


def test_phase153_r5_old_selector_call_remains_backward_compatible():
  candidate_step = _step(
    "candidate statement"
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(),
    proof_steps=(
      candidate_step,
    ),
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        candidate_step,
      ),
      (),
    )
  )

  assert selected == (
    candidate_step,
  )
