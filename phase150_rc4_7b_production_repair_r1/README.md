# Phase 150 RC4-7B Production Repair R1

## Target files

Production:

- `toda_group_proof_narrative_transition_renderer.py`
  - `render_toda_group_proof_narrative_transition_connector`

Tests:

- add `tests/test_phase150_rc4_7b_production_repair.py`

No other production file is changed.

## Scope

RC4-7B-7 showed that the relevant Arguments are not `DETACHED`.
RC4-7B-6 showed that DERIVATION sources reaching the body renderer are rendered.
The remaining gap is that a `SUPPORT` transition targeting the final `TARGET`
returns no connector, so the multi-Argument renderer does not pass the target
conclusion through its derivational rendering context.

This repair keeps the transition role as `SUPPORT`.
It only gives `SUPPORT -> TARGET` the same conclusion connector already used
for `DERIVATION`.

Definition-support transitions remain connector-free.
No group-specific branch is added.

## Changed import section

```python
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_transitions import (
  TodaGroupProofNarrativeTransition,
  TodaGroupProofNarrativeTransitionRole,
)
```

## Complete changed function

```python
def render_toda_group_proof_narrative_transition_connector(
  transition: TodaGroupProofNarrativeTransition,
) -> str | None:
  if not isinstance(
    transition,
    TodaGroupProofNarrativeTransition,
  ):
    raise TypeError(
      "transition must be a "
      "TodaGroupProofNarrativeTransition"
    )

  if (
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .DERIVATION
  ):
    return "以上より、"

  if (
    transition.role
    is TodaGroupProofNarrativeTransitionRole
    .SUPPORT
    and transition.target_block.role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .TARGET
  ):
    return "以上より、"

  if (
    transition.role
    in (
      TodaGroupProofNarrativeTransitionRole
      .SUPPORT,
      TodaGroupProofNarrativeTransitionRole
      .CALCULATION_CHAIN,
    )
  ):
    return None

  raise ValueError(
    "unsupported NarrativeTransition role"
  )
```

## New test file

The package contains the complete file:

- `test_phase150_rc4_7b_production_repair.py`

It verifies:

1. `SUPPORT -> TARGET` gets `以上より、`.
2. `SUPPORT -> DEFINITION` remains connector-free.

## Completion criteria

- The focused RC4-7B tests pass.
- Related Phase 143/144/147/148/150 Narrative tests pass.
- `pi_12^5` visible Narrative now receives a conclusion connector through the generic route.
- `pi_15^8` remains on its existing special renderer.
- No group-specific `pi_12^5` branch is introduced.
- Repository-wide tests are not run in this substep.

## Phase boundary

This repair does not implement RC5 EHP semantic naming.
It does not implement RC6 equation-numbering or general prose cleanup.
It does not change Argument ownership, child indices, discourse classification,
or transition role classification.
