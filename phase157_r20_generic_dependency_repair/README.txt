Phase157-R20 generic dependency repair

Goal
----
Correct the R19-repair13 architectural detour.

This package removes target-specific pi_6^3 Narrative construction and moves
the missing mathematics into the proof graph / generic semantic machinery.

Main changes
------------
1. Toda Proposition 2.2 right-composition rule becomes first-class literature
   provenance (`Proposition 2.2`).

2. Toda Equation 5.7 now requires the actual Proposition 2.2 proof step as a
   premise.  The rule no longer merely mentions Proposition 2.2 in prose.

3. Map-property dependency closure is generic:
   selected map properties recursively pull the relation/exactness premises
   needed to explain them, but stop at fixed literature statements.

4. Proposition 2.2 becomes a fixed literature component.  Equation 5.7 is
   treated as a derived/proof-internal statement for Narrative purposes so
   its premises can explain it.

5. Same-theorem earlier-component retention is generalized.  It no longer
   checks whether the root is pi_6^3 or whether the theorem is Proposition 5.6.

6. The pi_6^3-specific reference filter and all `_phase157_r19_*` finalizers
   are removed from the contribution renderer.

7. Hidden zero-map reasoning, adjacent eta suspension bridges, and adjacent
   EHP exactness-window merging are implemented from statement types and proof
   dependencies, not from n/k or generator names.

Changed files
-------------
- hopf_rules.py
- toda_rules.py
- toda_phase65_bootstrap.py
- toda_prop58_zero_bootstrap.py
- toda_proof_dependency.py
- toda_group_proof_narrative_semantics.py
- toda_literature_statement_boundary.py
- toda_group_proof_narrative_references.py
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase65_equation57_injectivity.py
- tests/test_phase157_r20_generic_dependency_architecture.py

No documentation changes in this substep.
No repository-wide pytest.

Completion criteria for this substep
------------------------------------
- `_phase157_r19_` occurrences in contribution renderer: 0
- `is_pi6_3` occurrences in contribution renderer: 0
- `filter_phase157_r3_pi6_3_reference_entries` occurrences: 0
- Proposition 2.2 is an actual premise of Equation 5.7.
- Phase30 / Phase65 / architecture focused tests pass.
- pi_6^3 Narrative remains mathematically inspectable without target-specific
  finalization.
