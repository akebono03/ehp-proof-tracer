# Phase 175 R4R12R13R8R6 — Common Citation Binding Contract

This package performs a read-only, source-first regression audit of the shared Proof Narrative Model and Renderer. It does not create proof steps, mathematical inferences, literature citations, or database facts.

## Scope

The audit checks three already-completed public targets: `(n,k)=(5,4)`, `(6,5)`, and `(7,5)`. It verifies bidirectional citation/step membership, registered fixed-statement bodies, direct GIVEN consumers, and the published `(5.11)` and `(5.8)` reference/body displays for the first target. It deliberately does not propagate citation numbers automatically to every multi-premise inference.

The `inspect_binding` function examines actual linked model data. A missing registered fixed-statement body is a regression; a DB-prior citation without an assertion ID is not treated as a registered literature statement. A direct-consumer child may legitimately have no owned citation number, because citations also travel through proof ancestry during rendering.

## Execution

Extract the package into the root of `akebono03/ehp-proof-tracer` on branch `develop`, then run from that root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r13r8r6_binding_contract\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r13r8r6_binding_contract\run.ps1
```

The second command runs only the focused tests and three live target audits, not the full pytest suite. The UTF-8 JSON report is written to `%TEMP%\EHP_Phase175_R13R8R6_contract.json`. Prefer reading it as UTF-8; PowerShell 5.1 may otherwise display Japanese characters incorrectly.

## Gate

`PASS_R13R8R6_COMMON_CITATION_CONTRACT_AUDITED` means this inspected target matrix passes the stated contract. It is **not** a theorem that every future typed source or every possible target is automatically displayable. Address any new class of missing source projection in a separately reviewed phase.

No production files are modified. Complete the final full test suite only when closing Phase 175.
