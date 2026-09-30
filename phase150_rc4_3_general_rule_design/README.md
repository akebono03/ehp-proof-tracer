# Phase 150 / RC4-3 — General rule design

This package is design-audit only. It does not modify production code or existing tests.

## Goal

Define the minimal production boundary for generic reason prose.

The central separation is:

```text
OrderedContribution = what / where to display
Reason              = why a conclusion follows
Renderer            = how to express that reason
```

RC4 must not alter RC3 contribution placement.

## Proposed RC4-4 production module

`toda_group_proof_narrative_reasons.py`

Minimal types:

- `TodaGroupProofNarrativeReasonKind`
- `TodaGroupProofNarrativeReason`
- `TodaGroupProofNarrativeReasonSidecar`
- `build_toda_group_proof_narrative_reason_sidecar(...)`

A reason records a typed relation between premise `ProofStep` objects and one conclusion `ProofStep`. It must not depend on a rendered Japanese sentence.

## Generality guards

Classification must not depend on:

- `(n, k)`;
- `pi_6^3`;
- `nu'`;
- proposition numbers;
- rendered text.

Ambiguous or unsupported relations produce no reason.

`OTHER` blocks are not promoted into reason prose in RC4.

EHP-specific naming remains outside RC4 and belongs to RC5.

## Run

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase150_rc4_3_general_rule_design.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase150_rc4_3_general_rule_design\run_phase150_rc4_3.ps1"
```

## Completion condition

RC4-3 is complete when the audit confirms:

1. RC4 has a separate typed reason model;
2. RC3 ordering APIs remain unchanged;
3. all proposed classifications specify the semantic evidence they require;
4. ambiguous relations have an explicit no-reason fallback;
5. RC4-4 has a minimal implementation boundary.
