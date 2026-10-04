Phase157-R20 repair8

Purpose
-------
Make generic Reference ancestry robust to equivalent ProofStep instances.

Root cause
----------
The proof repository can contain distinct ProofStep objects with equal
conclusions. Existing Reference selection already recognizes this by comparing
both step identity and conclusion equality.

repair6 descendant traversal started only from `id(reference_step)`. If the
visible consumer used another ProofStep instance with the same conclusion, the
Reference ancestry path was missed.

Generic repair
--------------
For descendant Reference usage, every presentation step whose conclusion equals
the Reference-owned step conclusion is treated as an equivalent starting node.

The same equivalence rule is applied while traversing descendants.

This is independent of:
- proposition number;
- group dimension;
- sphere dimension;
- generator;
- pi_6^3.

Changed files
-------------
- toda_group_proof_narrative_references.py
  - restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()
- tests/test_phase157_r20_repair8_reference_alias_descendants.py (new)

No documentation changes.
No repository-wide pytest.
