Phase 143-75S
=============

Purpose
-------
Add generic semantic rendering for
Toda58WhiteheadSquareUpToSignStatement.

Production file changed
-----------------------
toda_proof_narrative_renderer.py

Changed import
--------------
Toda58WhiteheadSquareUpToSignStatement is added to the existing
from toda_rules import (...) block.

Changed function
----------------
render_toda_proof_statement_latex

No new production class is added.

Semantic rule
-------------
The renderer uses only:

- statement.whitehead_square
- statement.positive_value

It does not inspect inference_rule.name, proposition numbers, or
literature metadata.

For a Sum positive_value, parentheses are added so that the sign
applies to the whole value:

[\iota_4,\iota_4] = \pm(2\nu_4-E\nu')

For a non-Sum value, no unnecessary parentheses are forced.

Tests
-----
Three focused tests are added.

The production audit checks all 45 occurrences discovered through the
Toda58EquationStatement aggregate components.

Important boundary
------------------
This phase does not render Toda58EquationStatement itself.
Therefore the global rule-name fallback count from Phase 143-75Q is
not expected to decrease yet.

Phase 143-75T may compose the three already-semantic aggregate
components.

No full pytest
--------------
Run only the focused Phase 143-75S tests and target audit.
The full suite remains deferred until the end of Phase 143.
