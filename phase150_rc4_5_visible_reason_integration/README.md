# Phase 150 / RC4-5 — Cross-group audit + visible Narrative integration

## Changed files

- New: `toda_group_proof_narrative_reason_renderer.py`
- Changed: `toda_group_proof_narrative_contribution_renderer.py`
- New: `tests/test_phase150_rc4_5_visible_reasons.py`

The new renderer file contains the complete new functions. The changed existing
function is shown below in full.

```python
def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )
  contribution_markdown = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base_markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  return insert_toda_group_proof_narrative_reason_prose(
    contribution_markdown,
    reason_sidecar,
  )

```

## Import additions

The changed import portion is:

```python
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
```

## Visible behavior

A typed `DEFINITION_APPLICABILITY` reason now renders:

`この前提条件を満たすので、次の定義を用いる.`

No `pi_6^3`, `nu'`, proposition-number, or rendered-text special case is used.

## Boundary

No RC3 ordering changes, no RC5 EHP naming, no RC6 numbering changes, and no
repository-wide pytest run.
