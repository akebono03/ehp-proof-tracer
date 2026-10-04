Phase157-R20 repair26

Purpose
-------
Fix both causes found by repair25.

Audit result
------------
1. `eta_3^3 = eta_3^3` is reinserted through relocated direct premises.
2. The rendered-reflexive helper returns False for that step.
3. The helper returns True for `eta_5 = eta_5`.

Why the helper failed
---------------------
The helper first required
`_try_render_generic_narrative_expression_latex()` to succeed.

For the eta_3^3 relation, one side contains a Suspension nested inside a
Composition. The generic recursive normalizer can render it, but the
non-recursive try-render helper rejects it.

Generic repair
--------------
1. Remove the preliminary try-render gate.
2. Directly normalize lhs and rhs with
   `_render_generic_narrative_expression_latex()`.
3. Catch TypeError / ValueError for unsupported expressions.
4. Hide normalized-reflexive equality steps in both:
   - normal `display_steps`;
   - `relocated_direct_premises`.

The proof steps remain in the proof graph and dependency structure.

Changed production file
-----------------------
- toda_group_proof_narrative_argument_body_renderer.py

Import changes
--------------
The now-unused import
`_try_render_generic_narrative_expression_latex`
is removed. All other current imports are retained.

Changed helper
--------------
- `_is_toda_group_proof_narrative_rendered_reflexive_equality_step()`

Changed method/function
-----------------------
- `render_toda_group_proof_narrative_argument_body_markdown()`
  adds the same generic filter to relocated direct premises.

New test
--------
- tests/test_phase157_r20_repair26_reflexive_helper_and_relocated_filter.py

Phase boundary
--------------
This repair addresses only rendered-reflexive equality leakage.
Remaining Phase157 work includes prose duplication cleanup and the explicit
eta_3^3 nonzero/order justification.

Repository-wide pytest is not run.
