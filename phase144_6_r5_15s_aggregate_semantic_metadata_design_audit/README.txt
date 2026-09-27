Phase 144-6-R5-15S
====================

Aggregate semantic metadata design audit.

Scope
-----
Audit only.

15R showed that the 9 remaining edge-local visible unresolved edges contain a
small number of recurring typed mathematical structures.

15S compares where that mathematical meaning should live.

Current architecture checked before this audit
----------------------------------------------
- Narrative SemanticSidecar:
  - premise-edge semantic role,
  - step semantic role,
  - dependency semantic role.
- MathematicalBlockRole:
  presentation-oriented block grouping.
- Aggregate statement catalog:
  boolean aggregate membership only.
- EvidenceContribution sidecar:
  premise-edge-specific contribution.
- group-structure semantics:
  contains an existing special interpretation for transported decomposition.

Design question
---------------
Keep these two concepts separate:

1. Statement semantic:
   What mathematical structure does this proof statement assert?

2. EvidenceContribution:
   What does this premise establish for this particular consumer?

Diagnostic candidate statement semantics
----------------------------------------
- GROUP_ORDER_TRANSPORT
- MAP_TRANSPORT
- GROUP_DECOMPOSITION_TRANSPORT
- RELATION_AGGREGATE

These names are audit vocabulary only, not production API.

Preferred prototype direction
-----------------------------
A separate Narrative aggregate-statement semantic sidecar, validated against
presentation proof steps.

Do not yet modify:
- EvidenceContribution,
- MathematicalBlockRole,
- R4 visibility,
- renderer,
- CLI,
- Web,
- proof core.

The next prototype should test whether explicit typed statement semantics plus
consumer role / Argument purpose can classify the 9 edges without
statement-class branching.

No n/k-specific production rule and no inference-rule-name production rule are
introduced.

Focused pytest only. Full pytest remains deferred until the end of Phase 144.
