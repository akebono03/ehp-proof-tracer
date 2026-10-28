# Phase 169 R10EM — Generator Transport Citation Provenance Audit

This package performs a **read-only** audit of how the already verified cyclic and direct-sum generator-transport presentations obtain their citations. It does not modify application code, infer any new mathematical statement, or promote a generator's textual name into proof evidence.

## Scope

R10EL unified the display-suppression decision. R10EM checks the remaining difference between the cyclic and direct-sum citation collection policies: an aggregate source citation versus a cited GIVEN ancestor for **each** generator image.

The audit uses the complete searched and trust-boundary-verified Proof Trees of pi_28^22, pi_32^22, pi_23^15, and pi_33^24. It verifies the existing presentation output, citations, proof-step identity, and expected hidden-step counts.

## Execution

Extract this folder into the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10em_citation_provenance_audit\run.ps1"
```

The runner requires the reviewed R10EL predecessor commit and checked source blob hashes, runs six limited isolated tests, then performs the real-proof audit. It disables pytest cache writes. Reports and rendered narratives go to an untracked timestamped output directory. No full pytest run is performed.

## Result interpretation

A passing case means **only** that its actual image ancestors contain individually cited GIVEN steps, every cited number is registered, and the existing projection uses the same aggregate citation set. It is not a proof of equivalent behavior for every possible group or input; R10A and R10EC continue to have distinct fail-closed policies.
