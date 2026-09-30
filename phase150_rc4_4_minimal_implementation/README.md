# Phase 150 / RC4-4 — Minimal implementation

This package introduces the minimal typed infrastructure for generic reason relations.

## Changed files

### New production file

- `toda_group_proof_narrative_reasons.py`

Adds:

- `TodaGroupProofNarrativeReasonKind`
- `TodaGroupProofNarrativeReason`
- `TodaGroupProofNarrativeReasonSidecar`
- `build_toda_group_proof_narrative_reason_sidecar(...)`

### New test file

- `tests/test_phase150_rc4_4_reasons.py`

## Implemented reason

RC4-4 intentionally implements only:

- `DEFINITION_APPLICABILITY`

It is derived from the already typed semantic dependency:

- `PRECONDITION_FOR_DEFINITION`

No reason is inferred from raw role pairs.

## Deliberately not implemented

The other RC4-2 classifications are not guessed from block-role adjacency. They require additional typed evidence or statement-shape checks before production use.

This package does not:

- change RC3 `OrderedContribution`;
- change contribution placement;
- change the Narrative renderer;
- introduce EHP semantic naming;
- change equation numbering;
- classify `OTHER` blocks;
- key behavior by `(n, k)`, `pi_6^3`, `nu'`, proposition number, or rendered text.

## Run

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase150_rc4_4_minimal_implementation.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase150_rc4_4_minimal_implementation\run_phase150_rc4_4.ps1"
```

## Completion condition

RC4-4 is complete when:

1. the typed reason sidecar is available in production;
2. `PRECONDITION_FOR_DEFINITION` produces `DEFINITION_APPLICABILITY`;
3. representative groups do not acquire invented reasons;
4. RC3 ordering remains unchanged;
5. focused tests pass.

Repository-wide tests remain reserved for the end of Phase 150.
