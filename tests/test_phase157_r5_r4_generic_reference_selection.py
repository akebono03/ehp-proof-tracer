from proof import (
  InferenceRule,
  LiteratureReference,
  ProofRule,
  ProofStep,
)
from toda_group_proof_narrative_references import (
  TodaGroupProofNarrativeReferenceEntry,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage,
)


def _reference(
  locator: str,
) -> LiteratureReference:
  return LiteratureReference(
    label="Toda " + locator,
    locator=locator,
  )


def _step(
  rule_name: str,
  locator: str | None,
  conclusion: str,
  premises=(),
) -> ProofStep:
  return ProofStep(
    conclusion=conclusion,
    premises=premises,
    rule=ProofRule.INFERENCE,
    inference_rule=InferenceRule(
      name=rule_name,
      literature_reference=(
        None
        if locator is None
        else _reference(
          locator
        )
      ),
    ),
  )


def test_phase157_r5_r4_generic_filter_applies_without_representative_target_guard():
  root_step = _step(
    "Phase157 R5-R4 arbitrary root",
    None,
    "arbitrary non-representative target",
  )

  fixed_step = _step(
    'Toda 4.5 stable-range iterated suspension isomorphism',
    '(4.5)',
    "fixed candidate",
  )
  internal_step = _step(
    'Toda 4.5 pi_4^3 finite-cyclic transport',
    '(4.5)',
    "proof-internal candidate",
  )
  aggregate_step = _step(
    'Toda Proposition 5.3 finite-dimensional integration',
    'Proposition 5.3',
    "aggregate fixed statement without component",
  )

  fixed_entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(
      '(4.5)'
    ),
    proof_steps=(
      fixed_step,
    ),
  )
  internal_entry = TodaGroupProofNarrativeReferenceEntry(
    number=2,
    reference=_reference(
      '(4.5)'
    ),
    proof_steps=(
      internal_step,
    ),
  )
  aggregate_entry = TodaGroupProofNarrativeReferenceEntry(
    number=3,
    reference=_reference(
      'Proposition 5.3'
    ),
    proof_steps=(
      aggregate_step,
    ),
  )

  filtered = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      (
        fixed_entry,
        internal_entry,
        aggregate_entry,
      ),
      root_step,
    )
  )

  assert len(
    filtered
  ) == 1
  assert filtered[
    0
  ].number == 1
  assert filtered[
    0
  ].proof_steps == (
    fixed_step,
  )


def test_phase157_r5_r4_generic_restore_applies_without_representative_target_guard():
  used_step = _step(
    'Toda 4.5 stable-range iterated suspension isomorphism',
    '(4.5)',
    "used fixed candidate",
  )
  retained_step = _step(
    'Toda 4.5 stable-range iterated suspension isomorphism',
    '(4.5)',
    "retained fixed candidate",
  )
  root_step = _step(
    "Phase157 R5-R4 arbitrary root",
    None,
    "arbitrary non-representative target",
    premises=(
      used_step,
      retained_step,
    ),
  )

  used_entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=_reference(
      '(4.5)'
    ),
    proof_steps=(
      used_step,
    ),
  )
  retained_entry = TodaGroupProofNarrativeReferenceEntry(
    number=2,
    reference=_reference(
      '(4.5)'
    ),
    proof_steps=(
      retained_step,
    ),
  )
  filtered_retained_entry = TodaGroupProofNarrativeReferenceEntry(
    number=1,
    reference=retained_entry.reference,
    proof_steps=retained_entry.proof_steps,
  )

  (
    restored_entries,
    restored_lines,
    restored_body,
  ) = (
    restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(
      (
        used_entry,
        retained_entry,
      ),
      {
        1: (
          "used fixed",
        ),
        2: (
          "retained fixed",
        ),
      },
      (
        filtered_retained_entry,
      ),
      {
        1: (
          "retained fixed",
        ),
      },
      "uses [R1]",
      root_step,
      frozenset(
        {
          id(
            used_step
          ),
          id(
            retained_step
          ),
        }
      ),
    )
  )

  assert len(
    restored_entries
  ) == 2
  assert tuple(
    entry.number
    for entry in restored_entries
  ) == (
    1,
    2,
  )
  assert restored_lines == {
    1: (
      "used fixed",
    ),
    2: (
      "retained fixed",
    ),
  }
  assert restored_body == "uses [R2]"
