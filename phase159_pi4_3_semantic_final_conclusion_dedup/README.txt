Phase 159 - pi4_3 semantic final-conclusion dedup

Purpose
-------
Fix the public Narrative duplication

  pi_4^3 = Z/2{eta_3}
  以上より, pi_4^3 = Z/2{eta_3}

without adding a pi_4^3-specific string rule.

Audit result
------------
The focused audit established:

  semantic_root_match_count = 1

Therefore the defect is not caused by two distinct ProofStep objects with
equivalent conclusions. The single root semantic statement is consumed twice
by the public rendering pipeline.

Implementation boundary
-----------------------
This patch introduces a shared semantic statement key and applies it only to
the final root conclusion deduplication.

It does not replace every historical string-based deduplication rule in this
Phase. That broader migration belongs to later work after the current public
contract is stabilized.

Semantic identity
-----------------
For Relation, semantic identity consists of:

- lhs
- rhs
- relation_type

Relation.source and Relation.note are provenance metadata and are intentionally
excluded.

Other dataclass statements are keyed recursively by concrete type and fields.

Retention rule
--------------
When the root semantic conclusion appears more than once in the same public
Narrative and at least one occurrence is a connected final form such as

  以上より, <root conclusion>

the last connected occurrence is retained and the other occurrences of that
same root semantic conclusion are suppressed.

Files
-----
New:
- toda_group_proof_narrative_statement_identity.py
- tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py

Modified:
- toda_group_proof_narrative_contribution_renderer.py

Focused tests only
------------------
The runner executes only the new semantic-dedup tests and directly related
existing pi_4^3 / Narrative tests.

The full test suite is intentionally not run in this package.
