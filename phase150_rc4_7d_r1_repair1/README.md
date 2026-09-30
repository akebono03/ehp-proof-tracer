# Phase 150 RC4-7D R1 Repair 1

## Changed target

- `toda_group_proof_narrative_reason_renderer.py`
  - add `_toda_group_proof_narrative_reason_insertion_index`
  - replace the body of `insert_toda_group_proof_narrative_reason_prose`
- add `tests/test_phase150_rc4_7d_reason_hidden_conclusion_anchor.py`

No production import changes.

## Diagnosis

The failed test already proves that `MAP_STRUCTURE_DERIVATION` is built for
`pi_12^5`. Its own intermediate conclusion is not rendered in the Narrative,
so the old insertion function silently skipped the reason.

## Minimal repair

The insertion anchor is selected generically:

1. use the reason's own visible conclusion line when present;
2. otherwise follow proof dependency edges from premise to parent;
3. choose the nearest downstream conclusion that is actually visible;
4. if none is visible, do not insert.

No group-specific branch is introduced.

## Phase boundary

Reason classification, Argument ownership, transitions, contribution ordering,
RC5 naming, and RC6 formatting are unchanged. Repository-wide pytest is not
run in this substep.
