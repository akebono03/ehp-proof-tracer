Phase 148 RC2-4 Repair R4.2
Calculation-premise semantic closure repair

GitHub develop inspection
-------------------------
Inspected before implementation:
- toda_group_proof_narrative_semantics.py
- toda_group_proof_narrative_equation_numbering.py
- toda_group_proof_narrative_argument_direct_premises.py
- toda_group_proof_narrative_argument_local_body.py
- tests/test_phase143_61b_direct_premise_narrative.py
- tests/test_phase144_5_generic_definition_order_equations.py
- tests/test_phase148_rc2_4_repair_r4_web_narrative_depth_parity.py
- proof.py Relation / RelationType definitions

R4.1 finding
------------
For pi_6^3 at depth=2:

EQ3:
2 nu' = eta_3^3
is already selected at shortest depth 2.

Its direct premises:
EQ1:
2 nu' = eta_3 E eta_3 eta_5
EQ2:
eta_3 E eta_3 eta_5 = eta_3^3
have shortest depth 3 and are absent from the current semantic closure.

The renderer can relocate their text, but equation numbering cannot number
steps that are absent from presentation/blocks.

Production change
-----------------
File:
toda_group_proof_narrative_semantics.py

Import change:
- add Relation
- add RelationType

Changed function:
build_toda_group_proof_narrative_semantic_closure_presentation

General rule
------------
Starting from the ORIGINAL input presentation only:

If a selected parent ProofStep concludes an EQUALITY Relation, add each direct
premise ProofStep that also concludes an EQUALITY Relation.

This calculation-premise rule is one level only:
- newly added equality premises do not recursively trigger the same rule;
- the existing registered semantic-definition closure remains unchanged.

Consequences
------------
- EQ3 can bring EQ1 and EQ2 into the presentation.
- Equation numbering can restore tags (1), (2), (3) and their connector.
- Exactness statements are not equality Relations and are not selected by
  this rule.
- No pi_6^3, rule-name, depth, block-index, or LaTeX hardcoding is added.
- Complete replay is not restored.

Test repair
-----------
The prior R4 Web-response test incorrectly asserted the Trace-only text
"Depth 2". Current template behavior for Narrative is "Selected depth: 2".
That stale assertion is corrected.

Completion criteria
-------------------
For Web pi_6^3, depth=2, Narrative:
- bounded replay remains the Web source;
- tags (1), (2), (3) are restored;
- "(1) と (2) より、" is restored;
- raw exactness phrase count remains zero;
- ord(nu') = 4 remains;
- pi_6^3 = Z/4{nu'} remains;
- the derived short exact sequence remains.

Phase boundary
--------------
No recursive calculation closure.
No exactness-policy change.
No contribution-layer cleanup.
No Narrative ordering change.
No repository-wide pytest.
