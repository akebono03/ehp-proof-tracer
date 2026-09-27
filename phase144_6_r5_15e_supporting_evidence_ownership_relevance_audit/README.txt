Phase 144-6-R5-15E
====================

Audit only. No production code, tests, or project documents are modified.

Purpose
-------
R5-15D showed that increasing global replay depth does not provide a generic
Narrative stopping rule. It recursively expands proofs of supporting facts.

R5-15E audits ownership/relevance instead of depth.

Selected owners
---------------
- required final-claim Narrative Argument conclusions
- required typed providers identified by the R5-13/R5-15C model

Evidence classes
----------------
CLAIM_EVIDENCE
  Direct proof premise of a selected final-claim Argument conclusion.

PROVIDER_EVIDENCE
  Direct proof premise of a selected typed provider.

NESTED_PROOF
  Descendant below direct evidence. This is recursive proof expansion.

UNRELATED_SUPPORT
  Outside the selected claim/provider ownership closure.

The audit also compares these classes with the existing R4 Argument-local
frontier visibility.

Important
---------
This is intentionally a structural first-pass ownership audit.

It does not yet assert that every direct premise must be displayed or that
every nested premise must be hidden. If a mathematically necessary explanatory
step is nested, the next audit should identify a generic semantic promotion
rule.

No n/k-specific rule is used.
No inference-rule-name parsing is used.
No pytest is run because production code is unchanged.
