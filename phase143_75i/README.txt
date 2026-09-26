Phase 143-75I
=============

Purpose
-------
Add generic semantic Narrative rendering for:
- TodaPi32WhiteheadSquareUpToSignStatement
- TodaProp27HopfInvariantUpToSignStatement
- Toda58WhiteheadSquareUpToSignStatement

Implementation boundary
-----------------------
Only toda_group_proof_narrative_renderer.py is changed.
No inference, AST, repository, bootstrap, or proof-graph semantics are changed.

Rendering rules
---------------
Whitehead-square statements:
  whitehead_square = \pm positive_value

Hopf-invariant statement:
  H(argument) = \pm positive_value

All nested expressions are delegated to the existing
render_toda_expression_latex() implementation.
No theorem names, generator names, dimensions, or inference-rule names
are parsed or hard-coded.

Expected target fallback reduction
----------------------------------
146 target occurrences should move from inference-rule-name fallback
to semantic rendering.
