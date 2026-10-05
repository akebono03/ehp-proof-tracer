# Phase157-R5-R6 repair2 changed code

## Production target

`toda_group_proof_narrative_references.py`

### Changed function

The complete changed function is emitted after apply to:

`phase157_r5_r6_repair2_output/select_reference_statement_steps_after.txt`

Core rule:

```python
  used_candidate_step_ids = (
    boundary_used_step_ids
    | entry_external_used_step_ids
  )

  used_candidates = tuple(
    step
    for step in eligible_candidates
    if id(
      step
    ) in used_candidate_step_ids
  )

  if used_candidates:
    return used_candidates
```

This replaces the old priority rule that returned
`boundary_used_candidates` immediately and thereby discarded
other used fixed components from the same Reference entry.

## Test changes

### Phase157 R2

`test_phase157_r2_equation53_inventory_has_no_group_order_policy()`

Now expects four components and four roles:
- bracket definition: MEMBERSHIP
- pi6^3 membership: MEMBERSHIP
- Hopf relation: MAP_VALUE
- double relation: RELATION

### Phase157 R5-R6

The complete file is rewritten.

It requires:
- bracket definition is FIXED_STATEMENT;
- specialization remains PROOF_INTERNAL;
- the bracket formula appears in `[R1] (5.3)`;
- Phase156 public-boundary behavior remains: Lemma 5.2 internal proof is not expanded in the body.

### Phase144 legacy contract

Two tests are updated because their old expectation predates
the Phase156 public-boundary collapse.

They now require the definition to appear in the Reference section
rather than as `"$\\nu'$ を定める."` in the body.
