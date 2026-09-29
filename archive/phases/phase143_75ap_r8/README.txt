Phase 143-75AP-R8

R7 repaired hopf_relation successfully.
The next failure is in Toda515Sigma8TransportedDecompositionStatement.

Known semantic field types from the Phase 143-75AO audit:
- prop44_isomorphism.map.target_group: TodaPrimaryGroup
- transported_group: DirectSumGroup

R8 repairs both renderer selections in that one branch:
- target_group -> homotopy-group renderer
- transported_group -> raw group-structure renderer

Both replacements are AST-targeted and require exactly one match.

Production file:
- toda_proof_narrative_renderer.py

Changed function:
- render_toda_proof_statement_latex()

No imports.
No new helpers.
No mathematical scope change.
Focused tests only.
No full pytest.
