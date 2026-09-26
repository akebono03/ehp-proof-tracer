Phase 143-75Y
=============

Purpose
-------
Add generic semantic rendering for
TodaLemma54Nu4ConstructionStatement.

Production file changed
-----------------------
toda_proof_narrative_renderer.py

Changed import
--------------
TodaLemma54Nu4ConstructionStatement is added to the existing
from toda_rules import (...) block.

New helper functions
--------------------
Inserted immediately before render_toda_proof_statement_latex:

- _render_toda_signed_expression_latex
- _render_toda_nu4_parameter_factor_latex
- _render_toda_nu4_construction_branch_latex

Changed function
----------------
render_toda_proof_statement_latex

Semantic inputs used
--------------------
statement.alpha_star
statement.nu4
statement.parameter
statement.whitehead_data.whitehead_square
statement.whitehead_data.sign_parameter
statement.double_suspension_value
branch.double_suspension_sign
branch.alpha_star_sign
branch.whitehead_coefficient_sign
branch.parameter_offset

No inference-rule name, proposition name, or literal variable name
"s"/"u" is inspected.

Safety boundary
---------------
Branch signs must be +/-1. Unexpected sign data returns None rather
than inventing a formula.

This phase does not add rendering for
TodaLemma54WhiteheadCorrectionDataStatement.

Focused tests
-------------
1. Current Phase 60-8 piecewise formula.
2. Parameter offset is read from branch data.
3. Unsupported branch sign returns None.

Expected production audit
-------------------------
112 groups
11033 presentation nodes
37 target occurrences
37 semantic renderings
0 target rule-name fallbacks
288 total rule-name fallbacks
29 remaining fallback statement types
0 errors

No full pytest
--------------
The full suite remains deferred until the end of Phase 143.
