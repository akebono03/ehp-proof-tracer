Phase 143-75T
=============

Purpose
-------
Add aggregate semantic rendering for Toda58EquationStatement.

Production file changed
-----------------------
toda_proof_narrative_renderer.py

Changed import
--------------
Toda58EquationStatement is added to the existing
from toda_rules import (...) block.

Changed function
----------------
render_toda_proof_statement_latex

Semantic inputs
---------------
The aggregate renderer uses only:

- delta_nu_relation
- whitehead_nu_relation
- delta_whitehead_relation

It does not inspect:

- inference_rule.name
- proposition/equation numbers
- literature text

Consistency checks
------------------
Before rendering, the aggregate verifies:

1. both delta components are TodaDeltaImageUpToSignStatement;
2. the middle component is Toda58WhiteheadSquareUpToSignStatement;
3. both delta statements use the same map;
4. both delta statements use the same source element;
5. delta_nu_relation.positive_value equals
   whitehead_nu_relation.positive_value;
6. delta_whitehead_relation.positive_value equals
   whitehead_nu_relation.whitehead_square.

If the aggregate is inconsistent, this renderer returns None.

Expected mathematical output
----------------------------
\Delta(\iota_9)
= \pm(2\nu_4-E\nu')
= \pm[\iota_4,\iota_4]

For a Sum positive representative, parentheses are retained so the
first sign applies to the whole sum.

Focused tests
-------------
Three tests:

1. expected aggregate output;
2. literature metadata does not affect rendering;
3. inconsistent semantic aggregate is rejected.

Production audit
----------------
Expected:

112 groups
11033 presentation nodes
45 target occurrences
45 target semantic renderings
0 target rule-name fallbacks
365 total rule-name fallbacks
31 remaining fallback statement types
0 errors

No full pytest
--------------
The full suite remains deferred until the end of Phase 143.

Next boundary
-------------
Phase 143-75U should re-audit or inspect the next largest remaining
fallback type. It must not be implemented in this phase.
