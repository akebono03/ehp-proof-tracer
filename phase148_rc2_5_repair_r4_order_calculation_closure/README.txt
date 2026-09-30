Phase 148 RC2-5 Repair R4

Production change:
- toda_group_proof_narrative_semantics.py
- build_toda_group_proof_narrative_semantic_closure_presentation only.

General rule:
1. depth=0 remains closed: no semantic premise expansion.
2. Find ORDER relations already present in the bounded presentation.
3. Find their direct EQUALITY premises.
4. Add one level of EQUALITY premises required by those calculation equalities.
5. Preserve the existing registered definition semantic closure.

This selects the order-calculation chain without hardcoding pi_6^3,
nu-prime, rule names, block indices, LaTeX, or a specific depth > 0.

R2 accidental test changes are repaired individually.
RC2 raw-exactness suppression expectations remain.

Focused regression only. Repository-wide pytest is not run.
