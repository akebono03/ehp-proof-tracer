# Phase 150 RC4-7D Generic Reason Vocabulary Expansion R1

## Changes

Production files:

- `toda_group_proof_narrative_reasons.py`
  - `TodaGroupProofNarrativeReasonKind`
  - add `_aggregate_derivation_reason`
  - add `_final_result_derivation_reason`
  - `build_toda_group_proof_narrative_reason_sidecar`
- `toda_group_proof_narrative_reason_renderer.py`
  - `render_toda_group_proof_narrative_reason_sentence`

Test file:

- `tests/test_phase150_rc4_7d_generic_reason_vocabulary.py`

RC4-7C found no built reasons in the representative cases. R1 therefore adds three generic reason kinds: `MAP_STRUCTURE_DERIVATION`, `GROUP_ORDER_DERIVATION`, and `FINAL_RESULT_DERIVATION`.

The first two reuse the existing aggregate semantic kinds `MAP_TRANSPORT` and `GROUP_ORDER_TRANSPORT`. The final-result reason is a fallback for finite-cyclic equality conclusions with direct proof premises. Existing `FINAL_GROUP_STRUCTURE` remains preferred when its stronger conditions hold.

No group-specific or generator-specific branch is added.

## Changed import section

```python
from dataclasses import dataclass
from enum import Enum

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  Multiple,
)
from homotopy_groups import (
  FiniteCyclicGroup,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from toda_rules import (
  TodaDeltaZeroStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaProp42ExactnessStatement,
  TodaSuspensionInjectiveStatement,
)
from toda_group_proof_narrative_aggregate_semantics import (
  TodaGroupProofNarrativeAggregateSemanticKind,
  build_toda_group_proof_narrative_aggregate_semantic_sidecar,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeReferenceApplicationSemantic,
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
```

The new helper functions are inserted immediately before `build_toda_group_proof_narrative_reason_sidecar`.

## Completion criteria

- Focused RC4-7D tests pass.
- Related Narrative regressions pass.
- `pi_10^4` has a generic final-result reason.
- `pi_12^5` has map-structure and final-result reasons.
- `pi_16^9` has group-order and final-result reasons.
- Visible snapshots contain the new prose.
- No repository-wide test is run in this substep.

## Boundary

RC5 EHP semantic naming and RC6 equation-numbering/prose-format cleanup are not implemented here. Full repository tests remain reserved for the end of Phase 150.
