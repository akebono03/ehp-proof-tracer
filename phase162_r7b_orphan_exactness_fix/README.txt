Phase 162 R7-B / orphan exactness introduction cleanup

Changed production function: suppress_toda_group_proof_narrative_dangling_connectors
File: toda_group_proof_narrative_contribution_renderer.py
No import changes. Entire new function is in modified_function.py.
New tests: test_r7b.py (six functions, complete imports).
The apply script backs up the production source and replaces the single function using AST lines.
The package does NOT remove delta steps, stable references, or mathematical derivations.
Focused pytest: test_r7b.py + existing test_phase157_r20_repair43_dangling_connector_cleanup.py.
Full suite: not run until Phase 162 closes.
Next Phase boundary: no new proof inference or generic stable transfer introduced.
