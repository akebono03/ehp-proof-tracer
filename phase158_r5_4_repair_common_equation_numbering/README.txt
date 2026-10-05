Phase 158-R5-4 repair — Common equation-numbering rule
=======================================================

監査済み GitHub baseline
------------------------
Repository:
  akebono03/ehp-proof-tracer

HEAD:
  65365234ff0bc52e5ca716dbb92cacd75d4a9c7b

R5-4 audit finding
------------------
Representative 7-group audit:
- rendered: 7
- exceptions: 0
- equation tags: 46
- tags without later reference: 27
- duplicate tags: 0
- parenthesized number uses without matching tag: 0
- old dedicated-route markers: 0

pi_8^5 exposed a forward-reference defect:
- "(1) より" appeared before the equation carrying \tag{1}
- "(2) より" appeared before the equation carrying \tag{2}

変更対象
--------
Production:
  toda_group_proof_narrative_equation_numbering.py
  - number_toda_group_proof_narrative_equations

Test:
  tests/test_phase158_r5_4_repair_common_equation_numbering.py
  - new focused tests

Imports
-------
Production import changes: none.

一般規則
--------
An equation receives \tag{N} only when:
1. it is a source of a narrative derivation transition;
2. its rendered equation line is actually visible in the current markdown;
3. that visible source line occurs before the target connector that will cite it.

Only then is the connector rewritten from:
  これらより,

to:
  (N) より,
or:
  (N) と (M) より,

Therefore:
- no tag is created merely because a transition exists structurally;
- no forward equation reference is created;
- every generated tag has at least one later reference;
- pi_6^3's already-correct calculation-chain numbering remains supported.

今回行わないこと
----------------
- prose repair
- proof data repair
- semantic structure repair
- route selection changes
- dedicated helper removal
- repository-wide R5-6 audit
- full pytest

Focused pytest
--------------
tests/test_phase158_r5_4_repair_common_equation_numbering.py
tests/test_phase144_5_generic_definition_order_equations.py
tests/test_phase144_5_r2_r2_api.py

Full pytest
-----------
Phase 158 closure only.
