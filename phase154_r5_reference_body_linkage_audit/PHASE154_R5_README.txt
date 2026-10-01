Phase 154-R5 — Reference ↔ proof body linkage refinement

This package is the initial graph audit for R5.

Production changes
------------------
none

Why audit first
---------------
The current public Narrative contains:

  また、[R1]を用いる。
  まず、[R2]を用いる。

These lines are produced after Reference statement suppression. At that point
the prose no longer states which mathematical consumer is supported by each
Reference.

Changing the wording from line adjacency alone could create a false
mathematical implication.

Therefore R5 first recovers linkage from the Proof graph.

Audit target
------------
pi11_4, Narrative, depth 2.

For each visible Reference:
- selected Reference statement
- direct consumers
- shortest graph path from selected statement to the root
- statement type
- rendered semantic statement
- literature reference ownership
- public Reference-section statement lines

Decision rule
-------------
1. Never infer Reference linkage from adjacent lines alone.
2. Prefer selected-step -> consumer/path relationships already present in the
   Proof graph.
3. If one visible consumer relation is unique, use that relation to generate
   linked prose.
4. If ownership is ambiguous, retain neutral "[R#]を用いる。" prose.
5. Do not add a pi11_4-specific branch.

Files added by this audit package
---------------------------------
- audit_phase154_r5.py
- run_phase154_r5.ps1
- PHASE154_R5_README.txt

Production files changed
------------------------
none

Focused pytest
--------------
- tests/test_phase154_r4_semantic_duplication_transition_refinement.py
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase154_r2_fix3_reference_marker_completion.py
- tests/test_phase153_r8_reference_use_prose_normalization.py

Full suite
----------
not run; reserved for the end of Phase 154.

Completion condition for this R5 audit
--------------------------------------
The selected [R1]/[R2] steps and their consumer paths are explicit enough to
choose a generic linkage rule.

Next boundary
-------------
If linkage is unique, implement the smallest generic Reference-linkage rule as
Phase 154-R5 Fix1.
If linkage is ambiguous, preserve the neutral reference-use sentence and only
repair ordering where supported by graph structure.
