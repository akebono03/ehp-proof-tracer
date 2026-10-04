Phase157-R20 repair40

Purpose
-------
Handle a renderer fallback that legitimately returns None.

Current failure
---------------
During the Phase157 representative cross-group Narrative regression,
`OddScalarStatement` reaches
`_render_phase153_r3_6_component_latex()`.

The first renderer returns None.
The second renderer also returns None without raising.
The current function passes that None into
`_normalize_generic_narrative_statement_latex()`, which requires str and raises
TypeError.

Minimal generic repair
----------------------
After `render_toda_proof_statement_latex(component)`, return None when the
renderer result is None.

This preserves the existing component-list behavior:
unsupported components are skipped rather than being exposed through an
internal fallback representation.

Changed production file
-----------------------
- toda_group_proof_generic_narrative_renderer.py

Changed function
----------------
- _render_phase153_r3_6_component_latex()

Import changes
--------------
None.

New test
--------
- tests/test_phase157_r20_repair40_none_component_latex_fallback.py

The tests verify:
- unsupported OddScalarStatement returns None;
- a component list containing only that unsupported component returns None.

Phase boundary
--------------
This repair does not add public rendering for OddScalarStatement and does not
change semantic classification. It only closes the invalid None-to-normalizer
path.

No documentation changes.
No repository-wide pytest.
