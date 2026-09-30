# Phase 150 / RC4-2 — Reason-prose classification

This package is audit-only. It does not modify production code or existing tests.

## Goal

Classify the RC4-1 prose gaps as generic semantic reason relations rather than `pi_6^3`-specific sentences.

The intended pipeline is:

```text
ProofStep / block role / dependency / exactness ownership / hidden transport
-> generic reason relation
-> generic prose
```

## Scope

The audit checks the six established representative groups:

- `pi_6^3`
- `pi_8^5`
- `pi_10^4`
- `pi_12^5`
- `pi_15^8`
- `pi_16^9`

It also diagnoses the RC4-1 `[3] current_required_facts_present=False` result from the proof structure instead of relying on rendered-text regular expressions.

## Non-goals

RC4-2 does not:

- change RC3 contribution ordering;
- implement reason prose;
- add EHP semantic naming;
- change equation numbering;
- run repository-wide tests.

## Run

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase150_rc4_2_reason_prose_classification.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase150_rc4_2_reason_prose_classification\run_phase150_rc4_2.ps1"
```

## Completion condition

RC4-2 is complete when:

1. the RC4-1 false result is structurally diagnosed;
2. reason-prose candidates are classified without target-specific names;
3. each class identifies its existing semantic inputs;
4. the result gives RC4-3 a minimal general-rule design boundary.
