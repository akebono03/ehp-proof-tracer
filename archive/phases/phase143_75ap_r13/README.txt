Phase 143-75AP R13

Confirmed runtime cause
=======================
The Toda515Sigma8TransportedDecompositionStatement step is:
- a direct derivation premise of the root Relation;
- in redundant_direct_premise_step_ids;
- in relocated_direct_premises;
- in a block explicitly preserved by the argument-level DERIVATION transition.

The body renderer therefore removed the semantic aggregate step before the
generic semantic renderer could see it.

Changed file
============
- toda_group_proof_narrative_argument_body_renderer.py

Changed function
================
- render_toda_group_proof_narrative_argument_body_markdown()

Import changes
==============
None.

New classes/functions
=====================
None.

Minimal behavior change
=======================
For a block already marked in preserve_provenance_block_ids, direct
derivation premises are not removed merely because they are classified as
redundant/relocatable. context_hidden_step_ids still applies.

No pi_15^8-specific branch is introduced.
No new mathematical rule is introduced.
No future-phase behavior is added.

Focused tests
=============
- tests/test_phase143_51a_r_provenance_semantic_catalog.py
- tests/test_phase143_51b_aggregate_statement_prose.py
- tests/test_phase134_24_pi15_8_narrative.py

Completion condition for this repair
====================================
The transported decomposition is rendered semantically and all focused
tests pass.

Next boundary
=============
If focused tests pass:
1. rerun Phase 143 fallback completion audit;
2. only then run the canonical full Phase 143 regression once.
