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


def _reference(
  locator: str,
) -> LiteratureReference:
  return LiteratureReference(
    label="Toda " + locator,
    locator=locator,
  )


def _step(
  conclusion: str,
  reference: LiteratureReference,
  premises: tuple[ProofStep, ...] = (),
) -> ProofStep:
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name="Toda " + reference.locator + " test",
      literature_reference=reference,
    ),
  )


def test_phase156_r3_same_entry_internal_consumers_do_not_expand_public_selection():
  reference = _reference(
    "Proposition 5.6"
  )
  first = _step(
    "first internal statement",
    reference,
  )
  second = _step(
    "second internal statement",
    reference,
  )
  internal_parent = _step(
    "same-entry parent",
    reference,
    premises=(
      first,
      second,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      first,
      second,
      internal_parent,
    ),
  )
  edges = (
    TodaProofEdge(
      parent_step=internal_parent,
      premise_step=first,
      premise_index=0,
    ),
    TodaProofEdge(
      parent_step=internal_parent,
      premise_step=second,
      premise_index=1,
    ),
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
  )


def test_phase156_r3_entry_external_consumer_preserves_existing_used_candidate_priority():
  reference = _reference(
    "Proposition 5.15"
  )
  used = _step(
    "used ancestry statement",
    reference,
  )
  unused = _step(
    "unused ancestry statement",
    reference,
  )
  external_parent = _step(
    "same-reference but entry-external parent",
    reference,
    premises=(
      used,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      unused,
      used,
    ),
  )
  edge = TodaProofEdge(
    parent_step=external_parent,
    premise_step=used,
    premise_index=0,
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


def test_phase156_r3_all_boundary_consumed_statements_remain_selected():
  reference = _reference(
    "Proposition 5.6"
  )
  consumer_reference = _reference(
    "Proposition 5.8"
  )
  first = _step(
    "first boundary statement",
    reference,
  )
  second = _step(
    "second boundary statement",
    reference,
  )
  external_parent = _step(
    "external consumer",
    consumer_reference,
    premises=(
      first,
      second,
    ),
  )
  entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=reference,
    proof_steps=(
      first,
      second,
    ),
  )
  edges = (
    TodaProofEdge(
      parent_step=external_parent,
      premise_step=first,
      premise_index=0,
    ),
    TodaProofEdge(
      parent_step=external_parent,
      premise_step=second,
      premise_index=1,
    ),
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
