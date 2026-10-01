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


def _step(
  name: str,
  premises: tuple[ProofStep, ...] = (),
) -> ProofStep:
  return ProofStep(
    conclusion=name,
    premises=premises,
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=name,
    ),
  )


def _entry(
  proof_steps: tuple[ProofStep, ...],
) -> TodaGroupProofNarrativeReferenceEntry:
  return TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=LiteratureReference(
      label="Toda test reference",
      locator="Proposition X",
    ),
    proof_steps=proof_steps,
  )


def test_phase153_r3_3_single_candidate_is_selected():
  candidate = _step(
    "candidate",
  )
  entry = _entry(
    (
      candidate,
    )
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        candidate,
      ),
      (),
    )
  )

  assert selected == (
    candidate,
  )


def test_phase153_r3_3_proof_used_candidate_is_preferred():
  unused = _step(
    "unused",
  )
  used = _step(
    "used",
  )
  parent = _step(
    "parent",
    premises=(
      used,
    ),
  )
  edge = TodaProofEdge(
    parent_step=parent,
    premise_step=used,
    premise_index=0,
  )
  entry = _entry(
    (
      unused,
      used,
    )
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        unused,
        used,
      ),
      (
        edge,
      ),
    )
  )

  assert selected == (
    used,
  )


def test_phase153_r3_3_keeps_all_distinct_proof_used_candidates_in_entry_order():
  first = _step(
    "first",
  )
  second = _step(
    "second",
  )
  parent = _step(
    "parent",
    premises=(
      second,
      first,
    ),
  )
  edges = (
    TodaProofEdge(
      parent_step=parent,
      premise_step=second,
      premise_index=0,
    ),
    TodaProofEdge(
      parent_step=parent,
      premise_step=first,
      premise_index=1,
    ),
  )
  entry = _entry(
    (
      first,
      second,
    )
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        first,
        second,
      ),
      edges,
    )
  )

  assert selected == (
    first,
    second,
  )


def test_phase153_r3_3_falls_back_to_first_candidate_when_none_is_proof_used():
  first = _step(
    "first",
  )
  second = _step(
    "second",
  )
  unrelated = _step(
    "unrelated",
  )
  parent = _step(
    "parent",
    premises=(
      unrelated,
    ),
  )
  edge = TodaProofEdge(
    parent_step=parent,
    premise_step=unrelated,
    premise_index=0,
  )
  entry = _entry(
    (
      first,
      second,
    )
  )

  selected = (
    select_toda_group_proof_narrative_reference_statement_steps(
      entry,
      (
        first,
        second,
      ),
      (
        edge,
      ),
    )
  )

  assert selected == (
    first,
  )
